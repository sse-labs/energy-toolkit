
#include <cstdlib>
#include <iostream>
#include <vector>
#include <ctime>
#include <algorithm>

const int LISTLENGTH = 10000;

int main(){
    std::vector<int> numberlist;

    for (int i = LISTLENGTH - 1; i >= 0 ; i--) {
        numberlist.push_back(i);
    }

    std::sort(numberlist.begin(), numberlist.end());

    return 0;
}