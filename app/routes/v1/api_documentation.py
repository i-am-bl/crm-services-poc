import os

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter()

cur_dir = os.getcwd()
tar_dir = "app/docs"
serv_dir = os.path.join(cur_dir, tar_dir)
file_ = "docs.html"
serve_file = os.path.join(serv_dir, file_)

router.mount("/docs", StaticFiles(directory=serv_dir), name="docs")


@router.get("/docs/v1/", response_class=HTMLResponse)
async def get_docs():
    # print(cur_dir)
    return FileResponse("/docs.html")
