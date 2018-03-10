MDP

    - Set up the Markov Decision Process environment.

Simulator

    - Where the training and testing happen.
    - Training: learn the optimal parameters to ensure as many bounces as possible.
    - Testing: use the learned parameters on an actual game, tracking # of bounces before losing.

runner.py

    - Set up the required parameters (\alpha,\gamma, \epsilon) and start the training.