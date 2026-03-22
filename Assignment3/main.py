from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

products = [
    {"id": 1, "name": "Notebook", "price": 499, "category": "Stationery", "in_stock": True},
    {"id": 2, "name": "Pen", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

def find_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product
    return None


@app.get("/products")
def get_products(name: Optional[str] = None):
    if name:
        filtered = [p for p in products if p["name"].lower() == name.lower()]
        return {"products": filtered, "total": len(filtered)}

    return {"products": products, "total": len(products)}
@app.post("/products")
def add_product(name: str, price: int, category: str, in_stock: bool):
    for p in products:
        if p["name"].lower() == name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "category": category,
        "in_stock": in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }


@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


@app.get("/products/audit")
def audit_products():
    total_products = len(products)

    in_stock_items = [p for p in products if p["in_stock"]]
    out_of_stock_items = [p for p in products if not p["in_stock"]]

    total_stock_value = sum(p["price"] * 10 for p in in_stock_items)

    most_expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_items),
        "out_of_stock_names": [p["name"] for p in out_of_stock_items],
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }


@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):
    if discount_percent <= 0 or discount_percent >= 100:
        return {"message":"Product not found"}

    updated = []

    for p in products:
        if p["category"].lower() == category.lower():
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {"message": "No products found in this category"}

    return {
        "updated_count": len(updated),
        "updated_products": updated
    }


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {"message":"404 Not Found"}
    return product


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = None,
    in_stock: Optional[bool] = None
):
    product = find_product(product_id)

    if not product:
        return {"message":"404 Not Found"}

    if price is not None:
        product["price"] = price

    if in_stock is not None:
        product["in_stock"] = in_stock

    return {
        "message": "Product updated",
        "product": product
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = find_product(product_id)

    if not product:
        return {"message":"404 Not Found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }