import streamlit as st
from vertexai.preview.language_models import TextGenerationModel


project_id = "hackaton-2-406607"


class Movie:
    name: str
    description: str


def generate_movie(temperature: float = 0.8) -> None:
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        "Give me a random famous movie with its name and description of its plot. List any visuals that come to mind when thinking about this movie. From the description and the visuals, create a set of 6 emojis that represent the movie. ",
        **parameters,
    )
    print(f"Response from Model: {response.text}")

    return response.text


def extract_emojis(movie_description) -> None:
    parameters = {
        "temperature": 0.0,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        f"Extract the emojis from the description of the movie {movie_description}",
        **parameters,
    )
    print(f"Response from Model: {response.text}")

    return response


def score_user_movies_suggestions(movie_to_find: str, movies_suggestions: str) -> str:
    parameters = {
        "temperature": 0.5,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        f"The use has to guess the movie name based on this emojie: {movie_to_find}. Here are the user guesses: {movies_suggestions}, give a similarity score for each movie based on the emoji description.",
        **parameters,
    )
    print(f"Response from 2: {response.text}")

    return response.text


st.title("Guess the movie from the emojis")

movie_to_find = "nothing"
emojis = ""
if st.button("Get Movie Title"):
    movie_to_find = generate_movie()
    emojis = extract_emojis(movie_to_find)
    print("movie_to_find", movie_to_find)

    movies_suggestions = st.text_input(
        f"Enter movie name suggestions for this emovi {emojis}"
    )

    movies_suggestions = "The matrix, Inception, The terminator, Dumbo, Men In Black"
    tata = score_user_movies_suggestions(movie_to_find, movies_suggestions)
    st.write("Your score", tata)
