import pandas as pd

def get_top_movies_by_director(df, director_name):
    director_df = df[
        df["directors"].str.contains(director_name, case=False, na=False)
    ]

    if director_df.empty:
        return None

    top_movies = (
        director_df
        .sort_values(by="averageRating", ascending=False)
        .head(5)
    )

    return top_movies[["title", "genres", "averageRating"]]
