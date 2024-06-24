import numpy as np
import glob

def read_schedule_file(filename):
    with open(filename, 'r') as file:
        num_machines = int(file.readline().strip())
        num_jobs = int(file.readline().strip())
        processing_times = list(map(int, file.readline().strip().split()))
    return num_machines, num_jobs, processing_times

class Ant:
    def __init__(self, num_jobs, num_machines, processing_times, pheromone, alpha, beta):
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.processing_times = processing_times
        self.pheromone = pheromone
        self.alpha = alpha
        self.beta = beta
        self.schedule = self._generate_schedule()
        self.makespan = self._calculate_makespan()

    def _generate_schedule(self):
        # Generate a random initial schedule
        schedule = [[] for _ in range(self.num_machines)]
        job_list = list(range(self.num_jobs))
        np.random.shuffle(job_list)

        for job in job_list:
            chosen_machine = np.random.choice(self.num_machines)
            schedule[chosen_machine].append(job)

        return schedule

    def _calculate_probabilities(self, schedule, job):
        pheromone_values = np.array([self.pheromone[machine][job] for machine in range(self.num_machines)])
        machine_loads = np.array([sum(self.processing_times[j] for j in machine_jobs) for machine_jobs in schedule])
        attractiveness = 1 / (machine_loads + 1)

        probabilities = (pheromone_values ** self.alpha) * (attractiveness ** self.beta)
        probabilities /= probabilities.sum()

        return probabilities

    def _assign_job_to_machine(self, schedule, job):
        probabilities = self._calculate_probabilities(schedule, job)
        chosen_machine = np.random.choice(self.num_machines, p=probabilities)
        return chosen_machine

    def _calculate_makespan(self):
        machine_loads = [sum(self.processing_times[job] for job in machine_jobs) for machine_jobs in self.schedule]
        return max(machine_loads)

class AntColonyOptimizer:
    def __init__(self, num_machines, num_jobs, processing_times, num_ants=500, num_iterations=200, alpha=1.0, beta=2.0, evaporation_rate=0.3):
        self.num_machines = num_machines
        self.num_jobs = num_jobs
        self.processing_times = processing_times
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone = np.ones((num_machines, num_jobs))
        self.best_schedule = None
        self.best_makespan = float('inf')

    def _calculate_makespan(self, schedule):
        machine_loads = [sum(self.processing_times[job] for job in machine_jobs) for machine_jobs in schedule]
        return max(machine_loads)

    def _update_pheromones(self, ants):
        self.pheromone *= (1 - self.evaporation_rate)
        for ant in ants:
            for machine_index, machine_jobs in enumerate(ant.schedule):
                for job in machine_jobs:
                    self.pheromone[machine_index][job] += 1 / ant.makespan

    def optimize(self):
        for iteration in range(self.num_iterations):
            ants = [Ant(self.num_jobs, self.num_machines, self.processing_times, self.pheromone, self.alpha, self.beta) for _ in range(self.num_ants)]
            for ant in ants:
                if ant.makespan < self.best_makespan:
                    self.best_makespan = ant.makespan
                    self.best_schedule = ant.schedule

            self._update_pheromones(ants)
            print(f"Iteration {iteration+1}/{self.num_iterations}, Best Makespan: {self.best_makespan}")

        return self.best_schedule, self.best_makespan

def main():
    # Path to the directory containing the schedule files
    file_path_pattern = '/Users/paulinaheine/Codes/ACOPMS/Instances/cmax/Big/*.txt'  # Update the path pattern as needed

    # Get the list of all files matching the pattern
    schedule_files = glob.glob(file_path_pattern)

    for filename in schedule_files:
        print(f"Processing file: {filename}")

        # Read the scheduling information from a file
        num_machines, num_jobs, processing_times = read_schedule_file(filename)

        # Initialize the ACO with a random initial schedule
        aco = AntColonyOptimizer(num_machines, num_jobs, processing_times, num_ants=500, num_iterations=200, alpha=1.0, beta=1.0, evaporation_rate=0.3)

        # Run the optimization
        best_schedule, best_makespan = aco.optimize()

        print(f"Best Schedule (ACO) for {filename}:", best_schedule)
        print(f"Best Makespan (ACO) for {filename}:", best_makespan)

if __name__ == "__main__":
    main()
