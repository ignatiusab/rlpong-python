from MDP.MDP import MDP
from random import uniform, randint

class Simulator:
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0):
        '''
        Setup the Simulator with the provided values.
        :param num_games - number of games to be trained on.
        :param alpha_value - 1/alpha_value is the decay constant.
        :param gamma_value - Discount Factor.
        :param epsilon_value - Probability value for the epsilon-greedy approach.
        '''
        self.num_games = num_games       
        self.epsilon_value = epsilon_value       
        self.alpha_value = alpha_value       
        self.gamma_value = gamma_value
        
        # Your Code Goes Here!
        self.curState = 0
        self.d_curState = 0
        self.Q = []
        for i in range (10369):
            self.Q.append([0,0,0])
        self.bounced = 0

        #start training    
        self.train_agent()
        print ("total bounced: "+ str(self.bounced))
        print ("avg bounced per game: "+ str(self.bounced/self.num_games))

    def f_function(self):
        '''
        Choose action based on an epsilon greedy approach
        :return action selected
        '''

        # Your Code Goes Here!
        if( uniform(0,1) < self.epsilon_value):
            action_selected = randint(0,2)
            #print "r"
        else:
            action_selected = 0
            self.d_curState = self.curState.discretize_state()
            if( self.Q[self.d_curState][action_selected] < self.Q[self.d_curState][1] ):
                action_selected = 1
            if( self.Q[self.d_curState][action_selected] < self.Q[self.d_curState][2] ):
                action_selected = 2
            #print action_selected
        
        return action_selected

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        # Your Code Goes Here!
        print ("start training")
        #print self.curState.discretize_state()
        for i in range (self.num_games):
            #print i
            self.play_game()
    
    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        '''
        # Your Code Goes Here!
        reward=0
        
        self.curState = MDP()
        self.d_curState = self.curState.discretize_state()
        while self.d_curState != 10368:
            old_State = self.d_curState
            action_selected = self.f_function()
            reward = self.curState.simulate_one_time_step(action_selected)
           
            if(reward == 1):
                #print reward
                self.bounced = self.bounced + 1
                
            next_State = self.curState.discretize_state()
            self.updateQ(old_State,reward,action_selected,next_State)
            #print str(self.d_curState)+ " " +str(self.curState.ball_x)

    def updateQ(self,old_State,reward,action_selected,next_State):
        # Q[S][a]= (1-alpha)*Q[S][a] + alpha*(R+gamma*max(Q[a']))
        self.Q[old_State][action_selected] = (1-self.alpha_value) * self.Q[old_State][action_selected] + self.alpha_value * (reward + self.gamma_value * max(self.Q[next_State]))
