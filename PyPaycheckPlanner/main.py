import time
import datetime
import os
import pickle


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
            while(dateToAdd.year == int(year)):
                dateToAdd = dateToAdd - datetime.timedelta(days = int(self.days[0]))

            dateToAdd = dateToAdd + datetime.timedelta(days = int(self.days[0]))
            while(dateToAdd.year == int(year)):
                datesToReturn.append(dateToAdd)
                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.days[0]))

        return datesToReturn



    def toString(self):
        return "Income\nName: %s\nNet Income: %s\nDate of first check: %s\nPaycheck Frequency: %s\n" % (self.name, self.netIncome, self.dateOfFirstCheck, self.days)


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

def saveToFile(objectToSave):
        foldername = str(objectToSave.__class__)
        foldername = foldername[17:-2]
        print(foldername)
        filename = foldername + "\\" + objectToSave.name + ".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
           pickle.dump(objectToSave, f, pickle.HIGHEST_PROTOCOL)

def openFile(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "rb") as f:
        return pickle.load(f)



def deleteFile(objectToDetele):
    foldername = str(objectToDetele.__class__)
    foldername = foldername[17:-2]
    filename = foldername + "\\" + objectToDetele.name + ".txt"
    try:
        os.remove(filename)
    except:
        print("Delete failed...")



"""testIncome = inputAnIncome()"""
incomes = []

incomes.append(Incomes("Metagenics", [14], 1100, datetime.date(2018,3,23)))
incomes.append(Incomes("CleanStart", [7,22], 1100, datetime.date(2018,3,22)))

print(incomes[0].toString())
print(incomes[1].toString())

print(incomes[0].getCheckDatesForYear(2018))
print(incomes[1].getCheckDatesForYear(2018))

saveToFile(incomes[0])
saveToFile(incomes[1])


















