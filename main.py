import streamlit as st
import pandas as pd

def load_sidebar():
    with st.sidebar:
        cols = st.columns(len(similarity_df.columns))
        for i, col in enumerate(cols):
            with col:
                button = st.button(label=f"{i+1}", key=i+1)
                if button:
                    st.session_state['current_game'] = st.session_state['game'][i]
                    print(st.session_state['current_game'].solution)

class Game:
    def __init__(self, solution: str, word_rank: pd.DataFrame):
        self.is_over = False
        self.solution = solution
        self.used_word = []
        self.word_rank = word_rank

    def user_guess(self, guess):
        print(self.word_rank)
        if guess in self.word_rank and guess not in self.used_word:
            rank = self.word_rank.loc[guess, "rank"].astype(int)
            self.used_word.append((guess, rank))
            return (rank, guess)
        elif guess in self.used_word:
            return (0, "err")
        return (-1, "err")

    def total_guess(self) -> int:
        return len(self.guesses)
    
if __name__ == "__main__":
    similarity_df = pd.read_csv('game.csv', index_col='indeks')

    load_sidebar()

    # Initialization
    st.session_state['game'] = []
    for word in similarity_df.columns:
        word_rank = similarity_df[[word]].sort_values(by=word, ascending=False)
        word_rank['rank'] = range(1, len(word_rank) + 1)
        game = Game(word, word_rank)
        st.session_state['game'].append(game)
    st.session_state['current_game'] = st.session_state['game'][0]

    title = st.title(word)
    user_guess = st.text_input('Type a word').lower()

    if st.button('Guess'):
        rank, word = st.session_state['current_game'].user_guess(user_guess)

        if rank == 0:
            st.error("Word is already used.")
        elif rank == -1:
            st.error("Word not found in vocabulary.")
        sorted_guesses = sorted(st.session_state['current_game'].used_word, key=lambda x: x[1], reverse=False)
        for guess, rank in sorted_guesses:
            st.write(f"Rank: {rank}, Word: {guess}")

    # Show the current guesses and their scores
    st.write("Current guesses:")
    for cnt, (guess, score) in enumerate(st.session_state['current_game'].used_word, start=1):
        st.write(f"{cnt}. Word: {guess}")