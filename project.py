import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="test_db",
        user="your_username",
        password="your_password"
    )

def create_user(name, email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.close()
    conn.close()
    print("User created.")

def read_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def update_user(user_id, new_email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
    conn.commit()
    cur.close()
    conn.close()
    print("User updated.")

def delete_user(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    print("User deleted.")

# Simple menu
while True:
    print("\n1. Create User\n2. Read Users\n3. Update User\n4. Delete User\n5. Exit")
    choice = input("Choose: ")
    if choice == "1":
        name = input("Name: ")
        email = input("Email: ")
        create_user(name, email)
    elif choice == "2":
        read_users()
    elif choice == "3":
        user_id = int(input("User ID: "))
        new_email = input("New Email: ")
        update_user(user_id, new_email)
    elif choice == "4":
        user_id = int(input("User ID: "))
        delete_user(user_id)
    elif choice == "5":
        break
