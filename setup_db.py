# Created by Ajay Path
# Date July 2022

# This script is used to setup the initial demo database for the slack app. Utilizing the Sqlite3 library, we created three tables to store the nessecary user information for the app.
# The first table is for users and stores their user_id, team_id, and other information about their drecs. The second table stores site location information depending on the team.
# The third table will be used to store the redeemed data of the users which will be import for users to track their impact.

# Import the needed libraries to create the database.
import site
import sqlite3
import re

# Create a connection to the database in order to access and edit it. This command will also create a new database if it cannot find it already.
connection = sqlite3.connect('powertrust_demobase.db')

# Create a cursor object in order to interact with the database.
c = connection.cursor()

# Use the execute command in order to create a new table within the powertrust_demobase.db.


# Table 1 - app_users table
c.execute('''CREATE TABLE IF NOT EXISTS app_users
               (user_id TEXT PRIMARY KEY,
                team_id TEXT,
                current_DRECs INTEGER,
                gifted_DRECs INTEGER)''')

# Table 2 - team_sites table
c.execute('''CREATE TABLE IF NOT EXISTS team_sites
               (team_id TEXT,
                site_name TEXT,
                remaining_DRECs INTEGER)''')

# Table 3 - data_log table
c.execute('''CREATE TABLE IF NOT EXISTS data_log
               (user_id TEXT,
                team_id TEXT,
                site_name TEXT,
                redeemed_DRECs INTEGER)''')


# Insert rows of data into each of the table in order to test from.

# Insert users into the database by typing your user_id into the first '' in the brackets. Then enter your team_id into the second ''.
# c.execute("INSERT INTO app_users VALUES ('U03L471LSD6', 'T03KT43EB9P', 10, 7)")

# # Next we will populate the team_sites table using example information for the sake of the demo. When using the real powertrust database, this information will be pulled from there.
c.execute("INSERT INTO team_sites VALUES ('TQX94CDQT', 'Wenchi', 50)")
c.execute("INSERT INTO team_sites VALUES ('TQX94CDQT', 'Steung_Chrov', 50)")
c.execute("INSERT INTO team_sites VALUES ('TQX94CDQT', 'Lingshed_Monastary', 50)")

# The information for the data_log table should be a combination of information pulled from the powertrust database as well as information recorded overtime.
# This is the main information that will be shown on each user profile. For the demo we have entered in some dummy data for my slack account.
# c.execute("INSERT INTO data_log VALUES ('U03L471LSD6', 'T03KT43EB9P', 'SITE_A', 2)")

# To save these changes use the commit command
connection.commit()

# The following block of code will display all the information for all the tables within the database
c.execute("SELECT * FROM app_users") 
x = c.fetchall()
print(x)

c.execute("SELECT * FROM team_sites") 
y = c.fetchall()
print(y)

c.execute("SELECT * FROM data_log") 
z = c.fetchall()
print(z)
