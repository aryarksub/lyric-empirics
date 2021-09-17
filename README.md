# LyricEmpirics
`lyric-empirics` provides users with a way to view song lyrics (from [Genius.com](https://www.genius.com)) and statistics based on rhymes.

## Setup
To use `lyric-empirics`, it is necessary to [create a free Genius.com account](https://genius.com/signup) that allows access to the Genius API used by this package. You will be provided with an access token that must be entered when using this package (see this project's [Usage](#Usage) section for further instructions).

## Installation
Python 3 is required to install this package. Use the following command:

```bash
pip install lyric-empirics
```

## Usage
There are two ways to use `lyric-empirics`: interfacing with the Genius API client and obtaining song statistics. In either case, the first step is to import this package and initialize the API client as follows:

```python
import lyric-empirics as lyremp
lyremp.init_genius(token)
```
You must provide an access token in order for `init_genius()` to successfully initialize the Genius API client. As mentioned in [Setup](#Setup), this token will be unique to your Genius.com account.

### Working with Genius
Interaction with the Genius API client can be done by either adjusting its settings or finding/saving songs. The following settings can be changed and examples are provided for clarity.

1. Timeout: The maximum amount of time taken to process a request
    - Default is 10 seconds
    - To change this setting, call `change_genius_timeout()` with a positive integer value as a parameter

        ```python
        lyremp.change_genius_timeout(20)
        ```

2. Sleep: The minimum amount of time to wait between consecutive requests
    - Default is 0.2 seconds
    - To change this setting, call `change_genius_sleep()` with a positive decimal (float) value as a parameter

        ```python
        lyremp.change_genius_sleep(0.5)
        ```

3. Excluded Words: A list of words to ignore when attempting to find song matches when searching through titles
    - The client will, by default, exclude live performances (the term "(Live)" is excluded)
    - To use a new list of excluded strings, call `change_excluded_words()` with the desired list of strings as a parameter

        ```python
        lyremp.change_excluded_words(["(Remix)", "(Skit)"])
        ```

    - To add a single string to exclude, call `add_excluded_word()` with the desired string to exclude as a parameter

        ```python
        lyremp.add_excluded_word("(Live)")
        ```
        
    - To remove a string from the excluded list, call `remove_excluded_word()` with the desired string to include as a parameter

        ```python
        lyremp.remove_excluded_word("(Skit)")
        ```
        
The Genius API client is automatically set up to display status messages when settings are changed or songs are found/saved. It is highly recommended to leave this setting turned on, but to turn off these messages, call `display_status_messages()` with a boolean that evaluates to `False`. The opposite can be done by providing a boolean that evaluates to `True`.

```python
lyremp.display_status_messages(False) # Turn status messages OFF
lyremp.display_status_messages(True)  # Turn status messages ON
```

To find a song, it is necessary to provide both its name and the artist when calling `find_song()`. The function will return a `Song` object that can later be used to extract statistics (continue [below](#Extracting-Statistics) for more information). The song returned is the one that most closely matches the given information, either in its title or lyrics. To obtain the most accurate match possible, provide the song's name and artist in their entirety. If no match is found, the function will return `None`.

```python
song = lyremp.find_song('rainmaker', 'bugzy') # Result: 'The Rainmaker' by Bugzy Malone
```

To save a song, call `save_song()` with a `Song` object as a parameter. The song's statistics will be saved to `song_data.csv` (located in the `LyricEmpiricsStorage` directory which is created in the current working directory). The song's lyrics will be saved to a file with an easily identifiable title in the `SongLyrics` directory (located within the `LyricEmpiricsStorage` directory). 

```python
song = lyremp.find_song('infinite', 'eminem') # Result: 'Infinite' by Eminem
lyremp.save_song(song) # Lyrics stored in Infinite_Eminem.txt
```

### Extracting Statistics
stats
