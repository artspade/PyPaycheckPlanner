import datetime
import os
import pickle


class Income:
    """
    Contains data and methods needed for Incomes. Such as the name, frequency, and amount from a source.
    """
    myDays = []
    myName = None
    myNetIncome = None
    myDateOfFirstCheck = None

    def __init__(self, theName, theDays, theNetIncome, theDateOfFirstCheck):
        """
        :param theName: of the income source (str)
        :param theDays: for payment ([1],[2,3])
        :param theNetIncome: received on payday (int/float)
        :param theDateOfFirstCheck: (datetime.date)
        """
        self.myDays = theDays
        self.myName = theName
        self.myNetIncome = theNetIncome
        self.myDateOfFirstCheck = theDateOfFirstCheck

    def getCheckDatesForRange(self, theStartDate, theEndDate):
        """
        Returns a list of all the dates for paychecks within the given date range.
        :param theStartDate:
        :param theEndDate:
        :return: a list of check dates for the given date range.
        """
        datesToReturn = []

        if (len(self.myDays) > 1):
            # Treat as fixed days in the month
            for x in range(theStartDate.year, theEndDate.year):  # year
                for y in range(1, 12):  # month
                    for z in self.myDays:  # day
                        datesToReturn.append(datetime.date(int(x), int(y), int(z)))
        else:
            # Treat as number of days between checks
            dateToAdd = self.myDateOfFirstCheck

            # if dateToAdd == theStartDate... Perfect!
            while (
                dateToAdd > theStartDate):  # brings dateToAdd to one check before theStartDate if dateToAdd is greater
                dateToAdd = dateToAdd - datetime.timedelta(days=int(self.myDays[0]))

            while (dateToAdd < theStartDate):  # brings dateToAdd to the first check after theStartDate
                dateToAdd = dateToAdd + datetime.timedelta(days=int(self.myDays[0]))

            while (dateToAdd <= theEndDate):  # add all paycheck dates for the range
                datesToReturn.append(dateToAdd)
                dateToAdd = dateToAdd + datetime.timedelta(days=int(self.myDays[0]))  # ++

        return datesToReturn

    def __str__(self):
        """
        :return: the string representation for the current class.
        """
        return "Name: %s\nNet Income: %s\nDate of first check: %s\nPaycheck Frequency: %s\n" % (
        self.myName, self.myNetIncome, self.myDateOfFirstCheck, self.myDays)


class Bill:
    """
    Contains data and methods needed to handle Bills. Such as the name, frequency, and cost.
    """

    myName = None
    myDueDay = None
    myNextDueDate = None
    myAmountDue = None

    def __init__(self, theName, theDueDay, theNextDueDate, theAmountDue):
        """
        :param theName: for the bill (str)
        :param theDueDay: the integer value for the day in the month of which the bill is due (int)
        :param theNextDueDate: the date that the bill is next due (datetime.date)
        :param theAmountDue: the cost of the bill (int/float)
        """
        self.myName = theName
        self.myAmountDue = theAmountDue
        self.myDueDay = theDueDay
        self.myNextDueDate = theNextDueDate

    def __str__(self):
        """
        :return: The string representation of a Bill
        """
        return "Name: %s\nDue Day: %s\nNext Due Date: %s\nAmount Due: %s\n" % (
        self.myName, self.myDueDay, self.myNextDueDate, self.myAmountDue)

    def getDueDatesForRange(self, theStartDate, theEndDate):
        """
        Returns a list of all the dates the bill is due given a date range
        :param theStartDate: the starting date range
        :param theEndDate: the ending date range
        :return: a list of datetime.date for all the bills due on the given date range
        """
        datesToReturn = []

        date = (self.myNextDueDate if self.myNextDueDate > theStartDate else datetime.date(theStartDate.year,
                                                                                           theStartDate.month,
                                                                                           self.myNextDueDate.day))
        while (date <= theEndDate):
            datesToReturn.append(date)
            date = (datetime.date(date.year, (date.month + 1), date.day) if (date.month + 1 <= 12) else datetime.date(
                date.year + 1, 1, date.day))

        return datesToReturn


class Debt(Bill):
    """
    Contains data and methods needed for Debt
    """
    myTotalAmountOwed = None
    myInterestRate = None

    def __init__(self, theName, theDueDay, theNextDueDate, theAmountDue, theTotalAmountOwed, theInterestRate):
        """
        :param theName: for the Debt (str)
        :param theDueDay: the day of the month the debt is due (int)
        :param theNextDueDate: the next due date for the debt (datetime.date)
        :param theAmountDue: the total amount that is due (int/float)
        :param theTotalAmountOwed: the total outstanding balance of the debt (int/float)
        :param theInterestRate: the interest rate being charged for the debt (float)
        """

        self.myTotalAmountOwed = theTotalAmountOwed
        self.myInterestRate = theInterestRate
        Bill.__init__(self, theName, theDueDay, theNextDueDate, theAmountDue)

    def __str__(self):
        """
        :return: The String representation of a Debt
        """
        return Bill.__str__(self) + "Total Amount Still Owed: %s\nInterest Rate: %s" % (
        self.myTotalAmountOwed, self.myInterestRate)



def inputAnIncome():
    """
    Prompts user for input for creating an Income object. Was used in early testing will be replaced with GUI at some point)
    :return: a new Income object
    """
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
    while (int(i)):
        if (int(selection) == 1):
            day = input("Please enter a day of the month for pay or '0' to exit: ")
            while (int(day)):
                inputDays.append(day)
                day = input("Please enter a day of the month for pay or '0' to exit: ")
            i = 0
        elif (int(selection) == 2):
            inputDays.append(input(
                "Please enter the number of days between checks. i.e. enter 14 days if you are paid every 2 weeks: "))
            i = 0
        else:
            selection = input("Please enter '1' for fixed dates of pay or '2' for number of days between checks: ")

    return Income(inputName, inputDays, inputNetIncome, inputDateOfInitialCheck)


def saveToFile(theObjectToSave):
    """
    Allows the user to save objects, such as Income, Debt, Bill, etc...
    :param theObjectToSave:
    :return:
    """
    foldername = str(theObjectToSave.__class__)
    foldername = foldername.split(".")[-1][:-2] + "s" #grabs the last word, being the name of the class, appended by an 's'
    filename = foldername + "\\" + theObjectToSave.myName + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(theObjectToSave, f, pickle.HIGHEST_PROTOCOL)


def openFile(theFilePath):
    """
    Allows the user to load the previously saved object back into data.
    :param theFilePath: the filepath of the file you wish to open
    :return: the object that is loaded
    """
    os.makedirs(os.path.dirname(theFilePath), exist_ok=True)
    with open(theFilePath, "rb") as f:
        return pickle.load(f)


def deleteFile(theObjectToDelete):
    """
    Allows the user to delete currently saved files
    :param theObjectToDelete:
    :return:
    """
    foldername = str(theObjectToDelete.__class__)
    #Always retrieves the leaf class
    foldername = foldername.split(".")[-1][:-2]
    filename = foldername + "\\" + theObjectToDelete.name + ".txt"
    try:
        os.remove(filename)
    except:
        print("Delete failed...")


def sandbox():
    """
    where testing happens
    :return:
    """
    # testIncome = inputAnIncome()
    incomes = []

    incomes.append(Income("Metagenics", [14], 1100, datetime.date(2018, 3, 23)))
    incomes.append(Income("CleanStart", [7, 22], 1100, datetime.date(2018, 3, 22)))

    saveToFile(incomes[0])
    saveToFile(incomes[1])

    bills = []

    bills.append(Bill("Phone Bill", 9, datetime.date(2018, 4, 9), 120))
    bills.append(Debt("Student Loan", 9, datetime.date(2018, 4, 9), 300, 40000, .05))

    saveToFile(bills[0])
    saveToFile(bills[1])

    bills[0] = openFile("Debts\Student Loan.txt")
    bills[1] = openFile("Bills\Phone Bill.txt")

    print(bills[0].getDueDatesForRange(datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)))
    print(bills[0].getDueDatesForRange(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)))
    print(bills[0].getDueDatesForRange(datetime.date(2017, 1, 1), datetime.date(2017, 12, 31)))

    print(bills[1].getDueDatesForRange(datetime.date(2018, 1, 1), datetime.date(2018, 12, 31)))
    print(bills[1].getDueDatesForRange(datetime.date(2019, 1, 1), datetime.date(2019, 12, 31)))
    print(bills[1].getDueDatesForRange(datetime.date(2017, 1, 1), datetime.date(2017, 12, 31)))


sandbox()
