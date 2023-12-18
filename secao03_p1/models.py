from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')

        return value
    
    @validator('aulas')
    def validar_aulas(cls, aulas: int):
        if aulas < 12:
            raise ValueError('A quantidade de aulas deve ser maior do que 12')
        
        return aulas
    
    @validator('horas')
    def validar_horas(cls, horas: int):
        if horas < 10:
            raise ValueError('A quantidade de horas deve ser maior que 10')

        return horas



cursos = [
    Curso(id=1, titulo="Curso de python", aulas=41, horas=120),
    Curso(id=2, titulo="Curso de Java", aulas=50, horas=180),

]