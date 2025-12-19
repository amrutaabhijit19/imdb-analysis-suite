import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Load and prepare data
# -------------------------------
def load_and_prepare_data(csv_file):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce")
    df["averageRating"] = pd.to_numeric(df["averageRating"], errors="coerce")
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")

    return df


# -------------------------------
# GRAPH 1: Movies by Runtime Category vs Rating
# -------------------------------
def plot_movies_by_runtime_category(df):
    temp = df.dropna(subset=["runtime", "averageRating"]).copy()

    bins = [0, 90, 120, 1000]
    labels = ["Short (<90 min)", "Medium (90–120 min)", "Long (>120 min)"]
    temp["runtime_category"] = pd.cut(temp["runtime"], bins=bins, labels=labels)

    movie_counts = temp["runtime_category"].value_counts().sort_index()
    avg_ratings = temp.groupby("runtime_category")["averageRating"].mean()

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.bar(movie_counts.index, movie_counts.values, alpha=0.7)
    ax1.set_ylabel("Number of Movies")

    ax2 = ax1.twinx()
    ax2.plot(avg_ratings.index, avg_ratings.values, marker="o")
    ax2.set_ylabel("Average IMDb Rating")

    ax1.set_xlabel("Runtime Category")
    plt.title("Movies by Runtime Category vs Average IMDb Rating")

    return fig


# -------------------------------
# GRAPH 2: Average Rating by Genre (Pie Chart)
# -------------------------------
def plot_avg_rating_by_genre(df):
    df = df.dropna(subset=["genres", "averageRating"]).copy()

    df["genres"] = df["genres"].str.split(",")
    genre_df = df.explode("genres")
    genre_df["genres"] = genre_df["genres"].str.strip()

    genre_rating = (
        genre_df.groupby("genres")["averageRating"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    fig, ax = plt.subplots()
    ax.pie(
        genre_rating.values,
        labels=genre_rating.index,
        autopct="%1.1f%%",
        startangle=140
    )
    ax.set_title("Top 5 Genres by Average IMDb Rating")

    return fig


# -------------------------------
# GRAPH 3: Average Budget by Genre
# -------------------------------
def plot_avg_budget_by_genre(df):
    df = df.dropna(subset=["genres", "budget"]).copy()

    df["genres"] = df["genres"].str.split(",")
    genre_df = df.explode("genres")
    genre_df["genres"] = genre_df["genres"].str.strip()

    avg_budget = (
        genre_df.groupby("genres")["budget"]
        .mean()
        .sort_values(ascending=False)
        .head(10)   # 🔹 TOP 10
    )

    # Convert to millions for readability
    avg_budget_m = avg_budget / 1_000_000

    fig, ax = plt.subplots(figsize=(10, 6))  # slightly bigger

    bars = ax.bar(
        avg_budget_m.index,
        avg_budget_m.values,
        color=plt.cm.viridis(
            avg_budget_m.values / avg_budget_m.values.max()
        )
    )

    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Budget (Million USD)")
    ax.set_title("Top 10 Genres by Average Production Budget")

    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Rotate labels for clarity
    ax.set_xticklabels(avg_budget_m.index, rotation=30, ha="right")

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.1f}M",
            ha="center",
            va="bottom",
            fontsize=9
        )

    return fig


