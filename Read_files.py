def read_instance(filename):
    """
    Read in all information from a jssp-instance
    :param filename: Path to the jssp-instance file
    :return jobs, machines, all_jobs
    """
    skip_lines = 0
    jobs = None
    machines = None
    all_jobs = []

    with open(filename) as f:
        for e, l in enumerate(f):
            if e == skip_lines:
                line = l.split()
                machines = int(line[0])
            if e == skip_lines+1:
                line = l.split()
                jobs = int(line[0])

            if e > skip_lines + 1:
                line = l.split()
                all_jobs = []
                for n in line:
                    all_jobs.append(int(n))

    return jobs, machines, all_jobs

#jobs, machines, all_jobs = read_instance("/Users/paulinaheine/Codes/ACOPMS/Instances/cmax/INSTANCES/NU_1_0010_05_0.txt")