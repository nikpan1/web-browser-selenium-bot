import sys
import os
#import pytest 

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from ItemDatabase import ItemDatabase

DATABASE_DIR = "test_db.csv"

def remove_db_file(file_path):
    try:
        os.remove(file_path)
        print(f"{file_path} has been successfully removed.")
    except FileNotFoundError:
        print(f"{file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def test_empty_db():
    remove_db_file(DATABASE_DIR)
    db = ItemDatabase(file_path=DATABASE_DIR)

def test_append():
    remove_db_file(DATABASE_DIR)
    db = ItemDatabase(file_path=DATABASE_DIR)
    
    db.db_append("test_item1", 1, "loc1")
    db.db_append("test_item2", 4, "loc2")
    db.db_append("test_item3", 1, "loc3")

    print(db.database)

def test_append_same():
    remove_db_file(DATABASE_DIR)
    db = ItemDatabase(file_path=DATABASE_DIR)
    
    db.db_append("test_item1", 1, "loc1")
    db.db_append("test_item1", 3, "loc1")
    
    print(db.database)

def test_appen_new_loc():
    remove_db_file(DATABASE_DIR)
    db = ItemDatabase(file_path=DATABASE_DIR)
    
    db.db_append("test_item1", 1, "loc1")
    db.db_append("test_item1", 1, "loc2")
    
    print(db.database)




