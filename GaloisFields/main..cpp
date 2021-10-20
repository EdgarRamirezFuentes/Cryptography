/**
 * Main function to use the Galois fields class
 * name: main.cpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/20/2021
 */ 
#include "./classes/GaloisFields.cpp"
#include <iostream>
#include <bitset>

int main(void) {
    GaloisFields galoisfield;
    unsigned long f = 2;
    unsigned long g = 21;
    unsigned long ip = 67;
    unsigned long  grade = 6;
    unsigned long product =  galoisfield.multiplication(f, g, ip, grade);
    std::cout << std::bitset<6>(f) << " * " << std::bitset<6>(g) << " = " << std::bitset<6>(product) << std::endl; 

    f = 13;
    g = 6;
    ip = 19;
    grade = 4;
    product =  galoisfield.multiplication(f, g, ip, grade);
    std::cout << std::bitset<4>(f) << " * " << std::bitset<4>(g) << " = " << std::bitset<4>(product) << std::endl; 
    return 0;
}