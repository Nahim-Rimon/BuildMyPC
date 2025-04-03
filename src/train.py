import torch
import torch.optim as optim
import torch.nn as nn
import pandas as pd
import joblib
from model import PCPricePredictor
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

# Load dataset
df = pd.read_csv("../pc_data.csv")  # Replace with actual file path

# Encode categorical columns
use_case_encoder = LabelEncoder()
category_encoder = LabelEncoder()

df["use_case"] = use_case_encoder.fit_transform(df["use_case"])
df["category"] = category_encoder.fit_transform(df["category"])

# Ensure components are stored as lists of strings
def parse_components(component_str):
    try:
        components_dict = eval(component_str)  # Convert string to dict
        if isinstance(components_dict, dict):
            return list(map(str, components_dict.values()))  # Ensure all values are strings
        return []
    except:
        return []

df["components"] = df["components"].apply(parse_components)

# Encode components using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
component_labels = mlb.fit_transform(df["components"])

# Convert DataFrame to tensors
X = torch.tensor(df[["budget", "use_case", "category"]].values, dtype=torch.float32)
Y = torch.tensor(component_labels, dtype=torch.float32)

# Define model
input_size = X.shape[1]  # 3 inputs
output_size = len(mlb.classes_)  # Number of unique components
model = PCPricePredictor(input_size, 10, output_size)

# Training setup
criterion = nn.BCEWithLogitsLoss()  # Binary cross-entropy loss for multi-label classification
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Train model
epochs = 1000
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, Y)
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch}/{epochs}, Loss: {loss.item()}")

# ✅ Save model and encoders correctly
torch.save(model.state_dict(), "models/model.pth")  # ✅ Model is saved properly

# ✅ Save encoders using joblib
joblib.dump(use_case_encoder, "models/use_case_encoder.pth")
joblib.dump(category_encoder, "models/category_encoder.pth")
joblib.dump(mlb, "models/mlb_encoder.pth")

print("✅ Model trained and saved successfully!")
