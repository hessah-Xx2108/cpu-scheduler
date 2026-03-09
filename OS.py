class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = -1
        self.finish_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.is_completed = False

def print_gantt_chart(gantt_chart):
    print("\nGantt Chart:")
    print("|", end="")
    for entry in gantt_chart:
        print(f" P{entry[2]} ({entry[0]}-{entry[1]}) |", end="")
    print()

def print_results(processes, total_waiting, total_turnaround, has_arrival_time):
    print("\nResult Table:")
    if has_arrival_time:
        print("PID | Arrival Time | Burst Time | Waiting Time | Turnaround Time")
        for process in sorted(processes, key=lambda x: x.pid):
            print(f"{process.pid:3} | {process.arrival_time:12} ms | {process.burst_time:10} ms | {process.waiting_time:12} ms | {process.turnaround_time:14} ms")
    else:
        print("PID | Burst Time | Waiting Time | Turnaround Time")
        for process in sorted(processes, key=lambda x: x.pid):
            print(f"{process.pid:3} | {process.burst_time:10} ms | {process.waiting_time:12} ms | {process.turnaround_time:14} ms")

    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    print(f"\nAverage Waiting Time: {avg_waiting:.2f} ms")
    print(f"Average Turnaround Time: {avg_turnaround:.2f} ms")

def fcfs(processes, has_arrival_time):
    processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
    if has_arrival_time:
        processes_copy.sort(key=lambda x: x.arrival_time)
    current_time = 0
    total_waiting = 0
    total_turnaround = 0
    gantt_chart = []

    for process in processes_copy:
        if has_arrival_time and current_time < process.arrival_time:
            current_time = process.arrival_time
            
        process.start_time = current_time
        process.waiting_time = current_time - (process.arrival_time if has_arrival_time else 0)
        current_time += process.burst_time
        process.finish_time = current_time
        process.turnaround_time = process.finish_time - (process.arrival_time if has_arrival_time else 0)

        total_waiting += process.waiting_time
        total_turnaround += process.turnaround_time
        gantt_chart.append((process.start_time, process.finish_time, process.pid))

    print("\nFCFS")
    print_gantt_chart(gantt_chart)
    print_results(processes_copy, total_waiting, total_turnaround, has_arrival_time)

def sjf_preemptive(processes, has_arrival_time):
    processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
    n = len(processes_copy)
    time = 0
    completed = 0
    total_waiting = 0
    total_turnaround = 0
    gantt_chart = []
    last_pid = -1
    last_start = 0

    while completed < n:
        available = [p for p in processes_copy if (not has_arrival_time or p.arrival_time <= time) and not p.is_completed]
        if available:
            current = min(available, key=lambda x: x.remaining_time)
            
            if last_pid != current.pid:
                if last_pid != -1:
                    gantt_chart.append((last_start, time, last_pid))
                last_start = time
                last_pid = current.pid

            current.remaining_time -= 1
            time += 1

            if current.remaining_time == 0:
                current.finish_time = time
                current.turnaround_time = current.finish_time - (current.arrival_time if has_arrival_time else 0)
                current.waiting_time = current.turnaround_time - current.burst_time
                current.is_completed = True
                total_waiting += current.waiting_time
                total_turnaround += current.turnaround_time
                completed += 1
                gantt_chart.append((last_start, time, current.pid))
                last_pid = -1
        else:
            time += 1

    print("\nSJF Preemptive (SRTF)")
    print_gantt_chart(gantt_chart)
    print_results(processes_copy, total_waiting, total_turnaround, has_arrival_time)

def sjf_non_preemptive(processes, has_arrival_time):
    processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
    n = len(processes_copy)
    completed = 0
    current_time = 0
    total_waiting = 0
    total_turnaround = 0
    gantt_chart = []

    while completed < n:
        available = [p for p in processes_copy if (not has_arrival_time or p.arrival_time <= current_time) and not p.is_completed]
        if available:
            shortest = min(available, key=lambda x: x.burst_time)
            shortest.start_time = current_time
            shortest.finish_time = current_time + shortest.burst_time
            shortest.waiting_time = shortest.start_time - (shortest.arrival_time if has_arrival_time else 0)
            shortest.turnaround_time = shortest.finish_time - (shortest.arrival_time if has_arrival_time else 0)
            shortest.is_completed = True

            total_waiting += shortest.waiting_time
            total_turnaround += shortest.turnaround_time
            gantt_chart.append((shortest.start_time, shortest.finish_time, shortest.pid))
            current_time = shortest.finish_time
            completed += 1
        else:
            current_time += 1

    print("\nSJF Non-Preemptive")
    print_gantt_chart(gantt_chart)
    print_results(processes_copy, total_waiting, total_turnaround, has_arrival_time)

def round_robin(processes, quantum, has_arrival_time):
    # Create fresh copies of all processes
    processes_copy = []
    for p in processes:
        new_p = Process(p.pid, p.arrival_time, p.burst_time)
        new_p.remaining_time = p.burst_time  # Explicitly set remaining_time
        processes_copy.append(new_p)
    
    time = 0
    queue = []
    gantt_chart = []
    total_waiting = 0
    total_turnaround = 0
    completed = 0
    n = len(processes_copy)
    
    # Reset all process states
    for p in processes_copy:
        p.start_time = -1
        p.finish_time = -1
        p.waiting_time = 0
        p.turnaround_time = 0
        p.is_completed = False
        p.remaining_time = p.burst_time  # Ensure remaining_time is an integer

    while completed < n:
        # Add arriving processes to queue
        for p in processes_copy:
            if not p.is_completed and (not has_arrival_time or p.arrival_time <= time):
                if p not in queue and p.remaining_time > 0:
                    queue.append(p)
        
        if not queue:
            time += 1
            continue
        
        current = queue.pop(0)
        if current.start_time == -1:
            current.start_time = time
            
        # Execute for quantum or remaining time, whichever is smaller
        exec_time = min(int(current.remaining_time), int(quantum))  # Force integer conversion
        gantt_chart.append((time, time + exec_time, current.pid))
        time += exec_time
        current.remaining_time -= exec_time
        
        # Check for completion
        if current.remaining_time <= 0:
            current.finish_time = time
            current.turnaround_time = current.finish_time - (current.arrival_time if has_arrival_time else 0)
            current.waiting_time = current.turnaround_time - current.burst_time
            current.is_completed = True
            total_waiting += current.waiting_time
            total_turnaround += current.turnaround_time
            completed += 1
        else:
            # Put back in queue if not finished
            queue.append(current)
    
    print("\nRound Robin")
    print_gantt_chart(gantt_chart)
    print_results(processes_copy, total_waiting, total_turnaround, has_arrival_time)

def get_positive_integers(prompt):
    while True:
        try:
            values = list(map(int, input(prompt).split()))
            if all(v >= 0 for v in values):
                return values
            print("Please enter non-negative integers!")
        except ValueError:
            print("Invalid input! Please enter numbers separated by spaces.")

def get_yes_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.")

def main():
    print("=== CPU Scheduling Algorithms Simulator ===")
    
    while True:
        # Ask if processes have arrival times
        has_arrival_time = get_yes_no("\nDo processes have arrival times? (y/n): ")
        
        # Get arrival times if needed
        if has_arrival_time:
            arrival_times = get_positive_integers("Enter arrival times (space-separated): ")
        
        # Get burst times
        burst_times = get_positive_integers("Enter burst times (ms, space-separated): ")
        
        # Validate input lengths
        if has_arrival_time and len(arrival_times) != len(burst_times):
            print("Error: Number of arrival times must match number of burst times")
            continue
            
        # Create processes
        processes = []
        for i in range(len(burst_times)):
            arrival = arrival_times[i] if has_arrival_time else 0
            processes.append(Process(i+1, arrival, burst_times[i]))
            
        if not processes:
            print("No processes added. Please enter at least one process.")
            continue
            
        # Get quantum for RR if needed
        quantum = 1
        if has_arrival_time:
            quantum_input = get_positive_integers("\nEnter quantum time for Round Robin: ")
            quantum = quantum_input[0] if quantum_input else 1  # Take first value if list is provided
        
        # Run all scheduling algorithms
        print("\nRunning all scheduling algorithms...")
        fcfs(processes, has_arrival_time)
        sjf_non_preemptive(processes, has_arrival_time)
        sjf_preemptive(processes, has_arrival_time)
        if has_arrival_time:
            round_robin(processes, quantum, has_arrival_time)
        
        # Ask to run again
        if not get_yes_no("\nDo you want to run the program again? (y/n): "):
            print("\nExiting simulator. Goodbye!")
            break

if __name__ == "__main__":
    main()
