from env import Screen
from random import randint
import time

width, height = 848, 480

s = Screen(width, height)

for i in range(200):
    s.reset()
    tot_rew=0   
    for _ in range(150):
        a = [randint(0,1), randint(0,1)]
        state, reward, done = s.step(a)
        tot_rew+=reward
        if done:
            break
    
    print(f"Episode {i+1}: {done} | Reward: {tot_rew}")

