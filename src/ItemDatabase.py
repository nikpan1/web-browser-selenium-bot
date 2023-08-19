import pandas as pd
from CoreSettings import *
import os

def create_empty_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass  # This creates an empty file


class ItemDatabase:
    def __init__(self, file_path=DATABASE_DIR):
        self.file_path = file_path
      # create_empty_file(file_path)
        self.load_database()

    def load_database(self):
        try:
            self.database = pd.read_csv(self.file_path)
        except:
            # If the file does not exist, create an empty database
            data = {'item_name': ["test_name"], 'item_count': [1], 'item_locs': [["loc1", "loc2"]]}
            self.database = pd.DataFrame(data)
            create_empty_file(self.file_path)

    def save_database(self):
        self.database.to_csv(self.file_path, index=False)

    def db_append(self, item, amount, loc):
         # Check if the item already exists in the database
        if item in self.database['item_name'].values:
            item_index = self.database.index[self.database['item_name'] == item][0]
            item_locs = eval(self.database.loc[item_index, 'item_locs'])

            # Check if loc is not already in item_locs, then append it
            if loc not in item_locs:
                item_locs.append(loc)
                self.database.at[item_index, 'item_locs'] = str(item_locs)
        else:
            # If the item doesn't exist, create a new row in the database
            new_row = {'item_name': item, 'item_count': int(amount), 'item_locs': [loc]}
            self.database = self.database.append(new_row, ignore_index=True)
               
        self.save_database()

if __name__ == "__main__":
    db = ItemDatabase("data/database/item_database.csv")
    db.db_append("test2_item", 9, "test_loc")

