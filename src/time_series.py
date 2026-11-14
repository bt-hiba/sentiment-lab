import pandas as pd


def load_sentiment140(file_path):
    """
    Load the Sentiment140 dataset.

    Parameters:
        file_path (str): Path to the CSV dataset.

    Returns:
        pandas.DataFrame: Dataset with named columns.
    """

    columns = [
        "target",
        "id",
        "date",
        "flag",
        "user",
        "text"
    ]

    df = pd.read_csv(
        file_path,
        header=None,
        names=columns,
        encoding="latin-1"
    )

    return df

def parse_dates(df):
    """
    Convert the date column into datetime values.
    """

    df = df.copy()

    # Replace PDT timezone abbreviation with its UTC offset
    dates = df["date"].str.replace(
        "PDT",
        "-0700",
        regex=False
    )

    df["date"] = pd.to_datetime(
        dates,
        format="%a %b %d %H:%M:%S %z %Y",
        utc=True
    )

    return df

def aggregate_daily_sentiment(df):
    """
    Calculate daily tweet and sentiment statistics.

    Parameters:
        df (pandas.DataFrame): Dataset with parsed dates.

    Returns:
        pandas.DataFrame: Daily sentiment statistics.
    """

    df = df.copy()

    # Extract the day from each tweet date
    df["day"] = df["date"].dt.strftime("%Y-%m-%d")

    # Identify positive and negative tweets
    df["is_positive"] = df["target"] == 4
    df["is_negative"] = df["target"] == 0

    # Group tweets by day and calculate statistics
    daily_stats = df.groupby("day").agg(
        total_tweets=("target", "size"),
        positive_tweets=("is_positive", "sum"),
        negative_tweets=("is_negative", "sum")
    ).reset_index()

    # Calculate sentiment percentages
    daily_stats["positive_rate"] = (
        daily_stats["positive_tweets"]
        / daily_stats["total_tweets"] * 100
    ).round(2)

    daily_stats["negative_rate"] = (
        daily_stats["negative_tweets"]
        / daily_stats["total_tweets"] * 100
    ).round(2)

    return daily_stats

def export_daily_stats(daily_stats, output_path):
    """
    Export daily sentiment statistics to a CSV file.
    """

    daily_stats.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )

def process_sentiment140_in_chunks(
    file_path,
    output_path,
    chunksize=100_000
):
    """
    Process the Sentiment140 dataset in chunks
    and export daily sentiment statistics.
    """

    columns = [
        "target",
        "id",
        "date",
        "flag",
        "user",
        "text"
    ]

    daily_results = []

    # Read the dataset progressively
    for chunk in pd.read_csv(
        file_path,
        header=None,
        names=columns,
        usecols=["target", "date"],
        encoding="latin-1",
        chunksize=chunksize
    ):

        # Convert dates
        chunk = parse_dates(chunk)

        # Calculate statistics for this chunk
        daily_stats = aggregate_daily_sentiment(chunk)

        # Keep only the daily counts
        daily_results.append(
            daily_stats[
                [
                    "day",
                    "total_tweets",
                    "positive_tweets",
                    "negative_tweets"
                ]
            ]
        )

    # Combine results from all chunks
    combined = pd.concat(daily_results)

    # Merge days that appear in different chunks
    final_stats = combined.groupby("day", as_index=False).sum()

    # Calculate final percentages
    final_stats["positive_rate"] = (
        final_stats["positive_tweets"]
        / final_stats["total_tweets"] * 100
    ).round(2)

    final_stats["negative_rate"] = (
        final_stats["negative_tweets"]
        / final_stats["total_tweets"] * 100
    ).round(2)

    # Export final statistics
    export_daily_stats(final_stats, output_path)

    return final_stats