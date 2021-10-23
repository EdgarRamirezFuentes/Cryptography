/**
 * Functions headers to work with Galois Fields.
 * name: app.cpp
 * Author: Edgar Alejandro Ramírez Fuentes
 * Last update: 10/23/2021
 */ 
#ifndef APP_HPP
#define APP_HPP

#include "./GaloisFields.cpp"
#include <iostream>
#include <regex>
#include <string>
#include <algorithm>

void run();
bool validate_input(const std::string&);
void multiplication();
void multiplication_table();
void addition();
void substraction();
bool menu();

#endif