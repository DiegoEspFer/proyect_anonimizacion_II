import os
from transformers import AutoTokenizer, AutoModelForTokenClassification

def descargar_y_guardar_modelo(model_id="BSC-NLP4BIA/bsc-bio-ehr-es-meddocan", save_directory="./modelo_local"):
    """
    Descarga el modelo y el tokenizador desde Hugging Face y los guarda en un directorio local.
    """
    print(f"Descargando tokenizador y modelo desde '{model_id}'...")
    
    # Crear el directorio si no existe
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
    # Descargar
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForTokenClassification.from_pretrained(model_id)
    
    print(f"Guardando los archivos en la carpeta local: {os.path.abspath(save_directory)}...")
    
    # Guardar localmente
    tokenizer.save_pretrained(save_directory)
    model.save_pretrained(save_directory)
    
    print("¡Descarga completada con éxito! Todos los archivos (config.json, pytorch_model.bin, vocab.txt, etc.) están en la carpeta local.")

if __name__ == "__main__":
    descargar_y_guardar_modelo()
