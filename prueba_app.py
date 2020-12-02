#!flask/bin/python
import sys
from flask import Flask, render_template, request, redirect, Response, url_for
import random, json

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('prueba.html')

@app.route('/xd')
def jalo():
    return 'xd'


@app.route('/receiver', methods = ['POST', 'GET'])
def worker():
    pass

    return redirect(url_for('jalo'))


if __name__ == '__main__':
	# run!
	app.run(debug=True)