import pandas as pd
import matplotlib.pyplot as plt
from chess_insight import ChessComApiCommunicator, LichessApiCommunicator
import chess_insight

# c1 = LichessApiCommunicator()
# c2 = ChessComApiCommunicator()

# games = list(c1.games_generator("pro100wdupe", 100, "blitz"))
# games += list(c2.games_generator("barabasz60", 100, "blitz"))
# chess_insight.export_games_to_csv(list(games))

# Load the CSV data into a DataFrame
data = pd.read_csv("games.csv")

# Extract the necessary columns for analysis
data["date"] = pd.to_datetime(data["date"])
data["year_month"] = data["date"].dt.to_period("M")
data["player_color"] = (
    data["player_color"].str.strip("[]").str.replace("'", "").str.split(", ")
)
data["result"] = data["result"].str.strip("[]").str.replace("'", "").str.split(", ")
data["opening"] = data["opening"].str.split(":").str[-1].str.strip()

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Subplot 1: Elo over time with respect to each host
player_elo_over_time = (
    data.groupby(["year_month", "host"])["player_elo"].mean().unstack()
)
player_elo_over_time.plot(kind="line", ax=axs[0, 0])
axs[0, 0].set_title("Player Elo Over Time with Respect to Each Host")
axs[0, 0].set_xlabel("Year-Month")
axs[0, 0].set_ylabel("Player Elo Rating")
axs[0, 0].legend(title="Host", loc="upper left")

# Subplot 2: 5 most popular short_openings when player_color is white
white_openings = data[data["player_color"].apply(lambda x: "white" in x)]
top_white_openings = white_openings["opening_short"].value_counts().nlargest(5)
top_white_openings.plot(kind="bar", ax=axs[0, 1], color="green")
axs[0, 1].set_title("Top 5 Short Openings When Player Color is White")
axs[0, 1].set_xlabel("Short Opening")
axs[0, 1].set_ylabel("Count")

# Subplot 3: 5 most popular short_openings when player_color is black
black_openings = data[data["player_color"].apply(lambda x: "black" in x)]
top_black_openings = black_openings["opening_short"].value_counts().nlargest(5)
top_black_openings.plot(kind="bar", ax=axs[1, 0], color="purple")
axs[1, 0].set_title("Top 5 Short Openings When Player Color is Black")
axs[1, 0].set_xlabel("Short Opening")
axs[1, 0].set_ylabel("Count")

# Subplot 4: Pie chart with win reasons
results = data["result"]
win_reasons = [result[-1] for result in results if result[-1] != "None"]
win_reason_counts = pd.Series(win_reasons).value_counts()
axs[1, 1].pie(
    win_reason_counts, labels=win_reason_counts.index, autopct="%1.1f%%", startangle=90
)
axs[1, 1].set_title("Reasons for Winning")
axs[1, 1].legend(win_reason_counts.index, loc="upper left")


# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
