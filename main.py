# average efficiency by warehouse per truck distance traveled in miles, 
#low number indicates less efficiency avg

import pandas as pd
import matplotlib.pyplot as plt

# reading in transportation data
file_path = '/Users/kimesha/Downloads/WeeklyShipmentData.csv'  
ship_data = pd.read_csv(file_path)

# warehouse column
ship_data['WarehouseNumber'] = ship_data['WarehouseNumber'].str.replace('Warehouse', '')

# replace zeros in 'TruckDistanceInMiles' with the median (if zero is not valid)
# this is to clean up any "dirty data"
truck_distance_median = ship_data['TruckDistanceInMiles'].median()
ship_data['TruckDistanceInMiles'].replace(0, truck_distance_median, inplace=True)

# fill missing values in 'TotalWeight' and 'TruckDistanceInMiles' with their median
# another cleaning up data step
ship_data['TotalWeight'].fillna(ship_data['TotalWeight'].median(), inplace=True)
ship_data['TruckDistanceInMiles'].fillna(truck_distance_median, inplace=True)

# make WarehouseNumber to numeric from string
ship_data['WarehouseNumber'] = pd.to_numeric(ship_data['WarehouseNumber'], errors='coerce')
ship_data.dropna(subset=['WarehouseNumber'], inplace=True)

# efficiency Analysis: Weight per Mile
ship_data['weight_per_mile'] = ship_data['TotalWeight'] / ship_data['TruckDistanceInMiles']

# ensure no infinite values
ship_data.replace([float('inf'), -float('inf')], truck_distance_median, inplace=True)

# calculating average weight/mile for each warehouse
average_weight_per_warehouse = ship_data.groupby('WarehouseNumber')['weight_per_mile'].mean()

# Plotting the results
plt.figure(figsize=(12, 8))
average_weight_per_warehouse.plot(kind='bar', color='skyblue')
plt.title('Average Efficiency (Weight per Mile) by Warehouse')
plt.xlabel('Warehouse Number')
plt.ylabel('Average Weight per Mile')
plt.xticks(rotation=45)  # so x-axis words and labels configure neatly 
plt.tight_layout()  
plt.show()

#create a second graph highlight the most ineffiecient/ calc avg weight/mile for each Warehouse

average_weight_per_warehouse = ship_data.groupby('WarehouseNumber')['weight_per_mile'].mean()

# top 5 least efficient warehouses
top_5_least_efficient = average_weight_per_warehouse.nsmallest(5)

# results for the top 5 least efficient warehouses
plt.figure(figsize=(10, 6))
top_5_least_efficient.plot(kind='bar', color='red')
plt.title('Top 5 Least Efficient Warehouses')
plt.xlabel('Warehouse Number')
plt.xticks(rotation=45)
plt.ylabel('Average Weight per Mile')
plt.show()

#correlation between shipment weight, distance, and efficiency
correlation_analysis = ship_data[['TotalWeight', 'TruckDistanceInMiles', 'weight_per_mile']].corr()

# printing correlation matrix
print("Correlation Matrix:")
print(correlation_analysis)

# solutions up for consideration based on analysis
print("\nPotential Solutions:")
if correlation_analysis.loc['TotalWeight', 'weight_per_mile'] < 0:
    print("- Consider increasing load sizes where feasible to improve transportation efficiency.")
if correlation_analysis.loc['TruckDistanceInMiles', 'weight_per_mile'] < 0:
    print("- Investigate long-distance shipments for potential route optimization or consolidation opportunities.")



