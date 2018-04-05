from flask import Flask, render_template, request
import json


w = json.load(open("worldl.json"))
for c in w:
	c['tld'] = c['tld'][1:]
page_size = 20
app = Flask(__name__)

@app.route('/')
def mainPage():
	
    return render_template('index.html',
    	w=w[0:page_size],page_number=0,page_size=page_size)

@app.route('/begin/<b>')
def beginPage(b):
	bn = int(b)
	if(bn<=0):
		hh='index-1.html'
	elif(bn>=len(w)-1):
		hh='index+195.html'
	else:
		hh='index.html'
	
	return render_template(hh, 
		w=w[bn:bn+page_size],
		page_number = bn,
		page_size = page_size
		)

@app.route('/continent/<a>')
def continentPage(a):
	cl = [c for c in w if c['continent']==a]
	return render_template(
		'continent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a
		)

@app.route('/country/<i>')
def countryPage(i):
	return render_template(
		'country.html',
		c = w[int(i)])

@app.route('/countryByName/<n>')
def countryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'country.html',
		c = c)

@app.route('/delete/<n>')

def deleteCountryPage(n):
	i=0
	for c in w:
		if c['name'] == n:
			break

		i+=1

	del w[i]
	return render_template('index.html',
		page_number=0,
		page_size=page_size,
		w = w[0:page_size])
#all deleted country will be back on the list after restarting the server

@app.route('/editcountryByName/<n>')
def editcountryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'country-edit.html',
		c = c)

@app.route('/updatecountrybyname')
def updatecountryByNamePage():
	n=request.args.get('name')
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	c['capital']=request.args.get('capital')
	c['continent']=request.args.get('continent') 
	return render_template(
		'country.html',
		c = c)

@app.route('/searchbyalphabet/<ab>')
def searchByAlphabet(ab):
	ab=ab.upper()
	alph=[]
	for i in w:
		name=i['name']
		if(name[0]==ab):
			alph.append(i)

	#al = [c for c in w if c['name']==ab]

	return render_template(
		'search.html',
		length_of_alph = len(alph),
		alph = alph,
		ab = ab)


app.run(host='0.0.0.0', port=5645, debug=True)




