import streamlit as st
import pandas as pd

def load_sidebar():
    with st.sidebar:
        cols = st.columns(len(similarity_df.columns))
        for i, col in enumerate(cols, start=0):
            with col:
                button = st.button(label=f'{i+1}', key=f"button_{i+1}")
                if button:
                    # Update the current target word in the session state
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
        st.session_state['current_number'] = 1

    load_sidebar()

    # Update the used DataFrame based on the current target word
    used_df = update_used_df()

    if 'guesses' not in st.session_state:
        st.session_state['guesses'] = []
        st.session_state['used_word'] = []

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

        # Display the sorted guesses and their rank
        for guess, rank in sorted_guesses:
            st.write(f"Rank: {rank}, Word: {guess}")

    # Show the current guesses and their ranks
    st.write("Current guesses:")
    for cnt, (guess, rank) in enumerate(st.session_state['guesses'], start=1):
        st.write(f"{cnt}. Word: {guess}, Rank: {rank}")
