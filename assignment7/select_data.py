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

# Select all records
print("\n1. Fetching all students:")
print("-" * 70)
cursor.execute("SELECT * FROM students ORDER BY id")
records = cursor.fetchall()

print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Age':<5}")
print("-" * 70)
for record in records:
    print(f"{record[0]:<5} {record[1]:<20} {record[2]:<30} {record[3]:<5}")

print(f"\n✓ Total students: {len(records)}")

# Select with WHERE clause
print("\n2. Fetching students aged 21 or above:")
print("-" * 70)
cursor.execute("SELECT * FROM students WHERE age >= 21 ORDER BY age")
filtered = cursor.fetchall()

print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Age':<5}")
print("-" * 70)
for record in filtered:
    print(f"{record[0]:<5} {record[1]:<20} {record[2]:<30} {record[3]:<5}")

print(f"\n✓ Students aged 21+: {len(filtered)}")

cursor.close()
conn.close()
print("\n✓ Database connection closed")
print("="*50)