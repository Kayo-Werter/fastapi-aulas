from typing import Optional, Any, List
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from models import Curso, cursos
from fastapi.responses import JSONResponse
from fastapi import Response
from fastapi import Path
from fastapi import Query
from fastapi import Header
from time import sleep
from fastapi import Depends

def fake_db():
    try:
        print('Abrindo conexão com BD')
        sleep(1)
    finally:
        print('Fechando conexão com BD')
        sleep(1)



app = FastAPI(
    title="API Cursos",
    version="0.0.1",
    description="Uma API para estudo do fastAPI"
    )



@app.get('/cursos', 
         description='Retorna todos os cursos ou uma lista vazia', 
         summary='retorna todos os cursos',
         response_model=List[Curso],
         response_description='Curso encontrados!')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/curso/{curso_id}')
async def get_curso(curso_id: int = Path(Default=None, title='ID do curso', description='Deve ser 1 ao 5', gt=0, lt=6), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso Não Encontrado')  


@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe curso com o ID {curso_id}")
    

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe curso com o ID {curso_id}")
    

@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None) , c: Optional[int]=None):
    soma: int = a + b
    if c:
        soma += c

    print(f'x-geek: {x_geek}')

    return{"resultado": soma}




if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
