import os
import pandas as pd
import streamlit as st
import plotly_express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Letterboxd Replay",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------------------------------------
# DATA LOADING AND CLEANING FUNCTION
@st.cache_data
def load_and_clean_data(uploaded_ratings_file):
    try:
        #Load user's ratings data
        if uploaded_ratings_file is not None:
            ratings_df = pd.read_csv(uploaded_ratings_file)
        else:
            ratings_df = pd.read_csv('ratings.csv')
        
        #Load and combine the IMDb genre data
        genre_folder = 'imdb_data'
        if not os.path.exists(genre_folder):
             st.error(f"Error: The '{genre_folder}' directory was not found. Please make sure it exists and contains the genre CSV files.")
             st.stop()

        all_genre_files = [f for f in os.listdir(genre_folder) if f.endswith('.csv')]
        imdb_df_list = []
        for file in all_genre_files:
            try:
                temp_df = pd.read_csv(os.path.join(genre_folder, file))
                imdb_df_list.append(temp_df)
            except Exception:
                pass 

        imdb_df = pd.concat(imdb_df_list, ignore_index=True)
        
        #Clean and prepare data for merging
        imdb_df['year'] = pd.to_numeric(imdb_df['year'], errors='coerce')
        ratings_df['Year'] = pd.to_numeric(ratings_df['Year'], errors='coerce')
        imdb_df.dropna(subset=['year'], inplace=True)
        ratings_df.dropna(subset=['Year'], inplace=True)

        # Strip whitespace and ensure correct data types for merging keys
        imdb_df['movie_name'] = imdb_df['movie_name'].str.strip().astype(str)
        ratings_df['Name'] = ratings_df['Name'].str.strip().astype(str)
        imdb_df['year'] = imdb_df['year'].astype(int)
        ratings_df['Year'] = ratings_df['Year'].astype(int)

        #Consolidate genres for each movie
        imdb_df_cleaned = imdb_df.groupby(['movie_name', 'year'])['genre'].apply(lambda x: ', '.join(x.unique())).reset_index()
        
        #Merge the two dataframes
        ratings_df.rename(columns={'Name': 'movie_name', 'Year': 'year'}, inplace=True)
        merged_df = pd.merge(ratings_df, imdb_df_cleaned, on=['movie_name', 'year'], how='inner')
        
        #Rename columns for better readability
        merged_df.rename(columns={'movie_name': 'Name', 'year': 'Year', 'genre': 'Genre'}, inplace=True)
        
        return merged_df
        
    except FileNotFoundError:
        # This will trigger if no file is uploaded AND the local 'ratings.csv' is missing.
        st.error("Could not find 'ratings.csv'. Please upload your Letterboxd ratings file to begin.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred during data loading: {e}")
        st.stop()

# --------------------------------------------------------------------------------
# SIDEBAR AND FILTERS

st.sidebar.header("🎬 Your Film Analyzer")
st.sidebar.write("""
This app analyzes your Letterboxd ratings to reveal your unique movie taste. 
Upload your `ratings.csv` file to get started!
""")

# Add the file uploader to the sidebar
uploaded_file = st.sidebar.file_uploader("Upload your ratings.csv file from Letterboxd", type="csv")

# Load the data using the uploader's state
df_original = load_and_clean_data(uploaded_file)

# --- Check if the merge was successful ---
if df_original.empty:
    st.warning("No movie matches were found between your ratings and the IMDb database. This could be due to differences in titles or release years.")
    st.stop()

# --- Continue with filters only if data is loaded and merged ---
st.sidebar.header("🔍 Filters")

rating_slider = st.sidebar.slider(
    'Filter by Rating:',
    min_value=0.5, max_value=5.0,
    value=(0.5, 5.0),
    step=0.5
)

genres_list = df_original['Genre'].str.split(', ').explode().unique()
genre_filter = st.sidebar.multiselect(
    'Filter by Genre:',
    options=genres_list,
    default=None
)

df_filtered = df_original[
    (df_original['Rating'] >= rating_slider[0]) &
    (df_original['Rating'] <= rating_slider[1])
]

if genre_filter:
    df_filtered = df_filtered[df_filtered['Genre'].apply(lambda x: any(g in x for g in genre_filter))]

if df_filtered.empty:
    st.warning("No movies found for the selected filters.")
    st.stop()

# --------------------------------------------------------------------------------
# MAIN APPLICATION BODY

st.title('🎬 Letterboxd Replay')
st.markdown(f"Exploring the cinematic taste of **{len(df_original)}** rated movies.")


# --- METRICS ---
st.header('Overall Stats')
col1, col2, col3 = st.columns(3)
col1.metric("Movies Analyzed (after filters)", len(df_filtered))
col2.metric("Average Rating", f"{df_filtered['Rating'].mean():.2f} ⭐")
col3.metric("Most Watched Year", int(df_filtered['Year'].mode()[0]))


# --- FILM PERSONALITY ANALYSIS ---
st.header('✨ Your Film Personality')

top_genre = df_filtered['Genre'].str.split(', ').explode().mode()[0]

personality_map = {
    "Action": "you are an **Action Enthusiast** who loves adrenaline and excitement! 💥",
    "Adventure": "you are an **Adventurer** who loves to explore new worlds! 🗺️",
    "Comedy": "you are a **Comedy Connoisseur** with a great sense of humor! 😂",
    "Drama": "you are a **Drama Guru** who appreciates the depth of human stories! 🎭",
    "Sci-fi": "you are a **Sci-Fi Visionary** with a big imagination for the future! 🚀",
    "Horror": "you are a **Thrill Seeker** who enjoys the suspense and scares! 👻",
    "Thriller": "you are a **Mystery Solver** who loves clever plots and tension! 🕵️",
    "Romance": "you are a **Romantic** at heart who enjoys emotional stories! ❤️",
    "Animation": "you are an **Animation Aficionado** with a creative soul! 🎨",
    "Fantasy": "you are a **Fantasy Wanderer** who believes in magical worlds! 🧙"
}

st.success(f"Your most-watched genre is **{top_genre}**. It looks like {personality_map.get(top_genre, 'you have a unique and diverse taste in film!')}")


# --- VISUALIZATIONS ---
st.header('Visual Analysis')
col1_viz, col2_viz = st.columns(2)

with col1_viz:
    st.subheader("Genre Distribution")
    genre_counts = df_filtered['Genre'].str.split(', ').explode().value_counts()
    fig_pie = px.pie(values=genre_counts.values, names=genre_counts.index, title="Your Genre Pie Chart")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2_viz:
    st.subheader("Ratings vs. Release Year")
    fig_scatter = px.scatter(df_filtered, x='Year', y='Rating', hover_data=['Name'], title="Your Ratings by Movie Release Year")
    st.plotly_chart(fig_scatter, use_container_width=True)


# --- RAW DATA ---
st.header("Filtered Data Set")
st.dataframe(df_filtered)
# --------------------------------------------------------------------------------