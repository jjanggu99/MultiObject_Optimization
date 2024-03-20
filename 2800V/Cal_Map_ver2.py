#02_Lamda_d, 03_Lamda_q, 04_Current_d, 05_Current_q.csv 파일 불러오기
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.ndimage import gaussian_filter


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

# 전압 조건에 따른 효율 데이터 필터링
# 전압이 2200V 이상인 데이터 포인트에 대해서만 효율을 계산
mask_voltage_above_2200 = df['Voltage(V)'] <= 2183*math.sqrt(2)
filtered_efficiency = df['Efficiency[%]'][mask_voltage_above_2200]
filtered_rpm = df['RPM'][mask_voltage_above_2200]
filtered_torque = df['Total_Torque[Nm]'][mask_voltage_above_2200]

# 고해상도 그리드 생성
grid_x, grid_y = np.mgrid[min(df['RPM']):max(df['RPM']):300j, min(df['Total_Torque[Nm]']):max(df['Total_Torque[Nm]']):300j]

# 보간된 효율 데이터
# 전압이 2200V 이상인 데이터 포인트만 사용하여 보간
# 보간된 효율 데이터
grid_z = griddata((filtered_rpm, filtered_torque), filtered_efficiency, (grid_x, grid_y), method='cubic', fill_value=np.nan)

# Apply Gaussian smoothing to the interpolated data
sigma = 2  # The standard deviation for the Gaussian kernel. Adjust this value based on your data.
grid_z_smoothed = gaussian_filter(grid_z, sigma=sigma)

# Now, use the smoothed data for plotting
plt.figure(figsize=(10, 8))

# 전압이 2200V 이상인 데이터에 대한 등고선 플롯 (채워진)
cmap = LinearSegmentedColormap.from_list("custom_gradient", ["blue", "green", "yellow", "red"], N=256)
contourf = plt.contourf(grid_x, grid_y, grid_z_smoothed, levels=np.linspace(90, 98, 256), cmap=cmap, extend='both')

# 등고선 레벨을 선으로 그리기 및 레이블 추가 (부드럽게 처리된 데이터 사용)
contours = plt.contour(grid_x, grid_y, grid_z_smoothed, levels=np.linspace(90, 98, 9), colors='black')
plt.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')

# 색상 바 추가
cbar = plt.colorbar(contourf, label='Efficiency [%]')
cbar.set_ticks(np.linspace(90, 98, 9))  # 색상 바의 주요 눈금 지정

# 레이블 및 제목 설정
plt.xlabel('RPM')
plt.ylabel('Torque [Nm]')
plt.title('Efficiency Map for the Motor in 2D (Voltage < 2,183V)')

# Save the figure to a file
plt.savefig('efficiency_map.png', dpi=600, bbox_inches='tight')

# 그래프 표시
plt.show()

df['Id'] = csv_Current_d['Current (Id)[A]']
df['Iq'] = csv_Current_q['Current (Iq)[A]']

# 이제 'Current'와 'Pout' 계산 가능
df['Current'] = np.sqrt(df['Id']**2 + df['Iq']**2)
df['Pout'] = df['Total_Torque[Nm]'] * df['RPM'] / 9.5488

# Calculate Pout, assuming df already contains 'RPM', 'Voltage(V)', and 'Total_Torque[Nm]'
df['Pout'] = df['Total_Torque[Nm]'] * df['RPM'] / 9.5488  # Convert RPM to rad/s for power in watts if Torque is in Nm

if df['Pout'].max() > 1000:
    df['Pout(kW)'] = df['Pout'] / 1000  # kW로 변환
    pout_label = 'Pout (kW)'
    pout_data = df['Pout(kW)']
else:
    pout_label = 'Pout (W)'
    pout_data = df['Pout']

fig, ax1 = plt.subplots(figsize=(10, 6))

# Voltage plot
color = 'tab:red'
ax1.set_xlabel('RPM')
ax1.set_ylabel('V', color=color)
ax1.plot(df['RPM'], df['Voltage(V)'], color=color, label='V')
ax1.tick_params(axis='y', labelcolor=color)

# Current plot
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('I', color=color)
ax2.plot(df['RPM'], df['Current'], color=color, label='I')
ax2.tick_params(axis='y', labelcolor=color)

# Torque plot
ax3 = ax1.twinx()
color = 'tab:green'
# Offset the third axis
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Torque', color=color)
ax3.plot(df['RPM'], df['Total_Torque[Nm]'], color=color, label='Torque')
ax3.tick_params(axis='y', labelcolor=color)

# Pout plot
ax4 = ax1.twinx()
color = 'tab:purple'
# Offset the fourth axis
ax4.spines['right'].set_position(('outward', 120))
ax4.set_ylabel(pout_label, color=color)
ax4.plot(df['RPM'], pout_data, color=color, label=pout_label)
ax4.tick_params(axis='y', labelcolor=color)

plt.title('Motor Characteristics')
fig.tight_layout()

# Show legend
handles, labels = [], []
for ax in fig.axes:
    for handle, label in zip(*ax.get_legend_handles_labels()):
        handles.append(handle)
        labels.append(label)
fig.legend(handles, labels, loc='upper right')

plt.show()

# Save the figure to a file
plt.savefig('motor_characteristics.png', dpi=300, bbox_inches='tight')