# Created by Ajay Path
# Date July 2022

from flask import Blueprint, request, render_template
import sqlite3
import os
import re

pages = Blueprint(__name__, "pages")

@pages.route("/map")
def map():
    return render_template('map.html')

@pages.route("/profile/<username>")
def profile(username):

    if request.method == 'GET':
        connection = sqlite3.connect('powertrust_demobase.db')
        c = connection.cursor()
        
        c.execute("SELECT * FROM app_users WHERE user_id = ?", (username,)) 
        x = c.fetchall()
        boosts = x[0][3]

        if boosts == 'None':
            boosts = 0

        # SITE_A
        c.execute("SELECT redeemed_DRECs FROM data_log WHERE user_id = ? AND site_name = 'Wenchi'", (username,))
        site_a = c.fetchone()
        site_a = str(site_a)
        site_a = re.sub(pattern="\W", repl="", string=site_a)

        if site_a == 'None':
            site_a = 0

        # SITE_B
        c.execute("SELECT redeemed_DRECs FROM data_log WHERE user_id = ? AND site_name = 'Steung_Chrov'", (username,))
        site_b = c.fetchone()
        site_b = str(site_b)
        site_b = re.sub(pattern="\W", repl="", string=site_b)

        if site_b == 'None':
            site_b = 0

        # SITE_C
        c.execute("SELECT redeemed_DRECs FROM data_log WHERE user_id = ? AND site_name = 'Lingshed_Monastary'", (username,))
        site_c = c.fetchone()
        site_c = str(site_c)
        site_c = re.sub(pattern="\W", repl="", string=site_c)

        if site_c == 'None':
            site_c = 0


    return render_template("base.html", site_a=site_a, site_b=site_b , site_c=site_c, boost_token=boosts)
    # c_DRECs=current_DRECs, 