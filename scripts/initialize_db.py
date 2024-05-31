#!/bin/python3

# Initialize sqlite database and tables

from utilities.orm.methods import create_new_tables, seed_database_with_canvass_results

if __name__ == "__main__":
    create_new_tables()
    seed_database_with_canvass_results()
