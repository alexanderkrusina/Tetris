from Tetris import Game
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

#%% Playing the game in console
#width = 10
#height = 20
#score = 0
#print("Starting game!")
#game = Game(width,height,display=True)
#while not game.gameOver:
#    bestAction = 0
#    bestReward = -1000000
#    for i in range(4*width):
#        test = copy.deepcopy(game)
#        test.showGame = False
#        test.makeMove(i)
#        if test.reward > bestReward:
#            bestReward = test.reward
#            bestAction= i
#    game.makeMove(bestAction)
#print("Game over! Final score:", game.score)

#%% Animating the game
width = 10
height = 20
fig, ax = plt.subplots()
boards = []
lines = []
# Creating colormap
colors = [(255, 255, 255), (93, 245, 230), (0, 0, 155), (255, 165, 0), (255, 255, 30), (0, 200, 0), (222, 34, 34), (138, 43, 226)]
for i,color in enumerate(colors):
    colors[i] = (color[0]/255, color[1]/255, color[2]/255)
cm = LinearSegmentedColormap.from_list('tetrisColormap', colors, N=8)

# Initializing board and label
im = ax.imshow(np.zeros([height,width]), vmin=0, vmax=7, cmap=cm)
label = ax.text(0,0.5, "Lines Cleared: 0", bbox={'facecolor':'w', 'alpha':0.75, 'pad':1, 'edgecolor':'white'})
# Removing axis labels
plt.xticks([])
plt.yticks([])
# Playing game and copying each state to display
game = Game(width,height,display=False)
while not game.gameOver:
    bestAction = 0
    bestReward = -1000000
    for i in range(4*width):
        test = copy.deepcopy(game)
        test.showGame = False
        test.makeMove(i)
        if test.reward > bestReward:
            bestReward = test.reward
            bestAction= i
    game.makeMove(bestAction)
    boards.append(copy.deepcopy(game.board))
    lines.append( game.totalLines)
boards.append(copy.deepcopy(game.board))
lines.append(game.totalLines)

# Function to animate
def animate(i):
    im.set_data(boards[i])
    label.set_text("Lines Cleared: " + str(lines[i]))
    return im,label

# Animating
numFrames = len(boards)
ani = animation.FuncAnimation(fig, func=animate, frames=numFrames, interval=100, blit=True, repeat=False,)
plt.show(block=False)

#%% To save the animation as a video file
#FFwriter = animation.FFMpegWriter(fps=10, extra_args=['-vcodec', 'libx264'])
#ani.save('Tetris.mp4', writer = FFwriter)
