import streamlit as st
import pandas as pd

def load_sidebar():
    with st.sidebar:
        cols = st.columns(len(similarity_df.columns))
        for i, col in enumerate(cols):
            with col:
                button = st.button(label=f'{i+1}', key=i+1)
                if button:
                    target_word = similarity_df.columns[i]
                    used_df = similarity_df[[target_word]].sort_values(by=target_word, ascending=False)
                    used_df['rank'] = range(1,used_df.shape[0]+1)

class Game:
    def __init__(self):
        ...
    def user_guess(self, guess):
        ...

if __name__ == "__main__":
    similarity_df = pd.read_csv('game.csv', index_col='indeks')

    load_sidebar()
    


    target_word = similarity_df.columns[0]
    used_df = similarity_df[[target_word]].sort_values(by=target_word, ascending=False)
    used_df['rank'] = range(1,used_df.shape[0]+1)

    if 'guesses' not in st.session_state:
        st.session_state['guesses'] = []
        st.session_state['used_word'] = []

    title = st.title(target_word)
    user_guess = st.text_input('Type a word').lower()

    if st.button('Guess'):
        if (user_guess in used_df.index.tolist()) & (user_guess not in st.session_state['used_word']):
            print('yes')
            # Retrieve the similarity score for the guess
            score = used_df.loc[user_guess, target_word]
            rank = int(used_df.loc[user_guess, "rank"])
            
            # Append the guess and score to the session state
            st.session_state['guesses'].append((user_guess, rank))
            st.session_state['used_word'].append(user_guess)
            
        elif user_guess in st.session_state['used_word']:
            st.error("Word has been used.")
        else:
            st.error("Word not found in the vocabulary.")
        
        # Sort the guesses based on the similarity score
        sorted_guesses = sorted(st.session_state['guesses'], key=lambda x: x[1], reverse=False)
        
        # Display the sorted guesses and their rank
        for guess, rank in sorted_guesses:
            st.write(f"Rank: {rank}, Word: {guess}")

    # Show the current guesses and their scores
    st.write("Current guesses:")
    for cnt, (guess, score) in enumerate(st.session_state['guesses'], start=1):
        st.write(f"{cnt}. Word: {guess}")