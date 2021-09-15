# Song class

import song_utility as sutil

## STATISTICS RECORDED FOR SONGS:
##    - Number of sections (NumSects)
##    - Word count (WdCnt): Number of total words
##    - Unique word count (UnqWdCnt): Number of unique words
##    - Unique word percentage (UnqWdPct): Percentage of total words that are unique
##    - Total rhyme score (TotRS): Sum of all words' rhyme scores
##    - Proximity rhyme score (ProxRS): Sum of words' rhyme scores calculated within a single section
##    - Rhyme density (RymDens): Percent of unique words with rhyme score >= 1
##    - Large rhyme density (LgRymDens): Percent of unique words with rhyme score >= 5
##    - Average section length (Wd/Sect): Number of words per section
##    - Average number of syllables (Syll/Wd): Number of syllables per word
##    - Average number of unique words per section (UnqWd/Sect)
##    - Average section rhyme score (RS/Sect)
##    - Average word rhyme score (RS/Wd)
##    - Average section proximity rhyme score (ProxRS/Sect)
##    - Average word proxmity rhyme score (ProxRS/Wd)
##    - Section similarity (SectSim): Percent of unique words that appear in at least two sections

class Song:
    '''
    Initializes an instance of the Song class.
        song_name   : Song name
        song_artist : Song primary artist
        song_lyrics : Song lyrics
        song_ID     : Song Genius.com ID
    '''
    def __init__(self, song_name: str, song_artist: str, song_lyrics: str, song_ID: str):
        self._name = song_name.replace("’", "'")
        self._artist = song_artist.replace("’", "'")
        self._lyrics = sutil.remove_tag(song_lyrics)
        self._ID = song_ID

        self._sections = sutil.extract_all_sections(self._lyrics)
        self._num_sections = len(self._sections)

        if self._num_sections != 0:
            self._find_stats()
        else:
            self._sections_unique = self._all_words = self._word_count = self._unique_words = \
                self._unique_word_count = self._avg_section_length = self._avg_section_unique_words = \
                self._unique_word_pct = self._section_similarity = self._avg_syllable_count = \
                self._rhyme_dict = self._total_rhyme_score = self._rhyme_density = \
                self._large_rhyme_density = self._avg_section_rhyme_score = self._avg_word_rhyme_score = \
                self._proximity_rhyme_score = self._avg_section_prox_score = self._avg_word_prox_score = None

    '''
    Find stats for the given song.
    '''
    def _find_stats(self) -> None:
        # Need to make everything None if self._num_sections is 0
        self._sections_unique = sutil.find_sections_unique_words(self._sections)
        self._all_words = [word for section in self._sections for line in section for word in line.split()]
        self._word_count = len(self._all_words)
        self._unique_words = set(self._all_words)
        self._unique_word_count = len(self._unique_words)

        self._avg_section_length = round(self._word_count / self._num_sections, 4)
        self._avg_section_unique_words = round(self._unique_word_count / self._num_sections, 4)
        self._unique_word_pct = round(self._unique_word_count / self._word_count, 4)

        self._section_similarity = sutil.find_shared_unique_pct(self._sections, self._sections_unique, self._unique_word_count)
        self._avg_syllable_count = sutil.find_syllables_per_word(self._all_words)

        self._rhyme_dict = sutil.find_rhyme_scores(self._unique_words)
        self._total_rhyme_score = sum(self._rhyme_dict.values())
        self._rhyme_density = round(sum(map(lambda x : self._rhyme_dict[x] >= 1, self._rhyme_dict)) / self._unique_word_count, 4)
        self._large_rhyme_density = round(sum(map(lambda x : self._rhyme_dict[x] >= 5, self._rhyme_dict)) / self._unique_word_count, 4)
        self._avg_section_rhyme_score = round(self._total_rhyme_score / self._num_sections, 4)
        self._avg_word_rhyme_score = round(self._total_rhyme_score / self._unique_word_count, 4)

        self._proximity_rhyme_score = sum(map(lambda x : sum(sutil.find_rhyme_scores(x).values()), self._sections_unique))
        self._avg_section_prox_score = round(self._proximity_rhyme_score / self._num_sections, 4)
        self._avg_word_prox_score = round(self._proximity_rhyme_score / self._unique_word_count, 4)        

    def __str__(self) -> str:
        return f'"{self._name}" by {self._artist}'

    def __eq__(self, other) -> bool:
        if other == None:
            return self._name == None or self._artist == None
        return self._name == other._name and self._artist == other._artist

    ### GETTER METHODS ###
    
    def get_name(self) -> str:
        return self._name

    def get_artist(self) -> str:
        return self._artist

    def get_lyrics(self) -> str:
        return self._lyrics

    def get_id(self) -> str:
        return self._ID

    def get_sections(self) -> [[str]]:
        return self._sections

    def get_sections_unique(self) -> [{str}]:
        return self._sections_unique

    def get_num_sections(self) -> int:
        return self._num_sections

    def get_all_words(self) -> [str]:
        return self._all_words

    def get_word_count(self) -> int:
        return self._word_count

    def get_unique_words(self) -> {str}:
        return self._unique_words

    def get_unique_word_count(self) -> int:
        return self._unique_word_count

    def get_avg_section_length(self) -> float:
        return self._avg_section_length

    def get_avg_syllable_count(self) -> float:
        return self._avg_syllable_count

    def get_avg_section_unique_words(self) -> float:
        return self._avg_section_unique_words

    def get_unique_word_pct(self) -> float:
        return self._unique_word_pct

    def get_section_similarity(self) -> float:
        return self._section_similarity

    def get_rhyme_dict(self) -> {str : float}:
        return self._rhyme_dict

    def get_total_rhyme_score(self) -> float:
        return self._total_rhyme_score

    def get_rhyme_density(self) -> float:
        return self._rhyme_density

    def get_large_rhyme_density(self) -> float:
        return self._large_rhyme_density

    def get_avg_section_rhyme_score(self) -> float:
        return self._avg_section_rhyme_score

    def get_avg_word_rhyme_score(self) -> float:
        return self._avg_word_rhyme_score

    def get_proximity_rhyme_score(self) -> float:
        return self._proximity_rhyme_score

    def get_avg_section_prox_score(self) -> float:
        return self._avg_section_prox_score

    def get_avg_word_prox_score(self) -> float:
        return self._avg_word_prox_score

    '''
    Get the group of statistics relevant to the song.
    '''
    def get_stat_group(self) -> 'List of stats':
        return [self._name, self._artist, self._ID, self._num_sections, self._word_count,
                self._unique_word_count, self._unique_word_pct, self._total_rhyme_score,
                self._proximity_rhyme_score, self._rhyme_density, self._large_rhyme_density,
                self._avg_section_length, self._avg_syllable_count, self._avg_section_unique_words,
                self._avg_section_rhyme_score, self._avg_word_rhyme_score,
                self._avg_section_prox_score, self._avg_word_prox_score, self._section_similarity]
                
   
            
        
