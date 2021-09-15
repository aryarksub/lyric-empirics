# utility.py

# General utility functions

import unicodedata
import pronouncing
import math
import syllables

'''
Return the given string with only alphanumeric characters.
    text : Original string
'''
def keep_alphanum(text: str) -> str:
    return ''.join(x for x in text if x.isalnum())

'''
Returns the cleaned version of a string by:
  - Making it lowercase
  - Keeping alphanumeric characters, middle-of-word apostrophes, and brackets []
  - Removing starting/ending apostrophes
  - Turning periods, hypens, and em dashes into spaces (they are word separators)
  - Turning '&' into 'and'
  - Removing all accents
    string : The string to clean
'''
def clean_string(string: str) -> str:
    string = string.lower().strip()
    words = string.split()
    new_words = []
    for word in words:
        new_word = ''
        for i in range(len(word)):
            c = word[i]
            if c.isalnum() or c == '[' or c == ']':
                new_word += c
            elif c == '\'':
                # Keep apostrophes that are not at the start/end of a word
                if i != 0 and i != len(word) - 1:
                    new_word += c
            elif c == '.' or c == '-' or c == '—':
                # Turn periods, hyphens, and em dashes into spaces
                new_word += ' '
            elif c == '&':
                new_word += 'and'
        new_words.append(new_word)
    new_str = ' '.join(new_words).strip()
    # Normalize unicode string
    nfkd_form = unicodedata.normalize('NFKD', new_str)
    # Encode into ASCII (remove accents)
    encoded = nfkd_form.encode('ascii', 'ignore')
    # Return string without accents
    return str(encoded.decode('utf-8'))

'''
Returns True if there is a vowel in word; False otherwise.
    word : String to check for vowels
'''
def vowel_in_word(word: str) -> bool:
    for vowel in ['A', 'E', 'I', 'O', 'U']:
        if vowel in word or vowel.lower() in word:
            return True
    return False

'''
Return the rhyme score of a pair of word (calculation described in comments).
    word1 : First word
    word2 : Second word
'''
def pair_rhyme_score(word1: str, word2: str) -> float:
    # Ignore pairs of words that are the same
    if word1 == word2:
        return 0

    rhymes_list1 = pronouncing.rhymes(word1) # words that rhyme with word1
    rhymes_list2 = pronouncing.rhymes(word2) # words that rhyme with word2
    if word1 in rhymes_list2 or word2 in rhymes_list1:
        # Rhyme score = 1 for perfect rhyme (determined by pronouncing package)
        return 1.0

    max_rhyme_score = 0

    # All pronunciations for words
    phones_for_word1 = pronouncing.phones_for_word(word1)
    phones_for_word2 = pronouncing.phones_for_word(word2)

    # Iterate through each pair of word pronunciations
    for i in range(len(phones_for_word1)):
        for j in range(len(phones_for_word2)):
            # Initialize phonemes1 at start of 2nd loop because its value changes
            # during this loop and we want to reset it before starting again
            phonemes1 = phones_for_word1[i]
            phonemes2 = phones_for_word2[j]

            # List with fewer phonemes is first (phonemes1)
            if len(phonemes1) > len(phonemes2):
                phonemes1, phonemes2 = phonemes2, phonemes1
            
            # Remove stress numbers from phonemes
            phonemes1 = [''.join([x for x in phoneme if x.isalpha()]) for phoneme in phonemes1.split()]
            phonemes2 = [''.join([x for x in phoneme if x.isalpha()]) for phoneme in phonemes2.split()]

            # If phonemes1 has 1 or 2 phonemes, it is either part of a perfect rhyme
            # (if its ending phoneme is the ending phoneme for phonemes2) or not.

            # If phonemes1 has 1 phoneme, it is part of a perfect rhyme if phonemes2
            # ends with the same phoneme and the phoneme is a "vowel" phoneme (the phoneme
            # contains a vowel). Otherwise, it is not part of any rhyme (perfect or not).
            if len(phonemes1) == 1:
                if vowel_in_word(phonemes1[0]) and phonemes1[0] == phonemes2[-1]:
                    return 1
                return 0

            # If phonemes1 has 2 phonemes, it is part of a perfect rhyme if phonemes2
            # ends with the same phoneme and the phoneme is a "vowel" phoneme, or
            # phonemes1 is the ending of phonemes2. Otherwise, it is not part of any rhyme.
            if len(phonemes1) == 2:
                if vowel_in_word(phonemes1[1]) and phonemes1[1] == phonemes2[-1]:
                    return 1
                if phonemes2[-2:] == phonemes1:
                    return 1
                return 0
            
            # If phonemes1 has n > 2 phonemes, a perfect rhyme requires the ending ceil(n/2)
            # phonemes to match in phonemes1 and phonemes2 (perfect rhyme : rhyme score = 1)
            # If a perfect rhyme doesn't exist, use ending lists of phonemes of size
            # ceil(n/2) - 1, ceil(n/2) - 2, ..., 2 and subtract 0.25 from the rhyme score
            # at each step ... Formula = 1 - 0.25*(ceil(n/2) - k) where 0 <= k <= ceil(n/2)
            # If the ending X phonemes do not match, check if the ending X phonemes from
            # phonemes1 match with any sequence of X phonemes in phonemes2. If they do, then
            # the rhyme score is 1/4 of what it would have been
            # i.e. Formula = (1 - 0.25*(ceil(n/2) - k)) / 4
            max_sub_len = math.ceil(len(phonemes1) / 2)
            sub_len = max_sub_len
            end_val = 2
            while sub_len >= end_val:
                phoneme_sub1 = phonemes1[-sub_len : ]
                phoneme_sub2 = phonemes2[-sub_len : ]
                if phoneme_sub1 == phoneme_sub2 and vowel_in_word(phoneme_sub1):
                    temp = 1 - 0.25*(max_sub_len - sub_len)
                else:
                    temp = 0
                for k in range(0, len(phonemes2) - sub_len + 1):
                    if phoneme_sub1 == phonemes2[k : k + sub_len] and vowel_in_word(''.join(phoneme_sub1)):
                        temp = (1 - 0.25*(max_sub_len - sub_len)) / 4
                        break
                else:
                    temp = 0
                max_rhyme_score = max(max_rhyme_score, temp)
                sub_len -= 1
    
    return max_rhyme_score

'''
Return (estimated) number of syllables in a word.
    word : String for counting syllables
'''
def syllable_count(word: str) -> int:
    return syllables.estimate(word)

    

    
