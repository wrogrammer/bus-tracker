#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
import requests
import urllib3
from requests.auth import HTTPDigestAuth
import pandas as pd
from time import strftime
import datetime as dt

app = Flask(__name__)


# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
# Disable SSL Warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = ''
USERNAME = ''
PASSWORD = ''


# It's a start page. Waiting for user input, so I'm creating empty dataframe.
@app.route("/", methods=['GET'])
def show_table():
    search = request.form.get('search')
    if search is None:
        df = pd.DataFrame()
        return render_template('view.html', empty=[pd.DataFrame.to_html(df)])


# Endpoint for POST method.
@app.route("/stop", methods=['POST'])
def table():
    search = request.form.get('search')
    # If typed value is empty response message.
    if search == '':
        flash('Nieprawidłowe dane!')
        return render_template('view.html')
    else:
        stops = pd.read_csv('out.csv', header=None, usecols=[0, 1])
        chosen_stop = stops[1] == str(search)
        # If typed stop name non exists response message.
        stoper = stops[chosen_stop].values.tolist()
        if not stoper:
            flash('Przystanek nie istnieje!')
            return render_template('view.html')
        else:
            # [0][0] --> stop code of specific stop name.
            # [0][1] --> stop name
            specific_url = URL + str(stoper[0][0])
            response_mpk = requests.get(specific_url, auth=HTTPDigestAuth(USERNAME, PASSWORD), verify=False)
            if len(response_mpk.content) > 0:
                data = response_mpk.json()
                df = pd.DataFrame.from_dict(data, orient='columns').rename(columns={'c': 'Kod:', 'd': 'Kierunek:',
                                                                                    'l': 'Linia:', 's': 'Symbol:'})
                # Remove column with date and time, separate time.
                df = df.join(df['t'].str.split(' ', expand=True).rename(
                    columns={0: 'Data', 1: 'Czas do odjazdu:'})).drop(['t', 'Data'], 1)

            start = str(strftime("%H:%M:%S"))

            # In time column change hours to current time.
            for (idx, row) in df.iterrows():
                end = row.loc['Czas do odjazdu:']
                start_dt = dt.datetime.strptime(start, '%H:%M:%S')
                end_dt = dt.datetime.strptime(end, '%H:%M:%S')
                diff = int((end_dt - start_dt).seconds / 60)
                if diff <= 0:
                    df.ix[idx, 'Czas do odjazdu:'] = 'Na przystanku...'
                if 0 < diff <= 1000:
                    df.ix[idx, 'Czas do odjazdu:'] = 'około ' + str(diff) + ' minut'
                if diff > 1000:
                    df.ix[idx, 'Czas do odjazdu:'] = 'Już odjechał...'
            return render_template('view.html', variable=stoperstoper[0][1], tables=[pd.DataFrame.to_html(df, index=False,
                                                                                                  justify='justify-all')
                                                                             ])


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)

