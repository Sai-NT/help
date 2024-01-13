def create_process(name, arrival_time, burst_time):
    return {
        'name': name,
        'arrival_time': arrival_time,
        'burst_time': burst_time,
        'remaining_time': burst_time,
        'end_time': 0,
        'turnaround_time': 0,
        'waiting_time': 0
    }

def validate_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Invalid input. Please enter a value between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main():
    min_processes, max_processes = 5, 10
    min_arrival_time, max_arrival_time = 0, 10
    min_burst_time, max_burst_time = 1, 15  # Adjusted min_burst_time to avoid zero burst time

    num_processes = validate_input(f"Enter the number of processes ({min_processes}-{max_processes}): ", min_processes, max_processes)
    processes = []

    for i in range(1, num_processes + 1):
        arrival_time = validate_input(f"Enter arrival time for process P{i} ({min_arrival_time}-{max_arrival_time}): ", min_arrival_time, max_arrival_time)
        burst_time = validate_input(f"Enter burst time for process P{i} ({min_burst_time}-{max_burst_time}): ", min_burst_time, max_burst_time)
        processes.append(create_process(f"P{i}", arrival_time, burst_time))

    total_burst_time = sum(process['burst_time'] for process in processes)
    current_time = 0

    while any(process['remaining_time'] > 0 for process in processes):
        available_processes = [process for process in processes if process['arrival_time'] <= current_time and process['remaining_time'] > 0]
        if not available_processes:
            current_time += 1
            print(f"Time {current_time}: CPU is idle")
            continue

        shortest_process = min(available_processes, key=lambda process: process['remaining_time'])
        shortest_process['remaining_time'] -= 1
        current_time += 1
        shortest_process['end_time'] = current_time

    for process in processes:
        process['turnaround_time'] = process['end_time'] - process['arrival_time']
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']

    print("\nSRTF Scheduling Table:")
    print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format("Process", "Arrival Time", "Burst Time", "End Time", "Turnaround Time", "Waiting Time"))
    for process in processes:
        print("{:<10} {:<15} {:<15} {:<15} {:<15} {:<15}".format(process['name'], process['arrival_time'], process['burst_time'], process['end_time'], process['turnaround_time'], process['waiting_time']))

    

    idle_time = current_time - total_burst_time
    cpu_utilization = (total_burst_time / (current_time + idle_time)) * 100
    avg_turnaround_time = sum(process['turnaround_time'] for process in processes) / num_processes
    avg_waiting_time = sum(process['waiting_time'] for process in processes) / num_processes

    print("\nStatistical Information:")
    print(f"CPU Utilization: {round(cpu_utilization, 2)}%")
    print(f"Average Turnaround Time: {round(avg_turnaround_time, 2)} ms")
    print(f"Average Waiting Time: {round(avg_waiting_time, 2)} ms")

if __name__ == "__main__":
    main()
