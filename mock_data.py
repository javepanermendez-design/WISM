"""Mock data for Ilocos Grocers Distribution Center."""
from datetime import date, timedelta

CATEGORIES = ["Rice & Grains", "Canned Goods", "Beverages", "Noodles & Pasta", "Condiments & Sauces", "Snacks & Biscuits", "Dairy & Frozen", "Household & Personal Care"]
CATEGORY_PREFIXES = {"Rice & Grains": "RG", "Canned Goods": "CG", "Beverages": "BV", "Noodles & Pasta": "NP", "Condiments & Sauces": "CS", "Snacks & Biscuits": "SB", "Dairy & Frozen": "DF", "Household & Personal Care": "HP"}
ZONES = ["A", "B", "C", "D"]
ZONE_NAMES = {"A": "Dry goods", "B": "Beverages", "C": "Chilled & frozen", "D": "Household & bulk"}
SUPPLIERS = ["Amianan Grain Mill", "Bantay Canning Cooperative", "Cordillera Refreshments", "Laoag Dairy Hub", "Vigan Pantry Works", "Northline Frozen Foods", "Ilocos Homecare Supply", "Abra Valley Trading"]
USERS = [{"id": 1, "name": "Maya Chen", "role": "Inventory supervisor", "initials": "MC"}, {"id": 2, "name": "Evan Brooks", "role": "Receiving clerk", "initials": "EB"}]

_specs = [
    ("Jasmine Rice 25kg sack", "Rice & Grains", "sack", 120, 40, 220), ("Premium Rice 5kg sack", "Rice & Grains", "sack", 68, 24, 140), ("Brown Rice 2kg pack", "Rice & Grains", "pack", 54, 20, 100), ("Glutinous Rice 1kg pack", "Rice & Grains", "pack", 31, 18, 80), ("Corn Grits 1kg pack", "Rice & Grains", "pack", 18, 25, 80), ("Mung Beans 500g pack", "Rice & Grains", "pack", 46, 18, 90),
    ("Sardines in Tomato Sauce 155g (50 cans/case)", "Canned Goods", "case", 42, 18, 90), ("Corned Beef 150g (48 cans/case)", "Canned Goods", "case", 27, 18, 70), ("Corn Kernels 425g (24 cans/case)", "Canned Goods", "case", 26, 20, 60), ("Fruit Cocktail 836g (24 cans/case)", "Canned Goods", "case", 39, 12, 70), ("Evaporated Milk 370ml (48 cans/case)", "Canned Goods", "case", 22, 15, 60), ("Tomato Paste 70g (100 sachets/carton)", "Canned Goods", "carton", 8, 18, 50),
    ("Bottled Water 500ml (24/case)", "Beverages", "case", 88, 30, 180), ("Sparkling Water 1L (12/case)", "Beverages", "case", 36, 15, 80), ("Calamansi Drink 350ml (24/case)", "Beverages", "case", 52, 20, 100), ("Iced Tea 1L (12/case)", "Beverages", "case", 15, 18, 70), ("Mango Juice 1L (12/case)", "Beverages", "case", 24, 20, 60), ("Coffee Drink 240ml (24/case)", "Beverages", "case", 44, 16, 80),
    ("Instant Pancit Canton 60g (40/box)", "Noodles & Pasta", "box", 74, 25, 140), ("Instant Mami Noodles 55g (40/box)", "Noodles & Pasta", "box", 61, 25, 140), ("Spaghetti 500g (20/carton)", "Noodles & Pasta", "carton", 29, 18, 80), ("Macaroni 400g (24/carton)", "Noodles & Pasta", "carton", 25, 18, 70), ("Rice Vermicelli 250g (30/carton)", "Noodles & Pasta", "carton", 32, 12, 70), ("Lasagna Sheets 250g (20/box)", "Noodles & Pasta", "box", 19, 10, 50),
    ("Soy Sauce 1L (12/case)", "Condiments & Sauces", "case", 46, 18, 90), ("Cane Vinegar 1L (12/case)", "Condiments & Sauces", "case", 41, 18, 90), ("Banana Ketchup 320g (24/case)", "Condiments & Sauces", "case", 17, 18, 70), ("Cooking Oil 1L (12/case)", "Condiments & Sauces", "case", 64, 24, 110), ("Fish Sauce 750ml (12/case)", "Condiments & Sauces", "case", 34, 14, 80), ("Chili Garlic Sauce 180g (24/case)", "Condiments & Sauces", "case", 21, 12, 60),
    ("Cream Crackers 250g (30/box)", "Snacks & Biscuits", "box", 96, 30, 180), ("Butter Cookies 300g (24/box)", "Snacks & Biscuits", "box", 45, 18, 100), ("Banana Chips 100g (50/carton)", "Snacks & Biscuits", "carton", 28, 16, 70), ("Cheese Puffs 60g (40/box)", "Snacks & Biscuits", "box", 7, 15, 60), ("Peanut Brittle 100g (30/box)", "Snacks & Biscuits", "box", 34, 12, 70), ("Wafer Sticks 90g (40/box)", "Snacks & Biscuits", "box", 22, 14, 60),
    ("Fresh Milk 1L (12/carton)", "Dairy & Frozen", "carton", 26, 12, 60), ("Cheddar Cheese 165g (24/box)", "Dairy & Frozen", "box", 20, 12, 45), ("Frozen Chicken 1kg (10/case)", "Dairy & Frozen", "case", 38, 14, 70), ("Frozen Mixed Vegetables 1kg (10/case)", "Dairy & Frozen", "case", 0, 10, 40), ("Ice Cream Tub 1.5L (6/case)", "Dairy & Frozen", "case", 20, 8, 40), ("Margarine 250g (24/box)", "Dairy & Frozen", "box", 17, 10, 50),
    ("Laundry Powder 1kg (12/case)", "Household & Personal Care", "case", 52, 18, 110), ("Dishwashing Liquid 500ml (24/case)", "Household & Personal Care", "case", 0, 15, 80), ("Bath Soap 90g (72/box)", "Household & Personal Care", "box", 72, 25, 160), ("Toothpaste 150g (48/box)", "Household & Personal Care", "box", 35, 18, 90), ("Kitchen Tissue 2-ply (24/pack)", "Household & Personal Care", "pack", 49, 20, 100), ("Garbage Bags Medium (20/pack)", "Household & Personal Care", "pack", 18, 12, 60),
]
_perishable = {"Dairy & Frozen", "Canned Goods", "Snacks & Biscuits", "Noodles & Pasta"}
_products = []
for index, (name, category, unit, stock, minimum, maximum) in enumerate(_specs, 1):
    prefix = CATEGORY_PREFIXES[category]
    expiry = None
    if category in _perishable:
        expiry_days = {7: 12, 12: 24, 21: 29, 34: 18}.get(index, 90 + index)
        expiry = (date.today() + timedelta(days=expiry_days)).isoformat()
    zone = ZONES[(index - 1) % len(ZONES)]
    _products.append({"id": index, "sku": f"{prefix}-{index:04d}", "name": name, "category": category, "zone": zone, "aisle": f"{(index - 1) % 12 + 1:02d}", "bin": f"{(index * 3) % 20 + 1:02d}", "location": f"{zone}-{(index - 1) % 12 + 1:02d}-{(index * 3) % 20 + 1:02d}", "stock": stock, "min_stock": minimum, "max_stock": maximum, "unit": unit, "supplier": SUPPLIERS[(index - 1) % len(SUPPLIERS)], "price": round(45 + index * 3.75, 2), "expiry_date": expiry})
products = _products[:45]

expected_deliveries = [{"id": i, "supplier": SUPPLIERS[(i - 1) % len(SUPPLIERS)], "delivery_no": f"ASN-{2600 + i}", "date": (date.today() + timedelta(days=i)).isoformat(), "lines": [{"product_id": i * 2, "quantity": 24 + i * 4}], "status": "Expected"} for i in range(1, 7)]
_customer_names = ["Rosa Sari-Sari Store", "Amianan Mini-Mart", "Bantay Corner Shop", "Laoag Family Store", "Vigan Daily Needs", "Pagudpud Quick Stop", "San Nicolas Market", "Narvacan Mini-Mart", "Candon Value Store", "Bacarra Sari-Sari", "Batac Neighborhood Shop", "Dingras Pantry"]
_statuses = ["Pending", "Picking", "Ready", "Completed", "Pending", "Picking", "Completed", "Ready", "Pending", "Completed", "Picking", "Pending"]
orders = [{"id": i, "number": f"ORD-{6200 + i}", "customer": customer, "status": _statuses[i - 1], "created": (date.today() - timedelta(days=i)).isoformat(), "completed_by": "Maya Chen" if _statuses[i - 1] == "Completed" else None, "completed_at": (date.today() - timedelta(days=max(1, i - 1))).isoformat() if _statuses[i - 1] == "Completed" else None, "lines": [{"product_id": i, "quantity": 5 + i % 5, "picked": 0 if _statuses[i - 1] == "Pending" else min(5 + i % 5, 3 + i % 5)}, {"product_id": i + 8, "quantity": 3, "picked": 3 if _statuses[i - 1] in ("Ready", "Completed") else 0}]} for i, customer in enumerate(_customer_names, 1)]
movements = [{"id": i, "product_id": (i % len(products)) + 1, "type": ["Received", "Released", "Transferred", "Adjusted"][i % 4], "quantity": (i % 12) + 1, "previous": 40 + i, "updated": 40 + i + (i % 12) + 1, "user": USERS[i % 2]["name"], "reference": f"REF-{8200 + i}", "created": (date.today() - timedelta(days=i % 14)).isoformat()} for i in range(1, 61)]
notifications = [{"id": i, "title": title, "body": body, "unread": i < 6, "created": "Today" if i < 10 else "Earlier"} for i, title, body in [(1, "Low stock alert", "Cheese Puffs 60g is below the reorder level."), (2, "Delivery due tomorrow", "Amianan Grain Mill · ASN-2601"), (3, "Order waiting", "ORD-6202 has been picking for 48 minutes."), (4, "Expiry watch", "Four grocery products expire within 30 days."), (5, "Order ready", "ORD-6203 is ready to dispatch."), (6, "Cycle count due", "Zone C chilled & frozen count is due today."), (7, "Delivery received", "Vigan Pantry Works delivery was closed."), (8, "New team member", "Evan Brooks joined receiving."), (9, "Report ready", "Weekly grocery stock movement report is ready."), (10, "Order completed", "ORD-6204 shipped successfully."), (11, "Low stock resolved", "Cane Vinegar is back above minimum."), (12, "Location changed", "Fresh Milk moved to C-09-10."), (13, "Delivery delayed", "Northline Frozen Foods moved one day."), (14, "Order waiting", "ORD-6212 is ready for picking."), (15, "System update", "Inventory sync completed.")]]
activity = [{"label": "Received 24 Premium Rice sacks", "detail": "Amianan Grain Mill · REF-8208", "quantity": "+24", "direction": "up", "time": "18 min ago"}, {"label": "Released 5 Sardines cases", "detail": "ORD-6202 · Evan Brooks", "quantity": "-5", "direction": "down", "time": "42 min ago"}, {"label": "Adjusted Frozen Chicken", "detail": "Cycle count · Maya Chen", "quantity": "+2", "direction": "up", "time": "1 hr ago"}, {"label": "Transferred Bottled Water cases", "detail": "B-03 to B-04", "quantity": "12", "direction": "neutral", "time": "2 hrs ago"}]

def get_product(product_id):
    return next((p for p in products if p["id"] == int(product_id)), None)

def enrich_product(product):
    return {**product, "status": status_for(product), "movements": [m for m in movements if m["product_id"] == product["id"]][-5:]}

def status_for(product):
    return "Out of Stock" if product["stock"] == 0 else "Low Stock" if product["stock"] <= product["min_stock"] else "In Stock"
