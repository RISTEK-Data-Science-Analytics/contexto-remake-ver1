import streamlit as st
import pandas as pd

def load_sidebar():
    with st.sidebar:
        cols = st.columns(len(similarity_df.columns))
        for i, col in enumerate(cols):
            with col:
                button = st.button(label=f"{i+1}", key=i+1)
                if button:
                    target_word = similarity_df.columns[i]
                    used_df = similarity_df[[target_word]].sort_values(by=target_word, ascending=False)
                    used_df['rank'] = range(1,used_df.shape[0]+1)

class Game:
    def __init__(self, solution: str, word_rank: pd.DataFrame):
        self.is_over = False
        self.solution = solution
        self.used_word = []
        self.word_rank = word_rank

    def user_guess(self, guess):
        if guess in word_rank:
            return (1, guess)
        elif guess == 0:
            rank = self.word_rank.loc[guess, "rank"].value
            self.used_word.append(guess)
            return (rank, guess)
        else:
            st.error("Word not found in vocabulary.")
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

    # if st.button('Guess'):
    #     if (user_guess in used_df.index.tolist()) & (user_guess not in st.session_state['used_word']):
    #         print('yes')
    #         score = used_df.loc[user_guess, target_word]
    #         rank = int(used_df.loc[user_guess, "rank"])
            
    #         st.session_state['guesses'].append((user_guess, rank))
    #         st.session_state['used_word'].append(user_guess)
            
    #     elif user_guess in st.session_state['used_word']:
    #         st.error("Word has been used.")
    #     else:
    #         st.error("Word not found in the vocabulary.")
        
    #     sorted_guesses = sorted(st.session_state['guesses'], key=lambda x: x[1], reverse=False)
        
    #     for guess, rank in sorted_guesses:
    #         st.write(f"Rank: {rank}, Word: {guess}")

    # Show the current guesses and their scores
    st.write("Current guesses:")
    for cnt, (guess, score) in enumerate(st.session_state['guesses'], start=1):
        st.write(f"{cnt}. Word: {guess}")