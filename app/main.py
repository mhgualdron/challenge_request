from fastapi import FastAPI

app = FastAPI(title="Invoice API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Invoice API"}
