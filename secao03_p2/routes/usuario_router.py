from fastapi import APIRounter


router = APIRounter()


@router.get('/api/v1/usuarios')
async def get_usuarios():
    return {"info": "Todos os usuários"}
