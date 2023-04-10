// team42: $1$4fTgjp6q$XJ4b7w1UQni3YpIwY2/99/:16653:0:99999:7:::
// md5 indicator: $1$ => 1
// Salt: $4fTgjp6q$ => 4fTgjp6q
// Password Hash: $XJ4b7w1UQni3YpIwY2/99/: => XJ4b7w1UQni3YpIwY2/99/
#include <iostream>
#include <string.h>
#include "hashlib2plus/trunk/src/hashlibpp.h"

using namespace std;

void Split(string, int&, string&, string& );

int main() {
    string totalHash = "$1$4fTgjp6q$XJ4b7w1UQni3YpIwY2/99/:16653:0:99999:7:::";

    // Hash Algorithm Indicator 
    int HAI = 0;

    string salt = "";
    string passwordHash = "";
    string password = "";

    // Splits the string
    Split(totalHash, HAI, salt, passwordHash);

    cout << "HAI: " << HAI << endl;
    cout << "Salt: " << salt << endl;
    cout << "Hash: " << passwordHash << endl;

    // do all the stuff to find it
    // md5()


    // prints the found password
    // cout << "password: " << password << endl;

    return 0;
}

void Split(string totalHash, int& HAI, string& salt, string& passwordHash) {
    int sepCnt = 0; 

    for (int i = 0; i < totalHash.length(); i++) {
        if(totalHash[i] == '$') 
            sepCnt++;
        else if (sepCnt == 1 && totalHash[i] != '$')
            HAI = totalHash[i] - 48;
        else if (sepCnt == 2 && totalHash[i] != '$')
            salt.push_back(totalHash[i]);
        else if (sepCnt == 3 && totalHash[i] != ':')
            passwordHash.push_back(totalHash[i]);
        else if (totalHash[i] == ':')
            return;
    }
}