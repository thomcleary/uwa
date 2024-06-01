from rand_agent import RandomAgent
from game import Game

agents = [
        RandomAgent(name='r1'), 
        RandomAgent(name='r2'),  
        RandomAgent(name='r3'),  
        RandomAgent(name='r4'),  
        RandomAgent(name='r5')
]

game = Game(agents)
game.play()




