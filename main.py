import streamlit as st
import pandas as pd

hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def rank_to_color(rank, max_rank_color):
    value = rank / max_rank_color
    if value >= 1:
        value=1
    green_value = 255 - int(value * 255)
    red_value = int(value * 255)
    return f'rgb({red_value},{green_value},0)'

def load_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; margin-bottom: 1rem;'>Pilih nomor permainan</h1>", unsafe_allow_html=True)
        num_games = len(similarity_df.columns)
        
        # Update the game number directly from the number_input
        selected_game = st.number_input("", min_value=1, max_value=num_games, value=st.session_state.get('current_number', 1), step=1)
        
        # Directly update session state variables if the selected game has changed
        if st.session_state.get('current_number', 1) != selected_game:
            st.session_state['current_number'] = selected_game
            st.session_state['current_target_word'] = similarity_df.columns[selected_game - 1]
            st.session_state['guesses'] = []  # Reset guesses
            st.session_state['used_word'] = []  # Reset used words
            st.session_state['curr_rank'] = len(similarity_df)

        # Footer
        footer = """
        <style>
        .footer {
            font-family: Arial, sans-serif;
            font-size: small;
            text-align: center;
            padding: 10px;
            margin-top: 20px;
        }
        </style>
        <div class="footer">
            &copy; 2023 <a href="https://www.ristek.cs.ui.ac.id/" target="_blank">RISTEK Fasilkom UI</a> <br>All rights reserved<br>
            Reference: <a href="https://contexto.me/" target="_blank">contexto.me</a>
        </div>
        """

        st.markdown(footer, unsafe_allow_html=True)



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
    max_rank_color = 10000
    max_rank_length = 15000
    
    if 'curr_rank' not in st.session_state:
        st.session_state['curr_rank'] = len(similarity_df)

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
    
    title = st.title(f"Konteksto - Nomor {st.session_state['current_number']}")
    desc = st.write(r"$\textsf{\large Permainan tebak kata berbahasa Indonesia}$")
    user_guess = st.text_input(r"$\textsf{\normalsize Pilih sebuah kata}$").lower()
    # user_guess = st.text_input("Type a word").lower()

    columns = st.columns(6)

    # Place the "Guess" button in the first column
    with columns[0]:
        guess_clicked = st.button('Tebak')

    # Place the "Hint" button in the second column
    with columns[4]:
        hint_clicked = st.button('Petunjuk')

    # Place the "Reveal Answer" button in the third column
    with columns[5]:
        reveal_clicked = st.button('Jawaban')

    if hint_clicked:
        hint_rank = st.session_state['curr_rank']//2 if st.session_state['curr_rank']//2 > 0 else 1
        hint_word = used_df.iloc[hint_rank-1].name  # Get the word at the 500th rank
        hint_message = f"Petunjuk: Kata pada peringkat {hint_rank} adalah **\"{hint_word}\"**"
        # Use custom HTML to display the hint in green
        st.success(hint_message)


    # Handle "Reveal Answer" button click
    if reveal_clicked:
        # Reveal the current target word
        answer_message = f"Jawaban: Target katanya adalah **\"{st.session_state['current_target_word']}\"**"
        # Use custom HTML to display the answer in green
        st.success(answer_message)

    sorted_guesses = ""
    if guess_clicked:
        if (user_guess in used_df.index.tolist()) and (user_guess not in st.session_state['used_word']):
            # Retrieve the similarity score and rank for the guess
            score = used_df.loc[user_guess, st.session_state['current_target_word']]
            rank = int(used_df.loc[user_guess, "rank"])
            
            if rank < st.session_state['curr_rank']:
                st.session_state['curr_rank'] = rank

            # Append the guess and rank to the session state
            st.session_state['guesses'].append((user_guess, rank))
            st.session_state['used_word'].append(user_guess)
            
        elif user_guess in st.session_state['used_word']:
            st.error(f"Kata **\"{user_guess}\"** telah digunakan.")
        else:
            st.error(f"Kata **\"{user_guess}\"** tidak ditemukan dalam kosa kata.")

    if st.session_state['guesses']:
        # Show the current guesses and their ranks
        st.write("Tebakan Saat Ini:")

        curr_guess, curr_rank = st.session_state['guesses'][-1]
        # Calculate the percentage width of the bar based on the rank
        curr_percentage_width = (1 - (curr_rank / max_rank_length) if curr_rank / max_rank_length <= 0.95 else 0.05) * 100
        # Generate the HTML for the custom bar with text inside it
        bar_html = f"""
        <div style="width: 100%; margin-bottom: 10px; background: linear-gradient(to right, {rank_to_color(curr_rank, max_rank_color)} {curr_percentage_width}%, lightgrey {1-curr_percentage_width}%); border-radius: 5px; padding: 8px; padding-left:16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #333;">
                {curr_guess} : {curr_rank}
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)

        # st.markdown("---")
        st.markdown("<hr style='margin: 15px 0; border-top: 1px solid #bbb;'/ >", unsafe_allow_html=True)

        # Create a DataFrame for the guesses
        sorted_guesses = sorted(st.session_state['guesses'], key=lambda x: x[1])
        df_guesses = pd.DataFrame(sorted_guesses, columns=['Word', 'Rank']).head(10)

        # Normalize the 'Rank' column to get the length of the bar
        df_guesses['Length'] = df_guesses.apply(lambda row: 1 - (row['Rank'] / max_rank_length) if (row['Rank'] / max_rank_length) <= 0.95 else 0.05, axis=1)

        # Map the 'Rank' to a color
        df_guesses['Color'] = df_guesses['Rank'].apply(lambda rank: rank_to_color(rank, max_rank_color))

        st.write("10 Tebakan Terbaik:")
        for _, row in df_guesses.iterrows():
            # Calculate the percentage width of the bar based on the rank
            percentage_width = row['Length'] * 100
            # Generate the HTML for the custom bar with text inside it
            bar_html = f"""
            <div style="width: 100%; margin-bottom: 10px; background: linear-gradient(to right, {row['Color']} {percentage_width}%, lightgrey {1-percentage_width}%); border-radius: 5px; padding: 8px; padding-left:16px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #333;">
                    {row['Word']} : {row['Rank']}
                </div>
            </div>

            """
            st.markdown(bar_html, unsafe_allow_html=True)

    st.empty()