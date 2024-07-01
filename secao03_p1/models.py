from typing import Optional
from pydantic import BaseModel, validators


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aula: int
    horas: int

    @validators('titulo')
    def validar_titulo(cls, value: str):
        # validation 1
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        # validation 2
        if value.islower():
            raise ValueError('O titulo deve ser em capitalizado.')

        return value


cursos = [
    Curso(id=1, titulo='Programação para Leigos', aula=42, horas=94),
    Curso(id=2, titulo='Lógica IA', aula=42, horas=94),
]
