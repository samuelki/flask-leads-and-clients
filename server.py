from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
import datetime

app = Flask(__name__)
app.secret_key = "as56df0a65s1g98"

@app.route('/')
def index():
    mysql = connectToMySQL('lead_gen_business')
    query = mysql.query_db("SELECT CONCAT(clients.first_name, ' ', clients.last_name) AS client_name, COUNT(leads.leads_id) AS number_of_leads FROM clients JOIN sites ON clients.client_id = sites.client_id JOIN leads ON sites.site_id = leads.site_id GROUP BY client_name;")
    return render_template('index.html', clients=query)

@app.route('/date', methods=['POST'])
def date():
    session['start'] = request.form['start']
    session['end'] = request.form['end']
    
    mysql = connectToMySQL('lead_gen_business')
    query = "SELECT CONCAT(clients.first_name, ' ', clients.last_name) AS client_name, COUNT(leads.leads_id) AS number_of_leads FROM clients JOIN sites ON clients.client_id = sites.client_id JOIN leads ON sites.site_id = leads.site_id WHERE leads.registered_datetime BETWEEN %(start)s AND %(end)s GROUP BY client_name;"
    data = {
        'start': request.form['start'],
        'end': request.form['end']
    }
    updated_leads = mysql.query_db(query, data)
    return render_template('index.html', clients=updated_leads)

# @app.route('/updated')
# def updated():
#     mysql = connectToMySQL('lead_gen_business')

#     return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)