import time
import datetime


class Incomes:
    days = []
    name = ""
    netIncome = 0
    dateOfFirstCheck = datetime.datetime(2018, 1, 1)

    def __init__(self, name, days, netIncome, dateOfFirstCheck):
        self.days = days
        self.name = name
        self.netIncome = netIncome
        self.dateOfFirstCheck = dateOfFirstCheck

    def getCheckDatesForYear(self, year):
        datesToReturn = []

        if(len(self.days) > 1):
            """Treat as fixed days in the month"""
            for x in range(1,12):
                for y in self.days:
                    datesToReturn.append(datetime.date(int(year), int(x), int(y)))
        else:
            """Treat as number of days between checks"""
            dateToAdd = self.dateOfFirstCheck
            while(self.dateOfFirstCheck.year != int(year)):
                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.days[0]))
            while(dateToAdd.year == int(year)):
                datesToReturn.append(dateToAdd)
                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.days[0]))

        return datesToReturn


"""Contains prompts to populate an Incomes object"""
def inputAnIncome():
    inputName = input("Please enter the name of the income source: ")
    inputNetIncome = input("Please enter the net income earned per pay period: ")

    print("You are going to enter information from a check that you have earned in the past.")
    year = input("Please enter the year of the check you are using to initialize: ")
    month = input("Please enter the month of the check you are using to initialize: ")
    day = input("Please enter the day of the check you are using to initialize: ")
    inputDateOfInitialCheck = datetime.date(int(year), int(month), int(day))

    i = 1
    inputDays = []
    selection = input("Please enter '1' for fixed dates of pay or '2' for number of days between checks: ")
    while(int(i)):
        if(int(selection) == 1):
            day = input("Please enter a day of the month for pay or '0' to exit: ")
            while(int(day)):
                inputDays.append(day)
                day = input("Please enter a day of the month for pay or '0' to exit: ")
            i = 0
        elif(int(selection) == 2):
            inputDays.append(input("Please enter the number of days between checks. i.e. enter 14 days if you are paid every 2 weeks: "))
            i = 0
        else:
            selection = input("Please enter '1' for fixed dates of pay or '2' for number of days between checks: ")


    return Incomes(inputName,inputDays,inputNetIncome,inputDateOfInitialCheck)


testIncome = inputAnIncome()

print(testIncome.getCheckDatesForYear(2018))














