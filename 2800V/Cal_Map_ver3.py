# Load the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

Pi_f = 1.010243563

dir_path = os.getcwd()

# Load CSV files
efficiency_map = pd.read_csv(dir_path + "\\" +'01_EfficiencyMap.csv')
lambda_d = pd.read_csv(dir_path + "\\" +'02_Lamda_d.csv')
lambda_q = pd.read_csv(dir_path + "\\" +'03_Lamda_q.csv')
current_d = pd.read_csv(dir_path + "\\" +'04_Current_d.csv')
current_q = pd.read_csv(dir_path + "\\" +'05_Current_q.csv')  # Assuming this is the correct file for Current q
PF = pd.read_csv(dir_path + "\\" +'06_PowerFactor.csv')
LoadAngle = pd.read_csv(dir_path + "\\" +'07_LoadAngle.csv')
Rorque_Ripple = pd.read_csv(dir_path + "\\" +'08_TorqueRipple.csv')
voltage = pd.read_csv(dir_path + "\\" +'09_Voltage.csv')

all_data_series = pd.concat([efficiency_map, lambda_d, lambda_q, current_d, current_q, PF, LoadAngle, Rorque_Ripple, voltage])

print(all_data_series)
all_data_series.to_csv('all_data_combined.csv', index=False, header=False)



# Calculate 'Current' and 'Pout'
A = pd.Series(np.sqrt(current_d['Current (Id)[A]']**2 + current_q['Current (Iq)[A]']**2))
lambda_d['Pout(W)'] = lambda_d['Torque[Nm]'] * lambda_d['Speed[r/min]'] / 9.5488

# Assuming Torque is from lambda_d for plotting and all DataFrames are aligned by index
# This will need to be adjusted based on actual data relationships and desired calculations

# Plotting setup - as an example, focusing on plotting Voltage first
plt.figure(figsize=(12, 8))
plt.plot(voltage['Speed[r/min]'], voltage['Voltage (Amplitude)[V]'], label='Voltage')

# Additional plots for Current, Torque, and Pout will be added here

plt.xlabel('RPM')
plt.ylabel('Values')
plt.legend()
plt.title('Motor Characteristics')
plt.show()