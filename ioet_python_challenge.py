#!/usr/bin/env python
import re
import sys
import csv
import argparse
from collections import defaultdict
CHECK_RAW_RECORD_REGEX = '((^[a-zA-Z]{2,15})=((MO|TU|WE|TH|FR|SA|SU)\d{2}:\d{2}-\d{2}:\d{2}(,)?)+$)'
GET_EMPLOYEE_NAME_REGEX = '^([a-zA-Z]{2,15})='
GET_EACH_EMPLOYEE_RECORD_REGEX = '^\w+=(.*)$'
GET_DAY_AND_TIME_HOURLY_RECORD_REGEX = '^(MO|TU|WE|TH|FR|SA|SU)(\d{2}:\d{2})-(\d{2}:\d{2})$'
GET_HOUR_AND_MINUTES_REGEX = '^(\d{2}):(\d{2})$'
DAYS_OF_WEEK = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')
BASE_TIMESHIFT_RATE_WAGE = {'Early Morning Shift':(0,540,25/60),'Normal Shift':(541,1080,15/60),'Night Shift':(1081,1440,20/60)}
EXTRA_WEEKEND_WAGE_PER_MINUTE = 5/60

#https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/

""" 
Parse the CLI invocation arguments  

:returns: returns all the arguments invoked with the script
"""
def parse_cli_invocation():
 parser = argparse.ArgumentParser()
 parser.add_argument('filename', help="filename which contains labour records")
 args = parser.parse_args()
 return args

"""
Read each line of input file supplied and return them as a list

:param filename: filename where records are contained
:returns: returns a list containing the records in the filename indicated
:raises FileNotFoundError: catches an exception if file is not present
:raises Exception: catches an exception if any other exception arises
"""
def read_input_file(filename):
 try:
  list_of_lines = [line.rstrip() for line in open(filename)]
  return list_of_lines
 except FileNotFoundError as e:
  sys.exit('File does not exist:' + str(e))
 except Exception as e:
  sys.exit('An error occurred during reading input file:' + str(e))

"""
Performs a RegEx over a text, returning the group specified

:param regex: RegEx to be performed
:param text:  text that is gonna be _regexed_
:param group: group that wants to be returned, 0 for whole match
:returns: returns a string containing the matched characters
"""
def regex_search_match(regex, text, group):
 regex = re.compile(regex)
 return regex.match(text).group(group)

"""
Checks if a _raw record_ (just a line in the input file supplied) complies with customer's format definition

:param raw_record: string containing the one-line record of an Employee
:returns: returns True if raw_record complains with customer's format definition, else False
"""
def check_raw_record(raw_record):
 return regex_search_match(CHECK_RAW_RECORD_REGEX, raw_record, 0)

"""
Gets the employee's name present in the _raw record_ and returns it as a string

:param raw_record: string containing the one-line record of an Employee
:returns: returns a string containing the employee's name
"""
def get_employee_name(raw_record):
 return regex_search_match(GET_EMPLOYEE_NAME_REGEX, raw_record, 1)

"""
Gets the employee's shift records as a comma-separated one-line string, and returns them as a sole string

:param raw_record: string containing the one-line record of an Employee
:returns: returns a string containing all the employee's shift records as a comma-separated one-line string
"""
def get_each_employee_record(raw_record):
 return regex_search_match(GET_EACH_EMPLOYEE_RECORD_REGEX, raw_record, 1)

"""
Gets the day, start and end time of a specific employee's shift record, and returns them as a string tuple

:param hourly_record: string according to customer's format definition
:returns: returns a tuple containing day, start and end time, as string values that will be _casted_ later
"""
def get_day_and_time_from_hourly_record(hourly_record):
 return (regex_search_match(GET_DAY_AND_TIME_HOURLY_RECORD_REGEX, hourly_record, 1), regex_search_match(GET_DAY_AND_TIME_HOURLY_RECORD_REGEX, hourly_record, 2), regex_search_match(GET_DAY_AND_TIME_HOURLY_RECORD_REGEX, hourly_record, 3))

"""
Converts a pair hours/minutes time string into an integer tuple, "00:00" defined by customer is converted to "24:00" for later _planar_ convertion

:param time_string: a string complying to "HH:MM" format, Customer's definition for "24:00" is "00:00", so this function turns "00:00" into "24:00"
:returns: returns an hour/minutes integer tuple
:raises Exception: raises an exception if any hours or minutes value is out of bounds
"""
def get_hour_and_minutes_from_time_string(time_string):
 hour = int(regex_search_match(GET_HOUR_AND_MINUTES_REGEX, time_string, 1))
 minutes = int(regex_search_match(GET_HOUR_AND_MINUTES_REGEX, time_string, 2))
 if (hour>24 or minutes>60):
  raise Exception(str(hour) + " or " + str(minutes) + " are out of bounds, check your input data file, please!")
 return (hour, minutes)

"""
Gets each time shift record for each employee from the file supplied, after a customer's definition format check is successful

:param records_from_file: records read from the file supplied
:returns: returns a dictionary containing all the time shift records of all employees
:raises Exception: raises an exception if no results are present at the end of the execution
:raises Exception: catches an exception if any unplanned situation occurs
"""
def get_data_from_input_file(records_from_file):
 results = defaultdict()
 raw_records = records_from_file
 try:
  for raw_record in (raw_records):
   if check_raw_record(raw_record):
    results[get_employee_name(raw_record)] = get_each_employee_record(raw_record).split(",")
  if not results:
   raise Exception("No records at all, check your input data file, please!")
  return results
 except Exception as e:
  sys.exit('An error occurred during information parsing:' + str(e))

"""
Checks wether if time shift start time is past (or not) than end time

:param record_start_time: time shift start time, using _planar_ (minutes) format
:param record_stop_time: time shift end time, using _planar_ (minutes) format
:returns: True if start time is before than end time, raises an exception otherwise
:raises Exception: raises an exception if start time is past end time

:TODO: Add Exceptions for handling out of bounds inputs!
"""
def record_time_interval_is_coherent(record_start_time, record_end_time):
 if (record_start_time<=record_end_time):
  return True
 else:
  raise Exception(str(record_start_time)+" as start time is ahead of "+str(record_end_time)+" end time, check your input data file, please!")

"""
Gets the ordinal number of the day, return it as an integer.
Customer's definition states week starts on Mondays!

:param day: day in customer's definition format
:returns: returns the equivalent integer for a day string

:TODO: Add Exceptions for handling out of bounds inputs!
"""
def get_number_of_day(day):
 return DAYS_OF_WEEK.index(day)+1 

"""
Checks whether a day is a normal one or a weekend one
Customer's definition states week starts on Mondays!

:param day_of_week: day as an integer, derived from customer's definition format, where the 1st. day is Monday
:returns: returns True if day is weekend one, False otherwise

:TODO: Add Exceptions for handling out of bounds inputs!
"""
def is_weekend(day_of_week):
 return (day_of_week>5)

"""
Midnight "00:00" in Customer's definiton format shift (start or end) time is converted to midnight "24:00" for later _planar_ convertion

:param hours: hours, in integer cast type
:param minutes: minutes, in integer cast type
:returns: returns 24 if "00:00" is supplied, else the original hours value is returned

:TODO: Add Exceptions for handling out of bounds inputs!
"""
def adjust_0000_to_2400(hours, minutes):
 if (hours==0) and (minutes==0):
 	return 24
 else:
 	return hours

"""
Converts "HH:MM" time shift format into _planar_ minutes, for an easy handling of time calculations.
Also midnight "00:00" shift start or end time defined by customer is converted to midnight "24:00".
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00

:param time: string complying to "HH:MM" customer's format definition
:returns: returns an integer representing the minutes of that specified time, if "00:00" is supplied, it is converted to 1440 minutes (a whole day long!)
"""
def time_to_planar_time(time):
 hours, minutes = get_hour_and_minutes_from_time_string(time)
 return (adjust_0000_to_2400(hours,minutes)*60)+minutes

"""
Gets the amount of money of a given time shift, where start and stop times are supplied as strings in customer's format definition "HH:MM", returns payment
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00
Note II: This function only works on SAME interval!

:param day: day as customer's definition format, where the 1st. day is Monday
:param start_time: time shift start time, using customer's format "HH:MM", later will be converted to _planar_ (minutes) format
:param stop_time: time shift end time, using customer's format "HH:MM", later will be converted to _planar_ (minutes) format
:returns: returns the amount of money to pay for the present time shift

:TODO: Add Exception Handling when start and end time are NOT on same interval (this is covered in _upper_ funcition!)
"""
def get_hourly_payment(day, start_time, end_time):
 day_of_week = get_number_of_day(day)
 planar_start_time = time_to_planar_time(start_time)
 planar_end_time = time_to_planar_time(end_time)
 if record_time_interval_is_coherent(planar_start_time, planar_end_time):
  return calculate_hourly_amount(day_of_week, planar_start_time, planar_end_time)

"""
Gets the amount of money of a given time shift, where start and stop times are supplied as _planar_ (minutes) integers
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00

:param day: day as an integer, derived from customer's definition format, where the 1st. day is Monday
:param start_time: time shift start time, using _planar_ (minutes) format
:param stop_time: time shift end time, using _planar_ (minutes) format
:returns: returns the amount of money to pay for the present time shift
"""
def calculate_basic_wage(day, start_time, end_time):
 return ((calculate_hourly_wage(day, start_time) + EXTRA_WEEKEND_WAGE_PER_MINUTE * is_weekend(day)) * (end_time - start_time))

"""
Gets the specific wage rater per minute given time and day supplied

:param day: day as an integer, derived from customer's definition format, where the 1st. day is Monday
:param start_time: time shift start time, using _planar_ (minutes) format
:returns: returns base wage per minute as an float
"""
def calculate_hourly_wage(day,start_time):
 for time_shift in BASE_TIMESHIFT_RATE_WAGE:
  if start_time in range(BASE_TIMESHIFT_RATE_WAGE[time_shift][0], BASE_TIMESHIFT_RATE_WAGE[time_shift][1]+1):
   return BASE_TIMESHIFT_RATE_WAGE[time_shift][2]

"""
Gets the upper limit of a time shift interval based on the time specified, return it as an integer

:param time_shift: string representing the time shift interval selected
:returns: returns the upper limit (as an integer) of the time shift interval selected
"""
def get_ceil_time_shift(time_shift):
 return (BASE_TIMESHIFT_RATE_WAGE[time_shift][1]) 

"""
Gets the time shift as a string, given a time reference which belongs to that time shift interval

:param time: time belonging to the time shift interval, using _planar_ (minutes) format
:returns: returns the time shift as a string
"""
def get_time_shift(time):
 for time_shift in BASE_TIMESHIFT_RATE_WAGE:
  if time in range(BASE_TIMESHIFT_RATE_WAGE[time_shift][0], BASE_TIMESHIFT_RATE_WAGE[time_shift][1]+1):
   return time_shift

"""
Checks whether if start and end times belong to same time shift interval

:param start_time: time shift start time, using _planar_ (minutes) format
:param end_time: time shift end time, using _planar_ (minutes) format
:returns: returns True if both times belong to same time shift interval, False otherwise
"""
def same_time_shift(start_time, end_time):
 return (get_time_shift(start_time) == get_time_shift(end_time))

"""
Recursive function that returns the amount for a labor time given day, start and end time
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00

:param day: day as an integer, derived from customer's definition format, where the 1st. day is Monday
:param start_time: time shift start time, using _planar_ (minutes) format
:param end_time: time shift end time, using _planar_ (minutes) format
:returns: returns (when it reaches the recursive base case!) the amount to pay as a float
"""
def calculate_hourly_amount(day, start_time, end_time):
 if not same_time_shift(start_time, end_time):
  time_shift_ceiling_for_present_start_time = get_ceil_time_shift(get_time_shift(start_time))
  hourly_amount =  calculate_basic_wage(day, start_time, time_shift_ceiling_for_present_start_time) + calculate_hourly_amount(day, time_shift_ceiling_for_present_start_time+1, end_time)
 else:
  hourly_amount = calculate_basic_wage(day, start_time, end_time)
 return hourly_amount 

"""
Calculates the amount to pay for a specific employee given all of his labor records
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00

:param weekly_employee_records: list of strings, representing all labor records for an specific employee
:returns: returns the amount to pay, as a float, to the specific employee
:raises Exception: raises an exception if any labor record does not comply to Customer's Definition Format
"""
def get_weekly_payment_for_specific_employee(weekly_employee_records):
 payment = 0
 for hourly_record in weekly_employee_records:
  day, start_time, end_time = get_day_and_time_from_hourly_record(hourly_record)
  try: 
   payment += get_hourly_payment(day, start_time, end_time)
  except Exception as e:
   print("Skipping record:", day, start_time, end_time, "Exception:",e)
   continue
 return payment

"""
Calculates the amount to pay to all the employees supplied given all of their labor records
Note: Customer's Format Definition does not let specify timeshift that spawns over more than one day, i.e. _from Monday 23:00 until Tuesday 02:00

:param weekly_records_of_all_employees: list of strings, representing all labor records of all employees
:returns: returns the amount to pay to each customers, as a dictionary where tuple format is ("employee":amount)
"""
def get_weekly_payment_for_all_employees(weekly_records_of_all_employees):
 payroll = defaultdict(list)
 for employee in weekly_records_of_all_employees:
  payroll[employee] = (get_weekly_payment_for_specific_employee(weekly_records_of_all_employees[employee]))
 return payroll

"""
Prints the amount to pay to each employee, according to Customer's Definition Format for data output
Note: cents are two decimals rounded, future version may consider changing amount format where cents are part of a tuple of integers

:param paychecks: amount to pay to each customer, as a dictionary, where tuple format is ("employee":amount) 
:returns: None
"""
def print_paychecks(paychecks):
 for employee in paychecks:
  print("The amount to pay",employee,"is:","%.2f" % paychecks[employee],"USD")

if __name__ == '__main__':
 filename_argument = parse_cli_invocation().filename
 employee_records = get_data_from_input_file(read_input_file(filename_argument))
 paychecks = get_weekly_payment_for_all_employees(employee_records)
 print_paychecks(paychecks)
