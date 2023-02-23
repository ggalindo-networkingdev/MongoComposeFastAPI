from urllib import response
from fastapi import Depends, FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from endpoints  import test
from fastapi.middleware.cors import CORSMiddleware


tags_metadata = [
    {
        "name": "test",
        "description": "this endpoints is for running a devices compare version",
    }
]


app = FastAPI(openapi_tags=tags_metadata)


v1 = APIRouter(prefix="/api")
v1.include_router(test.router)

app.include_router(v1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://172.17.0.2:5006", "http://192.168.39.200:5006/", "http://localhost:3978", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    response_html = """
    Authorized access only
    """
    return HTMLResponse(content=response_html, status_code=200)

