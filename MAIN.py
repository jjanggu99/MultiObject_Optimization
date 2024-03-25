import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from deap import base, creator, tools, algorithms
from scipy.stats.qmc import LatinHypercube
from scipy.stats import qmc
import random
import generate_lhs_samples

#먼저 변수 설정
class SimulationInput:
    def __init__(self):
        self.opt_variable_name = ['OPERATING_PHASE', 'DMAG1', 'DMAG2', 'DMAG3', 'MT1', 'MT2', 'MT3', 'MT4', 'MT5', 'MT6', 'MW1', 'MW2', 'MW3', 'MW4', 'OSW1', 'OSW2', 'OSW3', 'WMAG1', 'WMAG3', 'WMAG5']
        self.opt_variable_upper = np.array([80, 80, 32, 15, 14, 14, 14, 14, 14, 14, 45, 20, 30, 20, 35, 15, 15, 15, 15, 20])
        self.opt_variable_lower = np.array([65, 65, 15, 5, 5, 5, 5, 5, 5, 5, 20, 5, 10, 5, 2, 2, 2, 5, 5, 5])

        # Efficiency Map Variable
        self.SLOTS = 36
        self.POLE = 6
        self.RPM = 4500
        self.HEIGHT = 285
        self.MECHANICAL_LOSS = 20
        self.CURRENT_SOURCE = 353.5533906
        self.COILEND_H = 110
        self.VOLTAGE_SOURCE = 3086.448943904834

        # Heat Analysis Variable
        self.AIR_HTC = 10
        self.AIR_TC = 0.02
        self.COIL_TC = 400
        self.COIL_DENS = 8.96
        self.COIL_SH = 380
        self.SHAFT_TC = 25
        self.SHAFT_DENS = 7.8
        self.SHAFT_SH = 450
        self.HOUSING_H = 420
        self.HOUSING_T = 20
        self.HOUSING_TC = 25
        self.HOUSING_DENS = 7.8
        self.HOUSING_SH = 450

        self.AMBIENT = 70

        # Load Analysis Settings
        self.OPERATING_CURRENT = 200
        self.MAGNET_TEMP = 180
        # OPERATING_PHASE는 다변수 최적화에 사용되므로 여기에 포함되지 않습니다.
        self.OPERATING_RPM = 4387
        self.OPERATING_TRQ = 923

sim_input = SimulationInput()

samples = generate_lhs_samples(sim_input.opt_variable_name, sim_input.opt_variable_upper, sim_input.opt_variable_lower, n_samples=100)

# 생성된 샘플 확인
print("Shape of the generated samples:", samples.shape)

#J-mag 실행


#Surrogate Model 선택
#model_type = ['linear_regression', 'polynomial_regression', 'gaussian_process']
#surrogate_model = model_type[1]
