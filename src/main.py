from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict(
    budget: int = Body(...), 
    use_case: str = Body(...), 
    category: str = Body(...)
):
    if budget <= 0:
        return {
            "message": "Prediction Unsuccessful",
            "error": "Give Me A Suitable Budget First So I Can Make Your Dream PC!"
        }
    
    return {
        "message": "Prediction Successful",
        "budget": budget,
        "use_case": use_case,
        "category": category
    }

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="template"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("template/index.html")
