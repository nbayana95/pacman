from tkinter.filedialog import askopenfilename
import tkinter
import json
import numpy as np

filename = askopenfilename()

with open(filename, 'r') as file:
    data = json.load(file)

""" Find the logs of the Strategy-AI  """
StrategyAIDict = {'StrategyAIDist': list(), 'GhostGenType': list()}
logAnalytics = {'StrategyAIInfo': StrategyAIDict}

# find starting distances
startingNumber = data['GhostNumber'][0]
heroLocation = (data['HeroLocation']['x'][0], data['HeroLocation']['y'][0])
for i in range(startingNumber):
    ghostLocation = (data['GhostInfo']['x'][i], data['GhostInfo']['y'][i])
    dist = np.linalg.norm(np.array(heroLocation) - np.array(ghostLocation))
    logAnalytics['StrategyAIInfo']['StrategyAIDist'].append(dist)
    logAnalytics['StrategyAIInfo']['GhostGenType'].append(0)
# Calculating the difference between elements respectively
ghostDiffArray = np.array(data['GhostNumber'])
differenceArray = [ghostDiffArray[i+1] - ghostDiffArray[i] for i in range(len(ghostDiffArray) - 1)]
# Finding the index of elements that are 1
indexes = [i for i, x in enumerate(differenceArray) if x == 1]
# find ghost generation distances
for i in range(len(indexes)):
    selectedIndex = indexes[i]+1 #add 1 as starting point index
    heroLocation = (data['HeroLocation']['x'][selectedIndex], data['HeroLocation']['y'][selectedIndex])
    ghostLocation = (data['GhostInfo']['x'][selectedIndex], data['GhostInfo']['y'][selectedIndex])
    dist = np.linalg.norm(np.array(heroLocation) - np.array(ghostLocation))
    logAnalytics['StrategyAIInfo']['StrategyAIDist'].append(dist)
    logAnalytics['StrategyAIInfo']['GhostGenType'].append(1)


#% end the process
tkinter.Tk().wm_withdraw()

print(logAnalytics['StrategyAIInfo'])

