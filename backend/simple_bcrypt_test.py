#!/usr/bin/env python3
"""Simple bcrypt test to diagnose the issue"""

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "testpass123"
print(f"Password: '{password}'")
print(f"Password length: {len(password)} characters")
print(f"Password byte length: {len(password.encode('utf-8'))} bytes")

try:
    hashed = pwd_context.hash(password)
    print(f"Hash successful: {hashed[:30]}...")
except Exception as e:
    print(f"Hash failed: {e}")

# Test with shorter password
short_password = "test"
print(f"\nShort password: '{short_password}'")
print(f"Short password length: {len(short_password)} characters")

try:
    hashed = pwd_context.hash(short_password)
    print(f"Short hash successful: {hashed[:30]}...")
except Exception as e:
    print(f"Short hash failed: {e}")