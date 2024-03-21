from scipy.stats.qmc import LatinHypercube
from scipy.stats import qmc

def from scipy.stats.qmc import LatinHypercube
from scipy.stats import qmc

def generate_lhs_samples(variable_names, upper_bounds, lower_bounds, n_samples=100):
    """
    Generate samples using Latin Hypercube Sampling.
    
    Parameters:
    - variable_names: List of names of the variables.
    - upper_bounds: Array of upper bounds for each variable.
    - lower_bounds: Array of lower bounds for each variable.
    - n_samples: Number of samples to generate.
    
    Returns:
    - samples: A numpy array of shape (n_samples, n_variables) containing the samples.
    """
    n_variables = len(variable_names)  # Number of variables
    lhs = LatinHypercube(d=n_variables)
    samples = lhs.random(n=n_samples)

    # Scale samples from 0-1 range to the actual range of each variable
    scaled_samples = qmc.scale(samples, lower_bounds, upper_bounds)
    
    return scaled_samples

# Example usage
geometry_variable_name = ['OPERATING_PHASE', 'DMAG1', 'DMAG2', 'DMAG3', 'MT1', 'MT2', 'MT3', 'MT4', 'MT5', 'MT6', 'MW1', 'MW2', 'MW3', 'MW4', 'OSW1', 'OSW2', 'OSW3', 'WMAG1', 'WMAG3', 'WMAG5']
geometry_variable_upper = np.array([80, 80, 32, 15, 14, 14, 14, 14, 14, 14, 45, 20, 30, 20, 35, 15, 15, 15, 15, 20])
geometry_variable_lower = np.array([65, 65, 15, 5, 5, 5, 5, 5, 5, 5, 20, 5, 10, 5, 2, 2, 2, 5, 5, 5])

# Generate samples
samples = generate_lhs_samples(geometry_variable_name, geometry_variable_upper, geometry_variable_lower, n_samples=100)

# Print the shape of the samples to verify
print("Shape of the generated samples:", samples.shape)
# This should print: Shape of the generated samples: (100, 20)(variable_names, upper_bounds, lower_bounds, n_samples=100):
    """
    Generate samples using Latin Hypercube Sampling.
    
    Parameters:
    - variable_names: List of names of the variables.
    - upper_bounds: Array of upper bounds for each variable.
    - lower_bounds: Array of lower bounds for each variable.
    - n_samples: Number of samples to generate.
    
    Returns:
    - samples: A numpy array of shape (n_samples, n_variables) containing the samples.
    """
    n_variables = len(variable_names)  # Number of variables
    lhs = LatinHypercube(d=n_variables)
    samples = lhs.random(n=n_samples)

    # Scale samples from 0-1 range to the actual range of each variable
    scaled_samples = qmc.scale(samples, lower_bounds, upper_bounds)
    
    return scaled_samples

# Example usage
geometry_variable_name = ['OPERATING_PHASE', 'DMAG1', 'DMAG2', 'DMAG3', 'MT1', 'MT2', 'MT3', 'MT4', 'MT5', 'MT6', 'MW1', 'MW2', 'MW3', 'MW4', 'OSW1', 'OSW2', 'OSW3', 'WMAG1', 'WMAG3', 'WMAG5']
geometry_variable_upper = np.array([80, 80, 32, 15, 14, 14, 14, 14, 14, 14, 45, 20, 30, 20, 35, 15, 15, 15, 15, 20])
geometry_variable_lower = np.array([65, 65, 15, 5, 5, 5, 5, 5, 5, 5, 20, 5, 10, 5, 2, 2, 2, 5, 5, 5])

# Generate samples
samples = generate_lhs_samples(geometry_variable_name, geometry_variable_upper, geometry_variable_lower, n_samples=100)

# Print the shape of the samples to verify
print("Shape of the generated samples:", samples.shape)
# This should print: Shape of the generated samples: (100, 20)