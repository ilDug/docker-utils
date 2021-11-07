from config.conf import IMAGES_UPLOAD_PATH
from fastapi import APIRouter,  File,  UploadFile, Path, Depends, HTTPException, Body
import aiofiles
import os
from utils.string import generate_image_name, generate_image_name_b64
from middlewares.auth import authentication_guard, admin_guard
from models.images import ImageB64UploadRequestModel
import base64

router = APIRouter(tags=['images'])


@router.post("/images/upload/b64", dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def upload_image(file: ImageB64UploadRequestModel = Body(...)):
    dest_path = generate_image_name_b64(file.filename)
    try:
        async with aiofiles.open(dest_path, 'wb') as f:
            # async write chunk
            await f.write(base64.decodebytes(file.base64.encode()))
        return True
    except Exception as e:
        raise HTTPException(500, "ERRORE caricamento immagine: " + str(e))


@router.post("/images/upload", dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def upload_image(file: UploadFile = File(...)):
    dest_path = generate_image_name(file.content_type)
    try:
        async with aiofiles.open(dest_path, 'wb') as f:
            while content := await file.read(1024):  # async read chunk
                await f.write(content)  # async write chunk

        return True
    except Exception as e:
        raise HTTPException(500, "ERRORE caricamento immagine: " + str(e))


@router.delete("/images/{imagename}", dependencies=[Depends(authentication_guard), Depends(admin_guard)])
async def delete_image(imagename: str = Path(...)):
    file_path = IMAGES_UPLOAD_PATH / imagename
    if not file_path.exists():
        raise HTTPException(500, "il file non esiste")

    try:
        os.remove(file_path)
        return True
    except Exception as e:
        raise HTTPException(500, "errore eliminazione immagine")


@router.get("/images")
async def get_images():
    dir = IMAGES_UPLOAD_PATH
    extensions = [".png", ".jpeg", ".jpg"]
    files = [f for f in dir.iterdir() if f.is_file()]
    images = [img.name for img in files if img.suffix in extensions]
    images.sort(reverse=True)
    return images
