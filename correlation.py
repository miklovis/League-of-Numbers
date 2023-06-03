import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pointbiserialr

correlation_data = {}
df = {}
per_minute_stats = {    "kills", "deaths", "assists", "vision_score", "minions_killed", 
                        "net_kills", "net_deaths", "net_assists", "net_minions_killed", "net_vision_score"}

def calculate_per_minute_stat(df, x, y):
    new_stat = x + "_per_minute"
    df[new_stat] = (df[x] / df[y]).round(2)

def calculate_corr(df, x, y):
    correlation_data[x] = np.corrcoef(df[x], df[y])[0, 1]
    
def create_box_plot(df_victories, df_losses, stat):
    label = stat.replace("_", " ").replace('"', '').replace("'", "")
    label = label[0].upper() + label[1:]

    fig, axes = plt.subplots()
    axes.boxplot([df_victories[stat], df_losses[stat]], labels=['Victory', 'Defeat'])
    axes.set_xlabel('Outcomes')
    axes.set_ylabel(label)
    axes.set_title(f'{label} correlation: {correlation_data[stat]:.2f}')

    plt.show()


def main():
    with open("data.json", 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    for stat in per_minute_stats:
        calculate_per_minute_stat(df, stat, "game_duration")
    df['kda'] = np.where(df['deaths'] != 0, ((df['kills'] + df['assists']) / 2).round(2), df['kills'] + df['assists'])

    df_victories = df[df['outcome'] == 1]
    df_losses = df[df['outcome'] == 0]

    for column_name in df.columns[1:]:
        calculate_corr(df, column_name, df.columns[0])

    while True:
        print(df.columns[1:].tolist())
        print("If you want to quit the program, type 'quit'.")
        choice = input("Choose a category you would like to see the comparison for: ").lower()
        if choice == "quit":
            break
        else:
            create_box_plot(df_victories, df_losses, choice)


if __name__ == "__main__":
    main()
