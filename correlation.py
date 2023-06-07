import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pointbiserialr

correlation_data = {}
corr_data = {}
df = {}
per_minute_stats = {    "kills", "deaths", "assists", "vision_score", "minions_killed", 
                        "experience", "gold_earned", "damage_dealt",
                        "net_kills", "net_deaths", "net_assists", "net_minions_killed", "net_vision_score",
                        "net_experience", "net_gold_earned", "net_damage_dealt"}

lanes = {   "0": "All lanes",
            "1": "Top",
            "2": "Jungle",
            "3": "Middle",
            "4": "Bottom",
            "5": "Support"}



def calculate_per_minute_stat(df, x, y):
    new_stat = x + "_per_minute"
    df[new_stat] = (df[x] / df[y]).round(2)

def calculate_corr(df, x, y):
    correlation_data[x] = np.corrcoef(df[x], df[y])[0, 1]
    
def create_box_plot(df_victories, df_losses, position, stat):
    label = lanes[str(position)] + " " + stat.replace("_", " ").replace('"', '').replace("'", "")
    label = label[0].upper() + label[1:]

    fig, axes = plt.subplots()
    axes.boxplot([df_victories[stat], df_losses[stat]], labels=['Victory', 'Defeat'])
    axes.set_xlabel('Outcomes')
    axes.set_ylabel(label)
    axes.set_title(f'{label} correlation: {correlation_data[stat]:.2f}')

    plt.show()


def main(PUUID):
    with open(f"data/{PUUID}/{PUUID}_data.json", 'r') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    for stat in per_minute_stats:
        calculate_per_minute_stat(df, stat, "game_duration")

    position = 0
    choice = input("If you want to check the stats of a single position write 'position'. If you want to want to check stats of all lanes combined, write 'stats', If you want to quit the program, type 'quit'. ")
    if choice.lower() == "position":
        choice = int(input("Type 0 for top, 1 for jungle, 2 for mid, 3 for bot/adc, 4 for support: "))
        try:
            if 0 <= choice <= 4:
                position = choice + 1
        except ValueError:
            print("Invalid input.")

    if position == 0:
        df_position = df
        df_victories = df[df['outcome'] == 1]
        df_losses = df[df['outcome'] == 0]
    else:
        conditionW = (df['position'] == position-1) & (df['outcome'] == 1)
        conditionL = (df['position'] == position-1) & (df['outcome'] == 0)
        df_position = df[df['position'] == position-1]
        df_victories = df[conditionW]
        df_losses = df[conditionL]

    for column_name in df_position.columns[1:]:
        calculate_corr(df_position, column_name, df_position.columns[0])

    corr_data = pd.DataFrame(correlation_data, index=[0])
    corr_data.transpose().to_csv("data/corr_data.csv", index=True)

    while True:
        print(df.columns[1:].tolist())
        print("If you want to quit the program, type 'quit'.")
        choice = input("Choose a category you would like to see the comparison for: ").lower()
        if choice == "quit":
            break
        else:
            create_box_plot(df_victories, df_losses, position, choice)


if __name__ == "__main__":
    main()
