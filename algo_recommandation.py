import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

excel_file = "final_steam_games_updated.xlsx"
df = pd.read_excel(excel_file)

while True:
    user_game1_name = input("Entrez le nom du premier jeu : ")
    user_game2_name = input("Entrez le nom du deuxième jeu : ")
    
    if user_game1_name in df["Game_Name"].values and user_game2_name in df["Game_Name"].values:
        break
    else:
        print("L'un des jeux n'existe pas dans la base de données. Veuillez réessayer.")

user_game1 = df[df["Game_Name"] == user_game1_name].iloc[0]
user_game2 = df[df["Game_Name"] == user_game2_name].iloc[0]

def calculate_similarity(game1, game2):
    tags1 = game1["Tags"]
    categories1 = game1["Categories"]
    tags2 = game2["Tags"]
    categories2 = game2["Categories"]
    if pd.notna(tags1) and pd.notna(categories1) and pd.notna(tags2) and pd.notna(categories2):
        all_tags = set(tags1.split(", ") + tags2.split(", "))
        all_categories = set(categories1.split(", ") + categories2.split(", "))
        game1_vector = [1 if tag in tags1 else 0 for tag in all_tags] + \
                       [1 if category in categories1 else 0 for category in all_categories]
    
        game2_vector = [1 if tag in tags2 else 0 for tag in all_tags] + \
                       [1 if category in categories2 else 0 for category in all_categories]
        return cosine_similarity([game1_vector, game2_vector])[0][1]
    else:
        return 0.0
similarities = []
for index, row in df.iterrows():
    if row["Game_Name"] != user_game1_name and row["Game_Name"] != user_game2_name:
        similarity1 = calculate_similarity(user_game1, row)
        similarity2 = calculate_similarity(user_game2, row)
        average_similarity = (similarity1 + similarity2) / 2
        similarities.append((row["Game_Name"], average_similarity))

sorted_games = sorted(similarities, key=lambda x: x[1], reverse=True)
recommended_games = [game[0] for game in sorted_games[:3]]

print("Jeux recommandés:", recommended_games)
