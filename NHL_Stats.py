import pandas as pd  
import numpy as np               
import matplotlib.pyplot as plt     
import os
import tkinter as tk                
from tkinter import ttk

gs = pd.read_csv('Goalie_stats.csv')
ss = pd.read_csv('Skater_stats.csv')
ts = pd.read_csv('Team_stats.csv')
tl = pd.read_csv('Team_List.csv')
rsr = pd.read_csv('Regular_Season_Results.csv')

remove_player_file = 'Removed_Players.csv'

LJ = ss.filter(['Player','Tm','Team','Pos','GP','G','A','PTS','+/-','PIM','PP','SOG'], axis=1)
RJ = tl.filter(['Tm','Team'], axis=1)

fy = pd.merge(LJ, RJ, on ='Tm', how ='left') 
fy['Team'] = fy['Team'].fillna('').astype(str)
teams = sorted(fy['Team'].unique())
players = sorted(fy['Player'].unique())
poss = sorted(fy['Pos'].unique())

if os.path.exists(remove_player_file):
    removed_players_df = pd.read_csv(remove_player_file, header=None, names=['player_removed'])
    removed_players = removed_players_df['player_removed'].tolist()
    
    fy = fy[~fy['Player'].isin(removed_players)]

def Top_Players_All():
    fy50 = fy.head(50)
    plt.figure(figsize=(10, 6))
    plt.scatter(fy50['G'], fy50['A'], marker='o', color='red')
    plt.title(f'Top 50 Players')
    plt.xlabel('Goals')
    plt.ylabel('Assets')
    plt.grid(True)
    plt.show()

def remove_player():
    player_to_remove = player_var.get()
    global fy
    if player_to_remove in fy['Player'].values:
        fy = fy[fy['Player'] != player_to_remove]
        removed_player_df = pd.DataFrame({'player_removed': [player_to_remove]})
        removed_player_df.to_csv(remove_player_file, mode='a', header=False, index=False)
        print()
        print(f"Player '{player_to_remove}' is now removed!")
        print()

    else:
        print()
        print(f"Player '{player_to_remove}' not found!")
        print()

def Team_Fillter(df):
    team_select = team_var.get()
    if(team_select):
        df_by_team = df.loc[df['Team'] == team_select]
    else:
        df_by_team = df
    return df_by_team

def Pos_Fillter(df):
    pos_select = pos_var.get()
    if(pos_select):
        df_by_team = df.loc[df['Pos'] == pos_select]
    else:
        df_by_team = df
    return df_by_team

def Top_Goals():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['G'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_Assists():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['A'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_Points():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['PTS'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_PlusMinu():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['+/-'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_PIM():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['PIM'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_PP():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['PP'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()

def Top_SOG():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)
    print_data = new_fy.sort_values(by=['SOG'], ascending=False)
    print()
    print(print_data.head(15))
    print()
    print()


def Hexagon_Graph():
    player_select = player_var.get()
    if player_select in fy['Player'].values:
        players_fy_stats = fy[fy['Player'] == player_select].filter(['G','A','PTS','+/-','PIM','PP','SOG'], axis=1)
        players_fy_name = fy[fy['Player'] == player_select].filter(['Player', 'Pos','Team'], axis=1)
        full_fy_stats = fy.filter(['G','A','PTS','+/-','PIM','PP','SOG'], axis=1)

        max_values = full_fy_stats.max()
        percent_stats = players_fy_stats / max_values

        categories = ['G', 'A', 'PTS', '+/-', 'PIM', 'PP', 'SOG']
        num_vars = len(categories)
        
        points = percent_stats.iloc[0].to_list()
        actuals = players_fy_stats.iloc[0].to_list()
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        points += points[:1]
        angles += angles[:1]
        actuals += actuals[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, points, color='lightblue', alpha=0.25)
        ax.plot(angles, points, color='blue', linewidth=2)

        plt.title(f'{players_fy_name.iloc[0]["Team"]} - {players_fy_name.iloc[0]["Player"]} - {players_fy_name.iloc[0]["Pos"]}')
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        for j in range(num_vars):
            ax.text(angles[j], points[j] - 0.1, str(actuals[j]), horizontalalignment='center', size=9, color='black', weight='semibold')

        plt.show()
    else:
        print(f"Player '{player_select}' not found!")
        
def update_combobox(*args):
    typed = player_var.get()
    if typed == "":
        player_dropdown['values'] = players
    else:
        filtered_players = [player for player in players if typed.lower() in player.lower()]
        player_dropdown['values'] = filtered_players

def super_rank():
    team_fy = Team_Fillter(fy)
    new_fy = Pos_Fillter(team_fy)

    sorted_data = new_fy.sort_values(by=['G'], ascending=False).reset_index(drop=True)
    sorted_data['G R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['A'], ascending=False).reset_index(drop=True)
    sorted_data['A R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['PTS'], ascending=False).reset_index(drop=True)
    sorted_data['PTS R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['+/-'], ascending=False).reset_index(drop=True)
    sorted_data['+/- R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['PIM'], ascending=False).reset_index(drop=True)
    sorted_data['PIM R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['PP'], ascending=False).reset_index(drop=True)
    sorted_data['PP R'] = sorted_data.index + 1
    sorted_data = sorted_data.sort_values(by=['SOG'], ascending=False).reset_index(drop=True)
    sorted_data['SOG R'] = sorted_data.index + 1
    sorted_data['Power R'] = (sorted_data['G R'] + sorted_data['A R'] + sorted_data['PTS R'] + sorted_data['+/- R'] + sorted_data['PIM R'] + sorted_data['PP R'] + sorted_data['SOG R']) / 7

    sorted_data = sorted_data.sort_values(by=['Power R'], ascending=True).reset_index(drop=True)
    
    print()
    print(sorted_data.head(15))
    print()

# Create tkinker window
root = tk.Tk()
root.title("NHL Stats")
root.geometry("250x700")

plot_button_1 = tk.Button(root, text="Plot Top 50 Players", command=Top_Players_All)
plot_button_1.pack(pady=10)

team_var = tk.StringVar()
team_dropdown = ttk.Combobox(root, textvariable=team_var, values=teams)
team_dropdown.pack(pady=5)
pos_var = tk.StringVar()
pos_dropdown = ttk.Combobox(root, textvariable=pos_var, values=poss)
pos_dropdown.pack(pady=5)

player_var = tk.StringVar()
player_dropdown = ttk.Combobox(root, textvariable=player_var, values=players)
player_dropdown.pack(pady=5)
plot_button_3 = tk.Button(root, text="Player Graph", command=Hexagon_Graph)
plot_button_3.pack(pady=10)

plot_button_4 = tk.Button(root, text="Top Goals", command=Top_Goals)
plot_button_4.pack(pady=10)
plot_button_5 = tk.Button(root, text="Top Assists", command=Top_Assists)
plot_button_5.pack(pady=10)
plot_button_6 = tk.Button(root, text="Top Points", command=Top_Points)
plot_button_6.pack(pady=10)
plot_button_7 = tk.Button(root, text="Top +/-", command=Top_PlusMinu)
plot_button_7.pack(pady=10)
plot_button_8 = tk.Button(root, text=" Top PIM", command=Top_PIM)
plot_button_8.pack(pady=10)
plot_button_9 = tk.Button(root, text="Top PP", command=Top_PP)
plot_button_9.pack(pady=10)
plot_button_10 = tk.Button(root, text="Top SOG", command=Top_SOG)
plot_button_10.pack(pady=10)

plot_button_8 = tk.Button(root, text="Remove Player", command=remove_player)
plot_button_8.pack(pady=30)
plot_button_9 = tk.Button(root, text="Super Rank", command=super_rank)
plot_button_9.pack(pady=0)

player_var.trace('w', update_combobox)

root.mainloop()