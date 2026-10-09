from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

# Load the anime dataset
anime = pd.read_csv("data/anime.csv")

# Keep the columns we need
anime = anime[["name", "genre"]].copy()

# Remove rows with missing titles or genres
anime = anime.dropna(subset=["name", "genre"])

# Remove duplicate anime titles
anime = anime.drop_duplicates(subset=["name"])

# Reset row indexes
anime = anime.reset_index(drop=True)

print(anime.head())

print("\nTotal anime available:", len(anime))

# Convert genres into numerical vectors
vectorizer = CountVectorizer(
    token_pattern=r"(?u)\b[\w-]+\b"
)

genre_matrix = vectorizer.fit_transform(anime["genre"])

print("\nGenre matrix shape:")
print(genre_matrix.shape)

# Calculate similarity between anime
similarity_matrix = cosine_similarity(genre_matrix)

print("\nSimilarity matrix shape:")
print(similarity_matrix.shape)

def recommend_anime(anime_name, top_n=10):

    # Find the selected anime
    matches = anime.index[
        anime["name"].str.casefold() == anime_name.casefold()
    ].tolist()

    # Check whether the anime exists
    if not matches:
        print(f"Anime '{anime_name}' was not found.")
        return

    # Get the index of the selected anime
    anime_index = matches[0]

    # Get similarity scores for the selected anime
    similarity_scores = list(
        enumerate(similarity_matrix[anime_index])
    )

    # Sort from highest similarity to lowest
    similarity_scores.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # Remove the selected anime itself
    similarity_scores = [
        item for item in similarity_scores
        if item[0] != anime_index
    ]

    # Select the top recommendations
    top_recommendations = similarity_scores[:top_n]

    # Display the results
    print(f"\nAnime similar to {anime_name}:\n")

    for index, score in top_recommendations:
        title = anime.iloc[index]["name"]

        print(f"{title} | Similarity: {score:.2f}")


def recommend_anime(anime_name, top_n=10):
    # Find the selected anime
    matches = anime.index[
        anime["name"].str.casefold() == anime_name.casefold()
    ].tolist()

    if not matches:
        return []

    anime_index = matches[0]

    # Get similarity scores
    scores = list(enumerate(similarity_matrix[anime_index]))

    # Sort from highest to lowest
    scores.sort(key=lambda item: item[1], reverse=True)

    # Exclude the selected anime itself
    scores = [
        item for item in scores
        if item[0] != anime_index
    ]

    # Return the top recommendations
    results = []

    for index, score in scores[:top_n]:
        results.append({
            "name": anime.iloc[index]["name"],
            "genre": anime.iloc[index]["genre"],
            "similarity": float(score)
        })

    return results


if __name__ == "__main__":
    recommendations = recommend_anime("Attack on Titan")

    for item in recommendations:
        print(
            f"{item['name']} | "
            f"Similarity: {item['similarity']:.2f}"
        )
