import torch, joblib

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.model import PCPricePredictor

app = FastAPI()
app.mount("/static", StaticFiles(directory="template"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load encoders properly
use_case_encoder = joblib.load("src/models/use_case_encoder.pth")
category_encoder = joblib.load("src/models/category_encoder.pth")
mlb = joblib.load("src/models/mlb_encoder.pth")

# Initialize model
input_size = 3  # budget, use_case, category
output_size = len(mlb.classes_)  # Number of unique components
model = PCPricePredictor(input_size, 10, output_size)

# Load trained model weights
model.load_state_dict(torch.load("src/models/model.pth"))
model.eval()

print("✅ Model and encoders loaded successfully!")



@app.post("/predict")
def predict(budget: int = Body(...), use_case: str = Body(...), category: str = Body(...)):
    # Encode categorical inputs
    use_case_encoded = use_case_encoder.transform([use_case])[0]
    category_encoded = category_encoder.transform([category])[0]

    # Convert to tensor
    input_tensor = torch.tensor([[budget, use_case_encoded, category_encoded]], dtype=torch.float32)

    with torch.no_grad():
        predicted_output = torch.sigmoid(model(input_tensor)).flatten()
    print(predicted_output)

    # Threshold predictions (consider values > 0.5 as selected)
    predicted_output = predicted_output.cpu().numpy()
    binary_output = (predicted_output > 0.5).astype(int).reshape(1, -1)
    predicted_components = mlb.inverse_transform(binary_output)[0]

    return {"predicted_components": predicted_components}
    # if budget <= 0:
    #     return {
    #         "message": "Prediction Unsuccessful",
    #         "error": "Give Me A Suitable Budget First So I Can Make Your Dream PC!"
    #     }
    
    # return {
    #     "message": "Prediction Successful",
    #     "budget": budget,
    #     "use_case": use_case,
    #     "category": category
    # }

@app.get("/")
def serve_index():
    return FileResponse("template/index.html")
