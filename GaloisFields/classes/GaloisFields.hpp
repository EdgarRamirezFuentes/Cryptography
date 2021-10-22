/**
 * Galois fields addition, substraction, and multiplication
 * name: GaloisFields.hpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/20/2021
 */ 
#ifndef GALOISFIELDS_HPP
#define GALOISFIELDS_HPP

#include <vector>

class GaloisFields {
public:
    GaloisFields() {};
    ~GaloisFields() {};

    unsigned long addition(unsigned long, unsigned long);
    unsigned long substraction(unsigned long, unsigned long);
    unsigned long multiplication(unsigned long, unsigned long, unsigned long, unsigned long);
private:
    unsigned long XOR_operation(unsigned long f, unsigned long g);
    void get_irreducible_polynomial(unsigned long&, const unsigned long&);
    void calculate_multiplication_table (unsigned long, std::vector<std::vector<unsigned long>>&);
};

#endif