def create_surrogate_model(model_type, X_train, y_train):
    if model_type == 'linear_regression':
        model = LinearRegression()
    elif model_type == 'polynomial_regression':
        degree = 4  # Customize as needed
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    elif model_type == 'gaussian_process':
        kernel = DotProduct() + WhiteKernel()
        model = GaussianProcessRegressor(kernel=kernel)
    else:
        raise ValueError("Unknown model type provided.")
    
    model.fit(X_train, y_train)
    return model