import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def prepare_ml_data(df):
    df = df.dropna(subset=["budget", "runtime", "genres", "averageRating"])

    # Take first genre only
    df["primary_genre"] = df["genres"].apply(lambda x: x.split(",")[0].strip())

    # One-hot encode genre
    genre_dummies = pd.get_dummies(df["primary_genre"], prefix="genre")

    X = pd.concat(
        [df[["budget", "runtime"]], genre_dummies],
        axis=1
    )

    y = df["averageRating"]

    return X, y, genre_dummies.columns


def train_model(df):
    X, y, genre_columns = prepare_ml_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, genre_columns


def predict_rating(model, genre_columns, budget, runtime, genre):
    # Create empty input row
    input_data = pd.DataFrame(
        [[budget, runtime] + [0]*len(genre_columns)],
        columns=["budget", "runtime"] + list(genre_columns)
    )

    genre_col = f"genre_{genre}"
    if genre_col in input_data.columns:
        input_data[genre_col] = 1

    prediction = model.predict(input_data)
    return round(float(prediction[0]), 2)
