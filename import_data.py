from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

try:
    # Database credentials
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "supermarket_sales")

    # Connect to MySQL
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        print("✅ Connected to MySQL successfully!")

    # Read CSV
    df = pd.read_csv("data/supermarket_sales.csv")

    # Rename columns
    df.columns = [
        "invoice_id",
        "branch",
        "city",
        "customer_type",
        "gender",
        "product_line",
        "unit_price",
        "quantity",
        "tax",
        "sales",
        "sale_date",
        "sale_time",
        "payment",
        "cogs",
        "gross_margin_percentage",
        "gross_income",
        "rating"
    ]

    # Convert Date and Time
    df["sale_date"] = pd.to_datetime(df["sale_date"]).dt.date
    df["sale_time"] = pd.to_datetime(
        df["sale_time"],
        format="%I:%M:%S %p"
    ).dt.time

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO supermarket_sales (
        invoice_id, branch, city, customer_type, gender,
        product_line, unit_price, quantity, tax, sales,
        sale_date, sale_time, payment, cogs,
        gross_margin_percentage, gross_income, rating
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s)
    """

    data = [tuple(row) for _, row in df.iterrows()]

    cursor.executemany(insert_query, data)
    connection.commit()

    print(f"✅ {cursor.rowcount} rows inserted successfully!")
    print(f"✅ Loaded {len(df)} records from CSV.")

except Error as e:
    print("❌ Error:", e)

finally:
    if "cursor" in locals():
        cursor.close()

    if "connection" in locals() and connection.is_connected():
        connection.close()
        print("✅ MySQL connection closed.")