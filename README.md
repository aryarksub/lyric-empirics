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
client = lyremp.init_genius(access_token)
```
You must provide an access token in order for `init_genius` to successfully initialize the Genius API client. As mentioned in [Setup](#Setup), this token will be unique to your Genius.com account.

### Working with Genius
genius

### Extracting Statistics
stats
