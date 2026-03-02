from pydantic import BaseModel, Field

"""Modelo de datos para el análisis completo de un C.V."""

class AnalisisCV(BaseModel):
    nombre_candidato: str = Field(description="Nombre completo del candidato extraído del C.V.")
    experiencia_anios: int = Field(description="Años totales de experiencia laboral relevante")
    habilidades_clave: list[str] = Field(description="Lista de las 5-7 habilidades del candidato mas relevantes del candidato")
    education: str = Field(description="Nivel educativo mas alto y especialización principal")
    experiencia_relevante: str = Field(description="Resumen conciso de la experiencia mas relevante para el puesto especifico")
    fortalezas: list[str] = Field(description="3-5 principales fortalezas de la candidato")
    areas_mejora: list[str] = Field(description="2-4 áreas donde el candidato podría desarrollarse o mejorar")
    porcentaje_ajuste: int = Field(description="Porcentaje de ajuste al puesto (0-100) basada en experiencia, habilidades y formación del candidato", ge=0, le=100,)
