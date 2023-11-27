import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table

# Loading transportation data
file_path = '/Users/kimesha/Downloads/WeeklyShipmentData.csv'  # Update with the actual file path
transport_data = pd.read_csv(file_path)

# Convert WarehouseZIP to string and add leading zeros where necessary
transport_data['WarehouseZIP'] = transport_data['WarehouseZIP'].apply(lambda x: str(x).zfill(5))

# Assuming 'CustomerNumber' as the customer identifier
customer_column = 'CustomerNumber'  # Change this to your customer identifier column name

# Grouping by customer and ZIP code, calculating total distance and number of shipments
customer_zip_analysis = transport_data.groupby([customer_column, 'WarehouseZIP']).agg({
    'TruckDistanceInMiles': 'sum',
    'WarehouseNumber': 'count'  # Assuming this column represents the number of shipments
}).rename(columns={'WarehouseNumber': 'NumberOfShipments'}).reset_index()

# Identifying top 7 customers based on total truck distance
top_customers = customer_zip_analysis.groupby(customer_column)['TruckDistanceInMiles'].sum().nlargest(7).index

# Filter the analysis to only include these top 7 customers
filtered_data = customer_zip_analysis[customer_zip_analysis[customer_column].isin(top_customers)]

# Bar chart for Truck Distance Traveled for top 7 customers
plt.figure(figsize=(14, 7))
sns.barplot(x='CustomerNumber', y='TruckDistanceInMiles', hue='WarehouseZIP', data=filtered_data)
plt.title('Truck Distance Traveled for Top 7 Customers by ZIP Code')
plt.xlabel('Customer')
plt.ylabel('Total Truck Distance in Miles')
plt.yticks(range(0, int(filtered_data['TruckDistanceInMiles'].max()) + 10000, 10000))  # Setting y-axis ticks
plt.xticks(rotation=45)
plt.legend(title='Warehouse ZIP', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Bar chart for Number of Shipments for top 7 customers
plt.figure(figsize=(14, 7))
sns.barplot(x='CustomerNumber', y='NumberOfShipments', hue='WarehouseZIP', data=filtered_data, palette='Set2')
plt.title('Number of Shipments for Top 7 Customers by ZIP Code')
plt.xlabel('Customer')
plt.ylabel('Number of Shipments')
plt.xticks(rotation=45)
plt.show()

# Pie chart for Number of Shipments for the top customer among the top 7
top_customer = filtered_data['CustomerNumber'].value_counts().idxmax()
top_customer_data = filtered_data[filtered_data['CustomerNumber'] == top_customer]

plt.figure(figsize=(8, 8))
plt.pie(top_customer_data['NumberOfShipments'], labels=top_customer_data['WarehouseZIP'], autopct='%1.1f%%', startangle=140)
plt.title(f'Number of Shipments for Top Customer {top_customer} by ZIP Code')
plt.show()

# Graphic table for top 7 customers
fig, ax = plt.subplots(figsize=(12, 2)) 
ax.xaxis.set_visible(False) 
ax.yaxis.set_visible(False) 
ax.set_frame_on(False)  
tab = table(ax, filtered_data.round(2), loc='upper right', colWidths=[0.2]*len(filtered_data.columns))  
plt.title('Data Table for Top 7 Customers')
plt.show()
