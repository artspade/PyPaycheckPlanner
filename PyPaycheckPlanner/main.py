import datetime
import os
import pickle
import csv
import finances

def saveToFile(theObjectToSave):
    """
    Allows the user to save objects, such as Income, Debt, Bill, etc...
    :param theObjectToSave:
    :return:
    """
    foldername = str(theObjectToSave.__class__)
    foldername = foldername.split(".")[-1][:-2] + "s" #grabs the last word, being the name of the class, appended by an 's'
    filename = "Data\\" + foldername + "\\" + theObjectToSave.myName + ".txt"
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

def printReportToCSV(listToPrint):
    with open("Bill Report.csv", "w") as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerows(listToPrint)

def sandbox():
    """
    where inline testing happens
    :return:
    """
    # testIncome = inputAnIncome()

    incomes = []

    incomes.append(finances.Income("O'Blaneys", [14], 1100, datetime.date(2018, 3, 23)))
    incomes.append(finances.Income("Jackie's BBQ Pit", [7, 22], 1100, datetime.date(2018, 3, 22)))

    saveToFile(incomes[0])
    saveToFile(incomes[1])

    for income in incomes:
        saveToFile(income)


    bills = []

    bills.append(finances.Bill("Phone Bill", 9, datetime.date(2018, 5, 9), -120))
    bills.append(finances.Bill("Rent", 1, datetime.date(2018,6,1), -500))
    bills.append(finances.Bill("Avlis Student Loan", 6, datetime.date(2018,6,6), -200))
    bills.append(finances.Bill("Rohan Car Loan", 6, datetime.date(2018, 5, 6), -226))
    bills.append(finances.Bill("Upstart Loan", 18, datetime.date(2018,5,18), -700))
    bills.append(finances.Bill("Avlis Car Loan", 19, datetime.date(2018,5,19), -260))
    bills.append(finances.Bill("Rohan Student Loan", 20, datetime.date(2018,5,20), -300))

    for bill in bills:
        saveToFile(bill)


    toprint = finances.generateBalancedBillReport(datetime.date(2018, 1, 1), datetime.date(2018, 12, 31), bills, incomes)
    printReportToCSV(toprint)

def main():
    sandbox()


if __name__ == "__main__":
    main()
