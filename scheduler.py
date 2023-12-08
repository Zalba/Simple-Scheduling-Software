#This is a test project to get back into the groove of coding

#This will be a scheduler for a workplace
#First it will schedule based on worker availability, people needed, and weekday
#Then it will include people's requestoffs, and make sure the store Notary and Manager have "fulltime" hours
#Finally it will account for workers desired days off
#Creator: Zach Alba
#Latest update: 11/07/22 10:21PM

#Imports
import datetime
import json
import math

#Universal variables
one_day = datetime.timedelta(days=1)
#Functions
def available(time, weekday, data):
    avAM = []
    avPM = []
    for x in data['employees']:
        #check if employee is available
        if data['employees'][x]['availability'][weekday] != None:
            if time == 0:
                #check if available for Open on Saturday
                if weekday == "Saturday" and data['employees'][x]['availability']["Saturday"][0] == 9:
                    # print(x, " ", data['employees'][x]['availability'][weekday][0])
                    avAM.append(x)
                #check if available for Open on sunday
                elif weekday == "Sunday" and data['employees'][x]['availability'][weekday][0] == 10:
                    # print(x, " ", data['employees'][x]['availability'][weekday][0])
                    avAM.append(x)
                #check for availability for Open on Monday-Friday
                elif data['employees'][x]['availability'][weekday][0] == 8:
                    # print(x, " ", data['employees'][x]['availability'][weekday][0])
                    avAM.append(x)
            if time == 1:
                #check if available for Open on Saturday
                if weekday == "Saturday" and data['employees'][x]['availability']["Saturday"][time] == 16:
                    # print(x, " ", data['employees'][x]['availability'][weekday][time])
                    avPM.append(x)
                #check if available for Open on sunday
                elif weekday == "Sunday" and data['employees'][x]['availability'][weekday][time] == 15:
                    # print(x, " ", data['employees'][x]['availability'][weekday][time])
                    avPM.append(x)
                #check for availability for Open on Monday-Friday
                elif data['employees'][x]['availability'][weekday][time] == 19:
                    # print(x, " ", data['employees'][x]['availability'][weekday][time])
                    avPM.append(x)
    if time == 0:
        return avAM
    if time == 1:
        return avPM

def compare(l1, l2):
    ls = []
    #See if someone can only open or visversa
    for x in l1:
        z = 0
        for y in l2:
            if x == y:
                #print("found")
                z = 1
        if z == 0:
            #print (x)
            #print("This person should be scheduled first (special hours)")
            ls.append(x)
    return ls

def scheduling(s_date, data):
    #Load schedule template
    schedule = open('schedule_template.json','r')
    sch = json.loads(schedule.read())
    stats = {}
    for p in data['employees']:
        stats[p] = {'tDays': 0, 'tHours': 0, 'closes': 0, 'opens': 0}
    #Start scheduling (looping through work week)
    #print(stats)
    for x in data['week']:
        tscheduled = 0
        #Check morning and evening workers
        avAM = available(0, x, data)
        avPM = available(1, x, data)

        if x != "Saturday" and x != "Sunday":
            #See if any openers cannot close/any closers cannot open
            opener = compare(avAM,avPM)
            closer = compare(avPM, avAM)
            #Schedule openers
            if opener != []:
                for person in opener:
                    #person availability
                    person_av = data["employees"][person]["availability"][x]
                    if person_av[1]-person_av[0] <= 8:
                        sch["shifts"][x].append({"person": person,
                        "shift": person_av})
                        stats[person]['tDays'] += 1
                        stats[person]['tHours'] += person_av[1]-person_av[0]
                        stats[person]['opens'] += 1
                        tscheduled += 1

            #Check number of openers
            if tscheduled < 2:
                for person in avAM:
                    if stats[person]['tDays'] <= 0 and tscheduled < 2 or tscheduled < 2 and stats[person]['opens'] < 0:
                        #person availability
                        person_av = data["employees"][person]["availability"][x]
                        if 15-person_av[0] <= 8:
                            sch["shifts"][x].append({"person": person,
                            "shift": [person_av[0],15]})
                            stats[person]['tDays'] += 1
                            stats[person]['tHours'] += 15 - person_av[0]
                            stats[person]['opens'] += 1
                            tscheduled += 1

            #Schedule closers
            if closer != []:
                for person in closer:
                    #person availability
                    person_av = data["employees"][person]["availability"][x]
                    #less than an 8 hour day?
                    if person_av[1]-person_av[0] <= 8:
                        sch["shifts"][x].append({"person": person,
                        "shift": person_av})
                        stats[person]['tDays'] += 1
                        stats[person]['tHours'] += person_av[1]-person_av[0]
                        stats[person]['closes'] += 1
                        tscheduled += 1

            if len(sch["shifts"][x]) < 4:
                for person in avPM:
                    if stats[person]['tDays'] <= 0 and tscheduled < 4 or tscheduled < 4 and stats[person]['closes'] < 0:
                        #person availability
                        person_av = data["employees"][person]["availability"][x]
                        if person_av[0] <= 14:
                            sch["shifts"][x].append({"person": person,
                            "shift": [14,19]})
                            stats[person]['tDays'] += 1
                            stats[person]['tHours'] += 19 - person_av[0]
                            stats[person]['closes'] += 1
                            tscheduled += 1

        else:
            pass
        #print('day scheduled')
        #print('people scheduled:', len(sch["shifts"][x]))
        s_date = s_date + one_day
    print(stats)
    return sch


#Main function
def main():

    #Temp Code
    #Open dataset
    f = open('dataset.json', 'r')
    x = f.read()
    #Load it to a dictionary
    data = json.loads(x)

    #NEED TO AUTOMATE
    #Set date
    y = datetime.date(2022, 10, 16)
    new_sch = scheduling(y, data)
    print()
    print(new_sch)
    print()

main()
