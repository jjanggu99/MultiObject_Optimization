import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from deap import base, creator, tools, algorithms
import random

#먼저 변수 설정
#Jmag 실행 및 결과값 확인
#Surrogate Model 선택
model_type = ['linear_regression', 'polynomial_regression', 'gaussian_process']
surrogate_model = model_type[1]
