import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pointbiserialr

# Sample data (replace with your own data)
with open("data.json", 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

df['creeps_per_minute'] = (df['minions_killed'] / df['game_duration']).round(2)
df['kills_per_minute'] = (df['kills'] / df['game_duration']).round(2)
df['deaths_per_minute'] = (df['deaths'] / df['game_duration']).round(2)
df['assists_per_minute'] = (df['assists'] / df['game_duration']).round(2)
df['vision_score_per_minute'] = (df['vision_score'] / df['game_duration']).round(2)
df['KDA'] = np.where(df['deaths'] != 0, ((df['kills'] + df['assists']) / 2).round(2), df['kills'] + df['assists'])

print(df)

df_victories = df[df['outcome'] == 1]
df_losses = df[df['outcome'] == 0]

print(df_victories)
print(df_losses)

# Calculate correlation coefficient
correlation_data = {}

correlation_data['kills'] = np.corrcoef(df['kills'], df['outcome'])[0, 1]
correlation_data['kills_per_minute'] = np.corrcoef(df['kills_per_minute'], df['outcome'])[0, 1]

correlation_data['deaths'] = np.corrcoef(df['deaths'], df['outcome'])[0, 1]
correlation_data['deaths_per_minute'] = np.corrcoef(df['deaths_per_minute'], df['outcome'])[0, 1]

correlation_data['assists'] = np.corrcoef(df['assists'], df['outcome'])[0, 1]
correlation_data['assists_per_minute'] = np.corrcoef(df['assists_per_minute'], df['outcome'])[0, 1]

correlation_data['creeps'] = np.corrcoef(df['minions_killed'], df['outcome'])[0, 1]
correlation_data['creeps_per_minute'] = np.corrcoef(df['creeps_per_minute'], df['outcome'])[0, 1]

correlation_data['vision_score'] = np.corrcoef(df['vision_score'], df['outcome'])[0, 1]
correlation_data['vision_score_per_minute'] = np.corrcoef(df['vision_score_per_minute'], df['outcome'])[0, 1]

correlation_data['KDA'] = np.corrcoef(df['KDA'], df['outcome'])[0, 1]

'''
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
'''


# Create scatter plot
fig, axes = plt.subplots(1, 5, figsize=(12, 4))

# Plot 1
axes[0].boxplot([df_victories['deaths_per_minute'], df_losses['deaths_per_minute']], labels=['Victory', 'Defeat'])
axes[0].set_xlabel('Outcomes')
axes[0].set_ylabel('Deaths per minute')
axes[0].set_title(f'Death per minute correlation: {correlation_data["deaths_per_minute"]:.2f}')

# Plot 2
axes[1].boxplot([df_victories['kills_per_minute'], df_losses['kills_per_minute']], labels=['Victory', 'Defeat'])
axes[1].set_xlabel('Outcomes')
axes[1].set_ylabel('Kills per minute')
axes[1].set_title(f'Kill per minute correlation: {correlation_data["kills_per_minute"]:.2f}')

# Plot 3
axes[2].boxplot([df_victories['assists_per_minute'], df_losses['assists_per_minute']], labels=['Victory', 'Defeat'])
axes[2].set_xlabel('Outcomes')
axes[2].set_ylabel('Assists per minute')
axes[2].set_title(f'Assist per minute correlation: {correlation_data["assists_per_minute"]:.2f}')

axes[3].boxplot([df_victories['creeps_per_minute'], df_losses['creeps_per_minute']], labels=['Victory', 'Defeat'])
axes[3].set_xlabel('Outcomes')
axes[3].set_ylabel('Creeps per minute')
axes[3].set_title(f'Creeps per minute correlation: {correlation_data["creeps_per_minute"]:.2f}')

axes[4].boxplot([df_victories['vision_score_per_minute'], df_losses['vision_score_per_minute']], labels=['Victory', 'Defeat'])
axes[4].set_xlabel('Outcomes')
axes[4].set_ylabel('Vision score per minute')
axes[4].set_title(f'VS per minute correlation: {correlation_data["vision_score_per_minute"]:.2f}')

# Adjust spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()
