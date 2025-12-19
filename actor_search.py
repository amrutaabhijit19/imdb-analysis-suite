import pandas as pd

def get_top_movies_by_actor(df, actor_name):
    actor_df = df[
        df["cast"].str.contains(actor_name, case=False, na=False)
    ]

    if actor_df.empty:
        return None

    top_movies = (
        actor_df
        .sort_values(by="averageRating", ascending=False)
        .head(5)
    )

    return top_movies[["title", "genres", "averageRating"]]
