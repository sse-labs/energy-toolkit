
#include <cstdlib>
#include <iostream>
#include <vector>
#include <ctime>

const int LISTLENGTH = 10000;

void insertionsort(std::vector<int> v) {
    for(int i = 0; i < v.size(); i++) {
        int number = v[i];
        int j = i;

        while(j > 0 && v[j-1] > number) {
            v[j] = v[j-1];
            j = j - 1;
        }
        v[j] = number;
    }
}

int main(){
    std::vector<int> numberlist;

    for (int i = LISTLENGTH - 1; i >= 0 ; i--) {
        numberlist.push_back(i);
    }

    insertionsort(numberlist);

    // for(auto n : numberlist)
    //     std::cout << n << " " << std::endl;

    return 0;
}