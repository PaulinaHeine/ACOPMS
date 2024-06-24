import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def create_random_schedules(num_machines, num_jobs, num_ants):
    schedules = []
    for _ in range(num_ants):
        schedule = [[] for _ in range(num_machines)]
        job_list = list(range(num_jobs))
        np.random.shuffle(job_list)

        for job in job_list:
            chosen_machine = np.random.choice(num_machines)
            schedule[chosen_machine].append(job)

        schedules.append(schedule)
    return schedules


def count_paths(schedules, num_machines, num_jobs):
    path_count = {(f'M{i}', f'J{j}'): 0 for i in range(num_machines) for j in range(num_jobs)}
    for schedule in schedules:
        for machine_index, jobs in enumerate(schedule):
            for job in jobs:
                path_count[(f'M{machine_index}', f'J{job}')] += 1
    return path_count


def visualize_schedule_with_paths(path_count, num_machines, num_jobs):
    G = nx.DiGraph()
    pos = {}

    # Add nodes for machines
    for i in range(num_machines):
        G.add_node(f'M{i}', pos=(0, i))
        pos[f'M{i}'] = (0, i)

    # Add nodes for jobs
    for j in range(num_jobs):
        G.add_node(f'J{j}', pos=(1, j))
        pos[f'J{j}'] = (1, j)

    # Add edges with weights based on path count
    max_count = max(path_count.values())
    for (u, v), count in path_count.items():
        if count > 0:
            G.add_edge(u, v, weight=count)

    edges = G.edges(data=True)
    weights = [data['weight'] for _, _, data in edges]
    max_weight = max(weights) if weights else 1
    normalized_weights = [weight / max_weight * 10 for weight in weights]  # Normalize for better visibility

    # Draw the graph
    pos = nx.spring_layout(G, pos=pos, fixed=G.nodes())
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold',
            edge_color='gray')
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=normalized_weights, edge_color='blue')
    plt.title("Ant Colony Optimization - Path Frequencies")
    plt.show()


# Parameters
num_machines = 3
num_jobs = 10
num_ants = 50

# Create random schedules for multiple ants
schedules = create_random_schedules(num_machines, num_jobs, num_ants)

# Count the number of times each path is taken
path_count = count_paths(schedules, num_machines, num_jobs)

# Visualize the schedule with path frequencies
visualize_schedule_with_paths(path_count, num_machines, num_jobs)
