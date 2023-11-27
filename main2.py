import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# reading in shipment/transport data
file_path = '/Users/kimesha/Downloads/WeeklyShipmentData.csv'  
ship_data = pd.read_csv(file_path)

# convert WarehouseZIP to string and add leading zeros
ship_data['WarehouseZIP'] = ship_data['WarehouseZIP'].apply(lambda x: str(x).zfill(5))

# replace missing values and handle data
ship_data['TotalWeight'].fillna(ship_data['TotalWeight'].median(), inplace=True)
ship_data['TruckDistanceInMiles'].fillna(ship_data['TruckDistanceInMiles'].median(), inplace=True)
ship_data['TruckDistanceInMiles'].replace(0, ship_data['TruckDistanceInMiles'].median(), inplace=True)

# analysis: weight/mile
ship_data['weight_per_mile'] = ship_data['TotalWeight'] / ship_data['TruckDistanceInMiles']

# calculating averages for shipments
average_shipments = ship_data['WarehouseNumber'].count() / ship_data['WarehouseZIP'].nunique()
average_distance = ship_data['TruckDistanceInMiles'].mean()

# grouped by WarehouseZIP as string 
grouped_by_zip = ship_data.groupby('WarehouseZIP').agg({
    'weight_per_mile': 'mean',
    'TotalWeight': 'sum',
    'TruckDistanceInMiles': 'sum',
    'WarehouseNumber': 'count'
}).rename(columns={'WarehouseNumber': 'NumberOfShipments'})

# plotting efficiency by WarehouseZIP
plt.figure(figsize=(15, 8))
grouped_by_zip['weight_per_mile'].plot(kind='bar', color='teal')
plt.title('Efficiency by Warehouse ZIP Code')
plt.xlabel('Warehouse ZIP Code')
plt.xticks(rotation=45)
plt.ylabel('Average Weight per Mile')
plt.show()

# Displaying overall averages
print(f"Average Number of Shipments: {average_shipments}")
print(f"Average Distance Traveled: {average_distance} miles")
