import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading transportation data
file_path = '/Users/kimesha/Downloads/WeeklyShipmentData.csv'  # Update with the actual file path
ship_data = pd.read_csv(file_path)

# Replace 'Warehouse' with '' in the 'WarehouseNumber' column and handle missing data
ship_data['WarehouseNumber'] = ship_data['WarehouseNumber'].str.replace('Warehouse', '')
ship_data['TotalWeight'].fillna(ship_data['TotalWeight'].median(), inplace=True)
ship_data['TruckDistanceInMiles'].fillna(ship_data['TruckDistanceInMiles'].median(), inplace=True)
ship_data['TruckDistanceInMiles'].replace(0, ship_data['TruckDistanceInMiles'].median(), inplace=True)

# Efficiency Analysis: Weight per Mile
ship_data['weight_per_mile'] = ship_data['TotalWeight'] / ship_data['TruckDistanceInMiles']

# Scatter plot for TruckDistanceInMiles vs. TotalWeight, colored by weight_per_mile
plt.figure(figsize=(12, 8))
sns.scatterplot(data=ship_data, x='TruckDistanceInMiles', y='TotalWeight', hue='weight_per_mile', palette='coolwarm', size='weight_per_mile', sizes=(20, 200))
plt.title('Shipment Distance vs. Weight with Efficiency')
plt.xlabel('Truck Distance in Miles')
plt.ylabel('Total Weight (lbs)')
plt.colorbar(label='Weight per Mile (Efficiency)')
plt.show()
