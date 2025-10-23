 
def is_valid_universe(matrix):
    """
    (list)-> bool
    Receives an 2d list and returns if it is a valid universe.
    Returns True only for nxm Matrices with imputs 1 or 0
 
    >>> a = [[0,  0],  [1,  0],  [1,  0]]
    >>> is_valid_universe(a)
    True
 
    >>> a = [[0, 0],  [0, 0],  [0, 0]]
    >>> is_valid_universe(a)
    True
 
    >>> a = [[]]
    >>> is_valid_universe(a)
    True
 
    >>> a = [[0,  0],  [1,  12],  [1,  0]]
    >>> is_valid_universe(a)
    False
 
    >>> a = [[0,  0],  [1,  0],  [1, 0, 0]]
    >>> is_valid_universe(a)
    False
    """
 
    row_length=len(matrix[0])   # we use this to make sure all rows have same length
                                # column height is always equal
    for row in matrix:
        if type(row)!=list or len(row)!=row_length:
            return False
 
        for element in row:
            if element not in (0,1):    # Here we check if the inputs are 0 or 1
                return False
 
    return True
 
def universe_to_str(matrix):
    """
    (list)->str
    Represents the given universe as a string
 
    >>> block = [[0, 0, 0, 0],  [0, 1, 1, 0],  [0, 1, 1, 0],  [0, 0, 0, 0]]
    >>> str_block = universe_to_str(block)
    >>> print(str_block)
    +----+
    |    |
    | ** |
    | ** |
    |    |
    +----+
 
    >>> block = [[]]
    >>> str_block = universe_to_str(block)
    >>> print(str_block)
    ++
    ||
    ++
 
    >>> block = [[1]]
    >>> str_block = universe_to_str(block)
    >>> print(str_block)
    +-+
    |*|
    +-+
    """
    width=len(matrix[0])
    representation='+'+'-'*width+'+\n'  #top
 
    for row in matrix:              # body
        row_str=row[:]              # copy row
 
        for index,element in enumerate(row_str):          #replace 1 with '*' and 0 with ' '
            if element==0:
                row_str[index]=' '
            else:
                row_str[index]='*'
 
        representation+='|'+''.join(row_str)+'|\n'        #add to the representation
 
    return representation+'+'+'-'*width+'+'     #add bottom
 
 
def count_live_neighbors(matrix,i,j):    # We refer to the (i,j)th entry in the matrix, by convention in linear algebra
    """
    (list,int,int)->int
    Receives as input a universe and a position i,j. ie row number i (starting from 0) and column j (starting from 0)
    looks at the cell at position i,j and returns the number of live neighboors
 
    >>> beehive = [[0, 0, 0, 0, 0, 0], \
                   [0, 0, 1, 1, 0, 0], \
                   [0, 1, 0, 0, 1, 0], \
                   [0, 0, 1, 1, 0, 0], \
                   [0, 0, 0, 0, 0, 0]]
    >>> count_live_neighbors(beehive,  1,  3)
    2
 
    >>> beehive = [[1]]
    >>> count_live_neighbors(beehive,0,0)
    0
 
    >>> beehive = [[1,1],\
                   [1,1]]
    >>> count_live_neighbors(beehive,0,0)
    3
    """
    width=len(matrix[0])
    height=len(matrix)
    neighbours=-matrix[i][j]        # we subtract the value at ij because we will be adding it back later
 
    for row_num in range(max(i-1,0),min(i+2,height)):          # row_num= (i-1 , i , i+1) excluding invalid indices
        for column_num in range(max(j-1,0),min(j+2,width)):    # column_num= (j-1 , i , j+1) excluding invalid indices
            neighbours+=matrix[row_num][column_num]     
 
    return neighbours
 
def get_next_gen_cell(matrix,i,j):  # We refer to the (i,j)th entry in the matrix, by convention in linear algebra
    """
    (list,int,int)-> int
    For a given cell at position i,j in a given universe, returns the value of that cell in the nexr generation
 
    >>> beehive =   [[0, 0, 0, 0, 0, 0],\
                     [0, 0, 1, 1, 0, 0],\
                     [0, 1, 0, 0, 1, 0],\
                     [0, 0, 1, 1, 0, 0],\
                     [0, 0, 0, 0, 0, 0]]
    >>> get_next_gen_cell(beehive,  1,  3)
    1
 
    >>> beehive = [[1]]
    >>> get_next_gen_cell(beehive,  0,  0)
    0
 
    >>> beehive = [[1,1],\
                   [1,1]]
    >>> get_next_gen_cell(beehive,  0,  0)
    1
    """
    neighbours=count_live_neighbors(matrix,i,j)
    current_cell=matrix[i][j]                   # No need for this var, but makes it more readable
 
    if neighbours == 3 or (current_cell,neighbours)==(1,2):
        return 1
    return 0
 
 
def get_next_gen_universe(matrix):
    """
    (list)->list
    Given a universe, it will return the same universe in the next generation.
    >>> pentadec =  [[0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 1, 0, 1, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 1, 0, 1, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> pentadec_gen2 = get_next_gen_universe(pentadec)
    >>> pentadec_gen2[0:3]
    [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
 
    >>> gen1=[[1]]
    >>> gen2=get_next_gen_universe(gen1)
    >>> gen2
    [[0]]
 
    >>> gen1=[[1,1],[1,1]]
    >>> gen2=get_next_gen_universe(gen1)
    >>> gen2
    [[1, 1], [1, 1]]
    """
    deepcopy=[]                     # -mom, can we have copy.deepcopy
    for row in matrix:              # -No, we have copy.deepcopy at home
        deepcopy.append(row[:])     # <= *copy.deepcopy at home...
 
    # in hindsight i never needed to make a deep copy, i will not fix this. Hope you laughed at my subpar joke.
 
    for i,row in enumerate(deepcopy):       # Replace every cell in deepcopy with the next gen cell from matrix
        for j in range(len(row)):
            row[j]=get_next_gen_cell(matrix,i,j)
 
    return deepcopy
 
def get_n_generations(matrix,n):    # here, n refers to n, hence the name get_n_generations
    """
    (list,int)-> list
    Given a universe and an integer n, returns the string representaion of the first n generations produced.
    If the universe repeats it self before reaching n generations, the function stops there and returns the list as is.
 
    >>> pentadec =  [[0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 1, 0, 1, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 1, 0, 1, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],\
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> g = get_n_generations(pentadec, 20)
    >>> len(g)
    15
 
    >>> g = get_n_generations([[1]], 5)
    >>> len(g)
    2
    >>> print(g[1])
    +-+
    | |
    +-+
 
    >>> g = get_n_generations([[1,1],[1,1]], 5)
    >>> len(g)
    1
    >>> print(g[0])
    +--+
    |**|
    |**|
    +--+
    """
    if (type(matrix),type(n))!=(list,int):
        raise TypeError
    elif not is_valid_universe(matrix):
        raise ValueError
 
    current_generation=matrix
    generations=[]
 
    for i in range(n):
        current_string=universe_to_str(current_generation)
        if current_string in generations:                   # if the current generation is already in the list then the pattern
            break                                           # is sure to repeat it self. we stop the loop
        generations.append(current_string)
 
        current_generation=get_next_gen_universe(current_generation)
    
    return generations