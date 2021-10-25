/**
 * Functions to work with Galois Fields.
 * name: app.cpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/23/2021
 */ 

#include "./app.hpp"

/**
 * Start the application.
 */ 
void run() {
    bool again = false;
    do {
        std::cout << "Lab 4. Finite Fields" << std::endl;
        std::cout << "=====================" << std::endl;
        again = menu();
    } while(again);
    std::cout << "Thanks for using this program." << std::endl;
}
/**
 * Validate that the user input is a valid hexadecimal number.
 * @param input The user input.
 * @return true if the input is valid, false otherwise.
 */ 
bool validate_input(const std::string& input) {
    // It only accepts hexadecimal numbers that fit in an unsigned long int variable (4 bytes)
    return std::regex_match(input, std::regex("^[a-fA-F0-9]{1,4}"), std::regex_constants::match_not_eol);
}

/**
 * Show the menu and get the user input for the operation to perform.
 * @return true if the user wants to perform another operation, false otherwise.
 */ 
bool menu() {
    std::cout << "1. Addition" << std::endl;
    std::cout << "2. Substraction" << std::endl;
    std::cout << "3. Multiplication" << std::endl;
    std::cout << "4. Multiplication table" << std::endl;
    std::cout << "5. Exit" << std::endl;
    std::cout << "Enter your choice: ";
    std::string input;
    std::cin >> input;
    int choice;

    try {
        choice = std::stoi(input);
    } catch (std::exception& e) {
        std::cout << "Invalid input." << std::endl;
        return true;
    }

    switch(choice) {
        case 1:
            addition();
            break;
        case 2:
            substraction();
            break;
        case 3:
            multiplication();
            break;
        case 4:
            multiplication_table();
            break;
        case 5:
            return false;
        default:
            std::cout << "Invalid input." << std::endl;
            return true;
    }

    char continue_choice;
    do {
        std::cout << "Do you want to continue? (y/n): ";
        std::cin >> continue_choice;
        continue_choice = std::tolower(continue_choice);
    } while(continue_choice != 'y' && continue_choice != 'n');
    return (continue_choice == 'y');
}

/**
 * Perform multiplication operation in GF(2^n).
 */
void multiplication() {
    unsigned long f, g, grade, ip;
    std::string f_str, g_str, ip_str;
    GaloisFields gf;
    std::cout << "Multiplication" << std::endl;
    std::cout << "==============" << std::endl;
    std::cout << "Enter the polynomial f(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> f_str;
    transform(f_str.begin(), f_str.end(), f_str.begin(), ::toupper);
    std::cout << "Enter the polynomial g(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> g_str;
    transform(g_str.begin(), g_str.end(), g_str.begin(), ::toupper);
    std::cout << "Enter the grade of the field: ";
    std::cin >> grade;
    std::cout << "Enter the irreducible polynomial in its hexadecimal representation at most 4 digits: ";
    std::cin >> ip_str;
    transform(ip_str.begin(), ip_str.end(), ip_str.begin(), ::toupper);

    // Validate that the input is a valid hexadecimal number
    if(!validate_input(f_str) || !validate_input(g_str) || !validate_input(ip_str)) {
        std::cout << "Invalid input." << std::endl;
        return;
    }

    // Convert the strings to unsigned longs base 16
    try {
        f =  std::stoul(f_str, 0, 16);
        g = std::stoul(g_str, 0, 16);
        ip = std::stoul(ip_str, 0, 16);
    } catch (std::exception& e) {
        std::cout << "Invalid input." << std::endl;
        return;
    }
    std::cout << "0x" << f_str << " * " << "0x" << g_str << " = " << "0x" << std::hex << gf.multiplication(f, g, ip, grade) << std::endl;
}

/**
 * Perform addition operation in GF(2^n).
 */ 
void addition () {
    std::cout << "Addition" << std::endl;
    std::cout << "========" << std::endl;
    unsigned long f, g;
    std::string f_str, g_str;
    GaloisFields gf;
    std::cout << "Enter the polynomial f(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> f_str;
    transform(f_str.begin(), f_str.end(), f_str.begin(), ::toupper);
    std::cout << "Enter the polynomial g(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> g_str;
    transform(g_str.begin(), g_str.end(), g_str.begin(), ::toupper);

    // Validate that the input is a valid hexadecimal number
    if(!validate_input(f_str) || !validate_input(g_str)) {
        std::cout << "Invalid input." << std::endl;
        return;
    }

    // Convert the strings to unsigned longs base 16
    try {
        f =  std::stoul(f_str, 0, 16);
        g = std::stoul(g_str, 0, 16);
    } catch (std::exception& e) {
        std::cout << "Invalid input." << std::endl;
        return;
    }
    std::cout << "0x" << f_str << " + " << "0x" << g_str << " = " << "0x" << std::hex << gf.addition(f, g) << std::endl;
}

/**
 * Perform substraction operation in GF(2^n).
 */ 
void substraction () {
    std::cout << "Substraction" << std::endl;
    std::cout << "===========" << std::endl;
    unsigned long f, g;
    std::string f_str, g_str;
    GaloisFields gf;
    std::cout << "Enter the polynomial f(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> f_str;
    transform(f_str.begin(), f_str.end(), f_str.begin(), ::toupper);
    std::cout << "Enter the polynomial g(x) in its hexadecimal representation at most 4 digits: ";
    std::cin >> g_str;
    transform(g_str.begin(), g_str.end(), g_str.begin(), ::toupper);

    // Validate that the input is a valid hexadecimal number
    if(!validate_input(f_str) || !validate_input(g_str)) {
        std::cout << "Invalid input." << std::endl;
        return;
    }

    // Convert the strings to unsigned longs base 16
    try {
        f =  std::stoul(f_str, 0, 16);
        g = std::stoul(g_str, 0, 16);
    } catch (std::exception& e) {
        std::cout << "Invalid input." << std::endl;
        return;
    }
    std::cout << "0x" << f_str << " - " << "0x" << g_str << " = " << "0x" << std::hex << gf.substraction(f, g) << std::endl;
}

/**
 * Show the multiplication table of the GF(2^n).
 * The table is shown in the form of a matrix.
 */ 
void multiplication_table() {
    std::cout << "Multiplication table" << std::endl;
    std::cout << "===================" << std::endl;
    unsigned long grade;
    GaloisFields gf;
    std::cout << "Enter the grade of the field: ";
    do {
        std::cin >> grade;
        if (grade < 1) {
            std::cout << "The grade must be greater than 0." << std::endl;
        }
    } while(grade < 1);
    gf.show_multiplication_table(grade);
}
