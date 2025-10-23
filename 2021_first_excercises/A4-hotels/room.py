 
import datetime
 
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTHS_IN_YEAR = [1,2,3,4,5,6,7,8,9,10,11,12]
MONTH_STR_TO_INT = {'Jan':1,'Feb':2,'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
 
def is_leapyear(year):
	"""
	(int)->bool
	Takes a year and returns whether or not its a leap year
 
	>>> is_leapyear(1)
	False
	>>> is_leapyear(4)
	True
	>>> is_leapyear(200)
	False
	>>> is_leapyear(1200)
	True
	>>> is_leapyear(1946)
	False
	>>> is_leapyear(1964)
	True
	"""
	return not (bool(year%4) - bool(year%100) + bool(year%400)) # if divisible we get 0, if not we get 1. Use not to invert this
 
class Room:
	"""
	Room(str,num,float)
	Represents a Room
	Initialises with the type of the room, room number and the price for 1 night.
 
	Attribules
	-----------
	Class:
	TYPES_OF_ROOMS_AVAILABLE (list) : Types of rooms offered: twin, double, queen or king 
 
	instance:
	room_type (Room,str)     : type of room; 'twin', 'double', 'queen' or 'king'
	room_num (Room,int)      : number assigned to room
	price (Room,float)       : price
	availability(Room,dict)  : dictionary with (<year>,<month>) as keys pointing to list of availabilities for each day in that month. First input in list is None
 
	Methods
	-----------
	instance:
	set_up_room_availability(room, list, int)->void
		updates availability attribute
 
	reserve_room(room,date)->void
		reserves room for given date
 
	make_available(room,date)->void					
		clears room for given date
 
	is_available(room,date,date)->bool				
		returns whether or not given room is clear from start date to end date
	reserve_full_stay(room,date,date,bool)->void	
		marks room as reserved from start date to end date. Can clear the room instead by entering True as 4th argument
 
	Static:
	find_available_room(list,str,date,date)->Room or None
		finds a room of given type from a list of rooms that is clear from start date to end date
	"""
	TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']
 
	def __init__(self, room_type, room_num, price):
		"""
		(room,str,int,float)
		initialises room object with its type, number and price
 
		>>> Room(4,4,4.0)
		Traceback (most recent call last):
		AssertionError: Room class takes (str,int,float) as arguments. Given input was (4, 4, 4.0)
 
		>>> Room('bed',4,4.0)
		Traceback (most recent call last):
		AssertionError: Invalid room type inputed in Room class. Given type was "bed"
 
		>>> Room('twin',0,4.0)
		Traceback (most recent call last):
		AssertionError: Room class takes positive room_num. Given number was 0
 
		>>> Room('twin',4,-4.0)
		Traceback (most recent call last):
		AssertionError: Room class takes non-negative price. Given price was -4.0
		"""
		if (type(room_type),type(room_num),type(price))!=(str,int,float):
			raise AssertionError("Room class takes (str,int,float) as arguments. Given input was " +str((room_type,room_num,price)))
		elif room_type.lower() not in Room.TYPES_OF_ROOMS_AVAILABLE:
			raise AssertionError('Invalid room type inputed in Room class. Given type was "'+room_type+'"')
		elif room_num<=0:
			raise AssertionError('Room class takes positive room_num. Given number was '+str(room_num))
		elif price < 0:
			raise AssertionError('Room class takes non-negative price. Given price was '+str(price))
		self.room_type = room_type
		self.room_num = room_num
		self.price = price
		self.availability=dict()
 
	def __str__(self):
		"""
		String function returns 'Room [room_num],[room_type],[price]'
 
		>>> str(Room('king',4,4.0))
		'Room 4,king,4.0'
		"""
		return 'Room '+str(self.room_num)+','+self.room_type+','+str(self.price)
 
	def set_up_room_availability(self,months_list,year):
		"""
		(room,list,int)->void
		Updates availabity attribut for each months in list and given year.
 
		>>> r = Room("Queen", 105, 80.0)
		>>> r.set_up_room_availability(['May', 'Jun'], 2021)
		>>> len(r.availability)
		2
		>>> len(r.availability[(2021, 6)])
		31
		>>> r.availability[(2021, 5)][5]
		True
		>>> print(r.availability[(2021, 5)][0])
		None
 
		>>> r=Room('twin',2,2.0)
		>>> r.set_up_room_availability(['Jun', 'Feb'], 2020)
		>>> len(r.availability[(2020, 2)])
		30
		"""
		
		for month in months_list:
			month_int=MONTH_STR_TO_INT[month]
			mon_length=DAYS_PER_MONTH[month_int-1]      # list starts at zero hence -1
			if month_int==2:
				mon_length+=is_leapyear(year)           # if leapyear, we add 1, if not we add 0
 
			day_list=[None]+[True]*mon_length
			self.availability[(year,month_int)]=day_list
 
	def view_av(self,date_object):								#av is short for availability
		return self.availability[(date_object.year,date_object.month)][date_object.day]			# short hand to check availability with a date_object for testing
 
	def change_av(self,date_object, selection):
		self.availability[(date_object.year,date_object.month)][date_object.day]=selection 		# short hand to change availability with a date_object for testing
																			# i wanted to use change_av ad view_ave in the function bodies but it ended being worse
	def reserve_room(self,date_object):
		"""
		(room,date)->void
		updates availability at given date to be reserved [false]
 
		>>> r = Room("Queen", 105, 80.0)
		>>> r.set_up_room_availability(['May', 'Jun'], 2021)
		>>> date1 = datetime.date(2021, 6, 20)
		>>> r.reserve_room(date1)
		>>> r.availability[(2021, 6)][20]
		False
		>>> r.availability[(2021, 5)][3] = False
		>>> date2 = datetime.date(2021, 5, 3)
		>>> r.reserve_room(date2)
		Traceback (most recent call last):
		AssertionError: The room is not available at the given date
		"""
		
		if self.availability[(date_object.year,date_object.month)][date_object.day]==False:
			raise AssertionError("The room is not available at the given date")
		else:
			self.availability[(date_object.year,date_object.month)][date_object.day]=False
 
	def make_available(self,date_object):
		"""
		(room,date)->void
		updates availability at given date to be available [True]
 
		>>> r = Room("Queen", 105, 80.0)
		>>> r.set_up_room_availability(['May', 'Jun'], 2021)
		>>> date1 = datetime.date(2021, 6, 20)
		>>> r.make_available(date1)
		>>> r.availability[(2021, 6)][20]
		True
		>>> r.availability[(2021, 5)][3] = False
		>>> date2 = datetime.date(2021, 5, 3)
		>>> r.make_available(date2)
		>>> r.availability[(2021, 5)][3]
		True
 
		>>> r = Room("Queen", 105, 80.0)
		>>> r.set_up_room_availability(['May', 'Jun'], 2021)
		>>> d=datetime.date(2021,6,20)
		>>> r.reserve_room(d)
		>>> r.availability[(2021,6)][20]
		False
		>>> r.make_available(d)
		>>> r.availability[(2021,6)][20]
		True
		"""
		self.availability[(date_object.year,date_object.month)][date_object.day]=True
 
	def is_available(self,start,end):		# for some reason, i chose to optimize this code for people who want to stay over multiple years
		"""
		(Room,date,date)-> bool
		Checks if the room is available from start date to end date
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
		>>> date1 = datetime.date(2021, 5, 25)
		>>> date2 = datetime.date(2021, 6, 10)
		>>> r1.is_available(date1, date2)
		True
		>>> r1.availability[(2021, 5)][28] = False
		>>> r1.is_available(date1, date2)
		False
		
		>>> r1.availability[(2021, 5)][28] = True
		>>> r1.is_available(date1, date2)
		True
 
		>>> r1.availability[(2021, 6)][10] = False
		>>> r1.is_available(date1, date2)
		True
 
		>>> r1.availability[(2021, 6)][9] = False
		>>> r1.is_available(date1, date2)
		False
 
		>>> r1.is_available(date2, date1)
		Traceback (most recent call last):
		AssertionError: end date must occur after start date in is_available
 
		>>> r1.set_up_room_availability(MONTHS, 2021)
		>>> r1.set_up_room_availability(MONTHS, 2022)
		>>> r1.set_up_room_availability(MONTHS, 2023)
		>>> r1.availability[(2023, 12)][31] = False
		>>> date2= datetime.date(2024, 1, 1)
		>>> r1.is_available(date1, date2)
		False
		>>> r1.availability[(2023, 12)][31] = True
		>>> r1.is_available(date1, date2)
		True
		"""
		if start>=end:
			raise AssertionError('end date must occur after start date in is_available')
		
		end-=datetime.timedelta(1) # I programmed this to include the end date in calculation, this is an easy fix
 
		staydays=[]
		staymonths= MONTHS_IN_YEAR*(end.year-start.year+1)		# multiply months by number of years
		staymonths= staymonths[start.month-1:end.month-12 or None]	# slice out months outside of stay range. start.month needs to start at zero hence -1
																	# if end month is 12, we get [:0 or None] which evaluates to [:None] and we dont slice anything
		year=start.year
		leap_compensation=(end.month==2) and is_leapyear(end.year)	# Have to compensate in math if last month is a leapmonth, value is 1 or 0
 
		for last_month in staymonths:
			staydays+=self.availability[(year,last_month)] #we add the days_list for each month
			year+=last_month//12		#if last_month is december, we move to the next year
 
		staydays=staydays[start.day:end.day-DAYS_PER_MONTH[last_month-1]-leap_compensation or None]	#slice out days outside of range
								# total days in the last month, add 1 day if leap month, subtract days that are reserved. Implement [:0 or None] trick
 
		return False not in staydays	# return wether or not any given day is reserved
 
	@staticmethod
	def find_available_room(room_list, desired_type, start ,end):
		"""
		(room,str,date,date)-> room or None
		finds a room of given type from a list of rooms that is clear from start date to end date
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r2 = Room("Twin", 101, 55.0)
		>>> r3 = Room("Queen", 107, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> r2.set_up_room_availability(['May'], 2021)
		>>> r3.set_up_room_availability(['May'], 2021)
		>>> r1.availability[(2021, 5)][8] = False
		>>> r = [r1, r2, r3]
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
		>>> my_room == r3
		True
		>>> r3.availability[(2021, 5)][3] = False
		>>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
		>>> print(my_room)
		None
		>>> r = Room("King", 110, 120.0)
		>>> r.set_up_room_availability(['Dec'], 2021)
		>>> r.set_up_room_availability(['Jan'], 2022)
		>>> date1 = datetime.date(2021, 12, 20)
		>>> date2 = datetime.date(2022, 1, 8)
		>>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
		>>> print(my_room)
		None
		>>> my_room = Room.find_available_room([r], 'King', date1, date2)
		>>> my_room == r
		True
 
		>>> Room.find_available_room([r], 'King', date2, date1)
		Traceback (most recent call last):
		AssertionError: end date must occur after start date in find_available_room
		"""
		if start>=end:
			raise AssertionError('end date must occur after start date in find_available_room')		# ill do this again for the sake of clarity incase of new errors
 
		for last_room in room_list:					#i like to put last_ in loop variables because it always refers to the last value we checked
			if last_room.room_type != desired_type:
				continue
 
			if last_room.is_available(start,end):
				return last_room
 
	def reserve_full_stay(self, start , end , availability_status=False):
		"""
		(room,date,date,bool)->void
		Marks every date from start date to end date as reserved by default. Can clear room by setting availability_status=True
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
		>>> date1 = datetime.date(2021, 5, 2)
		>>> date2 = datetime.date(2021, 5, 5)
		>>> r1.reserve_full_stay(date1,date2)
		>>> r1.availability[(2021,5)][:10]
		[None, True, False, False, False, True, True, True, True, True]
 
		>>> r1.set_up_room_availability(MONTHS, 2021)
		>>> r1.set_up_room_availability(MONTHS, 2022)
		>>> r1.set_up_room_availability(MONTHS, 2023)
		>>> date1 = datetime.date(2021, 5, 25)
		>>> date2 = datetime.date(2021, 6, 5)
		>>> r1.reserve_full_stay(date1 , date2)
		>>> r1.availability[(2021,5)][20:]
		[True, True, True, True, True, False, False, False, False, False, False, False]
		>>> r1.availability[(2021,6)][:10]
		[None, False, False, False, False, True, True, True, True, True]
 
		>>> date2 = datetime.date(2022, 6, 5)
		>>> r1.reserve_full_stay(date1 , date2)
		>>> r1.availability[(2021,5)][20:]
		[True, True, True, True, True, False, False, False, False, False, False, False]
		>>> r1.availability[(2022,6)][:10]
		[None, False, False, False, False, True, True, True, True, True]
		>>> True in r1.availability[(2021,6)]
		False
		>>> True in r1.availability[(2021,12)]
		False
		>>> True in r1.availability[(2022,1)]
		False
		>>> True in r1.availability[(2022,2)]
		False
		>>> True in r1.availability[(2022,3)]
		False
		>>> True in r1.availability[(2022,5)]
		False
 
		>>> r2 = Room("Queen", 105, 80.0)
		>>> r2.set_up_room_availability(MONTHS, 2021)
		>>> r2.set_up_room_availability(MONTHS, 2022)
		>>> r2.set_up_room_availability(MONTHS, 2023)
		>>> date1 = datetime.date(2021, 1, 1)
		>>> date2 = datetime.date(2023, 12, 30)
		>>> r1.reserve_full_stay(date1 , date2, availability_status=True)
		>>> r1.availability==r2.availability
		True
		"""
		
		if start.month==end.month and start.year==end.year:
			self.availability[(start.year,start.month)][start.day:end.day]=[availability_status]*(end.day-start.day)#for that same month, the block between start and end
																												#is replaced with block of falses
		elif start.year==end.year:
			last_month=self.availability[(start.year,start.month)]
			last_month[start.day:]=[availability_status]*len(last_month[start.day:])
 
			for month_num in range(start.month+1,end.month):
				last_month=self.availability[(start.year,month_num)]						# i could write this without if blocks and avoid some repetition
				last_month[1:]=[availability_status]*(len(last_month)-1)					# but it would be ultimate harder to do and it would work slower for small 
																							# ranges and bookings in the same month
			if end.day==1:
				return
			last_month=self.availability[(end.year,end.month)]
			last_month[1:end.day]=[availability_status]*len(last_month[1:end.day])
 
		else:	# ------------------- explanations start here ------------------------- This is essentially just a complete version of the last block
				#																		we have to also account for years here.
			last_month=self.availability[(start.year,start.month)]	#start month, base case
			last_month[start.day:]=[availability_status]*len(last_month[start.day:]) # days starting from start.day are filled with false
 
			last_year=start.year
			for month_num in range(start.month+1,13):	#start year, all subsequent months are filled with false
				last_month=self.availability[(last_year,month_num)]	
				last_month[1:]=[availability_status]*(len(last_month)-1)
 
			for last_year in range(start.year+1,end.year):	#all years inbetween just get filled with False
				for month_num in range(1,13):
					last_month=self.availability[(last_year,month_num)]
					last_month[1:]=[availability_status]*(len(last_month)-1)
 
			for month_num in range(1,end.month):		#end year, all months leading up are filled with false
				last_month=self.availability[(end.year,month_num)]							
				last_month[1:]=[availability_status]*(len(last_month)-1)
 
			if end.day==1:		# if end day is the first of the month, we dont need to change anything. For catching KeyError
				return
			last_month=self.availability[(end.year,end.month)]	#end month, last case
			last_month[1:end.day]=[availability_status]*len(last_month[1:end.day])	# days leading to end.day are filled with false. Except for end.day itself
			# in retrospect, this could have been much easier if i just used the timedelta object
			# But its ok, if someoene decides to rent a room for 2 years, this is fundamentally better and faster code.
 