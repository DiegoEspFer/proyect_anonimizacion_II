"""
model_roberta.py
Anonimización clínica con RoBERTa + post-procesamiento de patrones.
"""
import os
import re
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


class ClinicalAnonymizer:
    """Anonimizador clínico con NER + reglas de post-procesamiento."""

    def __init__(self, model_path="./modelo_local", device=None):
        self.model_path = model_path
        if device is None:
            self.device = 0 if torch.cuda.is_available() else -1
        else:
            self.device = device

        print(f"[INFO] Cargando modelo desde: {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path)

        if hasattr(self.model.config, 'label2id'):
            self.model.config.id2label = {
                int(v): k for k, v in self.model.config.label2id.items()
            }

        self.nlp_pipeline = pipeline(
            "ner",
            model=self.model,
            tokenizer=self.tokenizer,
            aggregation_strategy="simple",
            device=self.device
        )
        print("[INFO] Modelo cargado correctamente.")

    def detect_entities(self, text, max_chars=1000, overlap=250, batch_size=8):
        if not isinstance(text, str) or not text.strip():
            return []

        chunks = []
        start_offsets = []
        total_len = len(text)
        start_idx = 0

        while start_idx < total_len:
            end_idx = min(start_idx + max_chars, total_len)
            if end_idx < total_len:
                corte = text.rfind(" ", start_idx, end_idx)
                if corte > start_idx + overlap:
                    end_idx = corte
            chunks.append(text[start_idx:end_idx])
            start_offsets.append(start_idx)
            siguiente_inicio = end_idx - overlap
            if siguiente_inicio <= start_idx:
                start_idx = end_idx
            else:
                start_idx = siguiente_inicio
            if end_idx >= total_len:
                break

        batch_results = self.nlp_pipeline(chunks, batch_size=batch_size)

        global_entities = []
        for chunk_res, start_offset in zip(batch_results, start_offsets):
            for ent in chunk_res:
                global_ent = ent.copy()
                global_ent['start'] = start_offset + ent['start']
                global_ent['end'] = start_offset + ent['end']
                global_entities.append(global_ent)

        return self._merge_overlapping_entities(global_entities)

    def _merge_overlapping_entities(self, entities):
        if not entities:
            return []
        entities = sorted(entities, key=lambda x: (x['start'], -x['end'], -x['score']))
        merged = []
        for current in entities:
            if not merged:
                merged.append(current)
                continue
            prev = merged[-1]
            if current['start'] < prev['end']:
                if current['entity_group'] == prev['entity_group']:
                    prev['end'] = max(prev['end'], current['end'])
                    prev['score'] = max(prev['score'], current['score'])
                else:
                    if current['score'] > prev['score']:
                        merged[-1] = current
                continue
            if current['entity_group'] == prev['entity_group'] and current['start'] <= prev['end'] + 2:
                prev['end'] = current['end']
                prev['score'] = max(prev['score'], current['score'])
                continue
            merged.append(current)
        return merged

    def _expandir_entidades_adyacentes(self, text, entities):
        """Captura apellidos huérfanos adyacentes a entidades detectadas."""
        if not entities:
            return entities

        entities = sorted(entities, key=lambda x: x['start'])
        expandidas = []

        palabras_excluidas = {
            'Registro', 'Médico', 'Especialidad', 'Servicio', 'Ingreso',
            'Egreso', 'Manejo', 'Diagnósticos', 'Nombre', 'Observaciones',
            'Tipo', 'Fecha', 'Respuesta', 'Pregunta', 'Cuenta', 'Tratamiento',
            'Primera', 'Segunda', 'Tercera', 'Impreso', 'Por',
            'Hospitalización', 'Adultos', 'Trasplante', 'Piso', 'Cáncer',
            'Alto', 'Costo', 'IntraHospitalario', 'Medicina', 'Especializada',
            'Hematologia', 'Patológicos', 'Quirúrgicos', 'Traumatológicos',
            'Ginecológicos', 'Obstétricos', 'Farmacológicos', 'Alérgicos',
            'Toxicológicos', 'HOSPITALIZACIÓN', 'ADULTOS', 'PBS',
            'CONTRIBUTIVO', 'Postoperatorio', 'Obstructiva', 'Crónica',
        }

        etiquetas_nombre = {
            'NOMBRE_PERSONAL_SANITARIO', 'NOMBRE_SUJETO_ASISTENCIA',
            'FAMILIARES_SUJETO_ASISTENCIA', 'PER', 'B-PER', 'I-PER'
        }

        for ent in entities:
            start = ent['start']
            end = ent['end']
            label = ent['entity_group']
            es_nombre = any(tag in label for tag in etiquetas_nombre)

            if es_nombre:
                texto_despues = text[end:]
                match_derecha = re.match(
                    r'^(\s{1,3})([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ]{2,})',
                    texto_despues
                )
                if match_derecha:
                    palabra = match_derecha.group(2).strip()
                    if palabra not in palabras_excluidas:
                        end = end + match_derecha.end()

                texto_antes = text[:start]
                match_izquierda = re.search(
                    r'([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑa-záéíóúñ]{2,})(\s{1,3})$',
                    texto_antes
                )
                if match_izquierda:
                    palabra = match_izquierda.group(1).strip()
                    if palabra not in palabras_excluidas:
                        start = start - len(match_izquierda.group(0))

            expandidas.append({
                'start': start, 'end': end,
                'entity_group': label, 'score': ent.get('score', 0.9)
            })

        return self._merge_overlapping_entities(expandidas)

    def _postprocesar_patrones_medicos(self, texto_anonimizado: str) -> str:
        """
        Captura patrones Dr./Dra./Enf. + Apellido que el modelo NER omitió.
        Solo reemplaza si NO hay ya un placeholder en esa posición.
        """
        placeholder = "<NOMBRE_PERSONAL_SANITARIO>"

        patron_doctor = re.compile(
            r'\b(Dra?\.\s+)'
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+'
            r'(?:\s+(?:de|del|la|los|las)\s+)?'
            r'(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
            re.UNICODE
        )

        patron_doctor_upper = re.compile(
            r'\b(DRA?\.\s+)'
            r'([A-ZÁÉÍÓÚÑ]{2,}(?:\s+[A-ZÁÉÍÓÚÑ]{2,})?)',
            re.UNICODE
        )

        def reemplazar(match):
            texto_completo = match.group(0)
            if '<' in texto_completo and '>' in texto_completo:
                return texto_completo
            prefijo = match.group(1)
            return prefijo + placeholder

        texto_anonimizado = patron_doctor.sub(reemplazar, texto_anonimizado)
        texto_anonimizado = patron_doctor_upper.sub(reemplazar, texto_anonimizado)

        return texto_anonimizado

    def _limpiar_fragmentos_residuales(self, texto: str) -> str:
        """
        Limpia fragmentos de texto pegados directamente a los placeholders.

        Resuelve casos como:
          <NOMBRE_PERSONAL_SANITARIO>GAUTA  →  <NOMBRE_PERSONAL_SANITARIO>
          JAIV<NOMBRE_PERSONAL_SANITARIO>   →  <NOMBRE_PERSONAL_SANITARIO>
          <FECHAS>:09                       →  <FECHAS>
        """
        # Fragmentos DESPUÉS del tag: <TAG>texto_pegado → <TAG>
        texto = re.sub(
            r'(<[A-Z_]+>)([A-ZÁÉÍÓÚÑa-záéíóúñ0-9:/.]+)',
            r'\1',
            texto
        )

        # Fragmentos ANTES del tag: texto_pegado<TAG> → <TAG>
        texto = re.sub(
            r'([A-ZÁÉÍÓÚÑa-záéíóúñ]+)(<[A-Z_]+>)',
            r'\2',
            texto
        )

        return texto

    def anonymize(self, text, placeholder_format="<{label}>"):
        """Anonimiza texto: NER + expansión + patrones + limpieza de residuos."""
        if not isinstance(text, str) or not text.strip():
            return text

        entities = self.detect_entities(text)
        entities = self._expandir_entidades_adyacentes(text, entities)

        if not entities:
            resultado = text
        else:
            sorted_entities = sorted(entities, key=lambda x: x['start'])
            fragments = []
            last_idx = 0
            for entity in sorted_entities:
                start = entity['start']
                end = entity['end']
                label = entity['entity_group']
                placeholder = placeholder_format.format(label=label)
                if start < last_idx:
                    continue
                fragments.append(text[last_idx:start])
                fragments.append(placeholder)
                last_idx = end
            fragments.append(text[last_idx:])
            resultado = "".join(fragments)

        # Post-procesamiento: patrones Dr./Dra.
        resultado = self._postprocesar_patrones_medicos(resultado)

        # Post-procesamiento: limpiar fragmentos residuales pegados a tags
        resultado = self._limpiar_fragmentos_residuales(resultado)

        return resultado

    def anonymize_file(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"El archivo no existe: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            text_content = file.read()
        return self.anonymize(text_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anonimización Clínica")
    parser.add_argument("--archivo", type=str, default=None)
    parser.add_argument("--guardar", type=str, default=None)
    args = parser.parse_args()

    anonymizer = ClinicalAnonymizer()
    if args.archivo:
        nombre_archivo = os.path.basename(args.archivo)
        if not nombre_archivo.endswith('.md'):
            nombre_archivo += '.md'
        ruta_completa = os.path.join("dataset", nombre_archivo)
        print(f"\nProcesando: {ruta_completa}...")
        try:
            texto_anonimizado = anonymizer.anonymize_file(ruta_completa)
            ruta_guardado = args.guardar or f"{nombre_archivo[:-3]}_anonimizada.txt"
            directorio = os.path.dirname(ruta_guardado)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            with open(ruta_guardado, 'w', encoding='utf-8') as f:
                f.write(texto_anonimizado)
            print(f"✅ Guardado en: {os.path.abspath(ruta_guardado)}")
        except FileNotFoundError:
            print(f"❌ No se encontró: '{nombre_archivo}' en 'dataset'.")