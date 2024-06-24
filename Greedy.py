import numpy as np
import glob


def read_schedule_file(filename):
    with open(filename, 'r') as file:
        num_machines = int(file.readline().strip())
        num_jobs = int(file.readline().strip())
        processing_times = list(map(int, file.readline().strip().split()))
    return num_machines, num_jobs, processing_times


def modified_greedy_scheduler(num_machines, processing_times):
    num_jobs = len(processing_times)

    # Initialize the machines with empty job lists and makespan of zero
    machines = [[] for _ in range(num_machines)]
    machine_loads = [0] * num_machines

    # Shuffle the jobs and assign the first job randomly to each machine
    job_list = list(range(num_jobs))
    np.random.shuffle(job_list)

    for i in range(num_machines):
        if job_list:
            first_job = job_list.pop(0)
            machines[i].append(first_job)
            machine_loads[i] += processing_times[first_job]

    # Sort the remaining jobs by processing time in descending order
    sorted_jobs = sorted(job_list, key=lambda x: processing_times[x], reverse=True)

    for job in sorted_jobs:
        # Find the machine with the least makespan
        least_loaded_machine = machine_loads.index(min(machine_loads))

        # Assign the job to this machine
        machines[least_loaded_machine].append(job)

        # Update the load of this machine
        machine_loads[least_loaded_machine] += processing_times[job]

    return machines, max(machine_loads)


def main():
    # Path to the directory containing the schedule files
    file_path_pattern = '/Users/paulinaheine/Codes/ACOPMS/Instances/cmax/Big/*.txt'  # Update the path pattern as needed

    # Get the list of all files matching the pattern
    schedule_files = glob.glob(file_path_pattern)

    for filename in schedule_files:
        print(f"Processing file: {filename}")

        # Read the scheduling information from a file
        num_machines, num_jobs, processing_times = read_schedule_file(filename)

        # Run the modified greedy scheduler
        best_schedule, best_makespan = modified_greedy_scheduler(num_machines, processing_times)

        print(f"Best Schedule (Modified Greedy) for {filename}:", best_schedule)
        print(f"Best Makespan (Modified Greedy) for {filename}:", best_makespan)


if __name__ == "__main__":
    main()

