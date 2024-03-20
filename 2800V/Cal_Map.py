#02_Lamda_d, 03_Lamda_q, 04_Current_d, 05_Current_q.csv 파일 불러오기
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap, Normalize


Effi_filename = "01_EfficiencyMap"
Lambda_d_filename = "02_Lamda_d"
Lambda_q_filename = "03_Lamda_q"
Current_d_filename = "04_Current_d"
Current_q_filename = "05_Current_q"
Volatage_filename = "09_Voltage"

dir_path = os.getcwd()

Effi_csvname = dir_path + "\\" + Effi_filename +".csv"
Lambda_d_csvname = dir_path + "\\" + Lambda_d_filename +".csv"
Lambda_q_csvname = dir_path + "\\" + Lambda_q_filename +".csv"
Current_d_csvname = dir_path + "\\" + Current_d_filename +".csv"
Current_q_csvname = dir_path + "\\" + Current_q_filename +".csv"
Voltage_csvname = dir_path + "\\" + Volatage_filename +".csv"

csv_Effi = pd.read_csv(Effi_csvname)
csv_Lambda_d = pd.read_csv(Lambda_d_csvname)
csv_Lambda_q = pd.read_csv(Lambda_q_csvname)
csv_Current_d = pd.read_csv(Current_d_csvname)
csv_Current_q = pd.read_csv(Current_q_csvname)
csv_Voltage = pd.read_csv(Voltage_csvname)

#print(csv_Current_d)
#Ld, Lq, Id, Iq만 불러오기

RPM =[]
Lambda_d = []
Lambda_q = []
Id = []
Iq = []
Ld = []
Lq = []
Torque_Mag = []
Torque_Rel = []
Total_Torque =[]
Effi =[]
Voltage =[]
Pole = 6

#Pi_f 자동 추출 추가해야함!!!!!!!!!!!!!!!!!!!!!!!!!!!
Pi_f = 1.010243563

#print(csv_Lambda_d[csv_Lambda_d.columns[2][1]])

#flux_column_index = csv_Lambda_d.columns.get_loc('Flux (d-Axis)[Vs]')
#values_below_flux = csv_Lambda_d.iloc[:, csv_Lambda_d.columns.get_loc('Flux (d-Axis)[Vs]')]

for i in range (len(csv_Lambda_d)-1):
    Effi.append(csv_Effi.iloc[:, csv_Effi.columns.get_loc('Efficiency[%]')][i])
    RPM.append(csv_Lambda_d.iloc[:, csv_Lambda_d.columns.get_loc('Speed[r/min]')][i])
    Lambda_d.append(csv_Lambda_d.iloc[:, csv_Lambda_d.columns.get_loc('Flux (d-Axis)[Vs]')][i])
    Lambda_q.append(csv_Lambda_q.iloc[:, csv_Lambda_q.columns.get_loc('Flux (q-Axis)[Vs]')][i])
    Id.append(csv_Current_d.iloc[:, csv_Current_d.columns.get_loc('Current (Id)[A]')][i])
    Iq.append(csv_Current_q.iloc[:, csv_Current_q.columns.get_loc('Current (Iq)[A]')][i])
    Voltage.append(csv_Voltage.iloc[:, csv_Voltage.columns.get_loc('Voltage (Amplitude)[V]')][i])

    #Ld, Lq 변환
    if Id[i] == 0:
        Ld.append(0)
        Lq.append(0)
        Torque_Mag.append(0)
        Torque_Rel.append(0)
        Total_Torque.append(Torque_Mag[i]+Torque_Rel[i])

    else:
        Ld.append((Lambda_d[i]-Pi_f) / Id[i])
        Lq.append(Lambda_q[i] / Iq[i])
        Torque_Mag.append((3/2)*(Pole/2)*Pi_f*Iq[i])
        Torque_Rel.append((3/2)*(Pole/2)*(Ld[i]-Lq[i])*Id[i]*Iq[i])
        Total_Torque.append(Torque_Mag[i]+Torque_Rel[i])

data = list(zip(RPM, Ld, Lq, Torque_Mag, Torque_Rel, Total_Torque, Effi, Voltage))

df = pd.DataFrame(data, columns=['RPM', 'Ld', 'Lq', 'Torque_Mag[Nm]', 'Torque_Rel[Nm]', 'Total_Torque[Nm]', 'Efficiency[%]', 'Voltage(V)'])

# Display the DataFrame (optional)
print(df)

# Save the DataFrame to a CSV file
csv_file_path = 'output_data.csv'
df.to_csv(csv_file_path, index=False)

print(f'Data has been written to {csv_file_path}')

csv_file_path = 'output_data.csv'
df = pd.read_csv(csv_file_path)

# Generate a custom color map
cmap = LinearSegmentedColormap.from_list(
    "custom_gradient",
    ["blue", "green", "yellow", "red"],
    N=256  # Number of color segments
)

# Convert data points to a higher resolution regular grid for smoother transitions
grid_x, grid_y = np.mgrid[min(df['RPM']):max(df['RPM']):200j, min(df['Total_Torque[Nm]']):max(df['Total_Torque[Nm]']):5000j]

# Interpolate efficiency data from irregular data points to a regular grid
grid_z = griddata((df['RPM'], df['Total_Torque[Nm]']), df['Efficiency[%]'], (grid_x, grid_y), method='cubic')

plt.figure(figsize=(10, 8))

# Plot a blue base for values below 85%
plt.contourf(grid_x, grid_y, grid_z, levels=[np.min(grid_z), 85], colors='blue')

# Overlay the contour plot for values above 85%
contourf = plt.contourf(grid_x, grid_y, grid_z, levels=np.linspace(85, 100, 256), cmap=cmap, extend='both')

# Add color bar, representing values from 85% to 100%
cbar = plt.colorbar(contourf, label='Efficiency [%]')
cbar.set_ticks(np.linspace(85, 100, 4))  # Major ticks for the color bar

# Set labels and title
plt.xlabel('RPM')
plt.ylabel('Torque [Nm]')
plt.title('Efficiency Map for the Motor in 2D (85% and Above)')

# Display the plot
plt.show()