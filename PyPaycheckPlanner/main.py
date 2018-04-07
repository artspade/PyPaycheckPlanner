import time
import datetime
import os
import pickle


class Incomes:
    myDays = []
    myName = None
    myNetIncome = None
    myDateOfFirstCheck = None

    def __init__(self, theName, theDays, theNetIncome, theDateOfFirstCheck):
        self.myDays = theDays
        self.myName = theName
        self.myNetIncome = theNetIncome
        self.myDateOfFirstCheck = theDateOfFirstCheck

    def getCheckDatesForYear(self, theYear):
        datesToReturn = []

        if(len(self.myDays) > 1):
            """Treat as fixed days in the month"""
            for x in range(1,12):
                for y in self.myDays:
                    datesToReturn.append(datetime.date(int(theYear), int(x), int(y)))
        else:
            """Treat as number of days between checks"""
            dateToAdd = self.myDateOfFirstCheck



            if(dateToAdd.year < int(theYear)):
                while(dateToAdd.year < int(theYear)):
                    dateToAdd = dateToAdd + datetime.timedelta(days = int(self.myDays[0]))


            elif(dateToAdd.year == int(theYear)):
                while(dateToAdd.year == int(theYear)):
                    dateToAdd = dateToAdd - datetime.timedelta(days = int(self.myDays[0]))

                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.myDays[0]))


            else:
                while(dateToAdd.year >= int(theYear)):
                    dateToAdd = dateToAdd - datetime.timedelta(days = int(self.myDays[0]))

                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.myDays[0]))

            while(dateToAdd.year == int(theYear)):
                datesToReturn.append(dateToAdd)
                dateToAdd = dateToAdd + datetime.timedelta(days = int(self.myDays[0]))






        return datesToReturn



    def __str__(self):
        return "Name: %s\nNet Income: %s\nDate of first check: %s\nPaycheck Frequency: %s\n" % (self.myName, self.myNetIncome, self.myDateOfFirstCheck, self.myDays)

class Bills:
    myName = None
    myDueDate = None
    myAmountDue = None

    def __init__(self, theName, theDueDate, theAmountDue):
        self.myName = theName
        self.myAmountDue = theAmountDue
        self.myDueDate = theDueDate

    def __str__(self):
        return "Name: %s\nDue Date: %s\nAmount Due: %s\n" % (self.myName, self.myDueDate, self.myAmountDue)


class Debts(Bills):
    myTotalAmountOwed = None
    myInterestRate = None

    def __init__(self , theName, theDueDate, theAmountDue, theTotalAmountOwed, theInterestRate):
        self.myTotalAmountOwed = theTotalAmountOwed
        self.myInterestRate = theInterestRate
        Bills.__init__(self, theName,theDueDate,theAmountDue)

    def __str__(self):
        return Bills.__str__(self) + "Total Amount Still Owed: %s\nInterest Rate: %s" % (self.myTotalAmountOwed, self.myInterestRate)

        





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
        foldername = foldername.split(".")[-1][:-2]
        filename = foldername + "\\" + objectToSave.myName + ".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
           pickle.dump(objectToSave, f, pickle.HIGHEST_PROTOCOL)

def openFile(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "rb") as f:
        return pickle.load(f)

def deleteFile(objectToDetele):
    foldername = str(objectToDetele.__class__)
    """Always retrieves the leaf class"""
    foldername = foldername.split(".")[-1][:-2]
    filename = foldername + "\\" + objectToDetele.name + ".txt"
    try:
        os.remove(filename)
    except:
        print("Delete failed...")

def sandbox():

    """testIncome = inputAnIncome()"""
    incomes = []

    incomes.append(Incomes("Metagenics", [14], 1100, datetime.date(2018,3,23)))
    incomes.append(Incomes("CleanStart", [7,22], 1100, datetime.date(2018,3,22)))

    print(incomes[0])
    print(incomes[1])

    print(incomes[0].getCheckDatesForYear(2017))
    print(incomes[0].getCheckDatesForYear(2018))
    print(incomes[0].getCheckDatesForYear(2019))

    saveToFile(incomes[0])
    saveToFile(incomes[1])

    bills = []

    bills.append(Bills("Phone Bill", datetime.date(2018, 5, 9), 120))
    bills.append(Debts("Student Loan", datetime.date(2018, 5, 6), 300,40000,.05))

    print(bills[0])
    print(bills[1])

    saveToFile(bills[0])
    saveToFile(bills[1])


    bills[0] = openFile("Debts\Student Loan.txt")
    bills[1] = openFile("Bills\Phone Bill.txt")

    print("\n")
    print(bills[0])
    print("\n")
    print(bills[1])




sandbox()

















