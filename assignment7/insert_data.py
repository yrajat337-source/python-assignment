import psycopg2
from datetime import datetime

print("="*50)
print(f"Execution Time: {datetime.now()}")
print("="*50)

# Database connection
conn = psycopg2.connect(
    host='localhost',
    database='course_db',
    user='postgres',
    password='your_password_here'  # Replace with YOUR password
)

cursor = conn.cursor()

# Insert single record
print("\n1. Inserting single record...")
insert_query = """
    INSERT INTO students (name, email, age) 
    VALUES (%s, %s, %s)
    RETURNING id;
"""
data = ("John Doe", "john.doe@example.com", 22)
cursor.execute(insert_query, data)
student_id = cursor.fetchone()[0]
conn.commit()
print(f"✓ Record inserted with ID: {student_id}")

# Insert multiple records
print("\n2. Inserting multiple records...")
students_data = [
    ("Jane Smith", "jane.smith@example.com", 21),
    ("Bob Johnson", "bob.johnson@example.com", 23),
    ("Alice Brown", "alice.brown@example.com", 20)
]

for student in students_data:
    cursor.execute(insert_query, student)
    student_id = cursor.fetchone()[0]
    print(f"✓ Inserted: {student[0]} (ID: {student_id})")

conn.commit()
print(f"\n✓ Total rows inserted: {len(students_data) + 1}")

cursor.close()
conn.close()
print("✓ Database connection closed")
print("="*50)