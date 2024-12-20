from pathlib import Path

import streamlit as st

from graph_utils import AnelkaNumberGraph

# load the graph - either create it or read it in from a pickle file
local_path = Path.cwd().joinpath("anelka-number")

#@st.cache_data
def get_graph():
    return AnelkaNumberGraph.get_graph(local_path.joinpath("graph.pkl"), local_path.joinpath("data", "transfers_cleaned.csv"))

graph = get_graph()

# #####################
# #   Streamlit app
# #####################

st.title("The 'Anelka Number'")
st.markdown("""
    Find a player's Anelka Number (the degree of separation from Nicolas Anelka). Like the [Bacon number](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon) or [Erdős number](https://en.wikipedia.org/wiki/Erd%C5%91s_number) but for footballers.

    Made by [David Asboth](https://davidasboth.com).

    Select a player to view the results.
""")

with st.expander("Details"):
    st.markdown("""
                
        ### Why Nicolas Anelka?
                
        Calculating degrees of separation makes sense for prolific people.
                Erdős collaborated with lots of other mathematicians, Kevin Bacon has acted alongside a lot of actors.
                Likewise, Nicolas Anelka is a journeyman footballer with a career spanning many leagues and countries.
                It made sense to base this number on him, but you could repeat the same exercise with anyone.

        ### About the data
                
        Uses transfer data between 1992 and 2022. Original source: https://www.kaggle.com/datasets/cbhavik/football-transfers-from-199293-to-202122-seasons
            
        #### Caveats
            
        - the accuracy relies on the completeness of the data used. Even if the data is incomplete, you can find a lot of players in the dropdown!
        - data is based on *transfers*, not "X player played at club Y in season Z"
        - "X player played at club Y in season Z" is calculated by a player transfering to a club and filling in the gaps until the next transfer
        - so if we see player X transferring to club A in the 2001/2002 season, then to club B in the 2003/2004 season, we can assume they played at club A in the 2002/2003 season
        - but if player X transferred to a club in 1992, played there for 10 years then retired, the app assumes they were there for one season then disappeared since we have no "second" transfer until which we can fill in the gap
            """)

#@st.cache_data
def get_players():
    return graph.get_players()

player_select = st.selectbox("Select a player",
                            get_players(),
                            label_visibility="collapsed",
                            index=None,
                            placeholder="Select a player...")

if player_select:
    anelka_number = graph.get_anelka_number(player_select)
    st.subheader(f"{player_select}'s Anelka number is {anelka_number}")
    
    # just load the image instead
    player_img_path = local_path.joinpath("images", f"{player_select}.png")
    st.image(str(player_img_path))