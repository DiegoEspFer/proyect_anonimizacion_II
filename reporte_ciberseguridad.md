ZAP por Informe de Escaneo Checkmarx http://172.30.19.93:9004/ - Conversor Markdown Sitio: http://172.30.19.93:9004 Generado a mar, 2 jun 2026 08:48:22 ZAP Versión: 2.17.0 ZAP by Checkmarx Sumario de Alertas

| Nivel de riesgo | Número de Alertas |
| --- | --- |
| Alto | 0 |
| Medio | 2 |
| Bajo | 3 |
| Informativo | 2 |

Insights

| Level | Razón | Site | Descripción | Statistic |
| --- | --- | --- | --- | --- |
| Bajo | Advertencia |  | ZAP errors logged - see the zap. log file for details | 5 |
| Bajo | Advertencia |  | ZAP warnings logged - see the zap. log file for details | 24 |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of responses with status code 1xx | 1 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of responses with status code 2xx | 86 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of responses with status code 3xx | 1 % |
|  |  |  | Percentage of |  |

| Información | Exceeded Low | http://172. 30.19.93: 9004 | responses with status code 4xx | 11 % |
| --- | --- | --- | --- | --- |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type application /javascript | 82 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type application /json | 1 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type application /octet- stream | 2 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type image /png | 2 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type text/css | 2 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type text /html | 4 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with content type text /plain | 1 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Percentage of endpoints with method GET | 100 % |
| Información | Informativo | http://172. 30.19.93: 9004 | Count of total endpoints | 69 |
| Información | Exceeded Low | http://172. 30.19.93: 9004 | Percentage of slow responses | 5 % |

Alertas

| Nombre | Nivel de riesgo | Número de Instancias |
| --- | --- | --- |
| Cabecera Content Security Policy (CSP) no configurada | Medio | 3 |
| Falta de cabecera Anti-Clickjacking | Medio | 3 |
| Cookie Sin Flag HttpOnly | Bajo | 1 |
| Divulgación de Marcas de Tiempo - Unix | Bajo | 5 |
| Falta encabezado X-Content-Type-Options | Bajo | Systemic |
| Aplicación Web Moderna | Informativo | 3 |
| Respuesta de Gestión de Sesión Identificada | Informativo | 2 |

Detalles de la Alerta

| Medio | Cabecera Content Security Policy (CSP) no configurada |
| --- | --- |
| Descripción | La Política de seguridad de contenido (CSP) es una capa adicional de seguridad que ayuda a detectar y mitigar ciertos tipos de ataques, incluidos Cross Site Scripting (XSS) y ataques de inyección de datos. Estos ataques se utilizan para todo, desde el robo de datos hasta la desfiguración del sitio o la distribución de malware. CSP proporciona un conjunto de encabezados HTTP estándar que permiten a los propietarios de sitios web declarar fuentes de contenido aprobadas que los navegadores deberían poder cargar en esa página; los tipos cubiertos son JavaScript, CSS, marcos HTML, fuentes, imágenes y objetos incrustados como applets de Java, ActiveX, archivos de audio y video. |
| URL | http://172.30.19.93:9004/ |
| Nombre del Nodo | http://172.30.19.93:9004/ |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |
| URL | http://172.30.19.93:9004/robots.txt |
| Nombre del Nodo | http://172.30.19.93:9004/robots.txt |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |
| URL | http://172.30.19.93:9004/sitemap.xml |
| Nombre del Nodo | http://172.30.19.93:9004/sitemap.xml |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |

| Instancia | 3 |
| --- | --- |
| Solución | Asegúrese de que su servidor web, servidor de aplicaciones, balanceador de carga, etc. esté configurado para establecer la cabecera Content-Security-Policy. |
| Referencia | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet. html https://www.w3.org/TR/CSP/ https://w3c.github.io/webappsec-csp/ https://web.dev/articles/csp https://caniuse.com/#feat=contentsecuritypolicy https://content-security-policy.com/ |
| CWE Id | 693 |
| WASC Id | 15 |
| Plugin Id | 10038 |

| Medio | Falta de cabecera Anti-Clickjacking |
| --- | --- |
| Descripción | La respuesta no protege contra ataques de "ClickJacking". Debes incluir Content- Security-Policy con la directiva "frame-ancestors" o X-Frame-Options. |
| URL | http://172.30.19.93:9004/ |
| Nombre del Nodo | http://172.30.19.93:9004/ |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |
| URL | http://172.30.19.93:9004/robots.txt |
| Nombre del Nodo | http://172.30.19.93:9004/robots.txt |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |
| URL | http://172.30.19.93:9004/sitemap.xml |
| Nombre del Nodo | http://172.30.19.93:9004/sitemap.xml |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información |  |
| Instancia | 3 |
| Solución | Los navegadores web modernos admiten las cabeceras HTTP Content-Security-Policy y X-Frame-Options. Asegúrese de que una de ellas está configurada en todas las páginas web devueltas por su sitio/aplicación. Si espera que la página esté enmarcada solo por páginas en su servidor (por ejemplo, si forma parte de un FRAMESET), utilice SAMEORIGIN; de lo contrario, si no espera que la página esté enmarcada, utilice DENY. Alternativamente, considere implementar la directiva "frame-ancestors" de la Política de Seguridad de Contenidos. |

| Referencia | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame- Options |
| --- | --- |
| CWE Id | 1021 |
| WASC Id | 15 |
| Plugin Id | 10020 |

| Bajo | Cookie Sin Flag HttpOnly |
| --- | --- |
| Descripción | Se ha establecido una cookie sin el flag HttpOnly, lo que significa que JavaScript puede acceder a la cookie. Si un script malicioso puede ser ejecutado en esta página, entonces la cookie será accesible y puede ser transmitida a otro sitio. Si se trata de una cookie de sesión, el secuestro de sesión puede ser posible. |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |
| Método | GET |
| Ataque |  |
| Evidencia | set-cookie: _streamlit_xsrf |
| Otra información |  |
| Instancia | 1 |
| Solución | Asegúrese de que la flag HttpOnly está establecida para todas las cookies. |
| Referencia | https://owasp.org/www-community/HttpOnly |
| CWE Id | 1004 |
| WASC Id | 13 |
| Plugin Id | 10010 |

| Bajo | Divulgación de Marcas de Tiempo - Unix |
| --- | --- |
| Descripción | Una marca de tiempo fue revelada por la aplicación/servidor web. - Unix |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |
| Método | GET |
| Ataque |  |
| Evidencia | 1780407500 |
| Otra información | 1780407500, que se evalúa como: 2026-06-02 08:38:20. |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |
| Método | GET |
| Ataque |  |
| Evidencia | 1780407512 |
| Otra información | 1780407512, que se evalúa como: 2026-06-02 08:38:32. |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |

| Método | GET |
| --- | --- |
| Ataque |  |
| Evidencia | 1780407526 |
| Otra información | 1780407526, que se evalúa como: 2026-06-02 08:38:46. |
| URL | http://172.30.19.93:9004/static/js/emotion-styled.browser.esm.BPUx6WuE.js |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/emotion-styled.browser.esm.BPUx6WuE.js |
| Método | GET |
| Ataque |  |
| Evidencia | 1540483477 |
| Otra información | 1540483477, que se evalúa como: 2018-10-25 11:04:37. |
| URL | http://172.30.19.93:9004/static/js/v4.D-g8Wqsd.js |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/v4.D-g8Wqsd.js |
| Método | GET |
| Ataque |  |
| Evidencia | 2080374784 |
| Otra información | 2080374784, que se evalúa como: 2035-12-04 04:53:04. |
| Instancia | 5 |
| Solución | Confirmar que los datos encontrados de información sobre la marca de tiempo no son sensibles, ni se pueden usar en patrones explotables de divulgación. |
| Referencia | https://cwe.mitre.org/data/definitions/200.html |
| CWE Id | 497 |
| WASC Id | 13 |
| Plugin Id | 10096 |

| Bajo | Falta encabezado X-Content-Type-Options |
| --- | --- |
| Descripción | La cabecera Anti-MIME-Sniffing X-Content-Type-Options no se ha establecido en 'nosniff'. Esto permite que las versiones anteriores de Internet Explorer y Chrome realicen MIME-sniffing en el cuerpo de la respuesta, lo que puede provocar que el cuerpo dé la respuesta se interprete y se muestre como un tipo de contenido distinto del tipo de contenido declarado. Las versiones actuales (principios de 2014) y heredadas de Firefox utilizarán el tipo de contenido declarado (si se establece uno), en lugar de realizar MIME- sniffing. |
| URL | http://172.30.19.93:9004/favicon.png |
| Nombre del Nodo | http://172.30.19.93:9004/favicon.png |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información | Este problema aún se aplica a las páginas de tipo error (401, 403, 500, etc.), ya que esas páginas a menudo se ven afectadas por problemas de inyección, en cuyo caso aún existe la preocupación de que los navegadores husmeen las páginas lejos de su tipo de contenido real. En el umbral «Alto» esta regla de análisis no alertará sobre respuestas de error del cliente o servidor. |

| URL | http://172.30.19.93:9004/static/js/assertNever.B_SfJlM1.js |
| --- | --- |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/assertNever.B_SfJlM1.js |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información | Este problema aún se aplica a las páginas de tipo error (401, 403, 500, etc.), ya que esas páginas a menudo se ven afectadas por problemas de inyección, en cuyo caso aún existe la preocupación de que los navegadores husmeen las páginas lejos de su tipo de contenido real. En el umbral «Alto» esta regla de análisis no alertará sobre respuestas de error del cliente o servidor. |
| URL | http://172.30.19.93:9004/static/js/eq.BGqw_fW_.js |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/eq.BGqw_fW_.js |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información | Este problema aún se aplica a las páginas de tipo error (401, 403, 500, etc.), ya que esas páginas a menudo se ven afectadas por problemas de inyección, en cuyo caso aún existe la preocupación de que los navegadores husmeen las páginas lejos de su tipo de contenido real. En el umbral «Alto» esta regla de análisis no alertará sobre respuestas de error del cliente o servidor. |
| URL | http://172.30.19.93:9004/static/js/loglevel.H4SN4KQm.js |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/loglevel.H4SN4KQm.js |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información | Este problema aún se aplica a las páginas de tipo error (401, 403, 500, etc.), ya que esas páginas a menudo se ven afectadas por problemas de inyección, en cuyo caso aún existe la preocupación de que los navegadores husmeen las páginas lejos de su tipo de contenido real. En el umbral «Alto» esta regla de análisis no alertará sobre respuestas de error del cliente o servidor. |
| URL | http://172.30.19.93:9004/static/js/preload-helper.CAj27AsG.js |
| Nombre del Nodo | http://172.30.19.93:9004/static/js/preload-helper.CAj27AsG.js |
| Método | GET |
| Ataque |  |
| Evidencia |  |
| Otra información | Este problema aún se aplica a las páginas de tipo error (401, 403, 500, etc.), ya que esas páginas a menudo se ven afectadas por problemas de inyección, en cuyo caso aún existe la preocupación de que los navegadores husmeen las páginas lejos de su tipo de contenido real. En el umbral «Alto» esta regla de análisis no alertará sobre respuestas de error del cliente o servidor. |

| Instancia | Systemic |
| --- | --- |
| Solución | Asegúrese de que la aplicación/servidor web establece el encabezado Content-Type adecuadamente, y que establece el encabezado X-Content-Type-Options a 'nosniff' para todas las páginas web. Si es posible, asegúrese de que el usuario final utiliza un navegador web moderno y compatible con los estándares que no realiza MIME-sniffing en absoluto, o que puede ser dirigido por la aplicación web/servidor web para que no realice MIME-sniffing. |
| Referencia | https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie- developer/compatibility/gg622941(v=vs.85) https://owasp.org/www-community/Security_Headers |
| CWE Id | 693 |
| WASC Id | 15 |
| Plugin Id | 10021 |

| Informativo | Aplicación Web Moderna |
| --- | --- |
| Descripción | La aplicación parece ser una aplicación web moderna. Si necesita explorarla automáticamente, el Ajax Spider puede ser más eficaz que el estándar. |
| URL | http://172.30.19.93:9004/ |
| Nombre del Nodo | http://172.30.19.93:9004/ |
| Método | GET |
| Ataque |  |
| Evidencia | <script> window.prerenderReady = false </script> |
| Otra información | No se han encontrado enlaces aunque sí scripts, lo que indica que se trata de una aplicación web moderna. |
| URL | http://172.30.19.93:9004/robots.txt |
| Nombre del Nodo | http://172.30.19.93:9004/robots.txt |
| Método | GET |
| Ataque |  |
| Evidencia | <script> window.prerenderReady = false </script> |
| Otra información | No se han encontrado enlaces aunque sí scripts, lo que indica que se trata de una aplicación web moderna. |
| URL | http://172.30.19.93:9004/sitemap.xml |
| Nombre del Nodo | http://172.30.19.93:9004/sitemap.xml |
| Método | GET |
| Ataque |  |
| Evidencia | <script> window.prerenderReady = false </script> |
| Otra información | No se han encontrado enlaces aunque sí scripts, lo que indica que se trata de una aplicación web moderna. |
| Instancia | 3 |
| Solución | Se trata de una alerta informativa, por lo que no es necesario realizar ningún cambio. |
| Referencia |  |
| CWE Id |  |
| WASC Id |  |
| Plugin Id | 10109 |

| Informativo | Respuesta de Gestión de Sesión Identificada |
| --- | --- |
| Descripción | Se ha identificado que la respuesta dada contiene un token de gestión de sesión. El campo 'Other Info' contiene un conjunto de tokens de cabecera que pueden utilizarse en el método Header Based Session Management (gestión de sesión basado en cabecera). Si la petición se encuentra en un contexto que tiene un método Session Management establecido en "Auto-Detect", esta regla cambiará la gestión de sesión para utilizar los tokens identificados. |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |
| Método | GET |
| Ataque |  |
| Evidencia | _streamlit_xsrf |
| Otra información | cookie:_streamlit_xsrf |
| URL | http://172.30.19.93:9004/_stcore/health |
| Nombre del Nodo | http://172.30.19.93:9004/_stcore/health |
| Método | GET |
| Ataque |  |
| Evidencia | _streamlit_xsrf |
| Otra información | cookie:_streamlit_xsrf |
| Instancia | 2 |
| Solución | Se trata de una alerta informativa y no de una vulnerabilidad, por lo que no hay nada que corregir. |
| Referencia | https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ |
| CWE Id |  |
| WASC Id |  |
| Plugin Id | 10112 |