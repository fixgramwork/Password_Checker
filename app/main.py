from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from .models import InputData
from .password_checker import check_password_strength

app = FastAPI()

# static 파일 마운트
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check")
async def check_password(input_data: InputData):
    try:
        if not input_data.input:
            raise HTTPException(status_code=400, detail="비밀번호를 입력해주세요")
        
        if len(input_data.input) > 40:  # 최대 길이 제한
            raise HTTPException(status_code=400, detail="비밀번호가 너무 깁니다")
            
        result = check_password_strength(input_data.input)
        return JSONResponse(content={"response": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))