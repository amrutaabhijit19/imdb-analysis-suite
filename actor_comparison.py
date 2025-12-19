import pandas as pd

def compare_two_actors(df, actor1, actor2):
    results = {}

    for actor in [actor1, actor2]:
        actor_df = df[
            df["cast"].str.contains(actor, case=False, na=False)
        ]

        if actor_df.empty:
            results[actor] = None
        else:
            results[actor] = actor_df["averageRating"].mean()

    return results

