import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading transportation data
file_path = '/Users/kimesha/Downloads/WeeklyShipmentData.csv'  
ship_data = pd.read_csv(file_path)

# Assuming 'CustomerID' or 'CustomerName' as the customer identifier
# Replace 'CustomerID' with the actual column name representing the customer
customer_column = 'CustomerNumber'  

# Grouping by customer and calculating total distance and number of shipments
customer_analysis = ship_data.groupby(customer_column).agg({
    'TruckDistanceInMiles': 'sum',
    'WarehouseNumber': 'count'  # Assuming this column represents the number of shipments
}).rename(columns={'WarehouseNumber': 'NumberOfShipments'}).sort_values('TruckDistanceInMiles', ascending=False)

# Displaying top customers (adjust the number as needed)
top_customers = customer_analysis.head(10)
print("Top Customers Table:")
print(top_customers)

# Plotting the data - Bar chart for top customers
plt.figure(figsize=(12, 6))
sns.barplot(x=top_customers.index, y='TruckDistanceInMiles', data=top_customers)
plt.title('Truck Distance Traveled for Top Customers')
plt.xlabel('Customer')
plt.ylabel('Total Truck Distance in Miles')
plt.xticks(rotation=45)
plt.show()

# Optional: Additional plot for number of shipments
plt.figure(figsize=(12, 6))
sns.barplot(x=top_customers.index, y='NumberOfShipments', data=top_customers, palette='Set2')
plt.title('Number of Shipments for Top Customers')
plt.xlabel('Customer')
plt.ylabel('Number of Shipments')
plt.xticks(rotation=45)
plt.show()
