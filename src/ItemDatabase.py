import pandas as pd
from CoreSettings import *

class ItemDatabase:
    def __init__(self, file_path=DATABASE_DIR):
        self.file_path = file_path
        self.load_database()

    def __del__(self):
        self.save_database()

    def load_database(self):
        try:
            self.database = pd.read_csv(self.file_path)
        except FileNotFoundError:
            # If the file does not exist, create an empty database
            data = {'item_name': [], 'item_count': [], 'item_locs': []}
            self.database = pd.DataFrame(data)

    def save_database(self):
        self.database.to_csv(self.file_path, index=False)

    def db_append(self, item, amount, loc):
        return 
        # Check if the item already exists in the database
        if item in self.database['item_name'].values:
        # Increment the item_count by 1
            self.database.loc[self.database['item_name'] == item, 'item_count'] += int(amount)

            # Check if loc is not already in item_locs, then append it
            if loc not in self.database.loc[self.database['item_name'] == item, 'item_locs'].values[0]:
                self.database.loc[self.database['item_name'] == item, 'item_locs'] += [loc]
        else:
        # If the item doesn't exist, create a new row in the database
            new_row = {'item_name': item, 'item_count': int(amount), 'item_locs': [loc]}
            self.database = pd.concat([self.database, pd.DataFrame([new_row])], ignore_index=True)


