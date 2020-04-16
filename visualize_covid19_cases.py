import io

import requests

import matplotlib.pyplot as plt
import pandas as pd


# Generate plot with single x-axis and two y-axes
# Reference - https://matplotlib.org/gallery/api/two_scales.html
def generate_twinx_plot(df, province, population):
    province_df = df[df["prname"] == province]
    fig, ax1 = plt.subplots()

    date = province_df["date"]
    num_cases = province_df["numtotal"]
    num_tested = province_df["numtested"]

    # Axis for total number of cases
    color = "tab:red"
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Total Number of Cases", color=color)
    ax1.plot(date, num_cases, color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)

    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()

    # Instantiate second y-axis
    ax2 = ax1.twinx()

    # Axis for total numbers tested
    color = "tab:blue"
    ax2.set_ylabel("Total Numbers Tested", color=color)
    ax2.plot(date, num_tested, color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    # Add annotation
    if province == "Quebec":
        ax2.annotate(
            "Ramped-up testing",
            xy=("2020-03-23", 9000),
            xytext=("2020-03-10", 40000),
            arrowprops=dict(facecolor="black", shrink=0.025),
        )

    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)

    ax2.get_yaxis().tick_right()

    # Avoid tight clipping of right y-label
    fig.tight_layout()

    # Rotate x-axis labels for better readability
    fig.autofmt_xdate()

    # Add title
    plt.title(province + " - Population " + str(population) + " Million")

    # Save and close
    plt.savefig(province + ".png", bbox_inches="tight")
    plt.cla()
    plt.clf()
    plt.close(fig)


# Download data into pandas
url = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode("utf-8")))

# Convert "date" column to datetime64[ns]
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")

# Apply date filter to plot only relevant dates
df_filtered = df[df["date"] > "2020-03-10"]

# Generate plots for Ontario and Quebec
generate_twinx_plot(df_filtered, "Ontario", 14.57)
generate_twinx_plot(df_filtered, "Quebec", 8.48)
generate_twinx_plot(df_filtered, "British Columbia", 5.07)
