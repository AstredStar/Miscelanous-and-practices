import random
from farkle_utils import *
 
 
SINGLE_ONE = 100
SINGLE_FIVE = 50
TRIPLET_MULTIPLIER = 100
STRAIGHT = 3000
THREE_PAIRS = 1500
 
def compute_score(dices): #the most straight forward way is to write a series of if statements.
    '''
    (list)->int
    takes a list of dice rolls and computes the score that should be given to the player
    >>>  compute_score([])
    0
    >>>  compute_score([1,2,3,4,5,6])
    3000
    >>>  compute_score([1,1,5,5])
    0
    >>>  compute_score([1,2,2,3,4,5])
    150
    '''
    score=0
    l=dices[:] #i dont want to risk some wierd interaction
    if len(l)>=6:
        if contains_all(l):
            return STRAIGHT
        
        elif count_num_of_pairs(l)>=3:
            return THREE_PAIRS
    
    i=1
    triple=[i]*3
    if is_included(l,triple):
        score+=10*TRIPLET_MULTIPLIER #doing 1 seperately is easier
    i=1
    triple=[i]*3
    if is_included(l,triple):
        score+=10*TRIPLET_MULTIPLIER #i am repeating this for a degub
        
    for i in range(6,1,-1): #the order is not important, im just doing largest score to smallest for my code
        triple=[i]*3
        if is_included(l,triple):
            l=get_difference(l,triple)
            score+=i*TRIPLET_MULTIPLIER
            
    for i in range(6,1,-1): #i am repeating this for a debug
        triple=[i]*3
        if is_included(l,triple):
            l=get_difference(l,triple)
            score+=i*TRIPLET_MULTIPLIER
    
    
    score+=SINGLE_ONE*l.count(1)
    score+=SINGLE_FIVE*l.count(5)
  
    return score
         
def get_winners(scorelist,limit):
    '''
    (list,num)->list
    returns the list of the winners. Highest scoring if multiple.
    >>>  get_winners([0], 0)
    [1]
    >>>  get_winners([1,2,3,4,5], 40)
    []
    >>>  get_winners([1,2,3,600,600], 500)
    [4, 5]
    '''
    l=scorelist[:]
    highest=max(l)
    winners=[]
    if highest>=limit:
        number_of_winners=l.count(highest)
        i=0
        for j in range(number_of_winners):
            i+=1+l[i:].index(highest)
            winners+=[i]
    return winners
 
def play_one_turn(p):
    '''
    (int)-> int
    initates a single round of farkle for player number p
    returns their winnings
    '''
    print("Player "+str(p)+" it's your turn!\n")
    leftdice=6
    current_score=0
    roll_pass=input('What would you like to do? (roll/pass): ').lower()
    
    while roll_pass=='roll':
        roll_list=dice_rolls(leftdice)
        print("Here's the result of rolling your "+str(leftdice)+" dice: "+str(roll_list).strip('[]'))
        remove_dice=input("Please select the dice you'd like to set aside for scoring: ").split()
        
        for i in range(len(remove_dice)):
            remove_dice[i]=int(remove_dice[i])
            
        remove_dice.sort()
        roll_list.sort()
        
        while remove_dice!=[]: #this looks horrible but it works
            if roll_list==remove_dice:
                roll_list=[]
                count_dice=remove_dice
                remove_dice=[]
            else:
                if get_difference(roll_list,remove_dice)==[]:
                    remove_dice=input('You do not have these dice. Select again: ').split()
                    for i in range(len(remove_dice)):
                        remove_dice[i]=int(remove_dice[i])
                    continue
                roll_list=get_difference(roll_list,remove_dice)
                count_dice=remove_dice
                remove_dice=[] #all of this for input validation
                
        added_score=compute_score(count_dice)
        leftdice=len(roll_list)
        
        if added_score==0:
            print('FARKLE! All the points accumulated up to now are lost')
            current_score=0
        
        elif leftdice==0:
            print('HOT DICE! You are on a roll. You get all six dice back.')
            leftdice=6
        
        current_score+=added_score
        print('Your current score this turn is: '+str(current_score))
        
        print('You have '+str(leftdice)+' dice to keep playing\n')
        
        roll_pass=input('What would you like to do? (roll/pass): ').lower()
    
    return current_score
 
def play_farkle():
    '''
    void->void
    
    initiates a game of farkle
    asks for the number of players and for a score limit
    
    Once the limit is reached, the game stops and the winner is announced.
    '''
    
    print('Welcome to COMP202_Farkle\n')
    player_number=input('Please select the number of players (2-8): ')
    
    while not player_number.isdecimal() or int(player_number) not in range(2,9):
        player_number=input('Please select a valid number of players (2-8): ')
    
    player_number=int(player_number)
    
    limit=input('Select the winning score for this game: ')
    
    while not limit.isdecimal() or int(limit)<=0:
        limit=input('Please select a valid winning score: ')
        
    limit=int(limit)
    
    score_list=[0]*player_number
    winner_list=get_winners(score_list,limit)
    round_counter=0
    print()
    while winner_list==[]:
        round_counter+=1
        for i in range(player_number):
            score_list[i]+=play_one_turn(i+1)
        print()
        print('After round '+str(round_counter)+' the scores are as follows:')
        for i in range(player_number):
            print('Player '+str(i+1)+' : '+str(score_list[i]))
            
        winner_list=get_winners(score_list,limit)
        print()
    
    print('Thank you for playing! The winner of this game is: Player'+str(pick_random_element(winner_list)))