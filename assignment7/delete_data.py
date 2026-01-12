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

# Show all records before deletion
print("\nBefore Deletion:")
print("-" * 70)
cursor.execute("SELECT * FROM students")
records = cursor.fetchall()
print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Age':<5}")
print("-" * 70)
for record in records:
    print(f"{record[0]:<5} {record[1]:<20} {record[2]:<30} {record[3]:<5}")
print(f"Total records: {len(records)}")

# Delete specific record
print("\nDeleting student 'Bob Johnson'...")
delete_query = "DELETE FROM students WHERE name = %s"
cursor.execute(delete_query, ("Bob Johnson",))
conn.commit()
print(f"✓ Rows deleted: {cursor.rowcount}")

# Show all records after deletion
print("\nAfter Deletion:")
print("-" * 70)
cursor.execute("SELECT * FROM students")
records = cursor.fetchall()
print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Age':<5}")
print("-" * 70)
for record in records:
    print(f"{record[0]:<5} {record[1]:<20} {record[2]:<30} {record[3]:<5}")
print(f"Total records: {len(records)}")

cursor.close()
conn.close()
print("\n✓ Database connection closed")
print("="*50)