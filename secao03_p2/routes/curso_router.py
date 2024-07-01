from fastapi import APIRounter


router = APIRounter()


@router.get('/api/v1/cursos')
async def get_cursos():
    return {"info": "Todos os cursos"}
