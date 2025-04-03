import random

categories = ["desktop", "laptop"]
use_cases = ["gaming", "content_creation", "workstation", "software_developements", "casual"]
cpus = ["Ryzen 5", "Ryzen 7", "Xeon", "Threadripper", "Core i3", "Core i9","Core i5","Core i7", "Pentium"]
gpus = ["GTX 1650", "RTX 3060", "RTX 4070", "RTX 4090", "RTX 4060", "RTX 4080", "RX 6700", "RX 6800", "RX 6900", 
        "RX 7900", "RX 7900XTX"]
rams = ["8GB", "16GB", "32GB", "64GB"]
rams_type = ["DDR4", "DDR5"]
storages = ["512GB SSD", "1TB SSD", "2TB SSD", "1TB HDD"]
storages_type = ["SSD", "HDD"]
laptops = ["Asus ROG", "Dell XPS", "MacBook Pro", "Macbook Air","Lenovo Legion", "HP Spectre", "Razer Blade", "MSI Stealth",
           "Alienware", "Acer Predator", "Gigabyte Aero", "Surface Laptop", "Lenovo ThinkPad", "HP Envy",
           "Asus ZenBook", "Dell Inspiron", "Razer Blade Stealth", "MSI GS Series", "Acer Swift", "HP Omen"]

def generate_random_data(num_entries=1000):
    data = []
    for _ in range(num_entries):
        budget = random.randint(500, 5000)
        use_case = random.choice(use_cases)
        category = random.choice(categories)
        if category == "desktop":
            components = {
                "CPU": random.choice(cpus),
                "GPU": random.choice(gpus),
                "RAM": random.choice(rams),
                "RAM Type": random.choice(rams_type),
                "Storage": random.choice(storages),
                "Storage Type": random.choice(storages_type),
                "Total Cost": budget
            }
        else:
            components = {
                "Laptop Model": random.choice(laptops),
                "RAM": random.choice(rams),
                "RAM Type": random.choice(rams_type),
                "Storage": random.choice(storages),
                "Storage Type": random.choice(storages_type),
                "Total Cost": budget
            }
        data.append({"budget": budget, "use_case": use_case, "category": category, "components": components})
    return data

