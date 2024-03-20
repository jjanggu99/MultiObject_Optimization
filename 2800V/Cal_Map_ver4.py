import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from scipy.interpolate import UnivariateSpline
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from scipy.signal import savgol_filter

# 데이터를 부드럽게 하는 함수
def smooth_data(y, window_length, polyorder):
    # window_length는 홀수이고 polyorder는 window_length보다 작아야 함
    if window_length % 2 == 0:  # window_length가 짝수이면 홀수로 만들기
        window_length += 1
    return savgol_filter(y, window_length, polyorder)

# Input
Pi_f = 1.010243563
########################################################################################

# 파일 경로 설정 (예시 경로)
dir_path = os.getcwd()

# 각 파일을 읽어오기
efficiency_map = pd.read_csv(f"{dir_path}/01_EfficiencyMap.csv")
lambda_d = pd.read_csv(f"{dir_path}/02_Lamda_d.csv")
lambda_q = pd.read_csv(f"{dir_path}/03_Lamda_q.csv")
current_d = pd.read_csv(f"{dir_path}/04_Current_d.csv")
current_q = pd.read_csv(f"{dir_path}/05_Current_q.csv")
PF = pd.read_csv(f"{dir_path}/06_PowerFactor.csv")
LoadAngle = pd.read_csv(f"{dir_path}/07_LoadAngle.csv")
Torque_Ripple = pd.read_csv(f"{dir_path}/08_TorqueRipple.csv")
voltage = pd.read_csv(f"{dir_path}/09_Voltage.csv")

# 기초 DataFrame 생성
TotalData = efficiency_map[['Speed[r/min]', 'Torque[Nm]']].copy()

# 각 데이터의 세 번째 열 추가
TotalData['Efficiency[%]'] = efficiency_map.iloc[:, 2]
TotalData['Lambda_d'] = lambda_d.iloc[:, 2]
TotalData['Lambda_q'] = lambda_q.iloc[:, 2]
TotalData['Current_d[A]'] = current_d.iloc[:, 2]
TotalData['Current_q[A]'] = current_q.iloc[:, 2]
TotalData['Current_amplitude[A]'] = np.sqrt(TotalData['Current_d[A]']**2 + TotalData['Current_q[A]']**2)
TotalData['PowerFactor'] = PF.iloc[:, 2]
TotalData['LoadAngle[deg]'] = LoadAngle.iloc[:, 2]
TotalData['TorqueRipple'] = Torque_Ripple.iloc[:, 2]
TotalData['Voltage[V]'] = voltage.iloc[:, 2]
TotalData['Pout[W]'] = TotalData['Torque[Nm]']*TotalData['Speed[r/min]']/60*2*np.pi

print(TotalData.head())  # 결과의 상위 5행을 출력하여 확인

# 합쳐진 데이터를 CSV 파일로 저장
TotalData.to_csv(f"{dir_path}/TotalData_combined.csv", index=False)

# 저장 완료 메시지 출력
print(f"TotalData_combined.csv has been successfully saved to: {dir_path}")


#효율맵 그림 코드
# Your existing setup, including the creation of filtered_data and custom_cmap
TotalData['Adjusted Efficiency'] = np.clip(TotalData['Efficiency[%]'], 85, 100)
filtered_data = TotalData[(TotalData['Speed[r/min]'] >= 0) & (TotalData['Torque[Nm]'] >= 0)]
colors = ['blue', 'green', 'red'] 
cmap_name = 'efficiency_custom'
custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

# Step 1: Prepare your data
x = filtered_data['Speed[r/min]']
y = filtered_data['Torque[Nm]']
z = filtered_data['Adjusted Efficiency']

# Step 2: Interpolate the data
# Create a grid over which to interpolate
xi = np.linspace(x.min(), x.max(), 100)  # Adjust granularity to your needs
yi = np.linspace(y.min(), y.max(), 100)  # Adjust granularity to your needs
xi, yi = np.meshgrid(xi, yi)

# Interpolate z values on the grid
zi = griddata((x, y), z, (xi, yi), method='cubic')

# Step 3: Plot the scatter plot (your existing code)
plt.figure(figsize=(10, 8))
scatter = plt.scatter(x, y, c=z, cmap=custom_cmap, alpha=0.9, vmin=85, vmax=97)
plt.colorbar(scatter, label='Efficiency [%]')
plt.xlabel('Speed [RPM]')
plt.ylabel('Torque [Nm]')
plt.title('Motor Efficiency Map')
plt.grid(True)

# Step 4: Add smooth contour lines over the scatter plot
zi_smoothed = gaussian_filter(zi, sigma=2.5)  # Adjust sigma as needed
contours = plt.contour(xi, yi, zi_smoothed, levels=np.linspace(90, 97, 8), colors='k')
plt.clabel(contours, inline=True, fontsize=8, fmt='%1.0f%%')
plt.savefig(f"{dir_path}/Motor_Efficiency_Map.png")

plt.show()

# Group by RPM and aggregate to find the maximum value for each characteristic
agg_data = TotalData.groupby('Speed[r/min]').agg({
    'Torque[Nm]': 'max',
    'Current_amplitude[A]': 'max',
    'Voltage[V]': 'max',
    'Pout[W]': 'max'
}).reset_index()

# Prepare your data from the aggregated DataFrame
rpm = agg_data['Speed[r/min]']
torque = agg_data['Torque[Nm]']
current_amplitude = agg_data['Current_amplitude[A]']
voltage = agg_data['Voltage[V]']
pout = agg_data['Pout[W]']

# Create a figure and a set of subplots
# Assuming 'agg_data' contains the aggregated and sorted data.
# The following code creates the plot with the same structure as the uploaded image.

# Setting up the plot with three y-axes
window_length = 51  # 변경 가능
polyorder = 2  # 변경 가능

# 스무딩 적용
torque_smoothed = smooth_data(torque, window_length, polyorder)
current_amplitude_smoothed = smooth_data(current_amplitude, window_length, polyorder)
voltage_smoothed = smooth_data(voltage, window_length, polyorder)
pout_smoothed = smooth_data(pout, window_length, polyorder)

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(12, 9))

# 토크 곡선
color = 'tab:green'
ax1.set_xlabel('Speed [RPM]')
ax1.set_ylabel('Torque [Nm]', color=color)
ax1.plot(rpm, torque_smoothed, color=color, label='Torque')
ax1.tick_params(axis='y', labelcolor=color)

# 전류 곡선 (오른쪽 y축)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Current [A]', color=color)
ax2.plot(rpm, current_amplitude_smoothed, color=color, label='Current', linestyle='dashed')
ax2.tick_params(axis='y', labelcolor=color)

# 전압 곡선 (오른쪽 y축 두 번째)
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))
color = 'tab:red'
ax3.set_ylabel('Voltage [V]', color=color)
ax3.plot(rpm, voltage_smoothed, color=color, label='Voltage')
ax3.tick_params(axis='y', labelcolor=color)

# 출력 곡선 (왼쪽 y축 두 번째)
ax4 = ax1.twinx()
ax4.spines["left"].set_position(('outward', 80))  # 'outward' 모드와 픽셀 값으로 왼쪽으로 이동
ax4.yaxis.set_label_position('left')  # 레이블 위치를 왼쪽으로 설정
ax4.yaxis.tick_left()  # 눈금을 왼쪽으로 설정

# 나머지 코드는 동일하게 유지
color = 'tab:purple'
ax4.set_ylabel('Pout [W]', color=color)
ax4.plot(rpm, pout_smoothed, color=color, label='Pout')
ax4.tick_params(axis='y', labelcolor=color)


# 레이아웃 조정 및 범례 설정
fig.tight_layout()  # 레이아웃 조정
plt.title('Motor Characteristic Curves with Smoothing')

# 범례
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles3, labels3 = ax3.get_legend_handles_labels()
handles4, labels4 = ax4.get_legend_handles_labels()
ax1.legend(handles1 + handles2 + handles3 + handles4, labels1 + labels2 + labels3 + labels4, loc='upper left')

# 그래프 보이기
plt.tight_layout()
# 그래프 저장하기
plt.savefig(f"{dir_path}/Motor_Characteristic_Curves_Smoothed.png")
plt.show()

