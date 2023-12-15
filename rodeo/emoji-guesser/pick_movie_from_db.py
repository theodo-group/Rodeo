import streamlit as st
import requests
import random


project_id = "hackaton-2-406607"


response = requests.get("http://www.omdbapi.com/?s=movie&apikey=26eeaa6d")
movies = response.json()["Search"]

print("Movies:", movies)


class Movie:
    name: str
    description: str


def pick_movie():
    # Pick a random movie
    movie = random.choice(movies)

    # Get the movie title
    title = movie["Title"]

    print(title)

    return title
