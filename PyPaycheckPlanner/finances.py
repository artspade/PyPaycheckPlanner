import datetime


class Income:
    """
    Contains data and methods needed for Incomes. Such as the name, frequency, and amount from a source.
    """
    myDays = []
    myName = None
    myAmount = None
    myDateOfFirstCheck = None

    def __init__(self, theName, theDays, theAmount, theDateOfFirstCheck):
        """
        :param theName: of the income source (str)
        :param theDays: for payment ([1],[2,3])
        :param theNetIncome: received on payday (int/float)
        :param theDateOfFirstCheck: (datetime.date)
        """
        self.myDays = theDays
        self.myName = theName
        self.myAmount = theAmount
        self.myDateOfFirstCheck = theDateOfFirstCheck

    def getDatesForRange(self, theStartDate, theEndDate):
        """
        Returns a list of all the dates for paychecks within the given date range.
        :param theStartDate:
        :param theEndDate:
        :return: a list of check dates for the given date range.
        """
        datesToReturn = []
        if (len(self.myDays) == 2):
            # Treat as fixed days in the month
            newStartDate = theStartDate if (datetime.date.today() < theStartDate) else datetime.date.today()
            endDate = theEndDate.year if (theStartDate.year != theEndDate.year) else theEndDate.year + 1
            for x in range(newStartDate.year, endDate):  # year


                for y in range(newStartDate.month, 13):  # month


                    for z in self.myDays:  # day

                        date = datetime.date(int(x), int(y), int(z))
                        if (date < datetime.date.today()):
                            break
                        datesToReturn.append(datetime.date(int(x), int(y), int(z)))

        else:

            # Treat as number of days between checks
            dateToAdd = self.myDateOfFirstCheck
            newStartDate = theStartDate if (datetime.date.today() < theStartDate) else datetime.date.today()
            # if dateToAdd == theStartDate... Perfect!
            while (
                        dateToAdd > newStartDate):  # brings dateToAdd to one check before theStartDate if dateToAdd is greater
                dateToAdd = dateToAdd - datetime.timedelta(days=int(self.myDays[0]))

            while (dateToAdd < newStartDate):  # brings dateToAdd to the first check after theStartDate
                dateToAdd = dateToAdd + datetime.timedelta(days=int(self.myDays[0]))

            while (dateToAdd <= theEndDate):  # add all paycheck dates for the range

                datesToReturn.append(dateToAdd)
                dateToAdd = dateToAdd + datetime.timedelta(days=int(self.myDays[0]))

        return datesToReturn

    def __str__(self):
        """
        :return: the string representation for the current class.
        """
        return "Name: %s\nNet Income: %s\nDate of first check: %s\nPaycheck Frequency: %s\n" % (
            self.myName, self.myAmount, self.myDateOfFirstCheck, self.myDays)


class Bill:
    """
    Contains data and methods needed to handle Bills. Such as the name, frequency, and cost.
    """

    myName = None
    myDueDay = None
    myNextDueDate = None
    myAmount = None

    def __init__(self, theName, theDueDay, theNextDueDate, theAmountDue):
        """
        :param theName: for the bill (str)
        :param theDueDay: the integer value for the day in the month of which the bill is due (int)
        :param theNextDueDate: the date that the bill is next due (datetime.date)
        :param theAmountDue: the cost of the bill (int/float)
        """
        self.myName = theName
        self.myAmount = theAmountDue
        self.myDueDay = theDueDay
        self.myNextDueDate = theNextDueDate

    def __str__(self):
        """
        :return: The string representation of a Bill
        """
        return "Name: %s\nDue Day: %s\nNext Due Date: %s\nAmount Due: %s\n" % (
            self.myName, self.myDueDay, self.myNextDueDate, self.myAmount)

    def getDatesForRange(self, theStartDate, theEndDate):
        """
        Returns a list of all the dates the bill is due given a date range
        :param theStartDate: the starting date range
        :param theEndDate: the ending date range
        :return: a list of datetime.date for all the bills' due dates on the given date range
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


def createIncomeAndBillListsSortedByDate(theBillList, theEndDate, theIncomeList, theStartDate):
    """
    Creates an in-order list of all Incomes and Bills sorted by date
    :param theBillList: list of all bills
    :param theEndDate: the ending date for our range
    :param theIncomeList: list of all incomes
    :param theStartDate: the starting date for our range
    :return an in-order list of all Incomes and Bills sorted by date
    """

    listToReturn = []
    for bill in theBillList:  # add all bills with dates as tuple (bill,date)
        dates = bill.getDatesForRange(theStartDate, theEndDate)

        for date in dates:
            tup = (bill, date)
            listToReturn.append(tup)

    for income in theIncomeList:  # add all incomes with dates as (bill,date)

        dates = income.getDatesForRange(theStartDate, theEndDate)
        for date in dates:
            tup = (income, date)
            listToReturn.append(tup)
    listToReturn.sort(key=lambda tup: tup[1])  # sort list by dates
    return listToReturn


def generateBalancedBillReport(theStartDate, theEndDate, theBillList, theIncomeList):
    """
    Generates a list of tuples representing incomes and bills to pay. This report attempts to balance the weight of burden
    from week to week.
    :param theStartDate: the starting date for our range
    :param theEndDate:  the ending date for our range
    :param theBillList: the list of bills we are using
    :param theIncomeList: the list of incomes we are using
    :return: a bill schedule that is balanced
    """
    incomeAndBillList = createIncomeAndBillListsSortedByDate(theBillList, theEndDate, theIncomeList, theStartDate)

    toReturn = []
    list = []
    listCeption = []

    storage = []

    for element in incomeAndBillList:  # place values into buckets.

        if element[0].__class__ is Income:  # signals the start of a new bucket.
            balance = 0
            for item in list:
                balance += item[0].myAmount
            list.insert(0, balance)
            listCeption.append(list)
            list = []

        list.append(element)

    if (listCeption[0] != int(0) or listCeption[
        0] is None):  # removes some output, varies depending on input.
        listCeption.pop(0)


    timetorun = 10
    excessMonthlyIncome = (
                              4400 - 2581.59) / 4  # !!!! replace amounts with amounts generated by values in the given lists

    for y in range(1, timetorun):
        for x in reversed(range(0, len(listCeption))):
            while listCeption[x][0] < excessMonthlyIncome:  # amount of money for "wiggle" room
                toInsert = listCeption[x].pop(-1)
                balanceHelper(listCeption[x])
                listNextIncomeDate = listCeption[x + 1][1][1]
                listNextBalance = listCeption[x + 1][0]
                if listNextIncomeDate < toInsert[1]:
                    listCeption[x + 1].append(toInsert)
                    balanceHelper(listCeption[x + 1])
                    x += 1

                else:
                    listCeption[x - 1].append(toInsert)
                    balanceHelper(listCeption[x - 1])


    for list in listCeption:

        for x in range(1, len(list)):
            tup = (list[x][0].myName, list[x][0].myAmount, list[x][1])
            toReturn.append(tup)
        tup = ("Balance: ", list[0])
        toReturn.append(tup)

    return toReturn


def balanceHelper(theList):
    balance = 0
    for item in theList[1:]:
        balance += item[0].myAmount

    theList.pop(0)
    theList.insert(0, balance)


def generateInlineBillPayReport(theStartDate, theEndDate, theBillList, theIncomeList):
    """    Creates the list of all bills due and when incomes are received
    :param theStartDate: starting date range we want to plan for
    :param theEndDate: ending date range we want to plan for
    :param theBillList: a list of bill objects
    :param theIncomeList: a list of income objects
    :return:
    """
    incomeAndBillList = createIncomeAndBillListsSortedByDate(theBillList, theEndDate, theIncomeList, theStartDate)
    formatedList = []
    purse = 0

    for element in incomeAndBillList:

        date = element[1]
        if element[0].__class__ is Income:
            tup = ("Balance: ", purse)
            formatedList.append(tup)
            purse = element[0].myAmount
        else:
            purse -= element[0].myAmount

        tup = (element[0].myName, element[0].myAmount, date)
        formatedList.append(tup)

    return formatedList
