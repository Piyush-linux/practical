#!/usr/bin/env python3
"""
ga_tsp.py
A Genetic Algorithm for the Traveling Salesman Problem (TSP).
Adapted and cleaned from the tutorial code you provided.
"""

import math
import random
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np


class City:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, city: "City") -> float:
        """Euclidean distance between two cities."""
        dx = self.x - city.x
        dy = self.y - city.y
        return math.hypot(dx, dy)

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


class Fitness:
    def __init__(self, route: List[City]):
        self.route = route
        self._distance = None
        self._fitness = None

    def routeDistance(self) -> float:
        """Total distance of the route (closed loop). Cached."""
        if self._distance is None:
            pathDistance = 0.0
            for i in range(len(self.route)):
                fromCity = self.route[i]
                toCity = self.route[(i + 1) % len(self.route)]
                pathDistance += fromCity.distance(toCity)
            self._distance = pathDistance
        return self._distance

    def routeFitness(self) -> float:
        """Fitness is inverse of distance (higher is better). Cached."""
        if self._fitness is None:
            dist = self.routeDistance()
            # Avoid division by zero; add small epsilon
            self._fitness = 1.0 / (dist + 1e-12)
        return self._fitness


def createRoute(cityList: List[City]) -> List[City]:
    route = random.sample(cityList, len(cityList))
    return route


def initialPopulation(popSize: int, cityList: List[City]) -> List[List[City]]:
    return [createRoute(cityList) for _ in range(popSize)]


def rankRoutes(population: List[List[City]]) -> List[Tuple[int, float]]:
    fitnessResults = {}
    for i, route in enumerate(population):
        fitnessResults[i] = Fitness(route).routeFitness()
    # sort by fitness desc (best first)
    return sorted(fitnessResults.items(), key=lambda item: item[1], reverse=True)


def selection(popRanked: List[Tuple[int, float]], eliteSize: int) -> List[int]:
    """Select route indices to be parents.
    Keep elites, then fill remainder by roulette-wheel selection.
    """
    selectionResults = []

    # Extract indices and fitnesses
    indices = [item[0] for item in popRanked]
    fitnesses = np.array([item[1] for item in popRanked], dtype=float)

    # Elitism: keep top elites
    for i in range(eliteSize):
        selectionResults.append(popRanked[i][0])

    # Roulette wheel selection for the rest
    fitness_sum = fitnesses.sum()
    cum_probs = np.cumsum(fitnesses) / fitness_sum

    # number to select
    n_to_select = len(popRanked) - eliteSize
    for _ in range(n_to_select):
        r = random.random()
        # find first index where cum_probs >= r
        idx = np.searchsorted(cum_probs, r)
        selectionResults.append(indices[idx])
    return selectionResults


def matingPool(
    population: List[List[City]], selectionResults: List[int]
) -> List[List[City]]:
    return [population[i] for i in selectionResults]


def breed(parent1: List[City], parent2: List[City]) -> List[City]:
    """Ordered crossover (OX) style - keep a slice from parent1 and fill with parent2 order."""
    child = []
    childP1 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    # slice from parent1
    for i in range(startGene, endGene + 1):
        childP1.append(parent1[i])

    # remaining genes from parent2 in order
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def breedPopulation(matingpool: List[List[City]], eliteSize: int) -> List[List[City]]:
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    # carry elites
    for i in range(eliteSize):
        children.append(matingpool[i])

    # breed to create the rest
    for i in range(length):
        child = breed(pool[i], pool[len(matingpool) - i - 1])
        children.append(child)
    return children


def mutate(individual: List[City], mutationRate: float) -> List[City]:
    for swapped in range(len(individual)):
        if random.random() < mutationRate:
            swapWith = int(random.random() * len(individual))
            individual[swapped], individual[swapWith] = (
                individual[swapWith],
                individual[swapped],
            )
    return individual


def mutatePopulation(
    population: List[List[City]], mutationRate: float
) -> List[List[City]]:
    return [mutate(route.copy(), mutationRate) for route in population]


def nextGeneration(
    currentGen: List[List[City]], eliteSize: int, mutationRate: float
) -> List[List[City]]:
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGen = mutatePopulation(children, mutationRate)
    return nextGen


def geneticAlgorithm(
    population: List[City],
    popSize: int,
    eliteSize: int,
    mutationRate: float,
    generations: int,
):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    for i in range(generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


def geneticAlgorithmPlot(
    population: List[City],
    popSize: int,
    eliteSize: int,
    mutationRate: float,
    generations: int,
):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])

    for i in range(generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])

    # Plot progress
    plt.figure(figsize=(10, 4))
    plt.plot(progress)
    plt.ylabel("Distance")
    plt.xlabel("Generation")
    plt.title("GA progress (distance vs generation)")
    plt.grid(True)
    plt.show()

    # Return best route and its distance
    bestIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestIndex]
    bestDistance = 1 / rankRoutes(pop)[0][1]
    return bestRoute, bestDistance


def plot_route(route: List[City], title: str = "Route"):
    xs = [c.x for c in route] + [route[0].x]
    ys = [c.y for c in route] + [route[0].y]
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, "o-", markersize=6)
    for i, c in enumerate(route):
        plt.text(c.x, c.y, str(i), fontsize=9)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def main():
    random.seed()  # or seed with an int for reproducibility

    # Create city list (example: 25 cities with coordinates in [0,200))
    cityList = [
        City(x=int(random.random() * 200), y=int(random.random() * 200))
        for _ in range(25)
    ]

    # GA parameters
    popSize = 100
    eliteSize = 20
    mutationRate = 0.01
    generations = 500

    # Run GA and plot progress
    bestRoute, bestDistance = geneticAlgorithmPlot(
        population=cityList,
        popSize=popSize,
        eliteSize=eliteSize,
        mutationRate=mutationRate,
        generations=generations,
    )

    print(f"Best distance: {bestDistance:.4f}")
    print("Best route (city coords):")
    print(bestRoute)

    # Plot final best route
    plot_route(bestRoute, title=f"Best route (distance {bestDistance:.2f})")


if __name__ == "__main__":
    main()
