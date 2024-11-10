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
    for(int i = 0; i<s.length(); i++){
    if(!isdigit(s[i])) return false;
    }
    return true;
}

void print_choice(){
            cout << "1. Tariff table\n2. Add resident information\n3. Show residents with benefits" << endl;
            cout << "4. Show residents without benefits\n5. The cost of all services\n6. Show all residents" << endl;
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

class Person{
    private:
        string last_name;
        string first_name;
        int ID_Resident;

    public:
        Person(int ID_Resident, string last_name, string first_name){
            this->first_name = first_name;
            this->last_name = last_name;
            this->ID_Resident = ID_Resident;
        }

        int getIDRes() {
            return this->ID_Resident;
        }
        void setIDRes(int ID_Resident) {
            this->ID_Resident = ID_Resident;
        }

        string getLName() {
            return this->last_name;
        }
        void setLast_name(string last_name) {
            this->last_name = last_name;
        }

        string getFName() {
            return this->first_name;
        }
        void setFirst_name(string first_name) {
            this->first_name = first_name;
        }

};

class Residentwb : public Person {
    private:
        vector<Service> appointments;

    public:
        Residentwb(int ID_Resident, string last_name, string first_name) : Person(ID_Resident, last_name, first_name) {}
        
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

        vector<Service> getAp(){
            return appointments;
        }

        ~Residentwb() {appointments.clear(); }
};

class Residentnb : public Person {
    public:
        Residentnb(int ID_Resident, string last_name, string first_name) : Person(ID_Resident, last_name, first_name) {}
        
        int Sum_consumed() {
            int total = 0;
            for (auto& appointment : appointments) {
                total += appointment.getPrice();
            }
            return total;
        }
};

class Housing_and_Utilities {
    private:
        vector<Service> Services;
        vector<Residentwb> Residentswb;
        vector<Residentnb> Residentsnb;
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
        
        void addRes(bool type, int id, string lname, string fname){
            if(type == 1){
                Residentswb.push_back(Residentwb(id, lname, fname));
            } else {
                Residentsnb.push_back(Residentnb(id, lname, fname));
            }
        }

        void addService(int id, string name, int price){
            Services.push_back(Service(id, name, price));
        }   

        int TotalSers() {
            return Cost_all_services;
        }

        void printServices() {
            cout << "List of services\n";
            for (auto& ser : Services) {
                cout << "ID: " << ser.getIDSer() << endl <<"Name: " << ser.getNameSer() << endl << "Cost: " << ser.getPrice() << endl;
                }
        }

        string findfnameResex(string lname){
            Residentwb* Res = findlname(lname);
            int idtmp;
            string idtmps;
            string found = "";
            if (Res != nullptr) {
                for (auto& Reslist : Residentswb) {
                    if (Reslist.getLName() == lname) {
                        cout << "ID: " << Reslist.getIDRes() << " Name: " << Reslist.getLName() << " " << Reslist.getFName() << endl;
                    }
                }


                do{
                cout << "Select the person you want to add service to by ID number: ";
                cin >> idtmps;
                } while(!isNum(idtmps));


                idtmp = stoi(idtmps);


                for (auto& Reslist : Residentswb) {
                    if (Reslist.getIDRes() == idtmp) {
                    found = Reslist.getFName();  
                    }
                }
            }
            return found;
        } 

        Residentwb* findlname(string lname) {
            for (auto& Res : Residentswb) {
                if (Res.getLName() == lname) {
                    return &Res;
                }
            }
            return nullptr;
        }

        void addSer_onRes(int idres, int idser, string lname, string fname) {
            Residentwb* Res = findReswb(lname, fname);

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

        Residentwb* findReswb(string lname, string fname) {
            for (auto& Res : Residentswb) {
                if (Res.getLName() == lname && Res.getFName() == fname) {
                    return &Res;
                }
            }
            return nullptr;
        }

        Residentnb* findResnb(string lname, string fname) {
            for (auto& Res : Residentsnb) {
                if (Res.getLName() == lname && Res.getFName() == fname) {
                    return &Res;
                }
            }
            return nullptr;
        }

        Service* findSer(int id) {
            for (auto& Ser : Services) {
                if (Ser.getIDSer() == id) {
                    return &Ser;
                }
            }
            return nullptr;
        }

        void printRes_Ser(){
            cout << "Residents and services information\n";
            for (auto& res : Residentswb) {
                Residentwb* resfind = findReswb(res.getLName(), res.getFName());
                if (resfind != nullptr){
                cout << "ID: " << res.getIDRes() << endl <<"Name: " << res.getLName() << " "<< res.getFName() << endl << "Services used: "; 
                for (auto& ser : resfind->getAp()) {
                cout << ser.getNameSer() << " ";
                }
                } else {
                cout << "No residents have benefited yet.";
                }
                cout << endl;
            }
        }

        void printRes_0Ser(){
            cout << "Residents and services information\n";
            for (auto& res : Residentsnb) {
                Residentnb* resfind = findResnb(res.getLName(), res.getFName());
                if (resfind != nullptr){
                cout << "ID: " << res.getIDRes() << endl <<"Name: " << res.getLName() << " "<< res.getFName() << endl; 
                } else {
                cout << "There are no residents yet without any benefits.";
                }
                cout << endl;
            }
        }

        void printAllRes(){
            cout << "The residents have benefits" << endl;
            printRes_Ser();
            cout << "The residents have no benefits" << endl;
            printRes_0Ser();
        }

        vector<Service> getSers(){
            return Services;
        } 

        vector<Residentwb> getResswb(){
            return Residentswb;
        }

        vector<Residentnb> getRessnb(){
            return Residentsnb;
        }

        ~Housing_and_Utilities(){
            Services.clear();
            Residentswb.clear();
            Residentsnb.clear();
        }  
};

Housing_and_Utilities* Housing_and_Utilities::instancePtsr = nullptr; 

int main()
{   

    string ser_repairfu = "Furniture repair", ser_painthouse = "House painting", ser_lightchange = "Replace the light bulb";
    string ser_clean = "Clean up", ser_mail = "Mailbox";
    enum Power mode = ON;
    string choice;
    int choicei, idres = 0;
    
    Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
        program->addService(0, ser_mail, 500);
        program->addService(1, ser_lightchange, 200);
        program->addService(2, ser_repairfu, 3500);
        program->addService(3, ser_clean, 2000);
        program->addService(4, ser_painthouse, 4000);
    
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
                //Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                program->printServices();
                }break;
                
                case 2: {
                    Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                    string lnameres, fnameres;
                    string serchoice, bachoice;
                    bool typeres;
                    int reschoice;
                    if (program->getSers().size() == 0){
                        cout << "There are currently no services available.\n";
                        continue;
                    }
                    cout << "You have selected additional services for residents\n1. Add new residents\n2. Add services for existing residents with benefits\nEnter your selection: ";
                    cin >> reschoice;
                    if(reschoice == 1){
                    cout << "Resident Information\nEnter resident's last name: ";
                    cin >> lnameres;
                    cout << "Enter resident's first name: ";
                    cin >> fnameres; 

                    do {
                        cout << "You have just entered resident information, please select resident type:\n1. Add new residents with benefits\n2. Add new residents without benefits\nEnter your selection: ";
                        cin >> bachoice;
                    } while(!isNum(bachoice));

                    if(bachoice == "1"){
                        typeres = 1; 
                        program->addRes(typeres, idres, lnameres, fnameres);
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
                    } else if(bachoice == "2"){
                        typeres = 0;
                        program->addRes(typeres, idres, lnameres, fnameres);
                        idres++;
                    }
                } else if(reschoice == 2){
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

                }break;
                
                case 3: {
                    Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                    program->printRes_Ser();}
                    break;
                
                case 4: {
                    Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                    program->printRes_0Ser();}
                    break;
                
                case 5: {
                    Housing_and_Utilities* program = Housing_and_Utilities::getInstance();
                    program->printAllRes();}
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