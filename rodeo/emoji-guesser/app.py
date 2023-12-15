import streamlit as st
from vertexai.preview.language_models import TextGenerationModel
import json

project_id = "hackaton-2-406607"


class Movie:
    name: str
    description: str
    emojis: list


def generate_movie(temperature: float = 1) -> str:
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        "Do the following tasks in order:"
        + "1. Pick a random famous movie (other that the matrix, lord of the rings, the godfather, inception and the given examples)."
        + "2. Give me its name and description of its plot. "
        + "2. List any visuals that come to mind when thinking about this movie. "
        + "3. From the description and the visuals, create a set of 6 emojis that represent the movie. "
        + "4. Reply in a specific format at all costs. Follow the examples below."
        + "EXAMPLES OF YOUR OUTPUTS: "
        + 'Ouput Example 1: {movie_name: "Fight Club", movie_description: "An insomniac office worker looking for a way to change his life crosses paths with a devil-may-care soap maker, and they form an underground fight club that evolves into something much, much more", emojis: ["👊", "🩸", "👥", "🚬", "🧼", "💣"]}'
        + 'Ouput Example 2: {movie_name: "The Lion King", movie_description: "Simba, a young lion who is exiled from his home after his father\'s death, must learn to embrace his destiny and return to take his rightful place as king.", emojis: ["🦁", "👑", "🌳", "🎶", "❤️", "🐾"]}'
        + 'Ouput Example 3: {movie_name: "The Titanic", movie_description: "A young third-class passenger aboard the RMS Titanic falls in love with a wealthy first-class passenger. They must overcome many obstacles, including the sinking of the ship, to be together.", emojis: ["🚢", "🌊", "❤️", "💔", "💰", "🎨"]}',
        **parameters,
    )
    print(f"Response from Model: {response.text}")

    return response.text


def extract_emojis(response_text: str) -> list:
    # Find the start and end indices of the emojis list in the response
    start = response_text.find("emojis: [") + len("emojis: [")
    end = response_text.find("]}", start)

    # Extract the emojis substring
    emojis_str = response_text[start:end].strip()

    # Parse the emojis substring as a list
    # Adding braces to make it a valid JSON format
    try:
        emojis = json.loads(f"[{emojis_str}]")
    except json.JSONDecodeError:
        # Handle cases where JSON decoding fails
        print("Failed to decode emojis from response.")
        emojis = []

    return emojis


def score_user_movies_suggestions(movie_to_find: str, movies_suggestions: str) -> str:
    parameters = {
        "temperature": 0.5,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    score_movies_suggestion_template = f"Do the following tasks in order: \
    1. Taking into consideration the movie name, description and emojis of the movie to predict {movie_to_find}, give a similarity score for each movie suggested by the user based on the emoji description. \
    1.b Here are the user guesses: {movies_suggestions} \
    1.c For each movie suggested by the user, give a score between 0 and 1, where 0 means no similarity and 1 means perfect similarity. \
    1.d Transform this score into a percentage. \
    2. Reply in a specific format at all costs. Follow the examples below. \
    EXAMPLES OF YOUR OUTPUTS: \
    Example 1: \
    | Underdogs : 50% \n\
    | The Titanic: 0% \n\
    | The godfather : 100% \n\
    | Matrix: 10% \n \
    Example 2: \
    | Once Upon A Time in Hollywood : 50% \n\
    | The Lion King: 100% \n"

    model = TextGenerationModel.from_pretrained("text-bison@002")
    response = model.predict(
        score_movies_suggestion_template,
        **parameters,
    )
    print(f"Response from 2: {response.text}")

    return response.text


st.title("Guess the movie from the emojis")


answer = st.text_input(
    "Your movie suggestion",
    key="answer",
)


st.session_state["user_answer"] = answer


def handle_pick_movie():
    st.session_state.clear()
    movie_to_find = generate_movie()
    st.session_state["movie_to_find"] = movie_to_find
    print("MOVIE_TO_FIND", movie_to_find)

    emojis = extract_emojis(movie_to_find)
    print("EMOJIS", "".join(emojis))
    st.session_state["emojis"] = "".join(emojis)
    st.write(f"Enter movie name suggestions for this emovi  {''.join(emojis)}")
    if len(emojis) != 6:
        st.write("Something went wrong, please try again")
        st.stop()

    print("USER_ANSWER", answer)


st.button("Pick a movie", key="pick_movie", on_click=handle_pick_movie)


def handle_submit_answer():
    print("MOVIE_TO_FIND_HANDLE_SUBMIT_ANSWER", st.session_state["movie_to_find"])
    score = score_user_movies_suggestions(
        st.session_state["movie_to_find"], st.session_state["user_answer"]
    )
    st.write(f"Have you guessed this emovi {st.session_state['emojis']} right ?")
    st.write("Your score:")
    st.write(score)


st.button("Submit Answer", key="submit", on_click=handle_submit_answer)
