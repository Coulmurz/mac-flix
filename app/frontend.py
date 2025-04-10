import streamlit as st

st.set_page_config(page_title="My Flix", layout="wide")
st.title("🎬 My Flix")

# Initialize navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

# Mock data: 5 sample movies
mock_movies = [
    {
        "id": 1,
        "title": "The Great Adventure",
        "poster_url": "https://image.tmdb.org/t/p/w500/8UlWHLMpgZm9bx6QYh0NFoq67TZ.jpg",  # Wonder Woman 1984
        "genres": ["Adventure", "Action"],
        "description": "An epic journey across uncharted lands.",
        "year": 2021,
        "rating": 88,
        "cast": ["Alice Smith", "Bob Johnson"],
        "director": "Jane Doe",
        "duration": 120,
        "language": "English",
        "trailer_url": ""
    },
    {
        "id": 2,
        "title": "Mystery of the Night",
        "poster_url": "https://image.tmdb.org/t/p/w500/6MKr3KgOLmzOP6MSuZERO41Lpkt.jpg",  # Cruella
        "genres": ["Mystery", "Thriller"],
        "description": "A detective unravels a dark secret.",
        "year": 2020,
        "rating": 75,
        "cast": ["Charlie Brown", "Diana Prince"],
        "director": "John Smith",
        "duration": 110,
        "language": "English",
        "trailer_url": ""
    },
    {
        "id": 3,
        "title": "Romance in Paris",
        "poster_url": "https://image.tmdb.org/t/p/w500/9O1Iy9od7uGZ3m9M4f2R3G9C0bM.jpg",  # La La Land
        "genres": ["Romance", "Drama"],
        "description": "A love story set in the heart of Paris.",
        "year": 2019,
        "rating": 92,
        "cast": ["Eve Adams", "Frank Miller"],
        "director": "Sophie Lee",
        "duration": 95,
        "language": "French",
        "trailer_url": ""
    },
    {
        "id": 4,
        "title": "Sci-Fi Odyssey",
        "poster_url": "https://image.tmdb.org/t/p/w500/2mtQwJKVKQrZgTz49Dizb25eOQQ.jpg",  # The Martian
        "genres": ["Science Fiction"],
        "description": "Exploring the far reaches of the galaxy.",
        "year": 2022,
        "rating": 80,
        "cast": ["George Lucas", "Hannah White"],
        "director": "Mark Green",
        "duration": 130,
        "language": "English",
        "trailer_url": ""
    },
    {
        "id": 5,
        "title": "Comedy Hour",
        "poster_url": "https://image.tmdb.org/t/p/w500/5YUYg5q7QfC4IoNwNUtiwdiYKPr.jpg",  # The Hangover
        "genres": ["Comedy"],
        "description": "A hilarious collection of sketches.",
        "year": 2018,
        "rating": 70,
        "cast": ["Ian Black", "Judy Blue"],
        "director": "Tom Orange",
        "duration": 85,
        "language": "English",
        "trailer_url": ""
    }
]

def show_home():
    st.subheader("Welcome to My Flix!")

    # Inject CSS for uniform poster size and center alignment
    st.markdown(
        """
        <style>
        .movie-card {
            width: 200px;
            margin-left: auto;
            margin-right: auto;
        }
        .movie-poster {
            width: 100%;
            height: 350px;
            object-fit: cover;
            display: block;
        }
        .center-text {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(5)
    for idx, movie in enumerate(mock_movies):
        with cols[idx % 5]:
            st.markdown(
                f'''
                <div class="movie-card">
                    <img src="{movie["poster_url"]}" class="movie-poster"/>
                    <div class="center-text"><small>{movie["year"]} | {", ".join(movie["genres"])}</small></div>
                    <div class="center-text"><strong>{movie["title"]}</strong></div>
                    <div class="center-text">Rotten Tomatoes: {movie["rating"]}%</div>
                    <div style="
                        text-align: center;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        display: -webkit-box;
                        -webkit-line-clamp: 3;
                        -webkit-box-orient: vertical;
                        font-size: 0.85em;
                        margin-top: 5px;
                        min-height: 60px;
                    ">
                        {movie["description"]}
                    </div>
                    <div style="text-align: center; margin-top: 8px;">
                        <a href="#" title="Watch Movie" style="margin: 0 5px; font-size: 1.5em; text-decoration: none;">🎬</a>
                        <a href="#" title="Play Trailer" style="margin: 0 5px; font-size: 1.5em; text-decoration: none;">▶️</a>
                        <a href="#" title="Download" style="margin: 0 5px; font-size: 1.5em; text-decoration: none;">⬇️</a>
                    </div>
                </div>
                ''',
                unsafe_allow_html=True,
            )
            # Add Streamlit button below emojis
            if st.button("Details", key=f"details_{movie['id']}"):
                st.session_state.history.append("home")
                st.session_state.selected_item = movie
                st.session_state.page = "details"
                st.rerun()

def show_details():
    movie = st.session_state.selected_item
    if not movie:
        st.write("No movie selected.")
        return

    # Back Home button at the top
    if st.button("⬅️ Back Home"):
        st.session_state.page = "home"
        st.session_state.selected_item = None
        st.session_state.history.clear()
        st.rerun()

    # Top section: poster + info + trailer
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(movie["poster_url"], width=200)
    with col2:
        st.header(f"{movie['title']} ({movie['year']})")
        st.caption(f"{', '.join(movie['genres'])} | {movie['duration']} min | {movie['language']}")
        st.write(f"**Rotten Tomatoes:** {movie['rating']}%")
        st.write(movie["description"])
        st.write(f"**Director:** {movie['director']}")
        st.write(f"**Cast:** {', '.join(movie['cast'])}")
        # Placeholder trailer
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")

    st.markdown("---")
    st.subheader("Videos")
    cols = st.columns(4)
    for col in cols:
        col.image("https://via.placeholder.com/200x120?text=Video", use_column_width=True)

    st.markdown("---")
    st.subheader("Photos")
    cols = st.columns(5)
    for col in cols:
        col.image("https://via.placeholder.com/150x100?text=Photo", use_column_width=True)

    st.markdown("---")
    st.subheader("Cast")
    cols = st.columns(5)
    for idx, actor in enumerate(movie.get("cast", [])):
        with cols[idx % 5]:
            st.image("https://via.placeholder.com/100x100?text=Actor", use_column_width=True)
            st.caption(actor)

    st.markdown("---")
    st.subheader("More Like This")
    cols = st.columns(4)
    for col in cols:
        col.image("https://via.placeholder.com/150x225?text=Movie", use_column_width=True)

    st.markdown("---")
    st.subheader("Storyline")
    st.write(movie["description"])

    st.markdown("---")
    st.subheader("Did You Know?")
    st.write("This is some fun trivia about the movie. Replace with real trivia later.")

    st.markdown("---")
    st.subheader("User Reviews")
    st.write("User1: Great movie! Loved it.\n\nUser2: Not my cup of tea.\n\nUser3: Amazing visuals and story.")

    st.markdown("---")
    st.subheader("FAQ")
    st.write("**Q:** When was this movie released?\n\n**A:** " + str(movie["year"]))
    st.write("**Q:** Who directed the movie?\n\n**A:** " + movie["director"])

    st.markdown("---")
    st.subheader("Details")
    st.write(f"Duration: {movie['duration']} min")
    st.write(f"Language: {movie['language']}")
    st.write("Box Office: $100M (mock data)")
    st.write("Technical Specs: Color, 4K, Dolby Atmos")

    st.markdown("---")
    st.subheader("Related News")
    st.write("No news available. Replace with real news later.")

    # Optional: Previous button at bottom
    if st.button("⬅️ Previous"):
        if st.session_state.history:
            st.session_state.page = st.session_state.history.pop()
            st.rerun()

if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "details":
    show_details()
else:
    st.write("Invalid page state.")
