import random
class Housing_and_Utilities:
    def __init__(self, number, name, num_residents):
        self.number = number
        self.name = name
        self.num_residents = num_residents
        self.payment = None
    def print_info(self):
        num_res = str(self.num_residents)
        num = str(self.number)
        payment = self.num_residents * 10000
        print("District name: " + self.name + "\nService price is 10000 per person\n" + "Housing and utility services office number: " + num + "\nNumber of residents: " + num_res)
        print("Monthly payment: " + str(payment))
    def getDebt(self, num_paid):
        num_notpaid = self.num_residents - num_paid
        Debt = str(num_notpaid*10000)
        print("Total Debt: " + Debt)
        
        

district_name = input("Enter the district name: ")
num = random.randint(10, 10000)
Lookup1 = Housing_and_Utilities(num, district_name, 100000)
Lookup1.print_info()
num_paid = int(input("Enter the number of people paid (less than the total number of residents): "))
Lookup1.getDebt(num_paid)

