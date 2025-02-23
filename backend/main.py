from fastapi import FastAPI
import time

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/validate-claim")
async def sample():
    print("Reading Documents...")
    time.sleep(2)
    print("Analyzing Documents...")
    time.sleep(2)
    print("Extracting Data...")
    time.sleep(2)
    print("Validating Data...")
    time.sleep(2)
    print("Generating Report...")
    time.sleep(2)
    return