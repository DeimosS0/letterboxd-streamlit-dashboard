# 🎬 Personal Movie Taste Analyzer

A Streamlit web application that analyzes your Letterboxd movie ratings and reveals your unique cinematic personality.

[![Streamlit App]

## 🌟 Features

- **Interactive Dashboard:** Analyze your movie ratings with a user-friendly interface.
- **Dynamic Filtering:** Filter your movie list by rating and genre.
- **Film Personality:** Discover your cinematic personality based on your most-watched genres.
- **Rich Visualizations:** Explore your taste through interactive pie charts and scatter plots.
- **Personal Data Upload:** Upload your own `ratings.csv` from Letterboxd to get a personalized analysis.

## 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/DeimosS0/letterboxd-streamlit-dashboard.git]
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the IMDb data:**
    * Create a folder named `imdb_data`.
    * Download the genre CSV files from [this source](https://www.kaggle.com/datasets/thedevastator/imdb-movies-from-2000-to-2022) (or a similar one) and place them inside the `imdb_data` folder.

5.  **Run the Streamlit app:**
    ```bash
    streamlit run analiz.py
    ```

## 📊 Data

-   **Personal Ratings:** Requires a `ratings.csv` file exported from your Letterboxd account.
-   **Genre Data:** Uses a collection of IMDb movie datasets by genre.
