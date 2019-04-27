from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add

INPUT_NUM = 22

playerLength = 50
playerWidth = 50

def dangerRight(self, player, bullet_list):
    for lsr in bullet_list:
        if (player.posy + playerLength >= lsr.posy) and (player.posy <= lsr.posy) and (lsr.posx >= player.posx):
            return True
    return False
def dangerLeft(self, player, bullet_list):
    for lsr in bullet_list:
        if (player.posy + playerLength >= lsr.posy) and (player.posy <= lsr.posy) and (lsr.posx <= player.posx):
            return True
    return False
def dangerUp(self, player, bullet_list):
    for lsr in bullet_list:
        if (player.posx + playerWidth >= lsr.posx) and (player.posx <= lsr.posx) and (lsr.posy >= player.posy):
            return True
    return False
def dangerDown(self, player, bullet_list):
    for lsr in bullet_list:
        if (player.posx + playerWidth >= lsr.posx) and (player.posx <= lsr.posx) and (lsr.posy <= player.posy):
            return True
    return False


class DQNAgent(object):


    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.model = self.network()
        self.model = self.network("weights.hdf5")
        self.epsilon = 0
        self.actual = []
        self.memory = []


    def get_state(self, bullet_list, player, opponent):

        dangerRightBool = dangerRight(self,player, bullet_list)
        dangerLeftBool = dangerLeft(self,player,bullet_list)
        dangerUpBool = dangerUp(self,player,bullet_list)
        dangerDownBool = dangerDown(self,player,bullet_list)


        state = [
            dangerRightBool,
            dangerLeftBool,
            dangerUpBool,
            dangerDownBool,

            player.posx == opponent.posx, # same vertical
            player.posx > opponent.posx, # right of opponent
            player.posx < opponent.posx, # left of opponent
            player.posy == opponent.posy, # same horizon
            player.posy > opponent.posy, # above opponent
            player.posy < opponent.posy, # below opponent


            player.velx < 0,  # move left
            player.velx > 0,  # move right
            player.velx == 0, # no horizontal movement
            player.vely < 0,  # move down
            player.vely > 0,  # move up
            player.vely == 0, # no vertical movement

            opponent.velx < 0,  # move left
            opponent.velx > 0,  # move right
            opponent.velx == 0, # no horizontal movement
            opponent.vely < 0,  # move down
            opponent.vely > 0,  # move up
            opponent.vely == 0, # no vertical movement
        ]

        for i in range(len(state)):
            if state[i]:
                state[i] = 1
            else:
                state[i] = 0

        return np.asarray(state)

    def set_reward(self, player, death):
        self.reward = 0
        if death:
            self.reward += -1000
            return self.reward
        else:
            self.reward += 50
        if player.kill:
            self.reward += 1000
        if (player.posx > 100) and (player.posx < 700):
            self.reward += 50
        if (player.posy > 100) and (player.posy < 700):
            self.reward += 50
        self.reward -= 30 #nothing happening = punishment
        return self.reward

    def network(self, weights = None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim = INPUT_NUM)) #originally 11
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=5, activation='softmax')) #originally 3
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))

    def replay_new(self, memory):
        if len(memory) > 1000: #1000
            minibatch = random.sample(memory, 1000) #1000
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target =  reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1,INPUT_NUM)))[0])
        target_f = self.model.predict(state.reshape((1,INPUT_NUM)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1,INPUT_NUM)), target_f, epochs=1,verbose=0)

