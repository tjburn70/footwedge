from fastapi import FastAPI, Request, HTTPException
import uvicorn


path_prefix = '/search'

app = FastAPI(openapi_prefix=path_prefix)

SEARCH_ENGINE_URL = "http://localhost:9200"


@app.get('/health')
async def root():
    return "Welcome to Search Service"


@app.post('/index')
async def create_index():
    pass


@app.put('/index')
async def add_to_index():
    pass


@app.get('/index')
async def search_index():
    pass


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8001, reload=True)
