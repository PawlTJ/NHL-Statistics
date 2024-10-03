import pandas as pd  
import numpy as np               
import matplotlib.pyplot as plt     
import tkinter as tk                
from tkinter import ttk

gs = pd.read_csv('Goalie_stats.csv')
ss = pd.read_csv('Skater_stats.csv')
ts = pd.read_csv('Team_stats.csv')
tl = pd.read_csv('Team_List.csv')
rsr = pd.read_csv('Regular_Season_Results.csv')

LJ = ss.filter(['Player','Tm','Team','Pos','GP','G','A','PTS','+/-','PIM','PP','SOG'], axis=1)
RJ = tl.filter(['Tm','Team'], axis=1)

fy = pd.merge(LJ, RJ, on ='Tm', how ='left') 
fy['Team'] = fy['Team'].fillna('').astype(str)
teams = sorted(fy['Team'].unique())
players = sorted(fy['Player'].unique())

def Top_Players_All():
    fy50 = fy.head(50)
    plt.figure(figsize=(10, 6))
    plt.scatter(fy50['G'], fy50['A'], marker='o', color='red')
    plt.title(f'Top 50 Players')
    plt.xlabel('Goals')
    plt.ylabel('Assets')
    plt.grid(True)

    plt.show()

def Top_Players_Select():
    team_select = team_var.get()
    print(fy.loc[fy['Team'] == team_select])
    print()
    print()


def Hexagon_Graph():
    player_select = player_var.get()
    players_fy_stats = fy[fy['Player'] == player_select].filter(['G','A','PTS','+/-','PIM','PP','SOG'], axis=1)
    players_fy_name = fy[fy['Player'] == player_select].filter(['Player', 'Pos','Team'], axis=1)
    full_fy_stats = fy.filter(['G','A','PTS','+/-','PIM','PP','SOG'], axis=1)

    max_values = full_fy_stats.max()
    percent_stats = players_fy_stats / max_values

    categories = ['G', 'A', 'PTS', '+/-', 'PIM', 'PP', 'SOG']
    num_vars = len(categories)
    num_players = len(players_fy_name)

    for i in range(num_players):
        points = percent_stats.iloc[i].to_list()
        actuals = players_fy_stats.iloc[i].to_list()
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        points += points[:1]
        angles += angles[:1]
        actuals += actuals[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, points, color='lightblue', alpha=0.25)
        ax.plot(angles, points, color='blue', linewidth=2)

        plt.title(f'{players_fy_name.iloc[i]["Team"]} - {players_fy_name.iloc[i]["Player"]} - {players_fy_name.iloc[i]["Pos"]}')
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        for j in range(num_vars):
            ax.text(angles[j], points[j] - 0.1, str(actuals[j]), horizontalalignment='center', size=9, color='black', weight='semibold')

        plt.show()
        

# Create tkinker window
root = tk.Tk()
root.title("NHL Stats")
root.geometry("250x700")

plot_button_1 = tk.Button(root, text="Plot Top 50 Players", command=Top_Players_All)
plot_button_1.pack(pady=20)

team_var = tk.StringVar()
team_dropdown = ttk.Combobox(root, textvariable=team_var, values=teams)
team_dropdown.pack(pady=5)
plot_button_2 = tk.Button(root, text="Team Stats", command=Top_Players_Select)
plot_button_2.pack(pady=20)

player_var = tk.StringVar()
player_dropdown = ttk.Combobox(root, textvariable=player_var, values=players)
player_dropdown.pack(pady=5)
plot_button_3 = tk.Button(root, text="Player Graph", command=Hexagon_Graph)
plot_button_3.pack(pady=20)


plot_button_4 = tk.Button(root, text="Top Goals", command=Hexagon_Graph)
plot_button_4.pack(pady=20)

plot_button_5 = tk.Button(root, text="Top Assects", command=Hexagon_Graph)
plot_button_5.pack(pady=20)

plot_button_6 = tk.Button(root, text="Top +/-", command=Hexagon_Graph)
plot_button_6.pack(pady=20)

plot_button_7 = tk.Button(root, text=" Top PIM", command=Hexagon_Graph)
plot_button_7.pack(pady=20)

plot_button_8 = tk.Button(root, text="Top PP", command=Hexagon_Graph)
plot_button_8.pack(pady=20)

plot_button_9 = tk.Button(root, text="Top SOG", command=Hexagon_Graph)
plot_button_9.pack(pady=20)



plot_button_8 = tk.Button(root, text="Remove Player", command=Hexagon_Graph)
plot_button_8.pack(pady=20)

plot_button_9 = tk.Button(root, text="Add Player", command=Hexagon_Graph)
plot_button_9.pack(pady=20)


root.mainloop()