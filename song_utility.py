# song_utility.py

# Utility functions specifically for songs

import utility
import re

'''
Remove ending tag (number followed by EmbedShare URLCopyEmbedCopy) placed
on the last line of lyrics by Genius. Return the resulting string. The
number will either be nonexistent, a single integer (XXXX), a decimal
number (XX.XX), or the previous two followed by a multiplier (K for thousand,
M for million, etc.).
    lyrics: Lyrics to remove the tag from
'''
def remove_tag(lyrics: str) -> str:
    lines = lyrics.split("\n")
    last = lines[-1]
    tag = 'EmbedShare URLCopyEmbedCopy'
    pattern = '([0-9]+(\.[0-9]+)?[KMB]?)?' + tag
    sequence = re.search(pattern, last)
    match = sequence.group(0)
    if match:
        lines[-1] = last[:last.find(match)]
    return '\n'.join(lines)

'''
Returns a list of strings where each string holds the lyrics for a
particular section in the song.
    lyrics : Song lyrics
'''
def extract_all_sections(lyrics: str) -> [[str]]:
    headers = ['verse','chorus','hook','refrain','bridge','pre chorus', 'post chorus']
    sections = []
    section = []
    inside_section = False
    for line in lyrics.split('\n'):
        line = utility.clean_string(line)
        if line == '':
            continue
        if len(line) >= 2 and line[0] == '[' and line[-1] == ']': # [] denotes section start
            for h in headers:
                if line.find(h) == 1: # header should be right after '['
                    inside_section = True
                    break
                else:
                    inside_section = False
            sections.append(section)
            section = []
        # line is not a section header AND we are in a section
        elif inside_section: 
            section.append(line)
    # If song ends on a section, we need to add "section" because it is nonempty
    # If song doesn't end on a section, adding "section" does nothing because
    #   it is empty
    sections.append(section)
    # Return nonempty lists only
    return [s for s in sections if s != []]

'''
Returns a list of sets where each set contains the unique words in a particular section.
    sections : List of sections that contain all words
'''
def find_sections_unique_words(sections: [[str]]) -> [{str}]:
    unique_words = []
    for section in sections: # section is a list of lines
        # ' '.join(section) creates one large string of words
        # split() gets a list of each individual word
        unique_words.append(set(' '.join(section).split()))
    return unique_words


'''
Returns the percentage of unique words that are shared by at least two sections.
    sections        : List of list of strings containing lyrics from each section
    sections_unique : List of unique words in each section
    unique_count    : Number of total unique words in the song
'''
def find_shared_unique_pct(sections: [[str]], sections_unique: [{str}], unique_count: int) -> float:
    shared_words = set()
    for i in range(len(sections_unique)):
        set1 = sections_unique[i]
        for j in range(i+1, len(sections_unique)):
            set2 = sections_unique[j]
            shared_words.update(set1.intersection(set2))
    return round(len(shared_words) / unique_count, 4)

'''
Returns the number of syllables per word in the song.
    words : List of all words in the song
'''
def find_syllables_per_word(words: [str]) -> float:
    return round(sum(utility.syllable_count(word) for word in words) / len(words), 4)

'''
Return a dict with keys being unique words and values being their rhyme scores.
    words : Unique word set of which to find rhyme scores
'''
def find_rhyme_scores(words: {str}) -> {str : float}:
    scores = dict()
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                rhyme_score = utility.pair_rhyme_score(word1, word2)
                scores[word1] = scores.get(word1, 0) + rhyme_score
    return scores
    
