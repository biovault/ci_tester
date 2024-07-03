#include <omp.h>
#include <iostream>


int main() {

#ifdef __x86_64__
    std::cout << " Compiled under x86_64\n";
#endif

#ifdef __arm64__
    std::cout << " Compiled under arm64\n";
#endif

    #pragma omp parallel for
    for(auto i=0; i<10; ++i) {
        #pragma omp critical
        std::cout << " Hello from thread: " << omp_get_thread_num() << "\n";
    }
}