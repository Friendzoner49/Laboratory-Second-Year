#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <string>
#include <bits/stdc++.h>  
#include <time.h>
using namespace std;

enum Power{
    OFF,
    ON
};

bool isNum(string s){
    bool check = 0;
    for(int i = 0; i<s.length(); i++){
    if(!isdigit(s[i])) return false;
    }
    return true;
}

void print_choice(){
            cout << "1. Add tariffs\n2. Tariff table\n3. Add information about residents and services consumed" << endl;
            cout << "4. Resident information and service table\n5. Find your services consumed\n6. The cost of all services" << endl;
            cout << "7. Close program\nEnter your selection: ";
}

class Service{
    private:
        int ID_Service;
        string Service_name;
        int price;
    public:
        Service(int id, string name, int cost) : ID_Service(id), Service_name(name), price(cost) {}
        
        int getIDSer(){
            return ID_Service;
        }

        string getNameSer() {
        return Service_name;
        }
        
        int getPrice() {
        return price;
        }
};

class Resident{
    private:
        int ID_Resident;
        string last_name;
        string first_name;
        vector<Service> appointments;
    public:
        Resident(int id, string lname, string fname) : ID_Resident(id), last_name(lname), first_name(fname) {}
        
        void addAps(Service appointment){
            appointments.push_back(appointment);
        }
        
        int Sum_consumed() {
            int total = 0;
            for (auto& appointment : appointments) {
                total += appointment.getPrice();
            }
            return total;
        }

        int getIDRes(){
            return ID_Resident;
        }

        string getLName() {
        return last_name;
        }

        string getFName() {
        return first_name;
        }

        vector<Service> getAp(){
            return appointments;
        }

        ~Resident() {appointments.clear(); }
};

class Housing_and_Utilities {
    private:
        vector<Service> Services;
        vector<Resident> Residents;
        int Cost_all_services = 0;
        static Housing_and_Utilities* instancePtsr;
        Housing_and_Utilities(){}
    public:
        Housing_and_Utilities(const Housing_and_Utilities* obj) = delete;

        static Housing_and_Utilities* getInstance() {
        if (instancePtsr == nullptr) {
            instancePtsr = new Housing_and_Utilities;
            return instancePtsr;
        }
        else return instancePtsr;
        }
        
        void addService(int id, string name, int price){
            Services.push_back(Service(id, name, price));
        }

        string findfnameResex(string lname){
            Resident* Res = findlname(lname);
            int idtmp;
            string idtmps;
            string found = "";
            if (Res != nullptr) {
                for (auto& Reslist : Residents) {
                    if (Reslist.getLName() == lname) {
                        cout << "ID: " << Reslist.getIDRes() << " Name: " << Reslist.getLName() << " " << Reslist.getFName() << endl;
                    }
                }

                do{
                cout << "Select the person you want to add service to by ID number: ";
                cin >> idtmps;
                } while(!isNum(idtmps));

                idtmp = stoi(idtmps);

                for (auto& Reslist : Residents) {
                    if (Reslist.getIDRes() == idtmp) {
                    found = Reslist.getFName();  
                    }
                }
            }
            return found;
        }    

        void addSer_onRes(int idres, int idser, string lname, string fname) {
            Resident* Res = findRes(lname, fname);
            if (Res == nullptr) {
                Residents.push_back(Resident(idres, lname, fname));
                Res = &Residents.back();
            }

            Service* Ser = findSer(idser);
            if (Ser != nullptr) {
                Res->addAps(*Ser);
                Cost_all_services += Ser->getPrice();
                cout << "Add information about resident named " << fname << " and service type " << Ser->getNameSer() << " SUCCESS.\n";
                }
            else {
                cout << "Service type " << Ser->getNameSer() << " NOT FOUND.\n";
                }
        }
        
        Resident* findlname(string lname) {
            for (auto& Res : Residents) {
                if (Res.getLName() == lname) {
                    return &Res;
                }
            }
            return nullptr;
        }

        Resident* findRes(string lname, string fname) {
            for (auto& Res : Residents) {
                if (Res.getLName() == lname && Res.getFName() == fname) {
                    return &Res;
                }
            }
            return nullptr;
        }

        int TotalSers() {
            return Cost_all_services;
        }

        Service* findSer(int id) {
            for (auto& Ser : Services) {
                if (Ser.getIDSer() == id) {
                    return &Ser;
                }
            }
            return nullptr;
        }

        void printServices() {
            cout << "List of services\n";
            for (auto& ser : Services) {
                cout << "ID: " << ser.getIDSer() << endl <<"Name: " << ser.getNameSer() << endl << "Cost: " << ser.getPrice() << endl;
                }
        }

        void printRes_Ser(){
            cout << "Residents and services information\n";
            for (auto& res : Residents) {
                    Resident* resfind = findRes(res.getLName(), res.getFName());
                    if (resfind != nullptr){
                    cout << "ID: " << res.getIDRes() << endl <<"Name: " << res.getLName() << " "<< res.getFName() << endl << "Services used: "; for (auto& ser : resfind->getAp()) {
                    cout << ser.getNameSer() << " ";
                    }
                    } else {
                    cout << "There are no registered services.";
                    }
                    cout << endl;
                }
            }
        

        void InfoRestotalpay(string lname, string fname) {
            Resident* res = findRes(lname, fname);
            if (res != nullptr) {
                cout << "Resident named "<< lname << " " << res->getFName() << " has used the following services:\n";
                for (auto& ser : res->getAp()) {
                    cout << ser.getNameSer() << " Cost: " << ser.getPrice() << endl;
                }
                cout << "Total residents need to pay: " << res->Sum_consumed() << endl;
            }
            else {
                cout << "Residents with the last name "<< lname << " have NOT REGISTERED.\n";
            }
        }

        vector<Service> getSers(){
            return Services;
        } 

        vector<Resident> getRess(){
            return Residents;
        }

        ~Housing_and_Utilities(){
            Services.clear();
            Residents.clear();
        }  
};

Housing_and_Utilities* Housing_and_Utilities::instancePtsr = nullptr; 

int main()
{   
    srand(time(0));
    

    enum Power mode = ON;
    string choice;
    int choicei, idser = 0, idres = 0;
    
    while (mode)
    {   
        print_choice();
        cin >> choice;
        if(isNum(choice)){
        choicei = stoi(choice);
        } else {
            cout << "Your selection is incorrect, please restart program.";
            mode = OFF;
            continue;
        }
        
        if(choicei > 0 && choicei < 8){
            switch (choicei) {
                case 1: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                string sername, serprice;
                
                cout << "Enter service name: ";
                cin >> sername;
                do{
                cout << "Enter service price: ";
                cin >> serprice;
                } while (!isNum(serprice));
                program->addService(idser, sername, stoi(serprice));
                idser++;
                }break;
                
                case 2: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                if (program->getSers().size() == 0){
                    cout << "There are currently no services available. Please re-enter.\n";
                    continue;
                }
                program->printServices();
                }break;
                
                case 3: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                string lnameres, fnameres;
                string serchoice, bachoice;
                bool check = OFF;
                if (program->getSers().size() == 0){
                    cout << "There are currently no services available.\n";
                    continue;
                }

                do {
                    cout << "You have selected additional services for residents\n1. Add new residents\n2. Add services for existing residents\nEnter your selection: ";
                    cin >> bachoice;
                } while(!isNum(bachoice));
                if(bachoice == "1"){
                    cout << "Resident Information\nEnter resident's last name: ";
                    cin >> lnameres;
                    cout << "Enter resident's first name: ";
                    cin >> fnameres;   
                    do {
                        program->printServices();
                        do{
                        cout << "Add ID of services used by residents: ";
                        cin >> serchoice;
                        //check = ON;
                        } while (!isNum(serchoice));
                    } while (program->findSer(stoi(serchoice)) == nullptr);
                    program->addSer_onRes(idres, stoi(serchoice), lnameres, fnameres);
                    idres++;
                } else {
                    cout << "Resident Information\nEnter resident's last name: ";
                    cin >> lnameres;
                    fnameres = program->findfnameResex(lnameres);
                    do {
                        program->printServices();
                        do{
                        cout << "Add ID of services used by residents: ";
                        cin >> serchoice;
                        //check = ON;
                        } while (!isNum(serchoice));
                    } while (program->findSer(stoi(serchoice)) == nullptr);
                    program->addSer_onRes(idres, stoi(serchoice), lnameres, fnameres);
                    }
                }
                break;
                
                case 4: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                if (program->getSers().size() == 0){
                    cout << "There are currently no services available. Please re-enter.\n";
                    continue;
                }
                if (program->getRess().size() == 0){
                    cout << "No residents have been registered. Please re-enter.\n";
                    continue;
                }
                program->printRes_Ser();}
                break;
                
                case 5: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                string lnamefind, fnameend;
                cout << "Input the last name of resident to find: ";
                cin >> lnamefind;
                fnameend = program->findfnameResex(lnamefind);
                program->InfoRestotalpay(lnamefind, fnameend);}
                break;
                
                case 6: {
                Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                cout << "The cost of all services: " << program->TotalSers() << endl;}
                break;
                
                case 7:
                mode = OFF;  
                break; 
            }
        } else {
            cout << "Your selection is incorrect, please re-enter.\n" << endl;
            //mode = OFF;
        } 
    }

return 0;   
}