# test_context.py
import os
from config import settings

print("=== BEFORE setting CONTEXT ===")
print(f"Context from settings: {settings.context}")
print(f"Is bstack: {settings.is_bstack}")
print(f"App URL: {settings.app_url}")

print("\n=== Setting CONTEXT=bstack ===")
os.environ["CONTEXT"] = "bstack"
settings._load_mobile_context()

print("\n=== AFTER setting CONTEXT ===")
print(f"Context from settings: {settings.context}")
print(f"Is bstack: {settings.is_bstack}")
print(f"App URL: {settings.app_url}")