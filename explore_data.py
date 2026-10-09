import pandas as pd

# Load the anime dataset
anime = pd.read_csv("data/anime.csv")

# Display the first five anime
print("FIRST FIVE ANIME")
print(anime.head())

# Display the number of rows and columns
print("\nDATASET SHAPE")
print(anime.shape)

# Display column names
print("\nDATASET COLUMNS")
print(anime.columns.tolist())

# Check missing values
print("\nMISSING VALUES")
print(anime.isnull().sum())

# Display basic information
print("\nDATASET INFORMATION")
anime.info()