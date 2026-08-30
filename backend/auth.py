import hashlib

from database import (
    create_user,
    get_user_by_username
)


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Convert a password into a SHA-256 hash.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password, role="user"):
    """
    Register a new user.
    """

    username = username.strip()

    if not username:
        return {
            "success": False,
            "message": "Username is required."
        }

    if not password:
        return {
            "success": False,
            "message": "Password is required."
        }

    if len(username) < 3:
        return {
            "success": False,
            "message": "Username must contain at least 3 characters."
        }

    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must contain at least 6 characters."
        }

    # Only allow valid roles
    if role not in ["user", "admin"]:
        role = "user"

    # Check whether username already exists
    existing_user = get_user_by_username(username)

    if existing_user:
        return {
            "success": False,
            "message": "Username already exists."
        }

    # Hash password before saving
    hashed_password = hash_password(password)

    user_id = create_user(
        username=username,
        password=hashed_password,
        role=role
    )

    if user_id is None:
        return {
            "success": False,
            "message": "Could not create account."
        }

    return {
        "success": True,
        "message": "Account created successfully.",
        "user": {
            "id": user_id,
            "username": username,
            "role": role
        }
    }


# ============================================================
# LOGIN USER
# ============================================================

def login_user(username, password):
    """
    Authenticate a user.
    """

    username = username.strip()

    if not username or not password:
        return {
            "success": False,
            "message": "Username and password are required."
        }

    user = get_user_by_username(username)

    if not user:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    hashed_password = hash_password(password)

    if hashed_password != user["password"]:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    return {
        "success": True,
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }