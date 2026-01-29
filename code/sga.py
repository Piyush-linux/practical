# ga_typing.py
import random

# Number of individuals in each generation
POPULATION_SIZE = 100

# Valid genes (characters allowed)
GENES = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ' 1234567890,.-;:_!"#%&/()=?@${[]}'
)

# Target string to be generated
TARGET = "Mithilesh Chauhan"


class Individual:
    """
    Class representing an individual in the population.
    Chromosome is a list of characters.
    """

    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.cal_fitness()

    @classmethod
    def mutated_genes(cls):
        """Create a random gene (character) for mutation."""
        return random.choice(GENES)

    @classmethod
    def create_gnome(cls):
        """Create a chromosome (list of genes) with same length as TARGET."""
        return [cls.mutated_genes() for _ in range(len(TARGET))]

    def mate(self, par2):
        """
        Perform mating (crossover + mutation) and produce new offspring.
        Probability choices:
         - take gene from parent1: prob < 0.45
         - take gene from parent2: 0.45 <= prob < 0.90
         - mutate gene (random): prob >= 0.90
        """
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):
            prob = random.random()
            if prob < 0.45:
                child_chromosome.append(gp1)
            elif prob < 0.90:
                child_chromosome.append(gp2)
            else:
                child_chromosome.append(self.mutated_genes())
        return Individual(child_chromosome)

    def cal_fitness(self):
        """
        Fitness score = number of characters that differ from TARGET.
        Lower is better. Perfect match => fitness 0.
        """
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness


def main():
    random.seed()  # system time or env seed; set an int for reproducibility
    generation = 1
    found = False
    population = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        gnome = Individual.create_gnome()
        population.append(Individual(gnome))

    MAX_GENERATIONS = 10000

    while not found and generation <= MAX_GENERATIONS:
        # sort population in increasing order of fitness
        population = sorted(population, key=lambda x: x.fitness)

        # display best of current generation
        best = population[0]
        print(
            f"Generation: {generation}\tString: {''.join(best.chromosome)}\tFitness: {best.fitness}"
        )

        # check if reached target
        if best.fitness == 0:
            print(
                f"\nFound target in generation {generation}:\n{''.join(best.chromosome)}"
            )
            found = True
            break

        new_generation = []

        # Elitism: 10% of fittest population move to next generation unchanged
        s = int((10 * POPULATION_SIZE) / 100)
        new_generation.extend(population[:s])

        # From top 50% of population, randomly select parents to create remaining children
        mating_pool_size = max(2, POPULATION_SIZE // 2)
        s = POPULATION_SIZE - s  # remaining number of individuals to generate
        for _ in range(s):
            parent1 = random.choice(population[:mating_pool_size])
            parent2 = random.choice(population[:mating_pool_size])
            child = parent1.mate(parent2)
            new_generation.append(child)

        population = new_generation
        generation += 1

    if not found:
        best = min(population, key=lambda x: x.fitness)
        print("\nMax generations reached.")
        print(f"Best solution: {''.join(best.chromosome)} (fitness={best.fitness})")


if __name__ == "__main__":
    main()
