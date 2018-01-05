# iCalendarGenerator
A quick and dirty iCalendarGenerator script to schedule reoccuring events

## How to use this script?
1. Make sure Python 3 is installed
1. Make sure you have dependancies installed using pip install 'package'
1. Download the icalGenerator.py script
1. Edit the constants at the top of the file
1. Create an input file, with each line being an event with the format
	* Event Name
	* Day of the Week
	* Start Time (hh:mm)
	* End Time (hh:mm)
1. Run the script using python ./icalGenerator.py
1. Voilla! You have a new ical file that (should) conform to GCal standards
