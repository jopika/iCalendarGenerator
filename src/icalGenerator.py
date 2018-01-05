from icalendar import Calendar, Event
from datetime import datetime, timedelta
from dateutil.rrule import rrule, WEEKLY
import pytz
import tempfile, os
import uuid

"""Very simple calendar generator for courses from a pre formatted file"""
# Files are described so that each line contains an event:
# {Event Name} <delim> {Day of Week} <delim> {Start Time} <delim> {End Time}
# Times are using 24 hour clock, in the form of hh:mm
# Events that repeat multiple times in a week must be spread out across multiple lines

# Constants
# Year of the class start
START_YEAR  = 2018
# Month of the class start
START_MONTH = 1
# Monday's date of the week where classes start
START_DAY   = 1
# Year of the class start
END_YEAR  = 2018
# Month of the class start
END_MONTH = 4
# Monday's date of the week where classes start
END_DAY   = 2
# Path to input file
IN_PATH = './tutorials.txt'
# Path to output file
OUT_PATH = './tutorials.ics'

# Data structures
dateOffset = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4
}

def create_event_from_string(event_string, delim):
    """Creates a new event from the string given"""

    new_event = Event()
    event_array = event_string.split(sep=delim)
    # Strip the values and retrieve the hours and minutes for beginning and end
    beg_hour = event_array[2].split(sep=':')[0].strip()
    beg_min  = event_array[2].split(sep=':')[1].strip()
    end_hour = event_array[3].split(sep=':')[0].strip()
    end_min  = event_array[3].split(sep=':')[1].strip()

    # Generate the offset-ed date
    offset_beg_date = START_DAY + dateOffset[event_array[1].strip()]
    offset_end_date = END_DAY + dateOffset[event_array[1].strip()]
    # Generate the beginning date of the event
    beg_date = datetime(year=START_YEAR, month=START_MONTH,
                        day=int(offset_beg_date),
                        hour=int(beg_hour),
                        minute=int(beg_min),
                        tzinfo=pytz.timezone('America/Vancouver'))
    # Generate the endtime for the event
    beg_date_end = datetime(year=START_YEAR, month=START_MONTH,
                        day=int(offset_beg_date),
                        hour=int(end_hour),
                        minute=int(end_min),
                        tzinfo=pytz.timezone('America/Vancouver'))
    # Generate the end of the until for the event
    end_date = datetime(year=END_YEAR, month=END_MONTH,
                        day=int(offset_end_date),
                        hour=int(end_hour),
                        minute=int(end_min),
                        tzinfo=pytz.timezone('America/Vancouver'))
    # While the RFC states that <until> is depreciated, GCals still uses it... Oh well
    repeat_rule = rrule(freq=WEEKLY, dtstart=beg_date, until=end_date)

    # Attempt to deal with escaped characters here, it'd probably fail
    rule_string = str(repeat_rule).split('\n')[1].replace("\\\;",";")
    print(rule_string)
    # Add the information regarding the events here
    new_event.add('dtstamp', datetime.now())
    new_event.add('rrule', rule_string, encode=False)
    new_event.add('summary', event_array[0].strip())
    new_event.add('description', "")
    new_event.add('uid', str(uuid.uuid1()))
    new_event.add('dtstart',beg_date)
    new_event.add('dtend',beg_date_end)
    return new_event



def display_formatted_ical(cal):
    """Debugging print statement for the calendars"""
    return cal.to_ical().replace('\r\n', '\n').strip()


if __name__ == '__main__':
    cal = Calendar()
    cal.add('prodid', '-//Generated Calendar//iCal 1.0//EN')
    cal.add('version', '2.0')

    # Read file
    f = open(IN_PATH, 'r')
    for line in f:
        # Every line should correspond to some kind of Event
        event = create_event_from_string(line, '//')
        cal.add_component(event)

    directory = tempfile.mkdtemp()
    out_f = open(OUT_PATH, 'wb')
    out_f.write((cal.to_ical()))
    out_f.close()

    # Hack-y method to insert the timezone details for iCalendar specifications
    out_f = open(OUT_PATH, 'r')
    contents = out_f.readlines()
    out_f.close()

    # Constant strings to declare timezone details
    contents.insert(3,"CALSCALE:GREGORIAN\nMETHOD:PUBLISH\nBEGIN:VTIMEZONE\nTZID:America/Vancouver\nTZURL:http://tzurl.org/zoneinfo/America/Vancouver\nX-LIC-LOCATION:America/Vancouver\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0700\nTZNAME:PDT\nDTSTART:20070311T020000\nRRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0700\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:20071104T020000\nRRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\nEND:STANDARD\nBEGIN:STANDARD\nTZOFFSETFROM:-081228\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:18840101T000000\nRDATE:18840101T000000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0700\nTZNAME:PDT\nDTSTART:19180414T020000\nRDATE:19180414T020000\nRDATE:19460428T020000\nRDATE:19470427T020000\nRDATE:19480425T020000\nRDATE:19490424T020000\nRDATE:19500430T020000\nRDATE:19510429T020000\nRDATE:19520427T020000\nRDATE:19530426T020000\nRDATE:19540425T020000\nRDATE:19550424T020000\nRDATE:19560429T020000\nRDATE:19570428T020000\nRDATE:19580427T020000\nRDATE:19590426T020000\nRDATE:19600424T020000\nRDATE:19610430T020000\nRDATE:19620429T020000\nRDATE:19630428T020000\nRDATE:19640426T020000\nRDATE:19650425T020000\nRDATE:19660424T020000\nRDATE:19670430T020000\nRDATE:19680428T020000\nRDATE:19690427T020000\nRDATE:19700426T020000\nRDATE:19710425T020000\nRDATE:19720430T020000\nRDATE:19730429T020000\nRDATE:19740428T020000\nRDATE:19750427T020000\nRDATE:19760425T020000\nRDATE:19770424T020000\nRDATE:19780430T020000\nRDATE:19790429T020000\nRDATE:19800427T020000\nRDATE:19810426T020000\nRDATE:19820425T020000\nRDATE:19830424T020000\nRDATE:19840429T020000\nRDATE:19850428T020000\nRDATE:19860427T020000\nRDATE:19870405T020000\nRDATE:19880403T020000\nRDATE:19890402T020000\nRDATE:19900401T020000\nRDATE:19910407T020000\nRDATE:19920405T020000\nRDATE:19930404T020000\nRDATE:19940403T020000\nRDATE:19950402T020000\nRDATE:19960407T020000\nRDATE:19970406T020000\nRDATE:19980405T020000\nRDATE:19990404T020000\nRDATE:20000402T020000\nRDATE:20010401T020000\nRDATE:20020407T020000\nRDATE:20030406T020000\nRDATE:20040404T020000\nRDATE:20050403T020000\nRDATE:20060402T020000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0700\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:19181027T020000\nRDATE:19181027T020000\nRDATE:19450930T020000\nRDATE:19461013T020000\nRDATE:19470928T020000\nRDATE:19480926T020000\nRDATE:19490925T020000\nRDATE:19500924T020000\nRDATE:19510930T020000\nRDATE:19520928T020000\nRDATE:19530927T020000\nRDATE:19540926T020000\nRDATE:19550925T020000\nRDATE:19560930T020000\nRDATE:19570929T020000\nRDATE:19580928T020000\nRDATE:19590927T020000\nRDATE:19600925T020000\nRDATE:19610924T020000\nRDATE:19621028T020000\nRDATE:19631027T020000\nRDATE:19641025T020000\nRDATE:19651031T020000\nRDATE:19661030T020000\nRDATE:19671029T020000\nRDATE:19681027T020000\nRDATE:19691026T020000\nRDATE:19701025T020000\nRDATE:19711031T020000\nRDATE:19721029T020000\nRDATE:19731028T020000\nRDATE:19741027T020000\nRDATE:19751026T020000\nRDATE:19761031T020000\nRDATE:19771030T020000\nRDATE:19781029T020000\nRDATE:19791028T020000\nRDATE:19801026T020000\nRDATE:19811025T020000\nRDATE:19821031T020000\nRDATE:19831030T020000\nRDATE:19841028T020000\nRDATE:19851027T020000\nRDATE:19861026T020000\nRDATE:19871025T020000\nRDATE:19881030T020000\nRDATE:19891029T020000\nRDATE:19901028T020000\nRDATE:19911027T020000\nRDATE:19921025T020000\nRDATE:19931031T020000\nRDATE:19941030T020000\nRDATE:19951029T020000\nRDATE:19961027T020000\nRDATE:19971026T020000\nRDATE:19981025T020000\nRDATE:19991031T020000\nRDATE:20001029T020000\nRDATE:20011028T020000\nRDATE:20021027T020000\nRDATE:20031026T020000\nRDATE:20041031T020000\nRDATE:20051030T020000\nRDATE:20061029T020000\nEND:STANDARD\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0700\nTZNAME:PWT\nDTSTART:19420209T020000\nRDATE:19420209T020000\nEND:DAYLIGHT\nBEGIN:DAYLIGHT\nTZOFFSETFROM:-0700\nTZOFFSETTO:-0700\nTZNAME:PPT\nDTSTART:19450814T160000\nRDATE:19450814T160000\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:-0800\nTZOFFSETTO:-0800\nTZNAME:PST\nDTSTART:19870101T000000\nRDATE:19870101T000000\nEND:STANDARD\nEND:VTIMEZONE\n")
    # Replace any escaped characters, we don't need them
    contents = map(lambda x: str.replace(x, "\\", ""), contents)

    out_f = open(OUT_PATH, 'w')
    contents = "".join(contents)
    out_f.write(contents)
    out_f.close()

    f.close()