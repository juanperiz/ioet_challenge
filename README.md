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

