import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from deap import base, creator, tools, algorithms
import random

#먼저 변수 설정
geometry_variable_name = ['OPERATING_PHASE', 'DMAG1', 'DMAG2', 'DMAG3',	'MT1', 'MT2', 'MT3', 'MT4', 'MT5', 'MT6', 'MW1', 'MW2', 'MW3', 'MW4', 'OSW1', 'OSW2', 'OSW3','WMAG1', 'WMAG3', 'WMAG5']
geometry_variable_upper = np.array([80, 80, 32, 15, 14, 14, 14, 14, 14, 14, 45, 20, 30, 20, 35, 15, 15, 15, 15, 20])
geometry_variable_lower = np.array([65, 65, 15, 5, 5, 5, 5, 5, 5, 5, 20, 5, 10, 5, 2, 2, 2, 5, 5, 5])

SLOTS=36
POLE=6
RPM=4500                                    #TN커브상의 MAX RPM
HEIGHT=285                                  #적층길이
AIR_TC=0.02                                 #공기 열전도율 (W/m/deg)
MECHANICAL_LOSS=20                          #기계손 (W/K RPM)
CURRENT_SOURCE=353.5533906                  #최대 전류(PEAK값)
COILEND_H=110                               #코일 앤드부 높이
VOLTAGE_SOURCE=3086.448943904834            #전압제한 (PEAK값)

OPERATING_CURRENT=200                       #지정 운전점 전류
COIL_TC=400                                 #코일 열 전도율 (W/m/deg)
MAGNET_TEMP=180                             #부하 영구자석 온도 조건



#J-mag 실행


#Surrogate Model 선택
model_type = ['linear_regression', 'polynomial_regression', 'gaussian_process']
surrogate_model = model_type[1]
