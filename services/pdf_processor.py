import PyPDF2
from io import BytesIO

def extraer_texto_pdf(archivo_pdf):
    """
    Extrae texto de un archivo PDF.

    Parámetros:
        archivo_pdf: objeto con método `read()` (p. ej. archivo subido en memoria).

    Retorna:
        str: Texto extraído con separadores por página o mensaje de error.

    Comportamiento:
        - Lee el contenido del archivo usando `archivo_pdf.read()`.
        - Usa `PyPDF2.PdfReader` para parsear el PDF y `extract_text()` por página.
        - Añade un encabezado `--- Página N ---` antes del texto de cada página no vacío.
        - Si no se extrae texto (p. ej. solo imágenes), devuelve un mensaje de error.
        - En caso de excepción, devuelve un mensaje con la descripción del error.
    """
    try:
        # Cargar PDF desde bytes en memoria
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""

        # Iterar páginas y concatenar texto no vacío con separadores
        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            texto_pagina = pagina.extract_text() or ""
            if texto_pagina.strip():
                texto_completo += f"\n--- Página {numero_pagina} ---\n"
                texto_completo += texto_pagina + "\n"

        texto_completo = texto_completo.strip()

        # Si no hay texto extraído, informar que el PDF puede contener solo imágenes
        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."

        return texto_completo

    except Exception as e:
        # Retornar un mensaje legible con la excepción capturada
        return f"Error al procesar el archivo PDF: {str(e)}"