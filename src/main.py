from fastapi import FastAPI
import helpers
app = FastAPI()

      

@app.get("/")
def read_index():
    return {"Hello": "World"}

@app.get("/generate_image")
def generate_image(prompt: str):
    return helpers.generate_image(prompt)