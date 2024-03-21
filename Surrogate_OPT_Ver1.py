import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import DotProduct, WhiteKernel
from deap import base, creator, tools, algorithms
import random


# 예제 데이터셋 (이 부분을 여러분의 데이터로 교체하세요)
X = np.random.rand(100, 1) * 10  # 입력 변수
y = np.sin(X).ravel() + np.random.randn(100) * 0.1  # 출력 (예: 토크)

# 서로게이트 모델 선택 함수
def build_surrogate_model(model_type, X_train, y_train):
    if model_type == 'linear_regression':
        model = LinearRegression()
    elif model_type == 'polynomial_regression':
        degree = 4  # 다항식 차수는 상황에 맞게 조정
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    elif model_type == 'gaussian_process':
        kernel = DotProduct() + WhiteKernel()
        model = GaussianProcessRegressor(kernel=kernel)
    else:
        raise ValueError("Unknown model type provided.")
    
    model.fit(X_train, y_train)
    return model

def evaluate(individual):
    X = np.array(individual).reshape(1, -1)
    prediction = model.predict(X)
    return prediction,

# 모델 유형을 선택하고 모델을 구축하세요
# 'linear_regression', 'polynomial_regression', 'gaussian_process'
model_type = 'polynomial_regression'  # 이 부분을 변경하여 다른 모델을 시험해보세요
model = build_surrogate_model(model_type, X, y)

# 예측 (새 데이터에 대한 예측을 수행하려면 이 부분을 사용하세요)
X_test = np.linspace(0, 10, 100).reshape(-1, 1)
y_pred = model.predict(X_test)

# 예측 결과 시각화 (선택적)
import matplotlib.pyplot as plt
plt.scatter(X, y, label='Training data')
plt.plot(X_test, y_pred, color='red', label='Surrogate model prediction')
plt.legend()
plt.show()

# 유전 알고리즘 설정
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 10)  # 입력 변수의 범위 설정
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)  # n=입력 변수의 수
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# 유전 알고리즘 실행
population = toolbox.population(n=50)
NGEN = 40
CXPB, MUTPB = 0.5, 0.2

for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, CXPB, MUTPB)
    fits = list(map(toolbox.evaluate, offspring))
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))

# 최적의 개체 추출
best_ind = tools.selBest(population, 1)[0]
print("Best Individual: ", best_ind, "Best Fitness: ", evaluate(best_ind))