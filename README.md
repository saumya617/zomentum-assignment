# zomentum-assignment
Movie Theatre Ticket Booking REST API services

#Tech and Frameworks used:
Framework: flask
Runtime Environment: python
For Database: MongoDB

#Functionalities involved:
1.Book a Movie Ticket.
2.Update the previously booked Ticket Timings.
3.View all the tickets for a particular time/show.
4.Delete a particular ticket.
5.View User based on ticket ID. 

->A movie ticket will be deleted automatically after 8 hours.

#Schema Involved
As we gonna have shows for which user books a ticket.So,a Show Schema
is there which contain some information about show and for updating
ticketid I have made a new collection sitedata which will assign different 
id always and also show the count of total tickets.

data_table Schema:
_id:tcid
username: username,
num: phone number of user,
movietime: movie time,  %6pm %1pm
time: current time of inserting to delete Query object after 8 hours.

ticketdata schema:
tctid:last id number assigned,
ctid:No. of tickets.
