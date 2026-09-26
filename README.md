# 🎬 IMDb Film Analysis Suite

A Streamlit-based web application for exploring and analyzing movie data. The application allows users to search for movies, compare actors, analyze directors, visualize movie trends, and predict IMDb ratings using machine learning.

---

##  Features

###  Movie Search
- Search for movies by title.
- View details such as:
  - IMDb Rating
  - Genre
  - Release Year
  - Cast
  - Director
  - Plot Summary

###  Actor Search
- Search for an actor.
- View movies featuring the selected actor.
- Explore actor filmography

###  Actor Comparison
- Compare two actors based on:
  - Number of movies
  - Average IMDb rating
  - Popular works

###  Director Search
- Search for a director.
- View movies directed by them.
- Analyze their filmography.

###  Movie Analysis
Generate visualizations including:
- IMDb Rating Distribution
- Movies Released Per Year
- Genre Distribution
- Top Rated Movies

###  IMDb Rating Predictor
Predict the IMDb rating of a movie using a machine learning model based on movie features.

---

##  Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Requests
- Kaggle Movie Dataset

---

##  Project Structure

```
IMDb-Film-Analysis-Suite/
│
├── app.py                  # Main Streamlit application
├── movie_api.py            # Movie search functionality
├── actor_search.py         # Actor search module
├── actor_comparison.py     # Compare two actors
├── director_search.py      # Director search module
├── analysis_graphs.py      # Data visualizations
├── rating_predictor.py     # IMDb rating prediction model
├── README.md
└── requirements.txt
```
##  Dataset

This project uses a movie dataset obtained from Kaggle containing information for over 10,000 movies.

Dataset includes:
- Movie Titles
- Genres
- Directors
- Actors
- IMDb Ratings
- Release Year
- Runtime
- Votes
- Revenue

