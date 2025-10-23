SUN1_SET= False
SUN2_SET= True
SOLAR_OBSERVATION_FEE_MULTIPLIER= 0.05
COMP202COIN_FLAT_FEE= 10
COMP202COIN_DOLLAR_EXCHANGE_RATE= 0.05
DOLLAR_COMP202COIN_EXCHANGE_RATE= 0.01
COMP202COIN_SUPPLY= "64"
 
def display_welcome_menu():
    """
    () --> None
    
    displays the welcome menu when run
    
    >>> display_welcome_menue()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars
    3. Exit program
    
    """
    print("""Welcome to the Orion IX COMP202COIN virtual exchange machine.
Available options:
1. Convert dollars into COMP202COIN
2. Convert COMP202COIN into dollars
3. Exit program\n""")
#adding indentation ^up here^ messes up the printed string
    
 
def get_solar_observation_fee(amount_of_comp202coin):
    """
    (str)->(float)
    
    Checks if both suns are down and returns the observation fee in dollars if there is no sun
    
    >>>SUN1_SET,SUN2_SET=0,1
    >>>get_solar_observation_fee('555')
    0
    >>>SUN1_SET,SUN2_SET=1,1
    >>>get_solar_observation_fee('555')
    68.25
    >>>SUN1_SET,SUN2_SET=1,1
    >>>get_solar_observation_fee('0')
    0
    """
    if SUN1_SET and SUN2_SET:
        #I should round this to 2 decimals but i dont need to given 0.05 exchange rate
        return int(amount_of_comp202coin,16)*SOLAR_OBSERVATION_FEE_MULTIPLIER
    return 0
 
def get_flat_fee():
    """
    (void) -> num
    
    returns the value of COMP202COIN_FLAT_FEE
    
    >>>COMP202COIN_FLAT_FEE=0
    >>>get_flat_fee()
    0
    
    >>>COMP202COIN_FLAT_FEE=12.5
    >>>get_flat_fee()
    12.5
    
    >>>COMP202COIN_FLAT_FEE=10
    >>>get_flat_fee()
    10
    """
    #What is the point of this function? why did i have to write a docstring for this?
    return COMP202COIN_FLAT_FEE
 
def convert_COMP202COIN_to_dollars(amount_of_comp202coin):
    """
    (str) -> (float)
    
    converts COMP202COIN into dollars and subtracts the fees. May return negative values.
    
    >>>convert_COMP202COIN_to_dollars('0')
    -10.0
    
    >>> convert_COMP202COIN_to_dollars('dad')
    165.05
    
    >>> convert_COMP202COIN_to_dollars('1')
    -9.95
    """
    decimal_com202coin=int(amount_of_comp202coin,16)
    amount_dollars=decimal_com202coin*COMP202COIN_DOLLAR_EXCHANGE_RATE-get_solar_observation_fee(amount_of_comp202coin)-get_flat_fee()
    #If i dont do this i get wierd numbers because of the division
    amount_dollars=round(amount_dollars,2)
    return amount_dollars
 
def convert_dollar_to_COMP202COIN(amount_of_dollars):
    """
    (num) -> str 
    
    converts dollars to COMP202COIN, effectively ripping off the customer with the insane conversion rates.
    Rounds the value of compcoins down to nearest hexadecimal
    
    >>>convert_dollar_to_COMP202COIN(10000000000)
    '0x5f5e100'
    >>>convert_dollar_to_COMP202COIN(99)
    '0x0'
    >>> convert_dollar_to_COMP202COIN(100)
    '0x1'
    """
    decimal_com202coin=int(amount_of_dollars*DOLLAR_COMP202COIN_EXCHANGE_RATE)
    return hex(decimal_com202coin)
 
def get_excess_dollars_after_conversion(amount_of_dollars):
    """
    (num) -> num
    
    returns the excess dollars that could not be converted into compcoins
    
    >>> get_excess_dollars_after_conversion(0)
    0.0
    
    >>> get_excess_dollars_after_conversion(199)
    99.0
    
    >>> get_excess_dollars_after_conversion(19999999999999)
    19999999999999.0
    """
    max_conversion=int(convert_dollar_to_COMP202COIN(amount_of_dollars),16)
    decimal_coin_supply=int(COMP202COIN_SUPPLY,16)
    
    if max_conversion>decimal_coin_supply:
        #code in quotes here is better code, took me a while to wrap my head around it and make it work. too bad!
        """
        supply_excess=max_conversion-decimal_coin_supply
        supply_excess=round(supply_excess/DOLLAR_COMP202COIN_EXCHANGE_RATE)
        #given the logic, the above variably should only be assigned integer values, im rounding incase the division acts wierd
        """
        
        #remove this return statement if you want to make the above code work
        return amount_of_dollars
    else:
        supply_excess= 0
        
    conversion_excess=amount_of_dollars%(1/DOLLAR_COMP202COIN_EXCHANGE_RATE)
    #This is not a good way of rounding a float to 2 decimals. too bad!
    #I could make this work by using math.floor and format("float", '1.2f') but im not going to ¯\_(ツ)_/¯
    conversion_excess=int(conversion_excess*100)/100
    
    return conversion_excess+supply_excess
 
def get_coin_after_conversion(amount_of_dollars):
    """
    (num) -> str
    
    Smarter version of convert_dollar_to_COMP202COIN
    checks if it is possible to convert the money before performing the conversion.
    
    >>>convert_dollar_to_COMP202COIN(0)
    '0x0'
    >>>convert_dollar_to_COMP202COIN(100)
    '0x1'
    >>> convert_dollar_to_COMP202COIN(10000000000000000000)
    '0x0'
    """
    #I wrote this so the program can work with the get_excess_dollars_after_conversion
    #This function is doesnt do anything special when the code in lines 58 to 62 is not executed.
    #it will only return 0 if the stock is not big enough and prompt the program to
    #tell the user the transaction cannot be completed.
    exchangeable_dollars=amount_of_dollars-get_excess_dollars_after_conversion(amount_of_dollars)
    return convert_dollar_to_COMP202COIN(exchangeable_dollars)
 
def button_1():
    """
    (void) -> void
    
    runs the conversion of dollars to compcoin in operate_machine
    Asks user for inputs for the money they wish to convert and returns the compcoins and the excess cash
    If not enough coins in stock or the user inputs insufficient funds, the program retuns all the money to the customer
    and tells that that the transaction could not be completed
    
    >>>button_1()
    The conversion rate for dollars to COMP202COIN is 0.01 and we have 64 COMP202COINs in stock.
        Don't just jam the money, just drop it and let it float down ↓↓↓↓ here ↓↓↓↓
 
                         Drop the money right here right here please:  input(1)
    Transaction could not be completed due to insufficient funds.
    Come back when you're a little, hmmmmmm, richer.
    
    >>>button_1()
    The conversion rate for dollars to COMP202COIN is 0.01 and we have 64 COMP202COINs in stock.
        Don't just jam the money, just drop it and let it float down ↓↓↓↓ here ↓↓↓↓
 
                         Drop the money right here right here please:  input(1234)
    Thanks for the 1234.0$  :3
    heres your 0xc COMP202COIN and your 34.0$ of change.
 
    >>>button_1()
    The conversion rate for dollars to COMP202COIN is 0.01 and we have 64 COMP202COINs in stock.
        Don't just jam the money, just drop it and let it float down ↓↓↓↓ here ↓↓↓↓
 
                         Drop the money right here right here please:  input(10000000000)
    Transaction could not be completed due to insufficient funds.
    Come back when you're a little, hmmmmmm, richer.
    """
    #This only executes in line 311, this is here just to make program more readable.
    dollars=float(input(
    """\nThe conversion rate for dollars to COMP202COIN is """+str(DOLLAR_COMP202COIN_EXCHANGE_RATE)+' and we have '+str(COMP202COIN_SUPPLY)+""" COMP202COINs in stock.
    Don't just jam the money, just drop it and let it float down ↓↓↓↓ here ↓↓↓↓\n
                     Drop the money right here right here please:  """))
        
    coins=get_coin_after_conversion(dollars)
        
    if coins<="0x0":
        print("Transaction could not be completed due to insufficient funds.\nCome back when you're a little, hmmmmmm, richer.")
        return
        
    print("Thanks for the "+str(dollars)+"$  :3")
    print("heres your "+str(coins)+" COMP202COIN and your "+str(get_excess_dollars_after_conversion(dollars))+"$ of change.")
 
def button_2():
    """
    (void) -> void
    
    runs the conversion of compcoin to dollars in operate_machine
    Asks user for inputs for the compcoin they wish to convert and returns the cash
    If the user puts insufficient funs, the program retuns all the coins to the customer
    and tells that that the transaction could not be completed
    
    >>> button_2()
 
    the conversion rate for COMP202COIN to CAD is 0.05 .
        There is also a base fee of 10 and an exchange fee of 0.05$ per COMP202COIN if there is no sunlight
        Please bundle your COMP202COIN toghether with the provided strings and insert them here:  input(33)
    Transaction could not be completed due to insufficient funds.
    Come back when you're a little, hmmmmmm, richer.
    
    >>> button_2()
    
    the conversion rate for COMP202COIN to CAD is 0.05 .
        There is also a base fee of 10 and an exchange fee of 0.05$ per COMP202COIN if there is no sunlight
        Please bundle your COMP202COIN toghether with the provided strings and insert them here:  input(ad34)
 
                    You inserted 0xad34 COMP202COINS. Here is your 2207.0$
                    
    >>> button_2()
    the conversion rate for COMP202COIN to CAD is 0.05 .
        There is also a base fee of 10 and an exchange fee of 0.05$ per COMP202COIN if there is no sunlight
        Please bundle your COMP202COIN toghether with the provided strings and insert them here:  input(444)
 
                    You inserted 0xad34 COMP202COINS. Here is your 44.6$
    """
    #This only executes in line 314, this is here just to make program more readable.
    coins=input(
    "\nthe conversion rate for COMP202COIN to CAD is "+str(COMP202COIN_DOLLAR_EXCHANGE_RATE)+""" .
    There is also a base fee of """+str(get_flat_fee())+" and an exchange fee of "+str(SOLAR_OBSERVATION_FEE_MULTIPLIER)+"""$ per COMP202COIN if there is no sunlight
    Please bundle your COMP202COIN toghether with the provided strings and insert them here:  """)
        
    #I want the format to be 0x[number] in my print statement
    coins=hex(int(coins,16))
    dollars=convert_COMP202COIN_to_dollars(coins)
        
    if dollars<=0:
        print("Transaction could not be completed due to insufficient funds.\nCome back when you're a little, hmmmmmm, richer.")
        return
        
    print("\n\t\tYou inserted "+coins+" COMP202COINS. Here is your "+str(dollars)+"$")
 
def operate_machine():
    """
    (void) -> void
    
    Asks user for the mode of operation. Asks for inputs and puts the inputs and uses them to calculate the currency it should exchange
    and return to the customer.
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars
    3. Exit program
    input(1)
    -> progran runs button_1() [ view line 172 ]
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars
    3. Exit program
    input(2)
    -> progran runs button_2() [ view line 220 ]
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars
    3. Exit program
    input(3)
    See you next time
    """
    #Was... was that the last docstring? am i finally free? 
    display_welcome_menu()
    button=input()
    
    if button=="3":
        print("See you next time")
    
    elif button=="1":
        button_1()
        
    elif button=="2":
        button_2()
        
    else:
        print("\n\nHow... how did you even press that, such a button doesn't even exist on my panel.")
        print('No seriously, where did you even find a "'+str(button)+'" button on my interface?')
        print("I mean... I wasn't programmed to respond to that. You can try running me again if you like...")
 