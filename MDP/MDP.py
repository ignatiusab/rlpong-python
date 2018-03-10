from random import uniform
from math import floor

class MDP:
    def __init__(self, 
                 ball_x=None,
                 ball_y=None,
                 velocity_x=None,
                 velocity_y=None,
                 paddle_y=None):
        '''
        Setup MDP with the initial values provided.
        '''
        self.create_state(
            ball_x=ball_x,
            ball_y=ball_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            paddle_y=paddle_y
        )
        
        # the agent can choose between 3 actions - stay, up or down respectively.
        self.actions = [0, 0.04, -0.04]
        
    def create_state(self,
              ball_x=None,
              ball_y=None,
              velocity_x=None,
              velocity_y=None,
              paddle_y=None):
        '''
        Helper function for the initializer. Initialize member variables with provided or default values.
        '''
        self.paddle_height = 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        self.paddle_y = 0.5
    
    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''
        # default reward
        reward = 0

        # update ball position
        self.ball_y = self.ball_y + self.velocity_y 
        self.ball_x = self.ball_x + self.velocity_x
        
        # check ball position boundary
        if(self.ball_y < 0):
          self.ball_y = -self.ball_y
          self.velocity_y = -self.velocity_y
        else:
          if(self.ball_y > 1):
            self.ball_y = 2 - self.ball_y
            self.velocity_y = -self.velocity_y
        
        if(self.ball_x < 0):
          self.ball_x = -self.ball_x
          self.velocity_x = -self.velocity_x
        else:
          # passed
          if(self.ball_x > 1):
            if((self.ball_y >= self.paddle_y) and self.ball_y <= self.paddle_y + self.paddle_height):
              self.ball_x = 2 * 1 - self.ball_x
              self.velocity_x = -self.velocity_x + uniform(-0.015, 0.015)
              self.velocity_y = self.velocity_y + uniform(-0.03, 0.03)
              reward = 1
            else:
              reward = -1
              return reward        
       
        # check ball velocity boundary
        # |velocity_x| > 0.03
        if( abs(self.velocity_x) < 0.03):
          if(self.velocity_x < 0):
            self.velocity_x = -0.03
          else:
            self.velocity_x = 0.03
        # |velocity_x| < 1
        else:
          if( abs(self.velocity_x) > 1):
            if(self.velocity_x < 0):
              self.velocity_x = -0.97
            else:
              self.velocity_x = 0.97
        
        # |velocity_y| < 1
        if(abs(self.velocity_y) > 1):
          if(self.velocity_y < 0):
            self.velocity_y = -0.94
          else:
            self.velocity_y = 0.94
        
        # update paddle position
        self.paddle_y = self.paddle_y + self.actions[action_selected]

        # check paddle position
        if(self.paddle_y < 0):
          self.paddle_y = 0
        else:
          if(self.paddle_y > 1 - self.paddle_height):
            self.paddle_y = 1 - self.paddle_height
        return reward
    
    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''
        # if ball outbound, last state
        if(self.ball_x > 1):
          state = 10368
        else:
          # discretize ball_x: 0-11
          if(self.ball_x == 1):
            d_ball_x = 11
          else:
            d_ball_x = floor(12 * self.ball_x)
          
          # discretize ball_y: 0-11
          if(self.ball_y == 1):
            d_ball_y = 11
          else:
            d_ball_y = floor(12 * self.ball_y)
          
          # discretize velocity_x: -1 or 1 -> 0 or 1
          d_velocity_x = floor(self.velocity_x + 1) - 1
          
          # discretize velocity_y: -1 or 0 or 1 -> 0 or 1 or 2
          d_velocity_y = floor(self.velocity_y + 1)
          
          # discretize paddle: 0-11
          if(self.paddle_y == (1 - self.paddle_height)):
            d_paddle = 11
          else:
            d_paddle = floor(12 * self.paddle_y / (1 - self.paddle_height))
          # calculate state number
          
          state = ( (864 * d_ball_x) +      # 12*3*2*12 = 864
                     (72 * d_ball_y) +      # 12*3*2 = 72
                     (36 * d_velocity_x) +  # 12*3 = 36
                     (12 * d_velocity_y) + 
                           d_paddle )
        return int(state)