import pandas as pd

print("Loading dataset...")

# Load dataset
df = pd.read_csv("Nassau_Candy_Distributor.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Create Shipping Lead Time
df['Shipping Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Normalize multi-year differences
df['Shipping Lead Time'] = df['Shipping Lead Time'] % 365
# Drop missing geographic values
df = df.dropna(subset=['State/Province', 'Region'])

print("Cleaning Done")

# -----------------------------
# ROUTE ANALYSIS
# -----------------------------

route_summary = df.groupby(['Region', 'State/Province']).agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Total_Shipments=('Order ID', 'count'),
    Total_Sales=('Sales', 'sum')
).reset_index()

route_summary = route_summary.sort_values('Total_Shipments', ascending=False)

print("\nTop 10 Routes by Shipment Volume:")
print(route_summary.head(10))
# -----------------------------
# BOTTLENECK DETECTION
# -----------------------------

avg_lead_time = route_summary['Avg_Lead_Time'].mean()
avg_volume = route_summary['Total_Shipments'].mean()

bottlenecks = route_summary[
    (route_summary['Avg_Lead_Time'] > avg_lead_time) &
    (route_summary['Total_Shipments'] > avg_volume)
]

print("\nPotential Bottleneck Routes:")
print(bottlenecks.sort_values('Total_Shipments', ascending=False))
# -----------------------------
# ROUTE EFFICIENCY SCORE
# -----------------------------

max_time = route_summary['Avg_Lead_Time'].max()
min_time = route_summary['Avg_Lead_Time'].min()

route_summary['Efficiency_Score'] = 1 - (
    (route_summary['Avg_Lead_Time'] - min_time) / (max_time - min_time)
)

route_summary = route_summary.sort_values('Efficiency_Score', ascending=False)

print("\nTop 10 Most Efficient Routes:")
print(route_summary.head(10))

print("\nBottom 10 Least Efficient Routes:")
print(route_summary.tail(10))
# Route Summary
route_summary = df.groupby(['Region', 'State/Province']).agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Total_Shipments=('Order ID', 'count'),
    Total_Sales=('Sales', 'sum')
).reset_index()

route_summary = route_summary.sort_values('Total_Shipments', ascending=False)

print("\nTop 10 Routes by Shipment Volume:")
print(route_summary.head(10))

# Save Cleaned Data
df.to_csv("cleaned_data.csv", index=False)

print("Cleaned data saved as cleaned_data.csv")

print("Overall Average Lead Time:", df['Shipping Lead Time'].mean())
# -----------------------------
# SHIP MODE ANALYSIS
# -----------------------------

ship_mode_summary = df.groupby('Ship Mode').agg(
    Avg_Lead_Time=('Shipping Lead Time', 'mean'),
    Total_Shipments=('Order ID', 'count'),
    Total_Sales=('Sales', 'sum')
).reset_index()

print("\nShip Mode Performance:")
print(ship_mode_summary)
