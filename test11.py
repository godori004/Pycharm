from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "테스트1"

@app.get("/report1")
def process_report1():
    return "레포트1"

@app.get("/report2")
def process_report2():
    return "레포트2"