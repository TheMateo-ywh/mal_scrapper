from gazpacho import get, Soup
import pandas as pd
import datetime as dt
import pathlib

list_dir = pathlib.Path('List')
list_dir.mkdir(parents=True, exist_ok=True)

def scrapping(card):
    rank = card.find('span', {'class':'lightLink top-anime-rank-text'}).text
    name = card.find('a', {'class':'hoverinfo_trigger'}, partial=False).text
    score = card.find('span', {'class':'text on score'}).text
    return {'rank': rank, 'name': name, 'score': score}

hoy = dt.date.today()
url1 = "https://myanimelist.net/topanime.php"
url2 = "https://myanimelist.net/topanime.php?limit=50"

html1 = get(url1)
html2 = get(url2)
soup1 = Soup(html1)
soup2 = Soup(html2)

cards1 = soup1.find('tr', {'class':'ranking-list'})
cards2 = soup2.find('tr', {'class':'ranking-list'})

text1 = [scrapping(i) for i in cards1]
text2 = [scrapping(i) for i in cards2]
text = text1 + text2

if text:
    df = pd.DataFrame(text)
    
    # Add date column
    df['date'] = hoy
    
    # Create a new CSV file with today's date
    csv_filename = f'mal_anime_rankings_{hoy}.csv'
    csv_path = list_dir / csv_filename
    
    # Save the DataFrame to a new CSV file
    df.to_csv(csv_path, index=False)
    print(f"Created new CSV file: {csv_path}")
    
else:
    error_file = list_dir / f'{hoy}_error.txt'
    error_file.write_text("Empty list of dictionaries.", encoding='utf-8')
    print(f"Error file created: {error_file}")
