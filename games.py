import streamlit as st
import pandas as pd

# Read Excel file
data = pd.read_excel(
    'https://raw.githubusercontent.com/faaabs1/game_leaderboard/main/trainingslager.xlsx',

    engine="openpyxl",
    sheet_name="python"
)
data.head()
print(data.head())
def get_game_winners(df):
    """
    Identifies the winner of each game and counts how many times each team has won.

    :param df: Pandas DataFrame containing game results.
    :return: DataFrame of teams and their win count.
    """
    # Identify the winner of each game by selecting the team with the highest 'Punkte'
    winners = df.groupby('Bewerb').apply(lambda x: x.loc[x['Punkte'].idxmax()])['Team']

    # Count how many times each team is the winner
    winner_counts = winners.value_counts()

    # Convert to DataFrame for easy display
    winner_counts_df = winner_counts.reset_index()
    winner_counts_df.columns = ['Team', 'Wins']

    return winner_counts_df

def update_leaderboard_with_wins(df):
    """
    Adds the win count column to the leaderboard DataFrame.

    :param df: Pandas DataFrame containing game results.
    :return: Updated DataFrame with 'Wins' column.
    """
    # Get the winner count DataFrame
    winner_counts_df = get_game_winners(df)

    # Aggregate the leaderboard by team and sum the points
    leaderboard_df = df.groupby('Team')['Punkte'].sum().reset_index()

    # Merge the leaderboard with the win count DataFrame
    leaderboard_df = pd.merge(leaderboard_df, winner_counts_df, on='Team', how='left')

    # Fill NaN values in the 'Wins' column with 0 (if a team has no wins)
    leaderboard_df['Wins'].fillna(0, inplace=True)

    # Sort the leaderboard by points (descending)
    leaderboard_df = leaderboard_df.sort_values(by=['Punkte', 'Wins'], ascending=[False, False])


    # Set 'Ranking' based on sorted leaderboard
    leaderboard_df['Ranking'] = range(1, len(leaderboard_df) + 1)
    leaderboard_df.set_index('Ranking',inplace=True)

    return leaderboard_df[['Team', 'Punkte', 'Wins']]



def game_result(game):
    filtered_df = data[data['Bewerb']== game]
    sorted_df = filtered_df.sort_values(by="Punkte", ascending=False)

    winner = sorted_df.iloc[0]['Team']

    # Create a new column 'Ranking' to represent the ranking starting from 1
    sorted_df['Ranking'] = range(1, len(sorted_df) + 1)
    # Set 'Team' as the index
    sorted_df.set_index('Ranking', inplace=True)
    # Only keep 'Team', 'Punkte', and 'Ranking' columns
    result_df = sorted_df[['Team','Punkte']]

    return result_df, winner




# Group and sort data
df_group = data.groupby('Team')['Punkte'].sum()  # This is a Series
df_sorted = df_group.sort_values(ascending=False)  # Sorting correctly



# Get the current winner
current_winner = df_sorted.idxmax()

# 🎯 Sidebar with Options
menu_option = st.sidebar.radio("Navigation", ["🏆 Leaderboard", "⚽ Game-by-Game Results"])

# 🏆 Leaderboard View
if menu_option == "🏆 Leaderboard":
    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("BSDS 2025 - SCSR Edition")

    with col2:
        st.image("/Users/fabs/Desktop/Fabian/Fußball/SCSR/scsr_logo.png")

    st.divider()

    # Display the current winner with a large font
    st.markdown(
        f"<h2 style='text-align: center; color: gold;'>🏆 Current Leader: {current_winner} 🏆</h2>",
        unsafe_allow_html=True
    )
    df_sorted = update_leaderboard_with_wins(data)
    # Display sorted leaderboard
    st.dataframe(df_sorted, use_container_width=True)

# ⚽ Game-by-Game Results View
elif menu_option == "⚽ Game-by-Game Results":
    st.title("⚽ Game-by-Game Results")

    # Dropdown for game selection
    selected_game = st.selectbox("Select a Game:", data["Bewerb"].unique())

    filtered_sorted_df,winner = game_result(selected_game)

    # Display the winner
    st.markdown(f"### 🏆 **Winner of {selected_game}: {winner}** 🏆")

    # Filter and display the results
    
    st.dataframe(filtered_sorted_df,use_container_width=True)
