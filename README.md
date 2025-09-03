# 🎬 Personal Movie Taste Analyzer

A Streamlit web application that analyzes your Letterboxd movie ratings and reveals your unique cinematic personality.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://letterboxd-replay.streamlit.app)

## 🌟 Features

- **Interactive Dashboard:** Analyze your movie ratings with a user-friendly interface.
- **Dynamic Filtering:** Filter your movie list by rating and genre.
- **Film Personality:** Discover your cinematic personality based on your most-watched genres.
- **Rich Visualizations:** Explore your taste through interactive pie charts and scatter plots.
- **Personal Data Upload:** Upload your own `ratings.csv` from Letterboxd to get a personalized analysis.

```markdown
## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    `git clone https://github.com/DeimosSO/letterboxd-streamlit-dashboard`
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd streamlit-movie-analyzer
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Download the IMDb data:**
    * Create a folder named `imdb_data`.
    * Download the genre CSV files from a source like [Kaggle](https://www.kaggle.com/datasets/rajugc/imdb-movies-dataset-based-on-genre) and place them inside the `imdb_data` folder.

6.  **Run the Streamlit app:**
    ```bash
    streamlit run analiz.py
    ```

## 📊 Data

-   **Personal Ratings:** Requires a `ratings.csv` file exported from your Letterboxd account.
-   **Genre Data:** Uses a collection of IMDb movie datasets by genre.
