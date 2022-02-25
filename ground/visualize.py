import matplotlib.pyplot as plt 
import time
from random import randint

# x axis values 
x = [] 
# corresponding y axis values 
y = []
    
fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')
axs[0].plot(x, y)

# plotting the points  
axs[0].plot(x, y) 
    
# naming the x axis 
"""axs[0].xlabel('x - axis') 
# naming the y axis 
axs[0].ylabel('y - axis') """
"""
# giving a title to my graph 
axs[0].title('My first graph!') """
    

t = 0
ly = 5

lastTime = time.time()

while True:
    if (time.time() - lastTime >= 1):
        x.append(t)
        ly += randint(-5,5)
        y.append(ly)
        plt.plot(x, y) 
        plt.draw()
        plt.pause(0.01)
        
        t += 1
        print(t)
        lastTime = time.time()