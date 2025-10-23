BASE8_CHARS='01234567'
BASE202_CHARS='0C2OMPIN'
#everything here is very straight forward
#no real comments 
 
def base10_to_202(n):
    '''
    (num)->str
    converts a number to base 202
    >>>base10_to_202(50)
    '0c000000I2'
    >>>base10_to_202(0)
    '0c00000000'
    >>>base10_to_202(454)
    '0c00000N0I'
    '''
    n=oct(n)
    n=n[2:]
    for i in range(1,8):
        if i==2:
            continue
        n=n.replace(BASE8_CHARS[i],BASE202_CHARS[i])
        
    return '0c'+'0'*(8-len(n))+n
 
def base202_to_10(c):
    '''
    (str)->int
    converts base202 to decimal
    >>> base202_to_10('0c00000OC2')
    202
    >>> base202_to_10('0c000IIOC2')
    27850
    >>> base202_to_10('0c00000000')
    0
    '''
    c=c[2:]
    c=c.upper()
    for i in range(1,8):
        if i==2:
            continue
        c=c.replace(BASE202_CHARS[i],BASE8_CHARS[i])
    return int(c,8)
 
def is_base202(s):
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
    s=s.upper()
    if s[:2]!='0C' or len(s)!=10:
        return False
    for i in s:
        if i not in BASE202_CHARS:
            return False
    return True
    
def get_nth_base202_amount(s, n):
    '''
    (str)->str
    finds the nth base202 integer
    >>> get_nth_base202_amount('0c00000000ccccccc0c22222222',2)
    ''
    >>> get_nth_base202_amount("BANKING TRANSACTIONS....PLANET ORION......FEBRUARY \15, 3019.......0cCCMMPP22........FEBRUARY 16,
    3019..........0cOCOCOCOC.........\FEBRUARY 17, 3019..........0C24242412", 0)
    '0cCCMMPP22'
    >>> get_nth_base202_amount('0c00000000ccccccc0c22222222',1)
    '0c22222222'
    '''
    for i in range(len(s)-9):
        possible=s[i:i+10]
        if is_base202(possible):
            if n==0:
                return possible
            else:
                s=s[:i]+s[i+10:]
                n-=1
    return ''
 
def get_total_dollar_amount(s):
    '''
    (str)->int
    takes a string, finds all instances of base202 numbers and adds them up to return an integer
    >>> get_total_dollar_amount("BANKING TRANSACTIONS....PLANET ORION......FEBRUARY\15, 3019.......0cCCMMPP22........FEBRUARY 16,
    3019..........0cOCOCOCOC........\FEBRUARY 17, 3019..........0C24242412")
    9167275
    >>> get_total_dollar_amount('0c00000000ccccccc0c22222222')
    4793490
    >>> get_total_dollar_amount('henlo')
    0
    '''
    i=0
    d=0
    c=get_nth_base202_amount(s, i)
    while c!='':
        d+=base202_to_10(c)
        i+=1
        c=get_nth_base202_amount(s, i)
    return d
    
def reduce_amounts(s,l):
    '''
    (str,int)->str
    adds all comp202 amounts in a string. if the sum is greater than the limit, will reduce the comp202 amounts in the string
    by the difference.
    >>>reduce_amounts("0cCCMMPP22  0cOCOCOCOC", 9000000)
    '0cCCOCMCI0  0cO0NOPNCN'
    reduce_amounts('0c00000000ccccccc0c22222222',900000)
    '0c00000000ccccccc0c0OOOPIM0'
    >>> reduce_amounts('danny phantom had 0c1234567',1)
    'danny phantom had 0c1234567'
    '''
    total = get_total_dollar_amount(s)
    if total>l:
        ratio=l/total
        i=0
        index=0
        c=get_nth_base202_amount(s, i)
        while c!='':
            reduced_c=base10_to_202(int(ratio*base202_to_10(c)))
            index=s.find(c,index)
            s=s[:index]+reduced_c+s[index+10:]
            i+=1
            c=get_nth_base202_amount(s, i)
    return s
#everything seems to work very smoothly here