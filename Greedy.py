def read_schedule_file(filename):
    with open(filename, 'r') as file:
        num_machines = int(file.readline().strip())
        num_jobs = int(file.readline().strip())
        processing_times = list(map(int, file.readline().strip().split()))
    return num_machines, num_jobs, processing_times


def greedy_scheduler(num_machines, processing_times):
    num_jobs = len(processing_times)

    # Initialize the machines with empty job lists and makespan of zero
    machines = [[] for _ in range(num_machines)]
    machine_loads = [0] * num_machines

    # Sort jobs by processing time in descending order
    sorted_jobs = sorted(range(num_jobs), key=lambda x: processing_times[x], reverse=True)

    for job in sorted_jobs:
        # Find the machine with the least makespan
        least_loaded_machine = machine_loads.index(min(machine_loads))

        # Assign the job to this machine
        machines[least_loaded_machine].append(job)

        # Update the load of this machine
        machine_loads[least_loaded_machine] += processing_times[job]

    return machines, max(machine_loads)


def main():
    # Read the scheduling information from a file
    filename = '/Users/paulinaheine/Codes/ACOPMS/Instances/cmax/INSTANCES/U_2_0500_25_9.txt'  # Replace with the path to your file
    num_machines, num_jobs, processing_times = read_schedule_file(filename)

    # Run the greedy scheduler
    best_schedule, best_makespan = greedy_scheduler(num_machines, processing_times)

    print("Best Schedule (Greedy):", best_schedule)
    print("Best Makespan (Greedy):", best_makespan)


if __name__ == "__main__":
    main()
