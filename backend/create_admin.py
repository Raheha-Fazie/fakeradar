from database import initialize_database, create_user

initialize_database()

username = "admin"
password = "admin123"

user_id = create_user(
    username=username,
    password=password,
    role="admin"
)

if user_id:
    print("Admin created successfully.")
    print("Username:", username)
    print("Password:", password)
else:
    print("Admin already exists.")