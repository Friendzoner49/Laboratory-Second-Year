#include <iostream>
#include <math.h> 
#include <iomanip>  
#include <time.h>
using namespace std;

class Housing_and_Utilities {
    private:
        int num_paid;
    public:
        string district;
        int number, num_residents;
        int num_not_paid;
        
        void setPaid(int a){
            num_paid = a;
            num_not_paid = num_residents - a;
        }

        int payment(int a){
            return a*10000;
        }
        int getnumPaid(){
            return num_paid;
        }
        int getDebt(){
            return num_not_paid * 10000;
        }
        Housing_and_Utilities(string s, int a, int b){
            district = s;
            number = a;
            num_residents = b;
        }
};

int main()
{   
    srand(time(0));
    int a = rand()%10000;
    int peo_paid;
    string dis_name;
    cout << "Enter the district name: ";
    cin >> dis_name;
    Housing_and_Utilities Lookup1(dis_name, a, 100000);
    cout << "District name: " << Lookup1.district << endl;
    cout << "Service price is 10000 per person" << endl;
    cout << "Housing and utility services office number: " << Lookup1.number << endl;
    cout << "Number of residents: " << Lookup1.num_residents << endl;
    cout << "Monthly payment: " << Lookup1.payment(Lookup1.num_residents) << endl;
    cout << "Enter the number of people paid (less than the total number of residents): ";
    cin >> peo_paid;
    Lookup1.setPaid(peo_paid);
    cout << "Total Debt: " << Lookup1.getDebt();
    
return 0;   
}
