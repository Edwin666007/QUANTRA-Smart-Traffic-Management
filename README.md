QUANTRA

Quantum-Inspired Intelligent Traffic Management System

Problem Statement

Urban traffic congestion causes serious delays for emergency vehicles such as ambulances and fire trucks.  
Most traffic signals still operate on fixed timing logic and cannot adapt to real-time emergency situations.
During the Golden Hour, even a small delay can result in loss of life.

Solution Overview

QUANTRA is a quantum-inspired intelligent traffic management system designed to dynamically coordinate traffic signals and prioritize emergency vehicles.
The system creates an Emergency Green Wave that allows ambulances to pass through congested intersections without unnecessary stopping.
The project is validated using a microscopic urban traffic simulation modeled on Anna Nagar, Chennai.

Simulation Environment

- Traffic Simulator: SUMO (Simulation of Urban Mobility)
- City Model: Anna Nagar, Chennai (simulated road network)
- Simulation Type: Microscopic traffic simulation
- Focus Area: Emergency vehicle prioritization
- Programming Language: Python

The simulation environment is used to validate and visualize the traffic intelligence logic.

Core System Modules

1. Real-Time Traffic Density Analysis

- Continuously monitors vehicle density and speed near intersections.
- Detects congestion buildup in real time.
- Triggers adaptive traffic signal logic when congestion thresholds are exceeded.

2. Emergency Green Wave Protocol

- Automatically detects emergency vehicles such as ambulances.
- Identifies the nearest and upcoming intersections.
- Overrides traffic signals to GREEN in real time.
- Sends yield instructions to surrounding vehicles.
- Ensures uninterrupted movement for emergency vehicles.

3. Quantum-Inspired Routing Logic

- Uses a simulated quantum optimization approach.
- Evaluates multiple traffic states in parallel.
- Selects the lowest-resistance route based on traffic density.
- Minimizes overall delay for emergency vehicles.

Demo Video
Project demonstration video link: https://drive.google.com/file/d/1AYLEKzIlLHA0kszxN4pxhIzOpNnn8p4G/view?usp=drivesdk

How to Run the Simulation
Prerequisites

- Python 3.8
- SUMO installed and added to system PATH

Installation

Run requirements.txt

Known Constraints

- The current implementation is validated only in a simulated environment.
- Real-world deployment would require integration with live traffic sensors, signal controllers, and emergency dispatch systems.

Hackathon Context

- Event: TEXUS Hackathon 2026
- Project Stage: Prototype / Simulation
- Role: Lead Architect & Simulation Engineer

Impact

QUANTRA demonstrates how intelligent and adaptive traffic coordination can significantly reduce emergency response time in dense urban environments.

By dynamically prioritizing emergency vehicles, the system has the potential to save lives during critical situations.

License

This project is released under the MIT License.
