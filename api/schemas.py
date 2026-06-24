"""JSON Schema для валидации API ответов"""

signup_response_schema = {
    "oneOf": [
        {"type": "string", "maxLength": 0},
        {
            "type": "object",
            "properties": {"errorMessage": {"type": "string"}},
            "required": ["errorMessage"],
            "additionalProperties": False,
        },
    ]
}

login_response_schema = {
    "type": "object",
    "properties": {"errorMessage": {"type": "string"}},
    "required": ["errorMessage"],
    "additionalProperties": False,
}

products_response_schema = {
    "type": "object",
    "properties": {
        "Items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "price": {"type": "number"},
                    "desc": {"type": "string"},
                    "category": {"type": "string"},
                    "cat": {"type": "string"},
                    "img": {"type": "string"},
                },
                "required": ["id", "title", "price"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["Items"],
    "additionalProperties": False,
}

product_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "desc": {"type": "string"},
        "category": {"type": "string"},
        "img": {"type": "string"},
    },
    "required": ["id", "title", "price"],
    "additionalProperties": False,
}
