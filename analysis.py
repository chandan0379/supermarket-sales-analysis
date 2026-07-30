from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Load .env file
load_dotenv()

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Read environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "supermarket_sales")

# Uncomment temporarily to check if password is loading
# print("Password:", DB_PASSWORD)

# Connect to MySQL
connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

print("✅ Connected to MySQL!")

# Read table from MySQL
query = "SELECT * FROM supermarket_sales"

df = pd.read_sql(query, connection)
df["sale_date"] = pd.to_datetime(df["sale_date"])
df["month"] = df["sale_date"].dt.strftime("%b")

print(df.head())

print("\n========== DATASET SUMMARY ==========\n")

print(f"Total Records : {len(df)}")
print(f"Total Columns : {len(df.columns)}")

print(f"\nTotal Sales : ₹{df['sales'].sum():,.2f}")
print(f"Average Sale : ₹{df['sales'].mean():.2f}")
print(f"Highest Sale : ₹{df['sales'].max():.2f}")
print(f"Lowest Sale : ₹{df['sales'].min():.2f}")

print(f"\nAverage Rating : {df['rating'].mean():.2f}")

# =====================================
# Sales by City
# =====================================

city_sales = df.groupby("city")["sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))

ax = city_sales.plot(kind="bar", color=["#4E79A7", "#F28E2B", "#59A14F"])

plt.title("Total Sales by City", fontsize=15, fontweight="bold")
plt.xlabel("City")
plt.ylabel("Total Sales")

for i, value in enumerate(city_sales):
    ax.text(i, value + 1000, f"{value:,.0f}", ha="center", fontsize=10)

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("charts/sales_by_city.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Sales by Branch
# =====================================

branch_sales = df.groupby("branch")["sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))

ax = branch_sales.plot(
    kind="bar",
    color=["#2E86AB", "#F6C85F", "#6F4E7C"]
)

plt.title("Total Sales by Branch", fontsize=15, fontweight="bold")
plt.xlabel("Branch")
plt.ylabel("Total Sales")

for i, value in enumerate(branch_sales):
    ax.text(i, value + 1000, f"{value:,.0f}", ha="center", fontsize=10)

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("charts/sales_by_branch.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Sales by Product Line
# =====================================

product_sales = (
    df.groupby("product_line")["sales"]
    .sum()
    .sort_values(ascending=True)
)

plt.figure(figsize=(10,6))

ax = product_sales.plot(
    kind="barh",
    color="teal"
)

plt.title("Total Sales by Product Line", fontsize=15, fontweight="bold")
plt.xlabel("Total Sales")
plt.ylabel("Product Line")

for i, value in enumerate(product_sales):
    ax.text(value + 500, i, f"{value:,.0f}", va="center")

plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("charts/product_line_sales.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Payment Method Distribution
# =====================================

payment_counts = df["payment"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    payment_counts,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Payment Method Distribution", fontsize=15, fontweight="bold")

plt.tight_layout()
plt.savefig("charts/payment_method_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Customer Type Distribution
# =====================================

customer_counts = df["customer_type"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    customer_counts,
    labels=customer_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=(0.05, 0)
)

plt.title("Customer Type Distribution", fontsize=15, fontweight="bold")

plt.tight_layout()
plt.savefig("charts/customer_type_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Gender Distribution
# =====================================

gender_counts = df["gender"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=(0.05, 0)
)

plt.title("Gender Distribution", fontsize=15, fontweight="bold")

plt.tight_layout()
plt.savefig("charts/gender_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Monthly Sales Trend
# =====================================

month_order = ["Jan", "Feb", "Mar"]

monthly_sales = (
    df.groupby("month")["sales"]
    .sum()
    .reindex(month_order)
)

plt.figure(figsize=(9,5))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    linewidth=3
)

plt.title("Monthly Sales Trend", fontsize=15, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales")

for x, y in zip(monthly_sales.index, monthly_sales.values):
    plt.text(x, y + 1000, f"{y:,.0f}", ha="center")

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Rating Distribution
# =====================================

plt.figure(figsize=(8,5))

plt.hist(
    df["rating"],
    bins=10,
    edgecolor="black"
)

plt.title("Customer Rating Distribution", fontsize=15, fontweight="bold")
plt.xlabel("Rating")
plt.ylabel("Frequency")

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("charts/rating_distribution.png", dpi=300, bbox_inches="tight")
plt.show()


# =====================================
# Correlation Heatmap
# =====================================

plt.figure(figsize=(10, 8))

numeric_df = df.select_dtypes(include=["number"])

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap", fontsize=16, fontweight="bold")

plt.tight_layout()
plt.savefig("charts/correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

# =====================================
# Top 5 Highest Sales
# =====================================

print("\n========== TOP 5 SALES ==========\n")

top_sales = df.nlargest(5, "sales")

print(
    top_sales[
        [
            "invoice_id",
            "city",
            "product_line",
            "sales",
            "payment",
            "rating",
        ]
    ]
)

# =====================================
# Average Rating by Product Line
# =====================================

rating = (
    df.groupby("product_line")["rating"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 5))

ax = rating.plot(
    kind="bar",
    color="orange"
)

plt.title("Average Rating by Product Line", fontsize=15, fontweight="bold")
plt.ylabel("Average Rating")

for i, value in enumerate(rating):
    ax.text(i, value + 0.03, f"{value:.2f}", ha="center")

plt.tight_layout()
plt.savefig("charts/average_rating_by_product_line.png", dpi=300, bbox_inches="tight")
plt.show()


connection.close()
print("✅ Connection Closed")