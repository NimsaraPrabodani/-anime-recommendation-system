
import streamlit as st

from recommender import anime, recommend_anime

# Page configuration
st.set_page_config(
    page_title="Anime Recommendation System",
    page_icon="🎌",
    layout="wide"
)

# Page styling
st.markdown("""
<style>
.stApp {
    background-color: #11111b;
    color: #f5f5f5;
}
h1, h2, h3 {
    color: #cba6f7;
}
</style>
""", unsafe_allow_html=True)

# Application heading
st.title("Anime Recommendation System")

st.write(
    "Discover your next favorite anime "
    "through intelligent recommendations."
)

st.divider()

# Anime selection
anime_titles = sorted(anime["name"].unique().tolist())

selected_anime = st.selectbox(
    "🔍 Search and select an anime",
    anime_titles,
    index=None,
    placeholder="Type an anime title..."
)

number_of_recommendations = st.slider(
    "Number of recommendations",
    min_value=5,
    max_value=10,
    value=10
)

# Generate recommendations
if selected_anime:
    st.subheader(f"Because you selected: {selected_anime}")

    selected_rows = anime[
        anime["name"] == selected_anime
    ]

    selected_genres = selected_rows.iloc[0]["genre"]

    st.write(f"**Genres:** {selected_genres}")

    recommendations = recommend_anime(
        selected_anime,
        top_n=number_of_recommendations
    )

    if recommendations:
        st.subheader("✨ Recommended Anime")

        for position, item in enumerate(recommendations, start=1):
            with st.container(border=True):
                st.markdown(
                    f"### {position}. {item['name']}"
                )
                st.write(f"**Genres:** {item['genre']}")
                st.progress(item["similarity"])
                st.caption(
                    f"Genre similarity: "
                    f"{item['similarity']:.1%}"
                )
    else:
        st.info("No recommendations found for this anime.")

else:
    st.info("Select an anime above to get recommendations.")

st.divider()

st.caption(
    "Recommendations are based on genre similarity. "
    "Similarity scores are not predicted user ratings."
)