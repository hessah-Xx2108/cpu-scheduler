# CPU Scheduling Algorithms Simulator

A Python-based simulator that demonstrates and compares different CPU scheduling algorithms used in operating systems.

## Overview

This simulator implements four classic CPU scheduling algorithms, allowing users to visualize process execution through Gantt charts and compare performance metrics. It's designed for educational purposes to help understand how different scheduling strategies affect process execution.

## Features

- **Four Scheduling Algorithms:**
  - First Come First Served (FCFS)
  - Shortest Job First (SJF) - Preemptive (SRTF)
  - Shortest Job First (SJF) - Non-Preemptive
  - Round Robin (with customizable quantum)

- **Process Management:**
  - Support for processes with or without arrival times
  - Handles up to 10+ concurrent processes
  - Proper queue management for ready processes

- **Visual Output:**
  - Gantt chart visualization for each algorithm
  - Process execution timeline display

- **Performance Metrics:**
  - Average Waiting Time
  - Average Turnaround Time
  - Per-process waiting and turnaround times

## How to Run

1. Ensure you have Python 3.x installed
2. Save the code as `cpu_scheduler.py`
3. Run the program:
   ```bash
   python cpu_scheduler.py
