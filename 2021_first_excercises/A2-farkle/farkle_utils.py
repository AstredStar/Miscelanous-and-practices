 
import random
 
def single_dice_roll():
    '''
    void->int
    generates a random number between 1 and 6
    >>>random.seed(1)
    >>>single_dice_roll()
    2
    >>> random.seed(2)
    >>> single_dice_roll()
    1
    >>> random.seed(3)
    >>> single_dice_roll()
    2
    '''
    return random.randint(1,6) #do i really need a whole function for this?
 
def dice_rolls(n):
    '''
    (num)->list
    generates a list with n dice rolls
    >>>random.seed(1)
    >>> dice_rolls(1)
    [2]
    >>> dice_rolls(4)
    [5, 1, 3, 1]
    >>> dice_rolls(6)
    [4, 4, 4, 6, 4, 2]
    '''
    rolls=[]
    for i in range(n):
        rolls+=[single_dice_roll()]
    return rolls
 
def contains_repetitions(l, n, m):
    '''
    >>>  contains_repetitions([1, 1, 1, 1, 1, 1], 1, 7)
    False
    >>>  contains_repetitions([1, 1, 1, 1, 1, 1], 1, 6)
    True
    >>>  contains_repetitions([], 1, 0)
    True
    '''
    for i in l:
        if i==n:
            m-=1
    return m<=0
 
def pick_random_element(l):
    '''
    (list)-> anything
    returns a random element in the given list
    >>>  pick_random_element([])
    >>> random.seed(1)
    >>> pick_random_element([1,2,3,4,5,6])
    2
    >>> pick_random_element(['lettuce','tomatoes','toes',['list']])
    'lettuce'
    '''
    if l==[]:
        return None
    return l[random.randint(0,len(l)-1)]
 
def contains_all(l):
    '''
    (list)-> bool
    Checks if the list has a straight starting from 1
    >>>  contains_all([])
    True
    >>>  contains_all([1,2,3,4,5])
    True
    >>>  contains_all([0,1,2,3,4,5])
    False
    '''
    for i in range(1,len(l)+1):
        if i not in l:
            return False
    return True
 
def count_num_of_pairs(mylist):
    '''
    (list)->int
    returns the number of instances of pairs in the list
    >>>  count_num_of_pairs([1, 1, 1, 2, 2, 1, 1])
    3
    >>>  count_num_of_pairs([1, 1, 1, 1, 1])
    2
    >>>  count_num_of_pairs([])
    0
    '''
    l=mylist[:]
    count=0
    while l>[]:
        num=l.pop(0) #this is so much better than using contains_repetitions
        if num in l:
            count+=1
            l.remove(num)
        
    return count
 
def is_included(biglist,sublist):
    '''
    (list,list)->bool
    >>>  is_included([6, 4, 4, 2, 6, 3], [4, 4, 6, 6])
    True
    >>> is_included([],[])
    True
    >>> is_included([1],[1])
    True
    '''
    l=biglist[:]
    for i in sublist:
        if i not in l:
            return False
        l.remove(i)
    return True
 
def get_difference(biglist,sublist):
    '''
    (list,list)->list
    returns a list that would complete the sublist into the biglist
    >>>  get_difference([1, 2, 3, 4, 5], [2, 4])
    [1, 3, 5]
    >>>  get_difference([], [])
    []
    >>>  get_difference([], [1])
    []
    >>>  get_difference([2,3], [])
    [2, 3]
    '''
    if not is_included(biglist,sublist):
        return []
    l=biglist[:]
    for i in sublist:
        l.remove(i)
    return l