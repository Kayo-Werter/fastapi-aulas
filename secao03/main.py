from typing import Optional, Any, List, Dict
from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends


from time import sleep
from models import Curso, cursos

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
         response_model=List[Curso])
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/curso/{curso_id}')
async def get_curso(curso_id: int = Path(Default=None, title='ID do curso', description='Deve ser 1 ou 2', gt=0, lt=5), db: Any = Depends(fake_db)):
    try:

        curso = cursos[curso_id]
        return curso  
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso Não Encontrado')  


@app.post('/cursos', 
          status_code=status.HTTP_201_CREATED,
          response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
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
