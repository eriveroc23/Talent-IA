from langchain_google_genai import ChatGoogleGenerativeAI
from models.cv_model import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts

def crear_evaluador_cv():
    """
    Crea y configura la cadena de evaluación de CV.

    Pasos:
    - Inicializa el modelo generativo (`ChatGoogleGenerativeAI`) con parámetros básicos
      (modelo y temperatura).
    - Envuelve el modelo para producir una salida estructurada según la clase `AnalisisCV`.
    - Construye el prompt del sistema mediante `crear_sistema_prompts` y lo concatena
      con el modelo estructurado para obtener la cadena de evaluación completa.

    Retorna:
        Una cadena lista para invocar con entradas del CV y descripción del puesto.
    """
    modelo_base = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    # Adaptar la salida del modelo a la estructura definida en AnalisisCV
    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)

    # Prompt del sistema que guía la evaluación (p. ej. instrucciones y formato)
    chat_prompt = crear_sistema_prompts()

    # Combina el prompt con el modelo estructurado formando la "pipeline" de evaluación
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion


def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    """
    Evalúa un CV frente a una descripción de puesto y devuelve un AnalisisCV.

    Args:
        texto_cv: Texto plano del CV a evaluar.
        descripcion_puesto: Descripción del puesto para comparar y ponderar el ajuste.

    Comportamiento:
    - Construye la cadena de evaluación mediante `crear_evaluador_cv`.
    - Invoca la cadena con un diccionario que contiene `texto_cv` y `descripcion_puesto`.
    - Si ocurre una excepción durante la invocación, devuelve un objeto `AnalisisCV`
      con valores indicativos de error para permitir manejo seguro aguas abajo.

    Retorna:
        Un objeto `AnalisisCV` con el resultado del análisis (o con campos de error).
    """
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        # Devolver el resultado del análisis cuando la invocación es exitosa
        return resultado

    except Exception:
        # Valor por defecto en caso de fallo; útil para evitar excepciones en el llamador.
        return AnalisisCV(
            nombre_candidato="Error en procesamiento.",
            experiencia_anios=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar",
            experiencia_relevante="Error durante el análisis,",
            fortalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcentaje_ajuste=0
        )

