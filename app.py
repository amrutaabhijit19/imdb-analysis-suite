import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# ===================== IMPORT MODULES =====================

# Module 1
from movie_api import get_movie_details

# Module 2
from analysis_graphs import (
    load_and_prepare_data,
    plot_movies_by_runtime_category,
    plot_avg_rating_by_genre,
    plot_avg_budget_by_genre
)



# Module 3
from actor_search import get_top_movies_by_actor
from director_search import get_top_movies_by_director
from actor_comparison import compare_two_actors

# Module 4
from rating_predictor import train_model, predict_rating


# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="IMDb Film Analysis Suite 🎬",
    layout="wide"
)

# ===================== LOAD DATA =====================
df = load_and_prepare_data("clean_movies_dataset.csv")

# ===================== SIDEBAR =====================
st.sidebar.title("🎥 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "🔍 Search movies",
        "📊 graphical analysis",
        "🎭 director and actor analysis",
        "🤖 Predict the rate of a movie"
    ]
)

# ===================== HOME PAGE =====================
if page == "🏠 Home":
    st.markdown(
        "<h1 style='text-align:center;'>🎬 IMDb Film Analysis Suite</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='text-align:center;'>A Modular Movie Data Analysis & ML Project 🍿</h4>",
        unsafe_allow_html=True
    )

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Module 1: Movie Search (API)")
        st.write("• Search any movie using live OMDb API")
        st.write("• View rating, genre, cast and plot")

        st.subheader("📊 Module 2: Graphical Analysis")
        st.write("• Runtime category vs average IMDb rating")
        st.write("• Genre-wise average IMDb rating")
        st.write("• Average budget comparison across genres")

    with col2:
        st.subheader("🎭 Module 3: Actor & Director Tools")
        st.write("• Actor search → top movies")
        st.write("• Director search → top movies")
        st.write("• Actor vs Actor comparison")

        st.subheader("🤖 Module 4: Machine Learning")
        st.write("• IMDb rating prediction")
        st.write("• Uses budget, runtime & genre")
        st.write("• Simple, explainable ML model")

# ===================== MODULE 1 =====================
elif page == "🔍 Search movies":
    st.header("🔍 Module 1: Movie Search (API) 🎞️")

    movie = st.text_input("🎬 Enter Movie Name")
    api_key = st.text_input("🔑 Enter OMDb API Key", type="password")

    if st.button("🔍 Search Movie"):
        if movie and api_key:
            data = get_movie_details(movie, api_key)

            if data is None:
                st.error("❌ Movie not found")
            else:
                st.success("🎉 Movie Found!")
                for key, value in data.items():
                    st.write(f"**{key}:** {value}")
        else:
            st.warning("⚠️ Please enter both movie name and API key")

# ===================== MODULE 2 =====================
elif page == "📊 graphical analysis":
    st.header("📊 Module 2: Graphical Analysis 📈")

    tab1, tab2, tab3 = st.tabs(
        [
            "⏱ Runtime vs Rating",
            "⭐ Genre vs Rating",
            "💰 Budget by Genre"
        ]
    )

    with tab1:
        st.pyplot(plot_movies_by_runtime_category(df))


    with tab2:
        st.pyplot(plot_avg_rating_by_genre(df))


    with tab3:
        st.pyplot(plot_avg_budget_by_genre(df))



# ===================== MODULE 3 =====================
elif page == "🎭 director and actor analysis":
    st.header("🎭 Module 3: Director & Actor Analysis 🎬")

    tab1, tab2, tab3 = st.tabs(
        ["🎬 Director Search", "🎭 Actor Search", "🆚 Actor vs Actor"]
    )

    # ---- Director Search ----
    with tab1:
        director = st.text_input("🎬 Enter Director Name")

        if st.button("🎥 Show Director Movies"):
            if director:
                result = get_top_movies_by_director(df, director)
                if result is None:
                    st.warning("No movies found for this director.")
                else:
                    st.dataframe(result.reset_index(drop=True))
            else:
                st.warning("Please enter a director name.")

    # ---- Actor Search ----
    with tab2:
        actor = st.text_input("🎭 Enter Actor Name")

        if st.button("🎬 Show Actor Movies"):
            if actor:
                result = get_top_movies_by_actor(df, actor)
                if result is None:
                    st.warning("No movies found for this actor.")
                else:
                    st.dataframe(result.reset_index(drop=True))
            else:
                st.warning("Please enter an actor name.")

    # ---- Actor vs Actor ----
    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            actor1 = st.text_input("🎭 Actor 1")

        with col2:
            actor2 = st.text_input("🎭 Actor 2")

        if st.button("🆚 Compare Actors"):
            if actor1 and actor2:
                result = compare_two_actors(df, actor1, actor2)

                names, ratings, table = [], [], []

                for actor, rating in result.items():
                    if rating:
                        names.append(actor)
                        ratings.append(round(rating, 2))
                        table.append({"Actor": actor, "Average Rating": round(rating, 2)})
                    else:
                        table.append({"Actor": actor, "Average Rating": "No data"})

                st.table(pd.DataFrame(table))

                if len(ratings) == 2:
                    fig, ax = plt.subplots()
                    ax.bar(names, ratings)
                    ax.set_ylim(0, 10)
                    ax.set_ylabel("IMDb Rating")
                    ax.set_title("Actor Rating Comparison")
                    st.pyplot(fig)
            else:
                st.warning("Please enter both actor names.")

# ===================== MODULE 4 =====================
elif page == "🤖 Predict the rate of a movie":
    st.header("🤖 Module 4: IMDb Rating Predictor 🎯")

    model, genre_cols = train_model(df)

    budget = st.number_input("💰 Enter Budget", min_value=0.0, step=1_000_000.0)
    runtime = st.number_input("⏱️ Enter Runtime (minutes)", min_value=1.0, step=10.0)

    genres = [g.replace("genre_", "") for g in genre_cols]
    genre = st.selectbox("🎭 Select Primary Genre", genres)

    if st.button("⭐ Predict Rating"):
        rating = predict_rating(model, genre_cols, budget, runtime, genre)
        st.success(f"🎉 Predicted IMDb Rating: {rating}")
