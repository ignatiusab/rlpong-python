from Simulator.simulator import Simulator

if __name__ == "__main__":
    alpha_value = 0.185
    gamma_value = 0.95
    epsilon_value = 0.01
    num_games = 200000
    print("a= "+str(alpha_value)+ " n= " +str(num_games))
    Simulator(num_games, alpha_value, gamma_value, epsilon_value)