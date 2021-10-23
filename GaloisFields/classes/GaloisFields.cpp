/**
 * Galois fields addition, substraction, and multiplication
 * name: GaloisFields.cpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/20/2021
 */ 
#include "./GaloisFields.hpp"
#include <cmath>
#include <iostream>

/**
 * Get the result of f(x) XOR g(x)
 * @param f is the first polynomial that belongs to the Galois field
 * @param g is the second polynomial that belongs to the Galois field
 * @return the result of f(x) XOR g(x)
 */ 
unsigned long GaloisFields::XOR_operation(unsigned long f, unsigned long g) {
    return f ^ g;
}

/**
 * Gets the result of f(x) + g(x) in the Galois field
 * @param f is the first polynomial that belongs to the Galois field
 * @param g is the second polynomial that belongs to the Galois field
 * @return the result of f(x) + g(x)
 */ 
unsigned long GaloisFields::addition(unsigned long f, unsigned long g) {
    return GaloisFields::XOR_operation(f, g);
}

/**
 * Gets the result of f(x) - g(x) in the Galois field
 * @param f is the first polynomial (bits representation) that belongs to the Galois field
 * @param g is the second polynomial (bits representation) that belongs to the Galois field
 * @return the result of f(x) - g(x)
 */ 
unsigned long GaloisFields::substraction(unsigned long f, unsigned long g) {
    return GaloisFields::XOR_operation(f, g);
}

/**
 * Gets the result of f(x) . g(x) in the Galois field
 * @param f is the first polynomial that belongs to the galois field
 * @param g is the second polynomial that belongs to the galois field
 * @param ip is the irreducible polynomial (bits representation)
 * @param grade is the grade of GF(2^n)
 * @return the product of f(x) . g(x)
 */ 
unsigned long GaloisFields::multiplication(unsigned long f,unsigned long g, unsigned long ip, unsigned long grade) {
    unsigned long product = 0;
    unsigned long most_sig_bit = 0;
    for (int i = 0; i < grade; i++) {
        // The least significant if g is set
        if (g & 1) {
            // XOR the current value of f with the product to delete the bits that are repeated
            product ^= f;
        }
        // Check if the most significant bit of f is set
        most_sig_bit = f & (1 << (grade - 1));
        // Applies left shift
        f <<= 1;
        // Turn off the bit next to the most significant bit to avoid carrying undesired bits when the left shift happens
        f &= ~(1 << (grade + 1));
        // Only will apply f XOR ip when the most significant bit is one
        if (most_sig_bit) {
            // This operation brings the product of bi+1 and prepare it to XOR it with the final product if the next bit is set
            f  ^= ip;
        }
        // Right shift to value the next bit of g to evaluate the next bit
        g >>= 1;
    }
    return product;
}

/**
 * Calculate the multiplication table of GF(2^n)
 * @param grade is the grade of GF(2^n)
 * @param multiplication_table is the table that will store the values of the multiplication table that belongs to GF(2^n)
 */ 
void GaloisFields::calculate_multiplication_table (unsigned long grade, std::vector<std::vector<unsigned long>>& multiplication_table) {
    // Irreducible polynomial used to calculate the multiplication table
    unsigned long ip = 0;
    // It is decremented by one because the matrix goes from 0 up to (2^n - 1)
    unsigned long table_size = (unsigned long) (pow((unsigned long) 2, grade) - 1);
    GaloisFields::get_irreducible_polynomial(ip, grade);
    for (unsigned long row = 0; row <= table_size; row++) {
        for (unsigned long col = 0; col <= table_size; col++) { 
            multiplication_table[row][col] = GaloisFields::multiplication(row, col, ip, grade);
        }
    }
}

/**
 * Show the multiplication table of GF(2^n) in its hexadecimal representation
 * @param grade is the grade of GF(2^n) and this must be greater or equal to 1.
 */ 
void GaloisFields::show_multiplication_table(unsigned long grade) {
    unsigned long table_size = (unsigned long) pow((unsigned long) 2, grade);
    std::vector<std::vector<unsigned long>> multiplication_table(table_size, std::vector<unsigned long>(table_size, 0));
    GaloisFields::calculate_multiplication_table(grade, multiplication_table);
    std::cout << "Multiplication table of GF(2^" << grade << "):\n";
    GaloisFields::print_multiplication_table(multiplication_table);
}

/**
 * Print the multiplication table of GF(2^n) in its hexadecimal representation
 * @param multiplication_table is a matrix that contains the values of the multiplication table of GF(2^n)
 */ 
void GaloisFields::print_multiplication_table(const std::vector<std::vector<unsigned long>>& multiplication_table) {
    for (auto row : multiplication_table) {
        for (auto col : row) {
            std::cout << " | " << "0x" << std::hex << col;
        }
        std::cout << " |\n";
    }
}

/**
 * Get an possible irreducible polynomial of GF(2^n)
 * @param ip is the variable that will store the irreducible polynomial
 * @param grade is the grade of GF(2^n)
 */ 
void GaloisFields::get_irreducible_polynomial(unsigned long& ip, const unsigned long& grade) {
    // Binary representation of the x + 1 polynomial
    ip = 3;

    // One of the irreducible polynomials of 2^1 is x + 1
    if (grade == 1) {return;}

    /*
        Set the bit that belongs to the grade
        i.e.
        ip = 3 = 11 (bynary) = x + 1 
        if the grade is n, a possible irreducible polynomial could be x^n + x + 1
        So, in order to get the desired irreducible polynomial it is needed to set the nth bit in ip
        i.e. grade = 5
        ip = 11 (binary value)
        ip or 1 << n will get the desired irreducible polynomial
        100000
        000011
        -------
        100011 = x^5 + x + 1 -> Possible irreducible polynomial
    */ 
    ip |= 1 << grade;
}