# LyricEmpirics
# Arya Kondur
# 9-3-2021

# lyric_empirics.py
# Program runs through this file. Holds public functions users can call.


import lyricsgenius as lg
from song import Song
import utility
import pathlib
import pandas as pd

_genius = None # Genius API Client
_song_df = None # Dataframe for songs
_dir1 = pathlib.Path('LyricEmpiricsStorage')
_dir2 = _dir1 / "SongLyrics"

'''
Return the Genius API Client object that allows requests to be made based on
the arguments given.
    token    : Client token (API key) that is provided by Genius
    max_time : Time (in seconds) before aborting a request
    sleep    : Time (in seconds) to wait between requests
    display  : Display status messages
    exclude  : Terms to ignore in song lyircs/titles when searching
'''
def init_genius(token: str, max_time: int = 10, sleep: float = 0.2,
                display: bool = True, exclude: [str] = ["(Live)"]) -> None:
    global _genius, _song_df
    if max_time <= 0:
        raise ValueError(f"init_genius: Parameter max_time must be a positive integer")
    if sleep <= 0:
        raise ValueError(f"init_genius: Parameter sleep must be positive")
    for word in exclude:
        if not isinstance(word, str):
            raise ValueError(f"init_genius: Parameter exclude must contain only strings")
    _genius = lg.Genius(token, timeout = max_time, sleep_time = sleep,
                     verbose = display, excluded_terms = exclude)
    if _genius.verbose:
        print('Genius API Client successfully created')

    _dir1.mkdir(exist_ok=True)
    _dir2.mkdir(exist_ok=True)

    # Also load songs from file into _song_df
    try:
        _song_df = pd.read_csv(_dir1 / 'song_data.csv')
    except:
        _song_df = pd.DataFrame()

'''
Change the timeout limit for the Genius API Client.
    new_time : New timeout (in seconds)
'''
def change_genius_timeout(new_time: int) -> None:
    global _genius
    _genius.timeout = new_time
    if _genius.verbose:
        print(f'New timeout limit set to {new_time} seconds')

'''
Change the sleep time for the Genius API Client.
    new_sleep : New sleep time (in seconds)
'''
def change_genius_sleep(new_sleep: float) -> None:
    global _genius
    _genius.sleep_time = new_sleep
    if _genius.verbose:
        print(f'New sleep time set to {new_sleep} seconds')

'''
Turn status messages on/off.
    display : If True, turn messages on; otherwise, turn messages off.
'''
def display_status_messages(display: bool) -> None:
    global _genius
    _genius.verbose = display
    if _genius.verbose:
        print(f'Status messages are now {"ON" if display else "OFF"}')

'''
Change the excluded words list.
    words : New words to exclude.
'''
def change_excluded_words(words: [str]) -> None:
    global _genius
    _genius.excluded_terms = words
    if _genius.verbose:
        print(f'Excluded words changed to: {words}')

'''
Add a word to exclude from title searches.
    word : New excluded word
'''
def add_excluded_word(word: str) -> None:
    global _genius
    _genius.excluded_terms.append(word)
    if _genius.verbose:
        print(f'\"{word}\" will be excluded in searches')

'''
Remove word that is currently excluded (i.e. include it in searches).
    word : New included word
'''
def remove_excluded_word(word: str) -> None:
    global _genius
    try:
        _genius.excluded_terms.remove(word)
        if _genius.verbose:
            print(f'\"{word}\" will be included in searches')
    except ValueError:
        if genius._verbose:
            print(f'\"{word}\" is not currently excluded')    

'''
Find song based on song title and artist name.
    name    : Song title
    artist  : Artist name
'''
def find_song(name: str, artist: str) -> Song:
    song_found = _genius.search_song(name, artist)
    if song_found != None:
        if _genius.verbose:
            print(f'Found {song_found.title} ~~~ {song_found.primary_artist.name}')
        return Song(song_found.title, song_found.primary_artist.name,
                               song_found.lyrics, song_found.id)
    else:
        return None

'''
Save the song to 'song_data.csv' and its lyrics to a separate text file.
    song: Song object to save
'''
def save_song(song: Song) -> None:
    global _song_df
    if song == None:
        if _genius.verbose:
            print('Song cannot be saved (it does not exist)')
            return
    name = utility.keep_alphanum(song.get_name())
    artist = utility.keep_alphanum(song.get_artist())

    lyrics_path = _dir2 / (name+'_'+artist+'.txt')

    with open(lyrics_path, 'w', encoding='utf-8') as file:
        file.write(song.get_lyrics())

    if _genius.verbose:
        print(f'Lyrics of {song} saved in {lyrics_path}')

    storage_path = _dir1 / 'song_data.csv'

    headers = ['Name','Artist','ID','NumSects','WdCnt','UnqWdCnt','UnqWdPct',
               'TotRS','ProxRS','RymDens','LgRymDens','Wd/Sect','Syll/Wd',
               'UnqWd/Sect','RS/Sect','RS/Wd','ProxRS/Sect',
               'ProxRS/Wd','SectSim','LyrStren']

    stat_group = song.get_stat_group()
    stats_as_str = [str(x) for x in stat_group]
    stat_dict = {headers[i] : stats_as_str[i] for i in range(len(headers))}
    
    if not _song_df.empty:
        _song_df.drop(_song_df[_song_df['ID'] == song.get_id()].index,inplace=True)
        if _song_df.empty: # Happens when the only row in the dataframe was of the song to be added
            _song_df = pd.DataFrame()
    _song_df = _song_df.append(stat_dict, ignore_index = True)
    _song_df.to_csv(storage_path, index=False, encoding='utf-8')
   

