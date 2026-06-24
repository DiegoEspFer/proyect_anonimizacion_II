import security_headers  # noqa: F401 — aplica cabeceras HTTP de seguridad (ZAP CWE-693, CWE-1021)

import streamlit as st
import os
import io
import zipfile
import tempfile
from pathlib import Path

from converter import convert_file, limpiar_texto_para_filtro
from fpdf import FPDF


# ==========================================
# ESTILOS
# ==========================================
def inject_hic_styling() -> None:
    st.markdown("""
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' ws: wss:; font-src 'self' data:; worker-src blob:; frame-ancestors 'none';">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <style>
    .block-container { padding-top: 1.2rem !important; padding-bottom: 1rem !important; max-width: 50rem !important; }
    header { display: none !important; }
    #MainMenu { visibility: hidden; }
    .stApp { background-color: #F8F9FA; }
    [data-testid="stFileUploadDropzone"] { border: 2px dashed #A0B3C6 !important; border-radius: 12px !important; background-color: #FFFFFF !important; padding: 2.5rem 1rem !important; }
    div[data-testid="stButton"] { width: 100% !important; }
    button[kind="primary"] { background-color: #004B87 !important; border-color: #004B87 !important; border-radius: 6px !important; font-weight: 600 !important; padding: 0.7rem 2rem !important; font-size: 1.1rem !important; width: 100% !important; display: block !important; }
    button[kind="primary"]:hover { background-color: #00335C !important; border-color: #00335C !important; }
    div.stDownloadButton { width: 100% !important; }
    div.stDownloadButton > button { width: 100% !important; padding: 0.6rem 1rem !important; border-radius: 6px !important; display: block !important; }
    .hic-title { color: #004B87 !important; font-size: 2.9rem !important; font-weight: 700 !important; margin: 0px !important; padding: 0px !important; line-height: 1.1; }
    .info-box { background-color: #E3F2FD; border-radius: 8px; padding: 10px 16px; margin: 8px 0; font-size: 0.9rem; color: #1565C0; }
    </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    inject_hic_styling()
    logo_filename = None
    for ext in [".png", ".jpg", ".jpeg", ".svg"]:
        test_path = Path("LOGO-HIC" + ext)
        if test_path.exists():
            logo_filename = str(test_path)
            break
    if logo_filename:
        col_logo, col_title = st.columns([1.6, 5], vertical_alignment="center")
        with col_logo:
            st.image(logo_filename, use_container_width=True)
        with col_title:
            st.markdown("<h1 class='hic-title'>Anonimizar datos PII</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 class='hic-title'>Anonimizar datos PII</h1>", unsafe_allow_html=True)


# ==========================================
# FUNCIONES DE GENERACIÓN
# ==========================================
def generar_pdf_bytes(texto: str) -> bytes:
    """Genera un PDF. Carácter no renderizable = espacio en blanco."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=9)

    # Solo reemplaza con espacio los que NO puede codificar
    texto_safe = ''.join(
        char if ord(char) < 256 else ' '
        for char in texto
    )

    pdf.multi_cell(0, 4.5, texto_safe)
    return bytes(pdf.output())


def generar_zip_txts(archivos_procesados: dict) -> bytes:
    """Genera un ZIP con todos los archivos como .txt (cada uno con su nombre original)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for nombre_original, texto_anonimizado in archivos_procesados.items():
            # Cambiar extensión a .txt
            nombre_base = Path(nombre_original).stem
            nombre_txt = f"{nombre_base}.txt"
            zf.writestr(nombre_txt, texto_anonimizado.encode('utf-8'))
    buffer.seek(0)
    return buffer.getvalue()


def generar_zip_pdfs(archivos_procesados: dict) -> bytes:
    """Genera un ZIP con todos los archivos como .pdf (cada uno con su nombre original)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for nombre_original, texto_anonimizado in archivos_procesados.items():
            nombre_base = Path(nombre_original).stem
            nombre_pdf = f"{nombre_base}.pdf"
            pdf_bytes = generar_pdf_bytes(texto_anonimizado)
            zf.writestr(nombre_pdf, pdf_bytes)
    buffer.seek(0)
    return buffer.getvalue()


# ==========================================
# CARGA DEL MODELO (CACHEADA)
# ==========================================
@st.cache_resource(show_spinner="Cargando modelo de IA...")
def cargar_modelo():
    from model_roberta import ClinicalAnonymizer
    return ClinicalAnonymizer(model_path="./modelo_local")


# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Anonimizador PII - HIC", page_icon="📄", layout="centered")

# Session state
if 'anonimizado_exitoso' not in st.session_state:
    st.session_state.anonimizado_exitoso = False
if 'archivos_procesados' not in st.session_state:
    st.session_state.archivos_procesados = {}  # {nombre_archivo: texto_anonimizado}
if 'zip_txts' not in st.session_state:
    st.session_state.zip_txts = b""
if 'zip_pdfs' not in st.session_state:
    st.session_state.zip_pdfs = b""

render_header()

# ==========================================
# CARGA DE ARCHIVOS (MÚLTIPLES)
# ==========================================
with st.container(border=True):
    uploaded_files = st.file_uploader(
        "Arrastra uno o más archivos aquí",
        type=["pdf", "txt"],
        accept_multiple_files=True,  # <<< MÚLTIPLES ARCHIVOS
        label_visibility="collapsed"
    )

# Mostrar info de archivos cargados
#if uploaded_files:
#    st.markdown(
#        f"<div class='info-box'>📎 <strong>{len(uploaded_files)}</strong> archivo(s) cargado(s): "
#        f"{', '.join([f.name for f in uploaded_files[:5]])}"
#        f"{'...' if len(uploaded_files) > 5 else ''}</div>",
#        unsafe_allow_html=True
#    )

# ==========================================
# BOTÓN PRINCIPAL
# ==========================================
if st.button("Iniciar anonimización", type="primary", use_container_width=True):
    if uploaded_files:
        modelo = cargar_modelo()
        archivos_procesados = {}
        barra_progreso = st.progress(0, text="Procesando archivos...")
        total = len(uploaded_files)
        errores = []

        for idx, uploaded_file in enumerate(uploaded_files):
            barra_progreso.progress(
                (idx) / total,
                text=f"Procesando: {uploaded_file.name} ({idx + 1}/{total})..."
            )

            try:
                # Guardar archivo temporal
                suffix = "." + uploaded_file.name.rsplit(".", 1)[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.getbuffer())
                    tmp_path = tmp.name

                # Extraer texto
                if suffix.lower() == ".pdf":
                    texto_extraido = convert_file(tmp_path)
                else:
                    texto_extraido = uploaded_file.getvalue().decode('utf-8')
                    texto_extraido = limpiar_texto_para_filtro(texto_extraido)

                os.unlink(tmp_path)

                if not texto_extraido or not texto_extraido.strip():
                    errores.append(f"⚠️ {uploaded_file.name}: No se pudo extraer texto.")
                    continue

                # Anonimizar
                texto_anonimizado = modelo.anonymize(texto_extraido)
                archivos_procesados[uploaded_file.name] = texto_anonimizado

            except Exception as e:
                errores.append(f"❌ {uploaded_file.name}: {str(e)}")
                if 'tmp_path' in locals() and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        barra_progreso.progress(1.0, text="¡Completado!")

        if archivos_procesados:
            # Generar ZIPs
            st.session_state.archivos_procesados = archivos_procesados
            st.session_state.zip_txts = generar_zip_txts(archivos_procesados)
            st.session_state.zip_pdfs = generar_zip_pdfs(archivos_procesados)
            st.session_state.anonimizado_exitoso = True

            st.success(f"✅ {len(archivos_procesados)}/{total} archivo(s) procesado(s) exitosamente.")
        else:
            st.error("❌ No se pudo procesar ningún archivo.")

        if errores:
            with st.expander("⚠️ Ver errores", expanded=False):
                for err in errores:
                    st.write(err)
    else:
        st.warning("⚠️ Por favor, sube al menos un archivo.")

# ==========================================
# VISTA PREVIA
# ==========================================
if st.session_state.anonimizado_exitoso and st.session_state.archivos_procesados:
    with st.expander(f"📋 Vista previa ({len(st.session_state.archivos_procesados)} archivo(s))", expanded=False):
        for nombre, texto in st.session_state.archivos_procesados.items():
            st.markdown(f"**{nombre}**")
            preview = texto[:1500] + ("\n\n[... truncado ...]" if len(texto) > 1500 else "")
            st.text_area(nombre, value=preview, height=150, disabled=True, key=f"preview_{nombre}")
            st.divider()

# ==========================================
# BOTONES DE DESCARGA - FILA SUPERIOR (Individuales: TXT y PDF)
# ==========================================
#st.markdown("#### 📥 Descargas")

# --- FILA 1: Descargas individuales (si es 1 archivo) o directas ---
col_top1, col_top2 = st.columns(2)

with col_top1:
    if st.session_state.anonimizado_exitoso and len(st.session_state.archivos_procesados) == 1:
        # Si es un solo archivo, descarga directa .txt
        nombre_orig = list(st.session_state.archivos_procesados.keys())[0]
        texto = list(st.session_state.archivos_procesados.values())[0]
        nombre_txt = Path(nombre_orig).stem + ".txt"
        st.download_button(
            label="📥 Descargar .txt",
            data=texto.encode('utf-8'),
            file_name=nombre_txt,
            mime="text/plain",
            disabled=not st.session_state.anonimizado_exitoso,
            use_container_width=True
        )
    else:
        st.download_button(
            label="📥 Descargar .txt",
            data=b"",
            file_name="anonimizado.txt",
            mime="text/plain",
            disabled=True,
            use_container_width=True,
            help="Disponible solo con 1 archivo. Para múltiples archivos usa el ZIP."
        )

with col_top2:
    if st.session_state.anonimizado_exitoso and len(st.session_state.archivos_procesados) == 1:
        nombre_orig = list(st.session_state.archivos_procesados.keys())[0]
        texto = list(st.session_state.archivos_procesados.values())[0]
        nombre_pdf = Path(nombre_orig).stem + ".pdf"
        pdf_bytes = generar_pdf_bytes(texto)
        st.download_button(
            label="📄 Descargar .pdf",
            data=pdf_bytes,
            file_name=nombre_pdf,
            mime="application/pdf",
            disabled=not st.session_state.anonimizado_exitoso,
            use_container_width=True
        )
    else:
        st.download_button(
            label="📄 Descargar .pdf",
            data=b"",
            file_name="anonimizado.pdf",
            mime="application/pdf",
            disabled=True,
            use_container_width=True,
            help="Disponible solo con 1 archivo. Para múltiples archivos usa el ZIP."
        )

# --- FILA 2: Descargas en ZIP (siempre disponibles) ---
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    n_archivos = len(st.session_state.archivos_procesados)
    st.download_button(
        label=f"📁 txt (.ZIP) — {n_archivos} archivo(s)" if st.session_state.anonimizado_exitoso else "📁 txt (.ZIP)",
        data=st.session_state.zip_txts if st.session_state.anonimizado_exitoso else b"",
        file_name="anonimizados_txt.zip",
        mime="application/zip",
        disabled=not st.session_state.anonimizado_exitoso,
        use_container_width=True
    )

with col_bot2:
    st.download_button(
        label=f"📁 pdf (.ZIP) — {n_archivos} archivo(s)" if st.session_state.anonimizado_exitoso else "📁 pdf (.ZIP)",
        data=st.session_state.zip_pdfs if st.session_state.anonimizado_exitoso else b"",
        file_name="anonimizados_pdf.zip",
        mime="application/zip",
        disabled=not st.session_state.anonimizado_exitoso,
        use_container_width=True
    )