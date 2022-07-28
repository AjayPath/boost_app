# Created by Ajay Path
# Date July 2022

# The following python file runs the slack_demo_app for the powertrust app. The main function of this app is to provide companies to increase employee engagement by allowing
# employees to boost their collegues. This slack app also helps companies offset their scope 2 emmissions.

# The app currently runs on a virtual enviroment. For this file we pip installed the slack_bolt library.
# Needed libraries
import sqlite3
import os
import re
from dotenv import load_dotenv, find_dotenv
from tkinter.tix import Select
from unicodedata import name
from unittest import result
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Get Slack Tokens from the .env file
load_dotenv(find_dotenv())

# Initialize you app with your bot token and socket mode handler
app = App(token = os.getenv('SLACK_BOT_TOKEN'))

# Use the sqlite3 library to connect to the powertrust_demobase.db
connection = sqlite3.connect('powertrust_demobase.db', check_same_thread=False)
c = connection.cursor()


# The following section are interaction commands the users will use
# /connect -> allows user to enter themselves into the powertrust_demobase
@app.command('/connect')
def connect(ack, respond, command):
    ack()
    
    # Get the user_id from the command payload
    user_id = command['user_id']
    team_id = command['team_id']
    
    try:
        # Enter the value into the app_users table
        c.execute("INSERT INTO app_users VALUES (?, ?, 3, 0)", (user_id, team_id,))
        connection.commit()

        # Display a message when the user has successfully been added
        respond(f'Thank you for connecting to the powertrust app.')
    except Exception:
        respond(f'You are already connected!')


# /total -> displays the total amount of boost tokens the user has
@app.command('/total')
def total (ack, respond, command):
    ack()

    user_id = command['user_id']

    # Get the row where the user_id's match and respond with their total value
    c.execute("SELECT * from app_users WHERE user_id=?", (user_id,))
    total_boosts = c.fetchone()
    respond(f"You can give {total_boosts[2]} more boosts!")


# Emoji: ZAP -> Boosts the author of the comment
@app.event('reaction_added')
def boost_user(event, say, ack):
    # Get values from payload
    reaction = event['reaction']
    user = event['user']
    boosted_user = event['item_user']

    if reaction == 'zap':
        ack()
        # Names
        try:
            # Get the boost total of the user and boosted user
            c.execute("SELECT * from app_users WHERE user_id=?", (user,))
            user_data = c.fetchone()

            c.execute("SELECT * from app_users WHERE user_id=?", (boosted_user,))
            boosteds_data = c.fetchone()

            # Use an IF/ELSE to check if the booster has any boosts
            if user_data[2] > 0:
                # Update the boosts
                new_user_value = user_data[2] - 1
                new_boosted_users_value = boosteds_data[2] + 1
                users_boosts_counter = user_data[3] + 1
                c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (new_user_value, user,))
                c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (new_boosted_users_value, boosted_user,))
                c.execute("UPDATE app_users SET gifted_DRECs = ? WHERE user_id = ?", (users_boosts_counter, user,)) 
                connection.commit()

                # Let the channel know about the boost
                say(f"<@{user}> just boosted <@{boosted_user}>! ⚡💖")
            else:
                msg = f"You do not have any boost to give out."
                app.client.chat_postMessage(channel=user, text=msg)
        except Exception:
            say(f"Error, user not in database.")


# /distribute -> takes the users amount of drecs and equally distributes them to all users
# This next section may cause issues due to rounding. If a company purchased 10 boosts and has 3 employees
# They will only have 3 boosts distributed to everyone and one will be lost.
# For now the current error proof is having the remaining boosts go back to the users who issued the command

@app.command('/distribute')
def distribute_boosts(command, say, ack, body, respond):
    # Get values from payload
    user_id = command['user_id']
    team_id = command['team_id']

    ack()

    # Returns the number of rows in the table that are from the same team
    c.execute("SELECT * FROM app_users WHERE team_id = ?", (team_id,))
    num = c.fetchall()
    num = len(num)

    # Return a list of all user_ids from the same team
    c.execute("SELECT user_id FROM app_users WHERE team_id = ?", (team_id,))
    users = c.fetchall()

    # Get the value of boosts from the user and convert to an int
    c.execute("SELECT current_DRECs FROM app_users WHERE user_id = ?", (user_id,))
    distribution_value = c.fetchone()
    distribution_value = str(distribution_value)
    distribution_value = re.sub(pattern="\W", repl="", string=distribution_value)
    distribution_value = int(distribution_value)

    # Calculate the amount of boost to distribute
    dist = int(distribution_value / num)

    # Create a check to see if the user has more then boosts then users from the team
    if distribution_value >= (num + 1):
        
        # Create a for loop to inderate through all users and increase their boost total
        for index in range(0, num):
            # Choose a user from the table
            current_user = str(users[index])
            current_user = re.sub(pattern="\W", repl="", string=current_user)

            # Get the users boost total
            c.execute("SELECT current_DRECs FROM app_users WHERE user_id = ?", (current_user,))
            current_DRECs = c.fetchone()
            current_DRECs = str(current_DRECs)
            current_DRECs = re.sub(pattern="\W", repl="", string=current_DRECs)
            current_DRECs = int(current_DRECs) + dist

            # Update the users value
            c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (current_DRECs, current_user,))
            connection.commit()

        my_value = int((distribution_value - (dist * num)) + dist)
        c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (my_value, user_id,))
        connection.commit()
        say(f"You have successfully distributed your boost tokens!")
    
    else:
        respond(f"You do not have enough boost tokens to distribute")


# /redeem -> Redeems a boost token by choosing a site you would like to support
# This command requires modifications as we continue to figure out how to word this function
# For now this slash-command will show a modal to a user with their companies sites where they can choose from
@app.command("/redeem")
def redeem_token_modal(ack, body, client):
    ack()
    user_id = body['user_id']
    team_id = body['team_id']

    c.execute("SELECT site_name FROM team_sites WHERE team_id = ?", (team_id,)) 
    site_name = c.fetchall()

    option1 = str(site_name[0])
    option1 = re.sub(pattern="\W", repl="", string=option1)

    option2 = str(site_name[1])
    option2 = re.sub(pattern="\W", repl="", string=option2)

    option3 = str(site_name[2])
    option3 = re.sub(pattern="\W", repl="", string=option3)

    app.client.views_open(
        trigger_id = body['trigger_id'],

        view = {
            "type": "modal",
            "callback_id": "view_2",
            "title": {
                "type": "plain_text",
                "text": "My App",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "block_id": "section_site",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Choose a site to boost from the list below ⚡"
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": f"{option1}",
                                    "emoji": True
                                },
                                "value": f"{option1}"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": f"{option2}",
                                    "emoji": True
                                },
                                "value": f"{option2}"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": f"{option3}",
                                    "emoji": True
                                },
                                "value": f"{option3}"
                            }
                        ],
                        "action_id": "static_select-action"
                    }
                }
            ]
        }
    )

@app.view("view_2")
def redeem_submissions(ack, body, say, view, logger, client):
    ack()
    
    user_id = body['user']['id']
    team_id = body['user']['team_id']
    chosen_site = view['state']['values']['section_site']['static_select-action']['selected_option']['value']
    chosen_site = str(chosen_site)
    chosen_site = re.sub(pattern="\W", repl="", string=chosen_site)

    c.execute("SELECT current_DRECs FROM app_users WHERE user_id = ?", (user_id,))
    current_DRECs = c.fetchone()
    c.execute("SELECT remaining_DRECs FROM team_sites WHERE team_id = ? AND site_name = ?", (team_id, chosen_site,))
    remaining_DRECs = c.fetchone()
    c.execute("SELECT redeemed_DRECs FROM data_log WHERE user_id = ? AND team_id = ? AND site_name = ?", (user_id, team_id, chosen_site,))
    redeemed_DRECs = c.fetchone()

    # Values from data_log table needed for error checking
    c.execute("SELECT * FROM data_log WHERE user_id = ? AND team_id = ? AND site_name = ?", (user_id, team_id, chosen_site,))
    user_exists = c.fetchall()

    if current_DRECs[0] > 0 and remaining_DRECs[0] > 0:

        if user_exists == []:
            new_current_DRECs_0 = current_DRECs[0] - 1
            new_remaining_DRECs_0 = remaining_DRECs[0] - 1

            c.execute("INSERT INTO data_log VALUES (?, ?, ?, 1)", (user_id, team_id, chosen_site,))
            c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (new_current_DRECs_0, user_id,))
            c.execute("UPDATE team_sites SET remaining_DRECs = ? WHERE team_id = ? AND site_name = ?", (new_remaining_DRECs_0, team_id, chosen_site,))
            connection.commit()
        else:
            new_current_DRECs = current_DRECs[0] - 1
            new_remaining_DRECs = remaining_DRECs[0] - 1
            new_redeemed_DRECs = redeemed_DRECs[0] + 1

            c.execute("UPDATE app_users SET current_DRECs = ? WHERE user_id = ?", (new_current_DRECs, user_id,))
            c.execute("UPDATE team_sites SET remaining_DRECs = ? WHERE team_id = ? AND site_name = ?", (new_remaining_DRECs, team_id, chosen_site,))
            c.execute("UPDATE data_log SET redeemed_DRECs = ? WHERE user_id = ? AND team_id = ? AND site_name = ?", (new_redeemed_DRECs, user_id, team_id, chosen_site,))
            connection.commit()

        msg = f"You have successfully redeemed your boost! ⚡"
        app.client.chat_postMessage(channel=user_id, text=msg)
    elif current_DRECs[0] == 0 and remaining_DRECs[0] > 0:
        msg = f"You do not have any boosts to redeem."
        app.client.chat_postMessage(channel=user_id, text=msg)
    else:
        msg = f"The site you have chosen has no more redeemable boosts."
        app.client.chat_postMessage(channel=user_id, text=msg)


@app.command('/profile')
def total (ack, respond, command):
    ack()

    user_id = command['user_id']
    respond(f"http://127.0.0.1:8000/profile/{user_id}")


@app.action("static_select-action")
def handle_some_action(ack, body, logger):
    ack()
    app.logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()