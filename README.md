# Autonomous Navigation & Decision-Making System

This project implements an autonomous agent operating under uncertainty by integrating localization, path planning, and probabilistic decision-making in simulated environments. The system is designed as a set of modular components that work together to enable robust navigation and tracking.

## System Overview
The system combines:
- Learning-based localization from noisy observations
- Graph-based path planning in dynamic environments
- Probabilistic target tracking under uncertainty

Each component was implemented and evaluated independently, then designed to work cohesively as part of a unified decision-making pipeline.

## Project Components

### 1. Hazard-Aware Path Planning
Computes optimal navigation paths using A* and Dijkstra algorithms while accounting for obstacles and environmental hazards.  
GitHub: https://github.com/DharmPatel02/autonomous-navigation-system

### 2. Probabilistic Target Tracking (Hit by Neutrino)
Tracks moving targets under sensor noise using Bayesian inference techniques.  
GitHub: https://github.com/DharmPatel02/Hit-by-Neutrino

### 3. CNN-Based Localization (Space Rats)
Estimates the agent’s position from noisy sensory inputs using a convolutional neural network.  
GitHub: https://github.com/DharmPatel02/Space-Rats

## Key Techniques
- Convolutional Neural Networks (CNNs)
- Bayesian Inference
- A* and Dijkstra Path Planning
- Probabilistic Reasoning under Uncertainty

## Technologies
Python, NumPy, PyTorch, Graph Search Algorithms
