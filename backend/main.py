from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import json
import secrets

load_dotenv()

app = FastAPI()
security = HTTPBasic()

@app.get("/")
async def download_button():
    return FileResponse("./index.html")

@app.get("/download")
async def download_file(g_recaptcha_response = Query(..., alias="g-recaptcha-response")):

    # Create body for captcha verification
    captcha_verification_body = {
        "secret": os.getenv("CAPTCHA_SECRET"),
        'response': g_recaptcha_response
    }

    # Verify the reCAPTCHA response
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data=captcha_verification_body).json()

    if res.get('success'):
        file_path = Path("./sample-text-file.txt")

        if not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(path=file_path, filename="sample-text-file.txt")
    else:
        raise HTTPException(status_code=400, detail="reCAPTCHA verification failed. Please try again.")

@app.get("/download2")
async def download2_file():

    file_path = Path("./sample-text-file.txt")

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename="sample-text-file.txt")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
