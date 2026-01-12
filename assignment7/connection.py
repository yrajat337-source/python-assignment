import psycopg2
from datetime import datetime

# Display timestamp
print("="*50)
print(f"Execution Time: {datetime.now()}")
print("="*50)

# Database connection parameters
db_config = {
    'host': 'localhost',
    'database': 'course_db',
    'user': 'postgres',
    'password': 'your_password_here'  # Replace with YOUR password
}

# Connect to PostgreSQL
try:
    print("\nAttempting to connect to PostgreSQL...")
    conn = psycopg2.connect(**db_config)
    
    print("✓ Connection successful!")
    print(f"✓ Database: {db_config['database']}")
    print(f"✓ User: {db_config['user']}")
    print(f"✓ Host: {db_config['host']}")
    
    # Get PostgreSQL version
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✓ PostgreSQL Version: {version[0][:50]}...")
    
    cursor.close()
    conn.close()
    print("\n✓ Connection closed successfully!")
    
except Exception as error:
    print(f"\n✗ Error connecting to PostgreSQL: {error}")

print("="*50)