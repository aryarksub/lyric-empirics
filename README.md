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
    - To change this setting, call `change_genius_timeout(new_time)` with a positive integer value as a parameter

        ```python
        lyremp.change_genius_timeout(20)
        ```

2. Sleep: The minimum amount of time to wait between consecutive requests
    - Default is 0.2 seconds
    - To change this setting, call `change_genius_sleep(new_sleep)` with a positive decimal (float) value as a parameter

        ```python
        lyremp.change_genius_sleep(0.5)
        ```

3. Excluded Words: A list of words to ignore when attempting to find song matches when searching through titles
    - The client will, by default, exclude live performances (the term "(Live)" is excluded)
    - To use a new list of excluded strings, call `change_excluded_words(words)` with the desired list of strings as a parameter

        ```python
        lyremp.change_excluded_words(["(Remix)", "(Skit)"])
        ```

    - To add a single string to exclude, call `add_excluded_word(word)` with the desired string to exclude as a parameter

        ```python
        lyremp.add_excluded_word("(Live)")
        ```
        
    - To remove a string from the excluded list, call `remove_excluded_word(word)` with the desired string to include as a parameter

        ```python
        lyremp.remove_excluded_word("(Skit)")
        ```

### Extracting Statistics
stats
