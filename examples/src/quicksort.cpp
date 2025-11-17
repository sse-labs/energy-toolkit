#include <cstdlib>
#include <iostream>
#include <vector>
#include <ctime>
#include <algorithm>

const int LISTLENGTH = 10000;

int partition(std::vector<int> &vec, int low, int high) {
    int pivot = vec[high];

    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {

        if (vec[j] > pivot) {
            i++;
            std::swap(vec[i], vec[j]);
        }
    }

    std::swap(vec[i + 1], vec[high]);

    return (i + 1);
}

void quickSort(std::vector<int> &vec, int low, int high) {
    if (low < high) {
        int pi = partition(vec, low, high);

        quickSort(vec, low, pi - 1);
        quickSort(vec, pi + 1, high);
    }
}

int main(){
    std::vector<int> numberlist;

    for (int i = LISTLENGTH - 1; i >= 0 ; i--) {
        numberlist.push_back(i);
    }

    quickSort(numberlist, 0, numberlist.size() - 1);

    // for(auto n : numberlist)
    //     std::cout << n << " " << std::endl;

    return 0;
}

