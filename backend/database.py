import sqlite3
import os
from datetime import datetime


# ============================================================
# DATABASE LOCATION
# ============================================================

DATABASE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "fakeradar.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # ========================================================
    # USERS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)

    # ========================================================
    # CLAIMS
    # ========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            verdict TEXT NOT NULL,
            confidence REAL NOT NULL,
            message TEXT,
            created_at TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # ========================================================
    # MIGRATE OLD CLAIMS TABLE
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(claims)"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    if "user_id" not in columns:

        print(
            "Updating claims table..."
        )

        cursor.execute("""
            ALTER TABLE claims
            ADD COLUMN user_id INTEGER
        """)

        print(
            "Added user_id column."
        )

    connection.commit()
    connection.close()

    print(
        "Database initialized successfully."
    )


# ============================================================
# ADD CLAIM
# ============================================================

def add_claim(
    text,
    verdict,
    confidence,
    message,
    user_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO claims (
            text,
            verdict,
            confidence,
            message,
            created_at,
            user_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        text,
        verdict,
        confidence,
        message,
        created_at,
        user_id
    ))

    claim_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return claim_id


# ============================================================
# GET CLAIMS
# ============================================================

def get_all_claims(user_id=None):

    connection = get_connection()
    cursor = connection.cursor()

    if user_id is not None:

        cursor.execute("""
            SELECT
                id,
                text,
                verdict,
                confidence,
                message,
                created_at,
                user_id
            FROM claims
            WHERE user_id = ?
            ORDER BY id DESC
        """, (
            user_id,
        ))

    else:

        cursor.execute("""
            SELECT
                id,
                text,
                verdict,
                confidence,
                message,
                created_at,
                user_id
            FROM claims
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# DELETE CLAIM
# ============================================================

def delete_claim(
    claim_id,
    user_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    if user_id is not None:

        cursor.execute("""
            DELETE FROM claims
            WHERE id = ?
            AND user_id = ?
        """, (
            claim_id,
            user_id
        ))

    else:

        cursor.execute("""
            DELETE FROM claims
            WHERE id = ?
        """, (
            claim_id,
        ))

    deleted = cursor.rowcount

    connection.commit()
    connection.close()

    return deleted > 0


# ============================================================
# CLAIM STATISTICS
# ============================================================

def get_claim_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM claims
    """)

    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM claims
        WHERE LOWER(verdict) = 'fake'
    """)

    fake = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM claims
        WHERE LOWER(verdict) = 'real'
    """)

    real = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM claims
        WHERE LOWER(verdict) = 'uncertain'
    """)

    uncertain = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT AVG(confidence) AS average_confidence
        FROM claims
    """)

    average_confidence = (
        cursor.fetchone()["average_confidence"]
    )

    if average_confidence is None:
        average_confidence = 0

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM users
    """)

    total_users = cursor.fetchone()["total"]

    connection.close()

    return {

        "total_claims": total,

        "fake_claims": fake,

        "real_claims": real,

        "uncertain_claims": uncertain,

        "average_confidence": round(
            float(average_confidence),
            2
        ),

        "total_users": total_users

    }


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    username,
    password,
    role="user"
):

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    try:

        cursor.execute("""
            INSERT INTO users (
                username,
                password,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            username,
            password,
            role,
            created_at
        ))

        user_id = cursor.lastrowid

        connection.commit()

        return user_id

    except sqlite3.IntegrityError:

        return None

    finally:

        connection.close()


# ============================================================
# GET USER BY USERNAME
# ============================================================

def get_user_by_username(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            password,
            role,
            created_at
        FROM users
        WHERE username = ?
    """, (
        username,
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return dict(user)

    return None


# ============================================================
# GET USER BY ID
# ============================================================

def get_user_by_id(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            password,
            role,
            created_at
        FROM users
        WHERE id = ?
    """, (
        user_id,
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return dict(user)

    return None


# ============================================================
# VERIFY USER
# ============================================================

def verify_user(
    username,
    password
):

    user = get_user_by_username(
        username
    )

    if user is None:
        return None

    if user["password"] != password:
        return None

    return user


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            username,
            role,
            created_at
        FROM users
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]