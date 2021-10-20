/**
 * Galois fields addition, substraction, and multiplication
 * name: GaloisFields.cpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/20/2021
 */ 
#include "./GaloisFields.hpp"

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
 *  
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