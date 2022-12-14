# IOET Challenge

## Customer's Requirements and Definition

### Problem Statement
The company ACME offers their employees the flexibility to work the hours they want. They will pay for the hours worked based on the day of the week and time of day, according to the following table:

### Wage Rate for Time Shift Intervals

Monday - Friday
00:01 - 09:00 25 USD
09:01 - 18:00 15 USD
18:01 - 00:00 20 USD

Saturday and Sunday
00:01 - 09:00 30 USD
09:01 - 18:00 20 USD
18:01 - 00:00 25 USD

### Days Format and week ordering

MO: Monday
TU: Tuesday
WE: Wednesday
TH: Thursday
FR: Friday
SA: Saturday
SU: Sunday

### Data Input
The data should be supplied inside a file, containing the name of an employee and the schedule they worked, indicating the time and hours. 
 
### Data Output
The customer wants the program to indicate how much the employee has to be paid, but does not specify type of ouput, so screen representation is chosen by development team

### Customer's Data Format Definition and Input/Output Examples

The Customer provided the Development Team with this data, in order to guide the design and development of the solution:

Case 1:
INPUT
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00

OUTPUT:
The amount to pay RENE is: 215 USD

Case 2:
INPUT
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00

OUTPUT:
The amount to pay ASTRID is: 85 USD

## Overview 
A script is is presented to solve Customer's stated problem.
A file containing labor records for all employees is proccessed by the script to output the payroll relative to that input data.

## Design Decisions
The most important relevant decision in the design phase was related to time format representation and handling, the "Discrete" Time issue.

So a _Planar_ system was designed, and later developed and the following paragraph explains the internal of this design decision that was chosen.

Due to Customer's Time Definition Format (which resembles a "discrete" time specification), with no date indication at all, a decision had to be chosen (among many of them!) for time handling regarding booked labor shift records which dealt with simplicity of coding it.

The alternative chosen involved converting hours to minutes and summing them to the remaining minutes. The resulting sum should range in the interval (0:1440].

Day values are not involved in this calculation because, as Customer's specification has this kind of "discrete" format where no datetime is used, there's no relation to dates (which indeed implies an ordinal relationship day after day, conforming months and years).

The following matrix summarizes the core idea behind time handling in the script, from Monday tom Monday, salary has three time shifts available for a wage rate, and if it's a weekend day, then USD5.- is added to the wage. Time intervals are converted to intervals (0:540] [541:1080][1081:1440].
A dictionary will hold this structure, and cell queries will be perform to obtain corresponding data:

![imagen](https://user-images.githubusercontent.com/69780507/207490516-19bead59-5445-4898-8fd2-098e8b7756f3.png)


Even tough a _planar_ time system was envisioned, still, booked records would present situations where an employee started his duties on an time interval and ended them in other one, which imply different wages for each time interval.

Even though the Customer didn't state it, our design will let the Customer process records like MO10:15-23:28. Given this _planar_ time system, it would only cost a recursive function to _disassemble_ the labor time shift in smaller intervals, where every one of them would _fit_ into the corresponding wage intervals.

The Customer specified three wage time intervals: 00:01-09:00 for USD 25, 09:01-18:00 for USD 15 and 18:01-00:00 for USD 20. So the record MO05:32-15:21 has to be processed like two time shift intervals, being MO05:32-09:00 for USD 25/hr and MO09:01-15:21 for USD 15/hr. If the day should have been Saturday, USD 5 additionally should have been summed to the two wage time intervals involved! 

Amount to pay to every employee would deal with calculating the quantity of _planar_ minutes each interval has multiplied by its wage rate (that we decided to make it USD/minute and not USD/hour to let the Customer specify every possible time for a day) taken into account the additional sum if the day is a weekend.   

Additionally, Customer should be asked for an enhancement request approval, regarding the use of datetime format instead the present one, which would permit to book shift records spawning over two or more days (i.e. start time Monday at 23:00 and ending at Tuesday 04:00) and also let present a broader coverage of booked records (ranging from months to years, not only an unidentified _week_ like now) instead of discrete days and minutes that only lets booking of in-day labor shifts up to just a week. 

If it's not possible to address an enhancement that implies using one of the many datetime formats available from ISO8601, at least Development Team should propose a new record format (i.e. MO23:00-TU04:00), which would permit the Customer to book shift records that _spawn_ over days (i.e. start time Monday at 23:00 and ending at Tuesday 04:00) instead of discrete days and minutes for only _intra-day_ labor records, that foresee a considerable solution for incoming possible situations that may arise.

Regarding Secure Coding Practices, the script should sanitize and/or distrust user input at its most extend possible, considering Customer could not assure data quality feeding into the script. _Accept All Inputs, Trust NO inputs_ is the Secure Coding Methodology that is going to be appled.

in this release, and given time constrains, _internal_ secure coding related to functions that doesn´t directly deal with input data, is left unsecure, mainly regarding exception handling, and is left for DevSecOps later analysis.  

## Development
A "quick and dirty" script is presented to solve Customer's stated problem, where KISS methodology drives all code solutions.

No OOP was coded, merely functions that calls one over another, making ~ 200 lines of code. Functions are documented (reST format) and tests are also presented that checks some specific situations handling.

Whenever Developed Team spotted possible expected emergencies, exceptions handling were coded. _Expecting the unexpected_ another pair of exception handling routines were coded, like skipping records that were not compliance with the Customer's data format (but spare the remaining ones to be processed!)    

Last but not least, an specific function was developed to address the issue when a labor record hits the end of the day, which from the Customer's perspective happens at "00:00" (note that time shift interval starts at 00:001!) but for practical purposes the Development Team adjusted internally that time to "24:00" to let the _planar_ time system developed to achieve the 1440 minute-mark corresponding to the end of the day.


The core payment calculation is held by the following chained functions:

```
get_weekly_payment_for_all_employees() -> get_weekly_payment_for_specific_employee() -> get_hourly_payment() -> calculate_hourly_amount() [R] -> calculate_basic_wage() -> calculate_hourly_wage()

[R] Recursive Function
```

All functions that directly deals with data coming from user input are "secure", meaning that bounds are checked for non-compliant data like hours "bigger" than 24, minutes "bigger" than 60, but also non-compliant checks are held respect to the Customer's Data Format that specifies labor records. These Customer's compliant checks are held with ReGex'es for ease and are thoroughly tested in the present code.  

## How to run the script locally
The script requires the filename where the input data is stored, full filepath+filename could also be specified.

You may run the script to get the call syntax this way:

```
./ioet_python_challenge.py 
usage: ioet_python_challenge.py [-h] filename
ioet_python_challenge.py: error: the following arguments are required: filename

```

Given the following file with these labor records present inside it:

```
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00
MIKE=TH09:00-18:00,TU04:00-23:00,SA05:00-19:00
LAURA=MO06:34-14:58,TU10:50-00:00
KIM=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00,MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
```

you may run the script in this way:

```
./ioet_python_challenge.py ioet_challenge_test_input_data.txt 
```

to get the following output on screen:

```
The amount to pay RENE is: 215.00 USD
The amount to pay ASTRID is: 85.00 USD
The amount to pay MIKE is: 818.42 USD
The amount to pay LAURA is: 377.25 USD
The amount to pay KIM is: 430.00 USD
```

You may also run tests regarding synthetic conditions this way:

```
./ioet_python_challenge_test.py
```

Which in turn will perform a series of test against the crucial functions of the script:


```
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.002s

OK
```

##TODO
* Some functions needs Exception Handling, like day_of_week(), record_time_interval_is_coherent(), is_weekend(), etc. If they're going to be used "outside" this script, EH should be added, because input is not sanitized by previous functions this script has!

* REGEX should be improved to handle name with spaces in between, but error can be done if only spaces are specified by the Customer, special sanitization should be carried, additionally besides the REGEX


* Code should be added to deal with overlapping non equal records for a same employee, like 'KIM=MO12:00-20:00,MO16:00-22:00', unifying in one labor time shift 12:00-22:00



* Add more tests cases


##ENHANCEMENT REQUEST
Wait for Customer's approval for implementing a "full" datetime compatible data format that would much improve the script
