from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session


router = APIRouter()


# POST curso
@router.post('/', status_code=201, response_model=CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo,
                            aulas=curso.aulas, hora=curso.horas)

    db.add(novo_curso)
    await db.commit()   #

    return novo_curso


# GET cursos
@router.get('/', response_model=list[CursoSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:   # inicia bloco
        query = select(CursoModel)
        resultado = await session.execute(query)    # await for execute
        cursos: list[CursoModel] = resultado.scalars().all()

        return cursos


# GET curso
@router.get('/{curso_id}', status_code=200, response_model=CursoSchema)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        resultado = await session.execute(query)
        curso = resultado.scalar_one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(
                detail='Curso não encontrado.', status_code=404)


# PUT curso
@router.put('/{curso_id}', response_model=CursoSchema, status_code=202)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        resultado = await session.execute(query)
        curso_up = resultado.scalar_one_or_none()

        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()

            return curso_up
        else:
            raise HTTPException(
                detail='Curso não encontrado.', status_code=404)


# DELETE curso
@router.delete('/{curso_id}', status_code=204)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        resultado = await session.execute(query)
        curso_del = resultado.scalar_one_or_none()

        if curso_del:
            await session.delete(curso_del)
            await session.commit()

            return Response(status_code=204)
        else:
            raise HTTPException(
                detail='Curso não encontrado.', status_code=204)
