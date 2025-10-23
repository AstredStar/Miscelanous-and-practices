import datetime, random, copy, os
from reservation import Reservation
from room import Room, MONTHS, DAYS_PER_MONTH, MONTH_STR_TO_INT, is_leapyear
 
class Hotel:
	"""
	Hotel(str,list=[],dict={})
	Represents a Hotel
	Takes as input the hotel name. Optionally, can also take a list of the rooms of the 
	hotel and a dictionary of reservation numbers poiting to reservation objects
 
	Attribules
	-----------
	instance:
	name(string)		: name of hotel
	rooms(list)			: list of Room objects available in the hotel
	reservations(dict)	: dictionary of booking numbers poiting to Reservations objects
 
	Methods
	-----------
	instance:
	make_reservation(Hotel,str,str,date,date)->int
		given a name, a room type, a checkin and checkout date, finds a room and makes a reservationupdates reservations attribute accordingyly
 
	get_receipt(Hotel,list)->float
		Given a list of booking numbers, returns the combined price of all respective reservations
 
	get_reservation_for_booking_number(Hotel,int)->Reservation
		Given a booking number, returns its Reservation object
 
	cancel_reservation(Hotel,int)->void
		Takes as input a booking number and removes it from the hotel and unreserves the corresponding room
 
	get_available_room_types(Hotel)->list
		returns a list of room types available at the hotel
 
	Static:
	load_hotel_info_file(str)->tuple
		Takes a file path of a hotel and its rooms. Returns the hotel name and a list of all of its room objects
	"""
	def __init__(self,name,ROOM_LIST=list(),RESERVATION_DICT=dict()):# It is very dangerous to assign a mutable object as a keyword argument. I would rather
															# put None and deal with this in the function body, but my hands are forced. Deepcopying is ok though.
		self.rooms=copy.deepcopy(ROOM_LIST)
		self.reservations=copy.deepcopy(RESERVATION_DICT)
		self.name=name
 
	def make_reservation(self,name,room_type,checkin,checkout):
		"""
		(Hotel,str,str,date,date)->int
		given a name, a room type, a checkin and checkout date, finds a room and makes a reservation
		updates reservations attribute accordingyly
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> h = Hotel("Secret Nugget Hotel", [r1])
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
		1953400675629
		>>> print(h.reservations[1953400675629])
		Booking number: 1953400675629
		Name: Mrs. Santos
		Room reserved: Room 105,Queen,80.0
		Check-in date: 2021-05-03
		Check-out date: 2021-05-10
 
		>>> h.make_reservation("Mrs. Santos", "king", date1, date2)
		Traceback (most recent call last):
		AssertionError: No rooms of this type are available during the duration of stay.
		"""
		res_room=Room.find_available_room(self.rooms,room_type,checkin,checkout)
		if res_room==None:
			raise AssertionError("No rooms of this type are available during the duration of stay.")	# if find_available_room returns None
 
		this_reservation=Reservation(name,res_room,checkin,checkout)
 
		self.reservations[this_reservation.booking_number]=this_reservation
		return this_reservation.booking_number
 
	def get_receipt(self,res_numbers_list):
		"""
		(Hotel,list)->float
		Given a list of booking numbers, returns the combined price of all respective reservations
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r2 = Room("Twin", 101, 55.0)
		>>> r3 = Room("Queen", 107, 80.0)
		>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
		>>> r2.set_up_room_availability(['May', 'Jun'], 2021)
		>>> r3.set_up_room_availability(['May', 'Jun'], 2021)
		>>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
		>>> h.get_receipt([num1])
		560.0
		>>> date3 = datetime.date(2021, 6, 5)
		>>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
		>>> h.get_receipt([num1, num2])
		2375.0
		>>> h.get_receipt([123])
		0.0
		"""
		total_monies=0.0
		for res_number in res_numbers_list:
 
						#if this expression below evaluates to False, everything evaluates to 0
			total_monies+=res_number in self.reservations and \
				(self.reservations[res_number].check_out - self.reservations[res_number].check_in).days*self.reservations[res_number].room_reserved.price
				#			↑ retreive checkout date ↑			↑ retrieve checkin date ↑					↑ retrieve price of room per night ↑
				# this subtraction gives us a timedelta object. timedelta.days gives us the days between the two dates. Multiply by the price per night
				# to get the total price. This is the most optimized way of doing this i think. Just 1 expression and no if checks
		return total_monies
 
	def get_reservation_for_booking_number(self,booking_num):
		"""
		(Hotel,int)->Reservation
		given a booking number, returns its Reservation object
 
		>>> random.seed(137)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> h = Hotel("Secret Nugget Hotel", [r1])
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
		>>> rsv = h.get_reservation_for_booking_number(num1)
		>>> print(rsv)
		Booking number: 4191471513010
		Name: Mrs. Santos
		Room reserved: Room 105,Queen,80.0
		Check-in date: 2021-05-03
		Check-out date: 2021-05-10
 
		>>> h.get_reservation_for_booking_number(1)==None
		True
		"""
		return self.reservations.get(booking_num) # if we cant find the booking number we return None
 
	def cancel_reservation(self,booking_num):
		"""
		(Hotel,int)->void
		Takes as input a booking number and removes it from the hotel and unreserves the corresponding room
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r1.set_up_room_availability(['May'], 2021)
		>>> h = Hotel("Secret Nugget Hotel", [r1])
		>>> date1 = datetime.date(2021, 5, 3)
		>>> date2 = datetime.date(2021, 5, 10)
		>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
		>>> h.cancel_reservation(num1)
		>>> num1 in h.reservations
		False
		>>> r1.availability[(2021, 5)][4]
		True
		"""
		res_obj=self.get_reservation_for_booking_number(booking_num)
		if not res_obj:
			return		# if get_reservation_for_booking_number returns nothing. we do nothing
 
		res_obj.room_reserved.reserve_full_stay(res_obj.check_in, res_obj.check_out , availability_status=True)	# this unreserves the room
		self.reservations.pop(booking_num)		# remove reservation item and booking num item from dictionary, booking_num is kept in
		return  								# Reservation.booking_numbers however
 
	def get_available_room_types(self):
		"""
		(Hotel)->list
		returns a list of room types available at the hotel
 
		>>> r1 = Room("Queen", 105, 80.0)
		>>> r2 = Room("Twin", 101, 55.0)
		>>> r3 = Room("Queen", 107, 80.0)
		>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
		>>> r2.set_up_room_availability(['May', 'Jun'], 2021)
		>>> r3.set_up_room_availability(['May', 'Jun'], 2021)
		>>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
		>>> types = h.get_available_room_types()
		>>> types.sort()
		>>> types
		['Queen', 'Twin']
		"""
		unchecked_types=copy.copy(Room.TYPES_OF_ROOMS_AVAILABLE)
		checked_types=[]
 
		for last_room in self.rooms:
			last_room_type=last_room.room_type.lower()
 
			if last_room_type in unchecked_types:
				checked_types.append(last_room.room_type)
				unchecked_types.remove(last_room_type)
 
			if not unchecked_types:	# when unchecked_types=[], not unchecked_types evaluates to true and the loop breaks
				break
 
		return checked_types
 
	@staticmethod
	def load_hotel_info_file(input_path):
		"""
		(str)->tuple
		Takes a file path of a hotel and its rooms. Returns the hotel name and a list of all of its room objects
 
		>>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
		>>> hotel_name
		'Overlook Hotel'
		>>> print(len(rooms))
		500
		>>> print(rooms[236])
		Room 237,Twin,99.99
		>>> f=open('hotels/overlook_hotel/hotel_info.txt','r')
		>>> f.readline().strip()
		'Overlook Hotel'
 
		>> for i in rooms:
			j=f.readline().strip()
			if str(i)!=j:
				print(i)
				print(j)
					
		>>> f.close()
		"""
		try:									# we must always make sure to close our file
			file_obj=open(input_path,'r')
			hotel_name = file_obj.readline().strip()	# strip out /n character
			room_list=[]
 
			for room_str in file_obj:
				room_info=room_str.strip('\nRoom ').split(',')	# remove '/n' and 'Room ' and turn into list with [room_num,type,price]
				
				room_list.append(Room(room_info[1],int(room_info[0]),float(room_info[2]) ) )
								    #(    type    , int(room_number),    float(price)    )
			return hotel_name,room_list
		finally:
			file_obj.close()
 
	def save_hotel_info_file(self):
		"""
		(Hotel)->void
		saves the hotel name and room information into txt file in the directory 'hotel\<hotel_name>'
 
		>>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
		>>> hotel_name
		'Overlook Hotel'
		>>> h=Hotel('Mock Overlook',rooms)
		>>> h.name
		'Mock Overlook'
		>>> h.save_hotel_info_file()
		>>> o=open('hotels/overlook_hotel/hotel_info.txt','r')
		>>> m=open('hotels/mock_overlook/hotel_info.txt','r')
 
		>> for i in range(501):
			line_o=o.readline()
			line_m=m.readline()
			if line_o!=line_m:
				print(line_o,line_m)
		Overlook Hotel
		 Mock Overlook
 
		>>> r1 = Room("Double", 101, 99.99)
		>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
		>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
		>>> h.save_hotel_info_file()
		>>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
		>>> fobj.read()
		'Queen Elizabeth Hotel\\nRoom 101,Double,99.99\\n'
		>>> fobj.close()
		"""
		name_lower=self.name.lower().replace(' ','_')	# lower all letters and replace all spaces with underscores
 
		try:					# we must always make sure to close our file
			info_file=open('hotels/'+name_lower+'/hotel_info.txt','w')
			info_file.write(self.name+'\n')
			for last_room in self.rooms:
				info_file.write(str(last_room)+'\n')
		finally:
			info_file.close()
	
	@staticmethod
	def load_reservation_strings_for_month(folder_name,month,year):
		"""
		(str,str,int)->dict
		Returns a dictionary of room numbers pointing to a list of tuples(year,month,day,reservation short_string)
 
		>>> name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
		>>> h = Hotel(name, rooms, {})
		>>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
		>>> print(rsvs[237])
		[(1975, 'Oct', 1, ''), (1975, 'Oct', 2, ''), (1975, 'Oct', 3, ''), (1975, 'Oct', 4, ''), \
(1975, 'Oct', 5, ''), (1975, 'Oct', 6, ''), (1975, 'Oct', 7, ''), (1975, 'Oct', 8, ''), \
(1975, 'Oct', 9, ''), (1975, 'Oct', 10, ''), (1975, 'Oct', 11, ''), (1975, 'Oct', 12, ''), \
(1975, 'Oct', 13, ''), (1975, 'Oct', 14, ''), (1975, 'Oct', 15, ''), (1975, 'Oct', 16, ''), \
(1975, 'Oct', 17, ''), (1975, 'Oct', 18, ''), (1975, 'Oct', 19, ''), (1975, 'Oct', 20, ''), \
(1975, 'Oct', 21, ''), (1975, 'Oct', 22, ''), (1975, 'Oct', 23, ''), (1975, 'Oct', 24, ''), \
(1975, 'Oct', 25, ''), (1975, 'Oct', 26, ''), (1975, 'Oct', 27, ''), (1975, 'Oct', 28, ''), \
(1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), \
(1975, 'Oct', 31, '9998701091820--Jack')]
		"""
		file_path='hotels/'+folder_name+'/'+str(year)+'_'+month+'.csv'
		rooms_reservations=dict()
 
		try:
			csv_file=open(file_path,'r')
 
			for line in csv_file:
				room_info=line.strip().split(',') # remvoe \n characters and make a list
				room_tuples=[]
 
				for day in range(1,len(room_info)):
					room_tuples.append((year,month,day,room_info[day]))
 
				rooms_reservations[int(room_info[0])]=room_tuples
 
			return rooms_reservations
		finally:
			csv_file.close()
 
	def save_reservations_for_month(self,month_string,year):
		"""
		(Hotel,str,int)->void
		Saves all reservations for every room during the given month into a csv file in hotels\<hotel_name>
 
		>>> random.seed(987)
		>>> r1 = Room("Double", 237, 99.99)
		>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
		>>> Reservation.booking_numbers = []
		>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
		>>> date1 = datetime.date(2021, 10, 30)
		>>> date2 = datetime.date(2021, 12, 23)
		>>> num = h.make_reservation("Jack", "Double", date1, date2)
		>>> h.save_reservations_for_month('Oct', 2021)
		>>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
		>>> fobj.read()
		'237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
		>>> fobj.close()
 
 
		"""
		month_num=MONTH_STR_TO_INT[month_string]
		month_length= DAYS_PER_MONTH[month_num-1]+(is_leapyear(year) and month_num==2)
		first_of_month=datetime.date(year,month_num,1)
		first_of_nextmonth=first_of_month+datetime.timedelta(month_length)
 
		room_days_reservations=dict()				# dictionary of rooms pointing to a month dictionary, days in this month dictionary point to reservations
		for res_obj in self.reservations.values():
			if res_obj.check_in>=first_of_nextmonth or res_obj.check_out<=first_of_month:	# if reservation happend outside of year-month we skip
				continue
 
			if res_obj.room_reserved not in room_days_reservations:
				room_days_reservations[res_obj.room_reserved]=dict()
			
			start = res_obj.check_in.day
			end = res_obj.check_out.day
 
			if res_obj.check_out>=first_of_nextmonth:	# if checkin occurs before first of month, we just start from the first of month
				end=month_length+1						# same thing for checkout and end of month
			if res_obj.check_in < first_of_month:
				start=1
 
			for day in range(start,end):
				room_days_reservations[res_obj.room_reserved][day]=res_obj.to_short_string()	# each reserved day gets its reservation short string
 
		name_lower=self.name.lower().replace(' ','_')	# lower all letters and replace all spaces with underscores
		file_path='hotels/'+name_lower+'/'+str(year)+'_'+month_string+'.csv'
		try:
			csv_file=open(file_path,'w')
			
			for last_room in self.rooms:
				csv_file.write(str(last_room.room_num))
				
				room_av=last_room.availability[(year,month_num)]
				for day in range(1,len(room_av)):
 
					csv_file.write(   (room_av[day] and ',')   or   (','+room_days_reservations[last_room][day])   )
 
			csv_file.write('\n')
		finally:
			csv_file.close()
 
	def save_hotel(self):
		"""
		(Hotel)->void
 
		>>> random.seed(987)
		>>> Reservation.booking_numbers = []
		>>> r1 = Room("Double", 237, 99.99)
		>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
		>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
		>>> date1 = datetime.date(2021, 10, 30)
		>>> date2 = datetime.date(2021, 12, 23)
		>>> h.make_reservation("Jack", "Double", date1, date2)
		1953400675629
		>>> h.save_hotel()
		>>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
		>>> fobj.read()
		'Queen Elizabeth Hotel\\nRoom 237,Double,99.99\\n'
		>>> fobj.close()
		>>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
		>>> fobj.read()
		'237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\\n'
		>>> fobj.close()
		"""
		name_lower=self.name.lower().replace(' ','_')
		file_dir='hotels/'+name_lower
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
 
		self.save_hotel_info_file()
 
 
		if not self.rooms:
			return
		else:
			first_room=self.rooms[0]
 
 
		for year,month in first_room.availability:
			month_str=MONTHS[month-1]
			self.save_reservations_for_month(month_str,year)
 
	@classmethod
	def load_hotel(cls,folder_name):
		"""
		>>> random.seed(137)
		>>> Reservation.booking_numbers = []
		>>> hotel = Hotel.load_hotel('overlook_hotel')
		>>> hotel.name
		'Overlook Hotel'
		>>> str(hotel.rooms[236])
		'Room 237,Twin,99.99'
		>>> print(hotel.reservations[9998701091820])
		Booking number: 9998701091820
		Name: Jack
		Room reserved: Room 237,Twin,99.99
		Check-in date: 1975-10-30
		Check-out date: 1975-12-24
		"""
		cvs_in_folder=os.listdir('hotels/'+folder_name)
		hotel_name, rooms = Hotel.load_hotel_info_file('hotels/'+folder_name+'/hotel_info.txt')
		cvs_in_folder.remove('hotel_info.txt')
 
		reservations_per_room= dict()	# this was originally supposed to be a nested list. It caused some r******* interaction and cost me 3 HOURS TO FIND AND FIX
										
		years_and_months=dict()		# dictionary of years and months the hotel is open. used in setup_room_availability
 
		for cvs_file in cvs_in_folder:
			year=int(cvs_file[:4])
			month=cvs_file[5:8]
 
			if year not in years_and_months:
				years_and_months[year]=[]
			years_and_months[year].append(month)
 
			cvs_dict = Hotel.load_reservation_strings_for_month(folder_name, month, year)
 
			for room_num in cvs_dict:
				if room_num not in reservations_per_room:		# for some reason, if reservations_per_room is a nested list here. It adds cvs_dict[room_num]
					reservations_per_room[room_num]=[]			# to every single sublist. What, why??????????
				reservations_per_room[room_num]+=cvs_dict[room_num]
 
		all_reservations=dict()
		for last_room in rooms:
 
			for year,month_list in years_and_months.items():
				last_room.set_up_room_availability(month_list,year)
 
			all_reservations.update(Reservation.get_reservations_from_row(last_room,reservations_per_room[last_room.room_num]))
 
		return cls(hotel_name,rooms,all_reservations)