from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"spotify to apple music"}