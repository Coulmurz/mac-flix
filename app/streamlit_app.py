import streamlit as st
import requests

# Initialize session state for category if it doesn't exist
if 'category' not in st.session_state:
    st.session_state.category = "Movies"

st.title("Mac Flix")

# Fetch data from backend
try:
    response = requests.get("http://localhost:8000/content")
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data from backend: {e}")
    data = []
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
    data = []

# Sidebar for filters
st.sidebar.header("Filters")

# Create functions to update session state
def set_movies():
    st.session_state.category = "Movies"
    
def set_tv_shows():
    st.session_state.category = "TV Shows"

# Category buttons with session state management
if st.sidebar.button("Movies", on_click=set_movies):
    pass
if st.sidebar.button("TV Shows", on_click=set_tv_shows):
    pass

# Get current category from session state
category = st.session_state.category

# Filter data based on category
filtered_data = [item for item in data if (category == "Movies" and item["type"] == "movie") or (category == "TV Shows" and item["type"] == "tv")]

# Create a dictionary to store the content
content_dict = {}
for item in filtered_data:
    content_dict[item["title"]] = item

# Create a selectbox to choose the content
if content_dict:
    selection = st.selectbox("Choose content", list(content_dict.keys()))
    
    # Get the selected content
    selected_content = content_dict[selection]

    if selected_content["type"] == "movie":
        # Display the selected content
        st.header(selected_content["title"])
        st.image(selected_content["poster_url"], width=200)
        st.write(f"Year: {selected_content['year']}")
        st.write(f"Rating: {selected_content['rating']}")
        st.write(f"Description: {selected_content['description']}")
        st.write(f"Cast: {selected_content['cast']}")
        
        # Video section - full width trailer
        st.subheader("Trailer")
        st.video(selected_content["trailer_url"])
        
        # Stream and download links in two columns
        st.subheader("Watch Options")
        col1, col2 = st.columns(2)
        
        # Stream button
        with col1:
            stream_url = f"http://localhost:8000/stream/{selected_content['id']}"
            st.markdown(f"[Stream Movie]({stream_url})")
        
        # Download button
        with col2:
            download_url = f"http://localhost:8000/download/{selected_content['id']}"
            st.markdown(f"[Download Movie]({download_url})")

    elif selected_content["type"] == "tv":
        st.header(selected_content["title"])
        st.image(selected_content["poster_url"], width=200)
        st.write(f"Year: {selected_content['year']}")
        st.write(f"Rating: {selected_content['rating']}")
        st.write(f"Description: {selected_content['description']}")
        st.write(f"Cast: {selected_content['cast']}")
        
        # Video section for main trailer - full width
        st.subheader("Series Trailer")
        st.video(selected_content["trailer_url"])
        
        st.subheader("Seasons")
        for season in selected_content["seasons"]:
            season_num = season['season_number']
            with st.expander(f"Season {season_num}"):
                for episode in season["episodes"]:
                    ep_num = episode['episode_number']
                    ep_title = episode['title']
                    
                    # Episode header
                    st.subheader(f"Episode {ep_num}: {ep_title}")
                    
                    # Episode image
                    st.image(episode["poster_url"], width=200)
                    
                    # Episode description
                    st.write(episode["description"])
                    
                    # Episode buttons
                    col1, col2 = st.columns(2)
                    
                    # Stream episode button
                    with col1:
                        stream_url = f"http://localhost:8000/stream/episode/{selected_content['id']}/{season_num}/{ep_num}"
                        st.markdown(f"[Stream Episode]({stream_url})")
                    
                    # Download episode button (assuming the same URL can be used)
                    with col2:
                        download_url = f"http://localhost:8000/download/{selected_content['id']}"
                        st.markdown(f"[Download Episode]({download_url})")
else:
    st.warning(f"No content found for category: {category}")
