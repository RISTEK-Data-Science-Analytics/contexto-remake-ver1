import streamlit as st
import pandas as pd

def rank_to_color(rank, max_rank):
    value = rank / max_rank
    green_value = 255 - int(value * 255)
    red_value = int(value * 255)
    return f'rgb({red_value},{green_value},0)'

def load_sidebar():
    with st.sidebar:
        st.sidebar.title("Choose a game number")
        cols = st.columns(len(similarity_df.columns))
        for i, col in enumerate(cols, start=0):
            with col:
                button = st.button(label=f'{i+1}', key=f"button_{i+1}")
                if button:
                    if st.session_state['current_number'] != i+1:  # Check if the game number has changed
                        st.session_state['guesses'] = []  # Reset guesses
                        st.session_state['used_word'] = []  # Reset used words
                        
                    # Update the current target word and game number in the session state
                    st.session_state['current_target_word'] = similarity_df.columns[i]
                    st.session_state['current_number'] = i+1

def update_used_df():
    # Update the DataFrame based on the current target word
    target_word = st.session_state['current_target_word']
    used_df = similarity_df[[target_word]].sort_values(by=target_word, ascending=False)
    used_df['rank'] = range(1, used_df.shape[0] + 1)
    return used_df

class Game:
    def __init__(self):
        ...
    def user_guess(self, guess):
        ...

if __name__ == "__main__":
    similarity_df = pd.read_csv('game.csv', index_col='indeks')

    if 'current_target_word' not in st.session_state:
        # Initialize the current target word with the first column name
        st.session_state['current_target_word'] = similarity_df.columns[0]
    
    if 'current_number' not in st.session_state:
        # Initialize the current game number
        st.session_state['current_number'] = 1
    
    if 'guesses' not in st.session_state:
        # Initialize guesses
        st.session_state['guesses'] = []
    
    if 'used_word' not in st.session_state:
        # Initialize used words
        st.session_state['used_word'] = []

    load_sidebar()

    # Update the used DataFrame based on the current target word
    used_df = update_used_df()

    title = st.title(f"Game number {st.session_state['current_number']}")
    user_guess = st.text_input('Type a word').lower()

    if st.button('Guess'):
        if (user_guess in used_df.index.tolist()) and (user_guess not in st.session_state['used_word']):
            # Retrieve the similarity score and rank for the guess
            score = used_df.loc[user_guess, st.session_state['current_target_word']]
            rank = int(used_df.loc[user_guess, "rank"])
            
            # Append the guess and rank to the session state
            st.session_state['guesses'].append((user_guess, rank))
            st.session_state['used_word'].append(user_guess)
            
        elif user_guess in st.session_state['used_word']:
            st.error("Word has been used.")
        else:
            st.error("Word not found in the vocabulary.")

        # Sort the guesses based on rank
        sorted_guesses = sorted(st.session_state['guesses'], key=lambda x: x[1])

        # Find the max rank for scaling the colors
        max_rank = 30346

        # Create a DataFrame for the guesses
        df_guesses = pd.DataFrame(sorted_guesses, columns=['Word', 'Rank'])

        # Normalize the 'Rank' column to get the length of the bar
        df_guesses['Length'] = 1 - (df_guesses['Rank'] / df_guesses['Rank'].max())
        # df_guesses['Length'] = 1- (df_guesses['Rank'] / max_rank)

        # Map the 'Rank' to a color
        df_guesses['Color'] = df_guesses['Rank'].apply(lambda rank: rank_to_color(rank, max_rank))

        # # Display the sorted guesses and their rank
        # for guess, rank in sorted_guesses:
        #     st.write(f"Rank: {rank}, Word: {guess}")

        for _, row in df_guesses.iterrows():
            # Calculate the percentage width of the bar based on the rank
            percentage_width = row['Length'] * 100
            # Generate the HTML for the custom bar with text inside it
            bar_html = f"""
            <div style="width: 100%; margin-bottom: 10px; background: linear-gradient(to right, {row['Color']} {percentage_width}%, lightgrey {1-percentage_width}%); border-radius: 3px; padding: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #333;">
                    {row['Word']} : {row['Rank']}
                </div>
            </div>

            """
            st.markdown(bar_html, unsafe_allow_html=True)


    # Show the current guesses and their ranks
    st.write("Current guesses:")
    for cnt, (guess, rank) in enumerate(st.session_state['guesses'], start=1):
        st.write(f"{cnt}. Word: {guess}, Rank: {rank}")
