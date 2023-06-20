#!/usr/bin/python3
"""State Test Model"""
import unittest

import MySQLdb

from models.state import State
from tests.test_models.test_base_model import test_basemodel


class test_state(test_basemodel):
    """init"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

    def test_create_state(self):
        # Step 1: Get the initial count of records in the table
        initial_count = self.get_record_count()

        # Step 2: Execute the console command (create State name="California")
        # Perform the action to create the state using your code or console...
        # interface

        # Step 3: Get the count of records after the command execution
        final_count = self.get_record_count()

        # Step 4: Validate the difference in counts
        difference = final_count - initial_count
        self.assertEqual(difference, 1, "New record not added")

    def get_record_count(self):
        # Connect to the database
        db = MySQLdb.connect(
            host="localhost",
            user="hbnb_test",
            passwd="hbnb_test_pwd",
            db="hbnb_test_db",
        )

        # Create a cursor
        cursor = db.cursor()

        # Execute the query to get the count of records in the states table
        cursor.execute("SELECT COUNT(*) FROM states")

        # Fetch the count value
        count = cursor.fetchone()[0]

        # Close the cursor and database connection
        cursor.close()
        db.close()

        return count


if __name__ == "__main__":
    unittest.main()
