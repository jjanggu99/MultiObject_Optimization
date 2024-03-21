def run_genetic_algorithm(model, n_individuals=50, n_gen=40, cxpb=0.5, mutpb=0.2):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, 0, 10)  # Adjust as needed
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)  # n=number of input variables
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    def evaluate(individual):
        X = np.array(individual).reshape(1, -1)
        prediction = model.predict(X)
        return prediction,
    
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    population = toolbox.population(n=n_individuals)
    for gen in range(n_gen):
        offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
        fits = list(map(toolbox.evaluate, offspring))
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
    
    best_ind = tools.selBest(population, 1)[0]
    return best_ind, evaluate(best_ind)