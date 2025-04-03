from src.data import generate_random_data

def get_sample_data():
    return generate_random_data()

def get_closest_match(budget, use_case, category):
    data = get_sample_data()
    filtered_data = [entry for entry in data if entry["category"] == category and entry["use_case"] == use_case]
    if not filtered_data:
        return {"error": "No matching configuration found"}
    closest = min(filtered_data, key=lambda x: abs(x["budget"] - budget))
    return closest