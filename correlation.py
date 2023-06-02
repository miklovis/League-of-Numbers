import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr

# Sample data (replace with your own data)
with open("duration.txt", 'r') as file:
    durations = json.load(file)

with open("deaths.txt", 'r') as file:
    deaths = json.load(file)

with open("outcomes.txt", 'r') as file:
    outcomes = json.load(file)

with open("kills.txt", 'r') as file:
    kills = json.load(file)

with open("assists.txt", 'r') as file:
    assists = json.load(file)

with open("creeps.txt", 'r') as file:
    creeps = json.load(file)
# Calculate correlation coefficient


kda = []
deathsPM = []
killsPM = []
assistsPM = []
creepsPM = []
for i in range(len(kills)):
    deathsPM.append(deaths[i] / durations[i])
    killsPM.append(kills[i] / durations[i])
    assistsPM.append(assists[i] / durations[i])
    creepsPM.append(creeps[i] / durations[i])
    if deaths[i] != 0:
        kda.append((kills[i] + assists[i]) / deaths[i])
    else:
        kda.append(kills[i] + assists[i])

deaths_true = [deaths[i] for i in range(len(deaths)) if outcomes[i]]
deaths_false = [deaths[i] for i in range(len(deaths)) if not outcomes[i]]

kills_true = [kills[i] for i in range(len(kills)) if outcomes[i]]
kills_false = [kills[i] for i in range(len(kills)) if not outcomes[i]]

assists_true = [assists[i] for i in range(len(assists)) if outcomes[i]]
assists_false = [assists[i] for i in range(len(assists)) if not outcomes[i]]

kda_true = [kda[i] for i in range(len(kda)) if outcomes[i]]
kda_false = [kda[i] for i in range(len(kda)) if not outcomes[i]]

deathsPM_true = [deathsPM[i] for i in range(len(deathsPM)) if outcomes[i]]
deathsPM_false = [deathsPM[i] for i in range(len(deathsPM)) if not outcomes[i]]

killsPM_true = [killsPM[i] for i in range(len(kills)) if outcomes[i]]
killsPM_false = [killsPM[i] for i in range(len(kills)) if not outcomes[i]]

assistsPM_true = [assistsPM[i] for i in range(len(assists)) if outcomes[i]]
assistsPM_false = [assistsPM[i] for i in range(len(assists)) if not outcomes[i]]

creepsPM_true = [creepsPM[i] for i in range(len(creeps)) if outcomes[i]]
creepsPM_false = [creepsPM[i] for i in range(len(creeps)) if not outcomes[i]]


correlationDeaths = np.corrcoef(deaths, outcomes)[0, 1]
correlationDeathsPM = np.corrcoef(deathsPM, outcomes)[0, 1]

correlationKills = np.corrcoef(kills, outcomes)[0, 1]
correlationKillsPM = np.corrcoef(killsPM, outcomes)[0, 1]

correlationAssists = np.corrcoef(assists, outcomes)[0, 1]
correlationAssistsPM = np.corrcoef(assistsPM, outcomes)[0, 1]

correlationCreeps = np.corrcoef(creeps, outcomes)[0, 1]
correlationCreepsPM = np.corrcoef(creepsPM, outcomes)[0, 1]

correlationKDA = np.corrcoef(kda, outcomes)[0, 1]

# Create scatter plot
fig, axes = plt.subplots(1, 5, figsize=(12, 4))

# Plot 1
axes[0].boxplot([deathsPM_true, deathsPM_false], labels=['Victory', 'Defeat'])
axes[0].set_xlabel('Outcomes')
axes[0].set_ylabel('Deaths per minute')
axes[0].set_title(f'Death per minute correlation: {correlationDeathsPM:.2f}')

# Plot 2
axes[1].boxplot([killsPM_true, killsPM_false], labels=['Victory', 'Defeat'])
axes[1].set_xlabel('Outcomes')
axes[1].set_ylabel('Kills per minute')
axes[1].set_title(f'Kill per minute correlation: {correlationKillsPM:.2f}')

# Plot 3
axes[2].boxplot([assistsPM_true, assistsPM_false], labels=['Victory', 'Defeat'])
axes[2].set_xlabel('Outcomes')
axes[2].set_ylabel('Assists per minute')
axes[2].set_title(f'Assist per minute correlation: {correlationAssistsPM:.2f}')

axes[3].boxplot([creepsPM_true, creepsPM_false], labels=['Victory', 'Defeat'])
axes[3].set_xlabel('Outcomes')
axes[3].set_ylabel('Creeps per minute')
axes[3].set_title(f'Creeps per minute correlation: {correlationCreepsPM:.2f}')

axes[4].boxplot([kda_true, kda_false], labels=['Victory', 'Defeat'])
axes[4].set_xlabel('Outcomes')
axes[4].set_ylabel('KDA')
axes[4].set_title(f'KDA correlation: {correlationKDA:.2f}')

# Adjust spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()
