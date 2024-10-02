import pandas as pd                 
import matplotlib.pyplot as plt     
import tkinter as tk                
from tkinter import ttk

gs = pd.read_csv('Goalie_stats.csv')
ss = pd.read_csv('Skater_stats.csv')
ts = pd.read_csv('Team_stats.csv')
tl = pd.read_csv('Team_List.csv')
rsr = pd.read_csv('Regular_Season_Results.csv')

teams = sorted(tl['Team'].unique())

# Create tkinker window
root = tk.Tk()
root.title("NHL Stats")
root.geometry("400x400")

plot_button = tk.Button(root, text="Plot")
plot_button.pack(pady=20)
plot_button = tk.Button(root, text="Plot")
plot_button.pack(pady=20)
plot_button = tk.Button(root, text="Plot")
plot_button.pack(pady=20)





def stat():
    # Create Labels
    team_1_label = tk.Label(root, text="Select First Team:")
    team_1_label.pack(pady=5)

    team_1_var = tk.StringVar()
    team_1_dropdown = ttk.Combobox(root, textvariable=team_1_var, values=teams)
    team_1_dropdown.pack(pady=5)

    team_2_label = tk.Label(root, text="Select Second Team:")
    team_2_label.pack(pady=5)

    team_2_var = tk.StringVar()
    team_2_dropdown = ttk.Combobox(root, textvariable=team_2_var, values=teams)
    team_2_dropdown.pack(pady=5)

root.mainloop()