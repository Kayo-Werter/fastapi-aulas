from typing import Optional
from pydantic import BaseModel

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int
    

cursos = [
    Curso(id=1, titulo='Programação python', aulas=12, horas=42),
    Curso(id=2, titulo='Programação Java', aulas=41, horas=54),
    Curso(id=3, titulo='Programação C++', aulas=23, horas=65),
]