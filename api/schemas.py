"""JSON Schema для валидации API ответов"""

# Для /signup - может быть пустая строка (успех) или объект с ошибкой
signup_response_schema = {
    "oneOf": [
        {"type": "string", "maxLength": 0},
        {
            "type": "object",
            "properties": {
                "errorMessage": {"type": "string"}
            },
            "required": ["errorMessage"],
            "additionalProperties": False
        }
    ]
}

# Для /login - всегда объект с errorMessage
login_response_schema = {
    "type": "object",
    "properties": {
        "errorMessage": {"type": "string"}
    },
    "required": ["errorMessage"],
    "additionalProperties": False
}

# Для /bycat - список товаров (с полями cat и img)
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
                    "img": {"type": "string"}
                },
                "required": ["id", "title", "price"],
                "additionalProperties": False
            }
        }
    },
    "required": ["Items"],
    "additionalProperties": False
}

# Для /view - один товар
product_response_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "price": {"type": "number"},
        "desc": {"type": "string"},
        "category": {"type": "string"},
        "img": {"type": "string"}
    },
    "required": ["id", "title", "price"],
    "additionalProperties": False
}