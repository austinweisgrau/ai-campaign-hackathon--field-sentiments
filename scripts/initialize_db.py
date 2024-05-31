#!/bin/python3

# Initialize sqlite database and tables

from utilities.orm.methods import create_new_tables

if __name__ == "__main__":
    create_new_tables()
