#include <cstdlib>
#include <iostream>
#include <vector>
#include <ctime>
#include <algorithm>

const int LISTLENGTH = 10000;

void bubbleSort(std::vector<int>& v) {
    int n = v.size();

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
          
            if (v[j] <= v[j + 1]){
                std::swap(v[j], v[j + 1]);
            }
        }
    }
}

int main(){
    std::vector<int> numberlist;

    for (int i = LISTLENGTH - 1; i >= 0 ; i--) {
        numberlist.push_back(i);
    }

    bubbleSort(numberlist);

    // for(auto n : numberlist)
    //     std::cout << n << " " << std::endl;

    return 0;
}