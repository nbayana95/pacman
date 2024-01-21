from tkinter.filedialog import askopenfilename
import tkinter
import json
import numpy as np
import matplotlib.pyplot as plt

filename = askopenfilename()

with open(filename, 'r') as file:
    data = json.load(file)

""" Find the logs of the Strategy-AI  """
StrategyAIDict = {'StrategyAIDist': list(), 'GhostGenType': list()}
TacticalAIDict = {'TacticalAIDist': list(), 'ChaseMode': list(), 'GhostID': list()}

logAnalytics = {'StrategyAIInfo': StrategyAIDict, 'TacticalAIDict': TacticalAIDict}

# find starting distances
startingNumber = data['GhostNumber'][0]
heroLocation = (data['HeroLocation']['x'][0], data['HeroLocation']['y'][0])
for i in range(startingNumber):
    ghostLocation = (data['GhostInfo']['x'][i], data['GhostInfo']['y'][i])
    unitDist = np.array(heroLocation) - np.array(ghostLocation)
    dist = abs(unitDist[0]) + abs(unitDist[1])

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
    unitDist = np.array(heroLocation) - np.array(ghostLocation)
    dist = abs(unitDist[0]) + abs(unitDist[1])
    logAnalytics['StrategyAIInfo']['StrategyAIDist'].append(dist)
    logAnalytics['StrategyAIInfo']['GhostGenType'].append(1)


""" Find the logs of the Tactical-AI """
ChaseModeList = data['GhostInfo']['chaseMode']
dataNumber = len(data['GhostNumber'])
k=-1
for i in range(dataNumber):
    ghostNum = data['GhostNumber'][i]
    heroLocation = (data['HeroLocation']['x'][i], data['HeroLocation']['y'][i])
    for j in range(ghostNum):
        k+=1
        if ChaseModeList[k] == 1:
            ghostLocation = (data['GhostInfo']['x'][k], data['GhostInfo']['y'][k])
            unitDist = np.array(heroLocation) - np.array(ghostLocation)
            dist = abs(unitDist[0]) + abs(unitDist[1])
            logAnalytics['TacticalAIDict']['TacticalAIDist'].append(dist)
            logAnalytics['TacticalAIDict']['ChaseMode'].append(1)
            logAnalytics['TacticalAIDict']['GhostID'].append(data['GhostInfo']['id'])

#% end the process
tkinter.Tk().wm_withdraw()
tkinter.Tk().destroy()

print(logAnalytics['StrategyAIInfo'])

print("Number of Chase Mode Distance is bigger than 10: ")
print(np.sum(np.array(logAnalytics['TacticalAIDict']['TacticalAIDist'])>10))

# Creating a figure and a set of subplots
fig, axs = plt.subplots(3, 1, figsize=(6, 8))

manhattanDist = np.array(logAnalytics['TacticalAIDict']['TacticalAIDist'])
chaseMode= logAnalytics['TacticalAIDict']['ChaseMode']
ghostIDs = np.array(logAnalytics['TacticalAIDict']['GhostID'])

# Plotting each array in a separate subplot
axs[0].plot(manhattanDist)
axs[0].set_title('Manhattan Distance')
axs[1].plot(chaseMode)
axs[1].set_title('Chase Modes')
axs[2].plot(ghostIDs)
axs[2].set_title('ghost IDs')
# Adjust layout to prevent overlap
plt.tight_layout()
# Saving the figure as a PNG file
fig.savefig(filename+'_log.png')

plt.close('all')
exit()

