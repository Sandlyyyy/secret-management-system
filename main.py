from fastapi import FastAPI

# создаём объект app, который uvicorn ищет
app = FastAPI(title="Secret Management System")

@app.get("/")
def root():
    return {"message": "Secret Management System API is running"}

# для удобного запуска через python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
