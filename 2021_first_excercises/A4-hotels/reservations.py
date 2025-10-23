import datetime
import random
from room import Room, MONTHS, DAYS_PER_MONTH, MONTH_STR_TO_INT
 
class Reservation:
	"""
	Room(str,Room,date,date,int=None)
	Represents a Reservation
	Takes as input the name of the client, the selected room, checkin date and checkout date and generates a reservation
	number. Reservation number may be inputted manually
	
	Attribules
	-----------
	Class:
	booking_numbers(list)	: list of all current booking numbers
	MIN_BOOKINGNUM(int)		: smallest 13 digit integer
	MAX_BOOKINGNUM(int)		: largest 13 digit integer
 
	instance:
	booking_number(int)	: booking number
	name(str)			: client's name
	room_reserved(Room)	: room reserved for client
	check_in(date)		: check in date
	check_out(date)		: check out date
 
	Methods
	-----------
	instance:
	to_short_string(Reservation)
		returns '<reservation number>--<name>'
 
	Class:
	from_short_string(class,str,date,date,Room)->Reservation
		uses a short string to generate a reservation
 
	Static:
	generate_bookingnum()->int					
		generates a valid booking number
 
	get_reservations_from_row(Room,list)->dict
		generates a dictionary of booking numbers pointing to reservations
	"""
 
	booking_numbers=[]
	MIN_BOOKINGNUM=1000000000000
	MAX_BOOKINGNUM=9999999999999
 
	def __init__(self,name,selected_room,checkin,checkout,booking_number=None):
		"""
		(Reservation,str,Room,date,date,num)
		initializes Reservation with clients name, the selected room, checkin date, check out date and a booking number.
		Selected room will be reserved for all days between checkin and checkout excluding the checkout date.
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
		>>> print(my_reservation.check_in)
		2021-05-03
		>>> print(my_reservation.check_out)
		2021-05-10
		>>> my_reservation.booking_number
		1953400675629
		>>> r1.availability[(2021, 5)][9]
		False
 
		>>> date3= datetime.date(2021, 5, 12)
		>>> my_reservation = Reservation('Mrs. Santos', r1, date2, date3,1000000000000)
		>>> my_reservation.booking_number
		1000000000000
 
		>>> my_reservation = Reservation('Mrs. Santos', r1, date2, date3,1)
		Traceback (most recent call last):
		AssertionError: Invalid booking number entered in Reservation
 
		>>> my_reservation = Reservation('Mrs. Santos', r1, date2, date3,10**14)
		Traceback (most recent call last):
		AssertionError: Invalid booking number entered in Reservation
 
		>>> my_reservation = Reservation('Mrs. Santos', r1, date2, date3, '')
		Traceback (most recent call last):
		AssertionError: Invalid booking number entered in Reservation
 
 
		>>> Reservation('','','','',1953400675629)
		Traceback (most recent call last):
		AssertionError: Booking number already in use. Error in Reservation __init__
 
		>>> Reservation('Mrs. Santos', r1, date1, date2)
		Traceback (most recent call last):
		AssertionError: Room not available between checkin and checkout dates. Error in Reservation __init__
 
		>>> Reservation.booking_numbers = []
		"""
		if booking_number!=None:
			if type(booking_number)!=int or not Reservation.MIN_BOOKINGNUM<=booking_number<=Reservation.MAX_BOOKINGNUM:
				raise AssertionError('Invalid booking number entered in Reservation')
			elif booking_number in Reservation.booking_numbers:
				raise AssertionError('Booking number already in use. Error in Reservation __init__')
		elif not selected_room.is_available(checkin,checkout):
			raise AssertionError('Room not available between checkin and checkout dates. Error in Reservation __init__')
		
		self.name=name
		self.check_in=checkin
		self.check_out=checkout
 
		self.booking_number=booking_number or Reservation.generate_bookingnum()			# if booking_number is None, generate_bookingnum will be evaluated
		Reservation.booking_numbers.append(self.booking_number)
 
		self.room_reserved=selected_room
		selected_room.reserve_full_stay(checkin,checkout)
	
	@staticmethod
	def generate_bookingnum():		# having an extra static method is worth making the file look cleaner
		"""
		(void)->int
		generates a valid booking number
 
		>>> Reservation.booking_numbers = []
		>>> random.seed(987)
		>>> Reservation.generate_bookingnum()
		1953400675629
		>>> Reservation.booking_numbers.append(1953400675629)
		>>> random.seed(987)
		>>> Reservation.generate_bookingnum()
		1296485824452
		>>> Reservation.booking_numbers.append(1296485824452)
		>>> Reservation.generate_bookingnum()
		1830129182153
		>>> Reservation.booking_numbers = []
		"""
		
		bookingnum=random.randint(Reservation.MIN_BOOKINGNUM,Reservation.MAX_BOOKINGNUM)
		while bookingnum in Reservation.booking_numbers:
			bookingnum=random.randint(Reservation.MIN_BOOKINGNUM,Reservation.MAX_BOOKINGNUM)
		return bookingnum
 
	def __str__(self):
		"""
		(Reservation)-> str
		return booking number, client name, room, checkin date and checkout date in 5 lines
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
		>>> print(my_reservation)
		Booking number: 1953400675629
		Name: Mrs. Santos
		Room reserved: Room 105,Queen,80.0
		Check-in date: 2021-05-03
		Check-out date: 2021-05-10
		>>> Reservation.booking_numbers = []
		"""
		line1='Booking number: '+str(self.booking_number)
		line2='\nName: '+self.name
		line3='\nRoom reserved: '+str(self.room_reserved)
		line4='\nCheck-in date: '+str(self.check_in)
		line5='\nCheck-out date: '+str(self.check_out)
		return line1+line2+line3+line4+line5
 
	def to_short_string(self):
		"""
		(Reservation)-> str
		Returns a short string containing the reservation number and name
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
		>>> my_reservation.to_short_string()
		'1953400675629--Mrs. Santos'
		"""
		return str(self.booking_number)+'--'+self.name
 
	@classmethod
	def from_short_string(cls,short_string,checkin,checkout,selected_room):
		"""
		(class,str,date,date,Room)->Reservation
		reserves a room using short-string format
 
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 4)
		>>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
		>>> print(my_reservation.check_in)
		2021-05-03
		>>> print(my_reservation.check_out)
		2021-05-04
		>>> my_reservation.booking_number
		1953400675629
		>>> r1.availability[(2021, 5)][3]
		False
		"""
		reservation_num=int(short_string[0:13])
		name=short_string[15:]
		return cls(name,selected_room,checkin,checkout,reservation_num)
 
	@staticmethod
	def get_reservations_from_row(room_obj,tup_list): #list[(int year, str month, int day, str short_string)]*n
		"""
		(Room,list)->dict
		Takes a room and a list of tuples in the format (int year, str month, int day, str short_string)
		Infers the checkin and checkout dates and reserves the room during those dates. Returns a dictionay where each booking
		number points to its respective Reservation.
		Same reservation number cannot be used for different reservations twice. Reservation number and name must
		be used toghether consistently throughout list
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = [] # needs to be reset for the test below to pass
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(MONTHS, 2021)
		>>> rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 7, '1953400675629--Jack')]
		>>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
		>>> print(rsv_dict[1953400675629])
		Booking number: 1953400675629
		Name: Jack
		Room reserved: Room 105,Queen,80.0
		Check-in date: 2021-05-03
		Check-out date: 2021-05-08
 
		>>> rsv_strs = [(2021, 'May', 1, '1953400675628--Mack'), (2021, 'May', 4, '1953400675628--Mack')]
		>>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
		Traceback (most recent call last):
		AssertionError: Room 105 is reserved during 2021-05-01 to 2021-05-05. Error in get_reservations_from_row
 
		>>> Reservation.booking_numbers = []
		>>> rsv_strs = [(2021, 'May', 4, '1953400675628--Mack'),(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 7, '1953400675629--Jack'),\
		(2021, 'May', 1, '1953400675628--Mack')]
		>>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
		Traceback (most recent call last):
		AssertionError: Room 105 is reserved during 2021-05-01 to 2021-05-05. Error in get_reservations_from_row
 
		>>> Reservation.booking_numbers = []
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(MONTHS, 2021)
		>>> r1.set_up_room_availability(MONTHS, 2022)
		>>> r1.set_up_room_availability(MONTHS, 2023)
		>>> date1 = datetime.date(2021, 1, 1)
		>>> date2 = datetime.date(2023, 12, 30)
		>>> r1.reserve_full_stay(date1 , date2)
		>>> date3 = datetime.date(2022,10,5)
		>>> r1.make_available(date3)
		>>> r2 = Room("Queen", 105, 80.0)
		>>> r2.set_up_room_availability(MONTHS, 2021)
		>>> r2.set_up_room_availability(MONTHS, 2022)
		>>> r2.set_up_room_availability(MONTHS, 2023)
		>>> rsv_strs = [(2021, 'May', 1, '1953400675628--Mack'), (2021, 'May', 4, '1953400675628--Mack'), (2021, 'Jan', 1, '1953400675628--Mack'),\
		(2021, 'May', 5, '2953400675628--Iack'),(2021, 'Nov', 25, '2953400675628--Iack'),(2022, 'May', 31, '2953400675628--Iack'),\
		(2022, 'Jun', 1, '3953400675628--Pack'),(2022, 'Oct', 4, '3953400675628--Pack'),(2022, 'Oct', 6, '4953400675628--Lack'),\
		(2022, 'Dec', 31, '4953400675628--Lack'),(2023, 'Jan', 2, '4953400675628--Lack'),(2023, 'Dec', 29, '4953400675628--Lack')]
		>>> rsv_dict = Reservation.get_reservations_from_row(r2, rsv_strs)
		>>> r1.availability==r2.availability
		True
 
		>>> r3= Room('king',2,12.0)
		>>> r3.set_up_room_availability(['Jan'],2021)
		>>> rsv_dict = Reservation.get_reservations_from_row(r3, [(2021,'Jan',1,'1234567890123--Kack')])
		>>> print(rsv_dict[1234567890123])
		Booking number: 1234567890123
		Name: Kack
		Room reserved: Room 2,king,12.0
		Check-in date: 2021-01-01
		Check-out date: 2021-01-02
 
		>>> dummy=Reservation.get_reservations_from_row(r3, [(2021,'Jan',6,'2234567890123--Uack'),(2021,'Jan',8,'3234567890123--Sack'),\
		(2021,'Jan',2,'4234567890123--Qack')])
		>>> r3.availability[(2021,1)][:11]
		[None, False, False, True, True, True, False, True, False, True, True]
 
		>>> r3.set_up_room_availability(['Jan'],2021)
		>>> dummy=Reservation.get_reservations_from_row(r3, [(2021,'Jan',6,''),(2021,'Jan',8,''),(2021,'Jan',2,'')])
		>>> r3.availability[(2021,1)][:11]
		[None, True, True, True, True, True, True, True, True, True, True]
 
		>>> Reservation.booking_numbers = []
		"""
		# This infering checkin checkout business is so incredibly bad
		# I actually have to find a way to add a day to my date object because the last day isnt actually the checkout day. why?
		# Ok, its actually a good thing i decided to read https://docs.python.org/3/library/datetime.html
		# I will use a timedelta object :)
 
		days_per_reservation=dict()
 
		for res_tup in tup_list:	# res_tup for reservation tuple
			short_str=res_tup[3]
			if not short_str: # if short_str == '' we skip
				continue
 
			if short_str not in days_per_reservation:
				days_per_reservation[short_str]=[]
			days_per_reservation[short_str].append(datetime.date(res_tup[0],MONTH_STR_TO_INT[res_tup[1]],res_tup[2]))
													#   year,     , month in integer format,    day
 
		res_dict=dict()
		for short_str, date_objects in days_per_reservation.items():
			checkin=min(date_objects)
			checkout=max(date_objects)+datetime.timedelta(1)
			
			if not room_obj.is_available(checkin,checkout):			# Man, why arent we allowed to just use assert statements?
				raise AssertionError('Room '+str(room_obj.room_num)+' is reserved during '+str(checkin)+' to '+str(checkout)+\
					'. Error in get_reservations_from_row')
 
			res_dict[int(short_str[0:13])]=Reservation.from_short_string(short_str,checkin,checkout,room_obj)
			#		first 13 digits from short_str
		return res_dict
		# I think i over-engineered this method. This will work for multple reservationg in one line regardless of wierd stuff.
		
