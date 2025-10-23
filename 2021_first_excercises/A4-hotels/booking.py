import random, datetime, os
import matplotlib.pyplot as plt
from hotel import *
 
class Booking: 
	def __init__(self,hotels):
		self.hotels=hotels
 
	@classmethod
	def load_system(cls):
		"""
		>>> system = Booking.load_system()
		>>> len(system.hotels)
		2
		>>> system.hotels[1].name
		'The Great Northern Hotel'
		>>> print(system.hotels[1].rooms[314])
		Room 315,Queen,129.99
		"""
		hotels_in_folder=os.listdir('hotels')
		hotel_list=[]
		for hotel_dir in hotels_in_folder:
			hotel_list.append(Hotel.load_hotel(hotel_dir))
 
		return cls(hotel_list)
 
	def menu(self):
		"""
		booking = Booking.load_system()
		booking.menu()
		"""
		line1="Welcome to Booking System"
		line2='\nWhat would you like to do?'
		line3='\n1\t Make a reservation'
		line4='\n2\t Cancel a reservation'
		line5='\n3\t Look up a reservation'
		goto=input(line1+line2+line3+line4+line5)
 
		if goto=='1':
			self.create_reservation
		elif goto=='2':
			self.cancel_reservation
		elif goto=='3':
			self.lookup_reservation
 
	def create_reservation(self):
		"""
		random.seed(137)
		booking = Booking.load_system()
		booking.create_reservation()
		"""
		name=input('Please enter your name: ')
		print('Hi '+name+'! Which hotel would you like to book?')
		for index in range(len(self.hotels)):
			print(str(index+1)+'\t'+self.hotels[index].name)
 
		hotel_selected=self.hotels[int(input())-1] # subtract 1 from input and selec the hotel at that index
 
		room_types= hotel_selected.get_available_room_types()
 
		print('Which type of room would you like?')
		for index in range(len(room_types)):
			print(str(index+1)+'\t'+room_types[index])
 
		type_selected=room_types[int(input())-1]
			
		checkin_str=input('Enter check-in date (YYYY-MM-DD): ')			#	  YYYY - MM - DD
		checkout_str=input('Enter check-out date (YYYY-MM-DD): ')		#	 0----4 5--7-8		These are the indices
		checkin_date=datetime.date(int(checkin_str[:4]),int(checkin_str[5:7]),int(checkin_str[8:]))
		checkout_date=datetime.date(int(checkout_str[:4]),int(checkout_str[5:7]),int(checkout_str[8:]))
 
		print('Ok. Making your reservation for a '+type_selected+' room')
 
		booking_num=hotel_selected.make_reservation(name,type_selected,checkin_date,checkout_date)
		price=round(hotel_selected.get_receipt([booking_num]),2)
 
		print('Your reservation number is: '+str(booking_num))
		print('Your total amount due is: $'+str(price))
		print('Thank you!')
 
	def cancel_reservation(self):
		"""
		booking = Booking.load_system()
		booking.cancel_reservation()
		9998701091820
		"""
		bookingnum=int(input('Please enter your booking number: '))
 
		if bookingnum not in Reservation.booking_numbers:
			print('Could not find a reservation with that booking number.')
			return
 
		for hotel in self.hotels:
			hotel.cancel_reservation(bookingnum)
 
		Reservation.booking_numbers.remove(bookingnum)
		print('Cancelled successfully.')
 
	def lookup_reservation(self):
		"""
		booking = Booking.load_system()
		booking.lookup_reservation()
		9998701091820
		"""
		yes_no=input("Do you have your booking number(s)? ")
 
		if yes_no.lower()=='yes':
			booking_numbers=[]
			end=None
			while True:
				end=input("Please enter a booking number (or 'end'): ")
				if end=='end':
					break
				booking_numbers.append(int(end))
			
			for hotel in self.hotels:
				for booking_num in booking_numbers:
					found_reservation=hotel.get_reservation_for_booking_number(booking_num)
 
					if found_reservation:	#doesnt execute for None
						price=hotel.get_receipt([found_reservation.booking_number])
 
						print('Reservation found at hotel '+hotel.name)
						print(found_reservation)
						print('Total amount due: '+str(round(price,2)))
 
		else:
			name=input('Please enter your name: ')
			hotel_name=input('Please enter the hotel you are booked at: ')
			room_num=input('Enter the reserved room number: ')
			checkin_str=input('Enter the check-in date (YYYY-MM-DD):')
			checkout_str=input('Enter the check-out date (YYYY-MM-DD):')
 
			room_num=int(room_num)
 
			checkin_date=datetime.date(int(checkin_str[:4]),int(checkin_str[5:7]),int(checkin_str[8:]))	#same as in create_reservation
 
			for hotel in self.hotels:
				if hotel_name.lower==hotel.name:	# if this is true, we have found the hotel
					break
			for reservation in hotel.reservations.values():	# we will check through all the reservations
				if reservation.name==name and checkin_date==reservation.check_in and reservation.room_reserved.room_num==room_num:
					break		# if these are truem we are sure to have found our reservation
				else:
					reservation=None	# this is for the if check later
 
			if reservation==None:
				print('No reservation found.')
			else:
				print('Reservation found under booking number '+str(reservation.booking_number))
				print('Here are the details:')
				price=hotel.get_receipt([reservation.booking_number])
				print(reservation)
				print('Total amount due: $'+str(round(price,2)))
 
	def delete_reservations_at_random(self):
		"""
		random.seed(1338)
		booking = Booking.load_system()
		booking.delete_reservations_at_random()
		len(booking.hotels[1].reservations)
		len(booking.hotels[0].reservations)
		"""
		print('You said the magic word!')
		num_hotels=len(self.hotels)
		index=random.randint(0,num_hotels-1)
 
		hotel=self.hotels[index]
 
		booknum_list=list(hotel.reservations.keys())	# this must be turned into list, otherwise deleting off the dictionary will
														# generate errors
 
		for booking_num in booknum_list:
			hotel.cancel_reservation(booking_num)
			Reservation.booking_numbers.remove(booking_num)
 
	def plot_occupancies(self, month_str):
		"""
		booking = Booking.load_system()
		booking.plot_occupancies('Oct')
		"""
		month_num=MONTH_STR_TO_INT[month_str]
		month_len=DAYS_PER_MONTH[month_num-1]
		days= list(range(1,month_len+1))
 
		occupancy_per_hotel={}
 
		for hotel in self.hotels:	#over all hotels
			occupancy=[0]*month_len
 
			for room in hotel.rooms:	#all rooms in hotel
 
				for key in room.availability:	# find the correct month in availability
 
					if key[1]==month_num:
 
						count_occupancy=room.availability[key][1:] #we need to slice out the None
						for index in range(len(count_occupancy)):
 
							occupancy[index]+=not count_occupancy[index]	# if True we add 0, if False, we add 1
 
				else:
					pass
			occupancy_per_hotel[hotel]=occupancy
 
		legend=[]
 
		out_put=[]		#2 tuple with list of days and occupancy per hotel
		for hotel in self.hotels:
			plt.plot(days,occupancy_per_hotel[hotel])
			legend.append(hotel.name)
			out_put.append((days,days,occupancy_per_hotel[hotel]))
 
		plt.legend(legend)
		plt.title('Occupancies for month of '+month_str)
		plt.xlabel("Day of month")
		plt.ylabel("Number of reservations")
			
		plt.show()
 
		return out_put