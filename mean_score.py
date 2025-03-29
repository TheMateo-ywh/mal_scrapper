import pandas as pd
import pathlib

list_dir = pathlib.Path('List')
output_file ='average_rank_per_anime.csv'

# Collect all CSV files in the directory
csv_files = sorted(list_dir.glob('mal_anime_rankings_*.csv'))

if csv_files:
    all_data = []
    dates = []

    for file in csv_files:
        # Extract date from the filename
        date_str = file.stem.split('_')[-1]
        dates.append(pd.to_datetime(date_str))

        # Read the CSV file
        df = pd.read_csv(file)
        all_data.append(df)

    # Concatenate all data
    combined_df = pd.concat(all_data)

    # Ensure numeric columns
    combined_df['rank'] = pd.to_numeric(combined_df['rank'], errors='coerce')
    combined_df['score'] = pd.to_numeric(combined_df['score'], errors='coerce')

    # Group by anime name and calculate averages
    aggregated_df = combined_df.groupby('name', as_index=False).agg({
        'rank': 'mean',
        'score': 'mean'
    }).rename(columns={'rank': 'average_rank', 'score': 'average_score'})

    # Determine the oldest and newest dates
    oldest_date = min(dates).date()
    newest_date = max(dates).date()

    # Add date columns to the aggregated DataFrame
    aggregated_df['oldest_date'] = oldest_date
    aggregated_df['newest_date'] = newest_date

    # Round average_rank and average_score to 2 decimal places
    aggregated_df['average_rank'] = aggregated_df['average_rank'].round(2)
    aggregated_df['average_score'] = aggregated_df['average_score'].round(2)

    # Sort the aggregated DataFrame by average_rank in ascending order
    aggregated_df = aggregated_df.sort_values(by='average_rank')

    # Save the results to a new CSV file
    aggregated_df.to_csv(output_file, index=False)
    print(f"Aggregated results per anime saved to: {output_file}")
else:
    print("No CSV files found in the List directory.")
