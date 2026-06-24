"""
Inyecta cabeceras HTTP de seguridad en todas las respuestas del servidor Tornado de Streamlit.

Mitiga los hallazgos del escaneo ZAP by Checkmarx:
  - CWE-693  (Medio):  Content-Security-Policy no configurada
  - CWE-1021 (Medio):  Anti-Clickjacking (X-Frame-Options / frame-ancestors)
  - CWE-693  (Bajo):   X-Content-Type-Options faltante

Importar este módulo al inicio de app.py aplica el parche de forma global
para todas las respuestas HTTP posteriores del proceso Tornado.
"""
import tornado.web

_original_finish = tornado.web.RequestHandler.finish


def _secure_finish(self, *args, **kwargs):
    try:
        # CWE-693: Content Security Policy
        # 'unsafe-inline' y 'unsafe-eval' son requeridos por la arquitectura interna de Streamlit.
        self.set_header(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "connect-src 'self' ws: wss:; "
            "font-src 'self' data:; "
            "worker-src blob:; "
            "frame-ancestors 'none';"
        )
        # CWE-1021: Anti-Clickjacking
        self.set_header("X-Frame-Options", "DENY")
        # CWE-693: MIME-sniffing prevention
        self.set_header("X-Content-Type-Options", "nosniff")
        # Cabecera adicional de buena práctica
        self.set_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.set_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
    except Exception:
        # Si los encabezados ya fueron enviados (streaming), se omite sin interrumpir la respuesta.
        pass
    return _original_finish(self, *args, **kwargs)


tornado.web.RequestHandler.finish = _secure_finish
