 
from coins import *
import random
 
ALPHABET = 'qwertyuiopasdfghjklzxcvbnm1234567890äéèçæœ'           # äéèçæ gave errors, i had to change the encoding whatever that means
PUNCTUATION = '`~!@#$%^&*()-=_+[]\{}|;\':",./<>? \t\n\r'
ALL_CHARACTERS = ALPHABET + PUNCTUATION
MIN_BASE10_COIN = 0
MAX_BASE10_COIN = 16777215
LETTERS_IN_POPULARITY_ORDER = ' EOTARNLISMHDYFGCWPUBVXK.,\'"-;'
BASE202_CHARS='0C2OMPIN'
 
def get_random_comp202coin(dummy):
    """
    (all)-> str
    Takes a dummy parameter. Returns a random coin value between MIN_BASE10_COIN and MAX_BASE10_COIN
    >>> random.seed(1338)
    >>> get_random_comp202coin([])
    '0cPMO2C2C0'
    >>> get_random_comp202coin('a')
    '0cM2PONOMI'
    >>> get_random_comp202coin(1000)
    '0cNMONO2NI'
    """
    return base10_to_202(random.randint(MIN_BASE10_COIN,MAX_BASE10_COIN))
 
def get_random_character(dummy):
    """
    (all)-> str
    Takes a dummy parameter. Returns a random character in ALL_CHARACTERS
    >>> random.seed(1338)
    >>> get_random_character(0)
    '!'
    >>> get_random_character([])
    '9'
    >>> get_random_character('a')
    '\\\\'
    """             # Doctest reads '\\\\' as only '\\' i guess??? bizzare interaction
                    # If i write '\\' it gets read as '\' and raises an error
    return ALL_CHARACTERS[random.randint(0,len(ALL_CHARACTERS)-1)]
 
def get_letter_of_popularity_order(index):
    """
    (int)->str
    returns the ith letter in LETTERS_IN_POPULARITY_ORDER. Returns str(index) if index is out of range
 
    >>> get_letter_of_popularity_order(5)
    'R'
    >>> get_letter_of_popularity_order(0)
    ' '
    >>> get_letter_of_popularity_order(29)
    ';'
    >>> get_letter_of_popularity_order(30)
    '30'
    >>> get_letter_of_popularity_order(-1)
    Traceback (most recent call last):
    AssertionError: function parameter must be positive integer
    >>> get_letter_of_popularity_order('')
    Traceback (most recent call last):
    AssertionError: function parameter must be positive integer
    """
    if type(index)!=int or index<0:
        raise AssertionError('function parameter must be positive integer')
    try:
        return LETTERS_IN_POPULARITY_ORDER[index]        # I wouldn't do this if i had to worry about performance/speed
    except IndexError:                                   # The alternative is harder to code and harder to read
        return str(index)                                # we essentially try to return the string and if the index is out of bounds
                                                         # we get an index error and return str(index)
def get_unique_elements(my_list):
    """
    (list)->list
    returns all of the unique elements in my_list
    >>> get_unique_elements([])
    []
    >>> get_unique_elements([[],1,2,2,3])
    [[], 1, 2, 3]
    >>> get_unique_elements([[1,1],(1,1),[1],[1,2]])
    [[1, 1], (1, 1), [1], [1, 2]]
    >>> get_unique_elements('a')
    Traceback (most recent call last):
    AssertionError: function parameter must be a list
    """
    if type(my_list)!=list:
        raise AssertionError('function parameter must be a list')
    uniques=[]
    for element in my_list:
        if element not in uniques:          # if element is already in uniques we skip it
            uniques.append(element)         # otherwise we append it
    return uniques
    
def is_base202(string):     # exception handling for this function is done in get_all_coins
    '''
    (str)->bool
    checks if a str is a valid base202 number
    >>> is_base202('20')
    False
    >>> is_base202('0c00000000')
    True
    >>> is_base202('0c00000c0')
    False
    ''' 
    string=string.upper()
    if string[:2]!='0C' or len(string)!=10:
        return False
    for char in string:
        if char not in BASE202_CHARS:
            return False
    return True
 
def get_all_coins(text):
    """
    (str)->list
    finds all instances of comp202coin and returns them as a list in order
 
    >>> get_all_coins('c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c00000000c0c0c0c0c0c0c0c0c0c0')
    ['0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0c0c', '0c0c0c0000', '0c0c0c0c0c', '0c0c0c0c0c']
 
    >>> get_all_coins('0c0MPNN0OC-0cM0OCCIOI-0c0MPNN0OC')
    ['0c0MPNN0OC', '0cM0OCCIOI', '0c0MPNN0OC']
 
    >>> get_all_coins('')
    []
 
    >>> get_all_coins(1)
    Traceback (most recent call last):
    AssertionError: parameter must be a string
    """
    if type(text)!=str:
        raise AssertionError('parameter must be a string')
    coins=[]
    ten=10
    while len(text)>9:              #for a valid coin to exist, there needs to be min 10 chars
        next_block=text[:ten]
        if is_base202(next_block):
            coins.append(next_block)    # if we find a coin, we save it and delete it from text
            text=text[ten:]
        else:
            next_index=max(text.find('0c'),text.find('0C'))
            text=text[1:]                # we eat text character by character to find a coin
    return coins                         # by the gods! this actually worked on the *second try!
 
def reverse_dict(my_dict):
    """
    (dict)->dict
    take a dictionary with unique values and returns another dictionary with the key values swtitched
    
    >>> reverse_dict({'a': 1, 'b': 3, 'd': 7})
    {1: 'a', 3: 'b', 7: 'd'}
 
    >>> reverse_dict({1:1})
    {1: 1}
 
    >>> reverse_dict({})
    {}
 
    >>> reverse_dict(0)
    Traceback (most recent call last):
    AssertionError: parameter must be a dictionary
 
    >>> reverse_dict({0:(),1:[]})
    Traceback (most recent call last):
    AssertionError: dictionary values must be immutable
 
    >>> reverse_dict({1:2,2:3,4:3})
    Traceback (most recent call last):
    AssertionError: dictionary values must be unique
 
    >>> reverse_dict({1:2,2:3,4:5})
    {2: 1, 3: 2, 5: 4}
    """
    if type(my_dict)!=dict:
        raise AssertionError('parameter must be a dictionary')
 
    reverse={}
    for key,value in my_dict.items():
 
        if type(value) in (list,dict):      
            raise AssertionError('dictionary values must be immutable')     # immutability check
        elif value in reverse:
            raise AssertionError('dictionary values must be unique')        # uniqueness check
 
        reverse[value]=key
    return reverse
 
def get_frequencies(my_list):
    """
    (list)->dictionary
    Reaturns a dictionay of each item in the list pointing to the frequency at which it appears in the list.
 
    >>> get_frequencies(['a', 'b', 'c'])
    {'a': 0.3333333333333333, 'b': 0.3333333333333333, 'c': 0.3333333333333333}
 
    >>> get_frequencies([])
    {}
 
    >>> get_frequencies([1,2,2,3])
    {1: 0.25, 2: 0.5, 3: 0.25}
 
    >>> get_frequencies(1)
    Traceback (most recent call last):
    AssertionError: parameter must be a list
 
    >>> get_frequencies([1,2,3,3,[1]])
    Traceback (most recent call last):
    AssertionError: list entries must be hashable
 
    >>> get_frequencies([1,2,3,3,{1:1}])
    Traceback (most recent call last):
    AssertionError: list entries must be hashable
    """
    if type(my_list)!=list:
        raise AssertionError( 'parameter must be a list')   # type check
 
    freq_dict=dict()
    list_length=len(my_list)
    for entry in my_list:
        if type(entry) in (list,dict):
            raise AssertionError( 'list entries must be hashable')  # hashability check
                                                                    
        freq_dict[entry]=freq_dict.get(entry,0)+1                   # if the input is new, we just get 0 from get method
                                                                    # adding 1/list_length here sucks, i did an extra for loop
    for key in freq_dict:
        freq_dict[key]/=list_length
    return freq_dict
    
def sort_keys_by_values(my_dict):
    """
    (dict)->list
    Takes a dictionary with string as keys and numeric values.
    Returns the list of the keys in descending order of numeric values.
    If two keys have the same value, the largest string key appears first
 
    >>> sort_keys_by_values({'mmm': 5, 'zzz': 5, 'abc': 5})
    ['zzz', 'mmm', 'abc']
 
    >>> sort_keys_by_values({'a': 6, 'b': 5, 'c': 5})
    ['a', 'c', 'b']
 
    >>> sort_keys_by_values({})
    []
 
    >>> sort_keys_by_values([])
    Traceback (most recent call last):
    AssertionError: parameter must be a dictionary
 
    >>> sort_keys_by_values({'a': 6, 12: 5, 'c': 5})
    Traceback (most recent call last):
    AssertionError: dictionary keys must be strings
 
    >>> sort_keys_by_values({'a': 6, 'b': '14', 'c': 5})
    Traceback (most recent call last):
    AssertionError: dictionary values must be numeric
    """
    if type(my_dict)!=dict:
        raise AssertionError('parameter must be a dictionary')          # type check
 
    num_str_list=list()
 
    for string, num in my_dict.items():
        if type(string)!=str:
            raise AssertionError('dictionary keys must be strings')     # key check
        if type(num) not in (int, float):
            raise AssertionError('dictionary values must be numeric')     # value check
        
        num_str_list.append((num,string))                       # list of the tuples (value,key) from my_dict
    
    num_str_list.sort()     # sorts in order of first values, if there is a tie, the second values are compared
 
    str_list=[]
 
    for i, string in num_str_list:      # we only care about the second values in the tuples
        str_list.insert(0,string)       # we insert larger entries at the begining of the list, maintaining descending order
 
    return str_list
 
def swap_letters(text, letter1, letter2):
    """
    (str,str,str)->str
    Swaps all instances of letter 1 with letter 2 and vice versa
 
    >>> swap_letters("ABCDEF abcdef", 'a', 'f')
    'ABCDEF fbcdea'
 
    >>> swap_letters("abc", 'a', '')
    Traceback (most recent call last):
    AssertionError: 2nd and 3rd parameters must be single letters
 
    >>> swap_letters("abc", 'a', 'a')
    'abc'
 
    >>> swap_letters("abc", 'd', 'a')
    'dbc'
 
    >>> swap_letters("", 'd', 'a')
    ''
 
    >>> swap_letters("a\\tb\\nc", '\\n', '\\t')
    'a\\nb\\tc'
 
    >>> swap_letters([], 'd', 'a')
    Traceback (most recent call last):
    AssertionError: all parameters must be strings
 
    >>> swap_letters('', 'dd', 'a')
    Traceback (most recent call last):
    AssertionError: 2nd and 3rd parameters must be single letters
    """
    if (type(text),type(letter1),type(letter2)) != (str,str,str):
        raise AssertionError('all parameters must be strings')
    elif (len(letter1),len(letter2))!=(1,1):
        raise AssertionError('2nd and 3rd parameters must be single letters')
    elif letter1== letter2:
        return text
 
    sep_letter1=text.split(letter1)             # use letter1 as a seperator
 
    sep_letter1_and_swap2for1=[]
 
    for substring in sep_letter1:               # swap letters in substrings
        sep_letter1_and_swap2for1.append(substring.replace(letter2,letter1))
 
    return letter2.join(sep_letter1_and_swap2for1)      # insert letter2 where letter1 used to be
 
def get_pct_common_words(text, common_words_filename):
    """
    (str,str)-> float
    opens a file common_words_filename. Returns what percentage of letters in text are in common words.
 
    >>> s = "The quick brown fox jumps over the lazy dog."
    >>> get_pct_common_words(s, 'common_words.txt')
    0.22727272727272727
 
    >>> get_pct_common_words('', 'common_words.txt')
    0.0
 
    >>> s = 'The'
    >>> get_pct_common_words(s, 'common_words.txt')
    1.0
 
    >>> s = 'die sonne scheint'
    >>> get_pct_common_words(s, 'common_words.txt')
    0.0
 
    >>> s = 'The!The,The\The'
    >>> get_pct_common_words(s, 'common_words.txt')
    0.8
 
    >>> get_pct_common_words(74, 'common_words_filename.txt')
    Traceback (most recent call last):
    AssertionError: both parameters must be strings
 
    """
    if (type(text), type(common_words_filename))!=(str,str):
        raise AssertionError('both parameters must be strings')
    if text=='':
        return 0.0                      #catch the ZeroDivisionError
 
    text_len=len(text)
 
    for char in PUNCTUATION:
        text=text.replace(char,' ')     # replace all punctiation with a space character
 
    text=text.lower()
    
    text_list = text.split(' ')
    
    common_chars_counter=0
 
    try:                                            # if anything goes wrong after opening, we must close the file!
        common_words=open('common_words.txt','r')
        common_words_list=[]
        for word in common_words:
            common_words_list.append(word.strip())                  # remove /n and spaces if any
 
        for word in text_list:
            if word in common_words_list:
                common_chars_counter+=len(word)         # if the word is common, we count all of its characters
 
        return common_chars_counter/text_len
 
    finally:
        common_words.close()
 
        # the following functions are used for testing purposes
 
def tester_rand1_3(dummy):
	"""
	(any)->int
	returns a random integer between 1 and 3. made for testing purposes.
 
	>>> random.seed(0)
	>>> tester_rand1_3('')
	'2'
	>>> tester_rand1_3([])
	'2'
	>>> tester_rand1_3(5)
	'1'
	"""
	return str(random.randint(1,3))
 
def tester_index(index):
	"""
	(any)->str
	Returns the given parameter as a string. Returns the index in get_crypt_dictionary.
 
	>>> tester_index('')
	''
	>>> tester_index([])
	'[]'
	>>> tester_index(5)
	'5'
	"""
	return str(index)
 
def tester_return_1(dummy):
	"""
	(any)->aint
	Returns 1
 
	>>> tester_return_1('')
	1
	>>> tester_return_1([])
	1
	>>> tester_return_1(5)
	1
	"""
	return 1