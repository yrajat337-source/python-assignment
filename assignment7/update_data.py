import psycopg2
from datetime import datetime

print("="*50)
print(f"Execution Time: {datetime.now()}")
print("="*50)

conn = psycopg2.connect(
    host='localhost',
    database='course_db',
    user='postgres',
    password='your_password_here'
)

cursor = conn.cursor()

# Show data before update
print("\nBefore Update:")
print("-" * 50)
cursor.execute("SELECT * FROM students WHERE name = 'John Doe'")
record = cursor.fetchone()
if record:
    print(f"ID: {record[0]}, Name: {record[1]}, Email: {record[2]}, Age: {record[3]}")

# Update record
print("\nUpdating record...")
update_query = "UPDATE students SET age = %s, email = %s WHERE name = %s"
cursor.execute(update_query, (25, "john.updated@example.com", "John Doe"))
conn.commit()
print(f"✓ Rows updated: {cursor.rowcount}")

# Show data after update
print("\nAfter Update:")
print("-" * 50)
cursor.execute("SELECT * FROM students WHERE name = 'John Doe'")
record = cursor.fetchone()
if record:
    print(f"ID: {record[0]}, Name: {record[1]}, Email: {record[2]}, Age: {record[3]}")

cursor.close()
conn.close()
print("\n✓ Database connection closed")
print("="*50)