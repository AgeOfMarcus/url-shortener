#!/usr/bin/python3

from flask import Flask, request, redirect
import sqlite3, uuid

host = "http://localhost:5000/" #CHANGEME

def sql(cmd):
	with sqlite3.connect("urls.db") as db:
		cursor = db.cursor()
		res = cursor.execute(cmd).fetchall()
		db.commit()
	return res

def fix_sql(lst):
	res = []
	for i in lst: res.append(i[0])
	return res

def startup():
	sql("CREATE TABLE IF NOT EXISTS urls (ID TEXT PRIMARY KEY, URL TEXT);")

app = Flask(__name__)

@app.route("/shorten",methods=['GET'])
def shorten_url():
	if not 'url' in request.args:
		return "", 200
	url = request.args['url']
	try:
		exist = fix_sql(sql("SELECT ID FROM urls WHERE URL='%s'" % url))
		if url in exist:
			return host + exist[0], 200
	except Exception as e:
		print("\n\nError checking if url exists: " + str(e) + "\n\n")
	id = ''.join(str(uuid.uuid4()).split("-"))
	short = ''
	while short == '' or short in fix_sql(sql("SELECT ID FROM urls")):
		if short == '':
			short += id[0]
			continue
		short += id[len(short)]
	sql("INSERT INTO urls (ID, URL) VALUES ('%s','%s')" % (short,url))
	return host + short, 200

@app.route("/<id>",methods=['GET'])
def redir(id):
	try:
		url = sql("SELECT URL FROM urls WHERE ID='%s'" % id)[0][0]
	except:
		url = host
	return redirect(url)

def main():
	startup()
	app.run(host="0.0.0.0",port=5000)

if __name__ == "__main__":
	main()
