product_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "integer"},
        "description": {"type": "string"},
        "category": {"type": "string"}
    },
    "required": ["id", "title", "price"]
}

products_response_schema = {
    "type": "object",
    "properties": {
        "Items": {
            "type": "array",
            "items": product_schema
        }
    },
    "required": ["Items"]
}

error_schema = {
    "type": "object",
    "properties": {
        "errorMessage": {"type": "string"}
    },
    "required": ["errorMessage"]
}