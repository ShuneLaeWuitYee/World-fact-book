from flask import Flask, render_template, request
import json

w = json.load(open("worldl.json"))
alist=sorted(list(set([c['name'][0] for c in w])))
for c in w:
	c['tld'] = c['tld'][1:]
page_size = 20
app = Flask(__name__)

@app.route('/')
def mainPage():	
    return render_template('index.html',
    	w=w[0:page_size],page_number=0,page_size=page_size,alist=alist)

@app.route('/begin/<b>')
def beginPage(b):
	bn = int(b)
	if(bn<0):
		hh='index-1.html'
	elif(bn>=len(w)-1):
		hh='index+195.html' 
	else:
		hh='index.html'	
	return render_template(hh, 
		w=w[bn:bn+page_size],
		page_number = bn,
		page_size = page_size,alist=alist
		)

@app.route('/continent/<a>,<n>')
def continentPage(a,n):	
	a=a.replace("'","")
	a=a.replace("(","")
	#a=a.replace(' ','')
	n=n.replace("'","")
	n=n.replace(")","")
	#n=n.replace(' ','')
	cl = [c for c in w if c['continent']==a]
	return render_template(
		'continent.html',
		length_of_cl = len(cl),
		cl = cl,
		a = a,
		n = n,
		alist=alist
		)

@app.route('/country/<i>')
def countryPage(i):
	return render_template(
		'country.html',
		c = w[int(i)],
		alist=alist)

@app.route('/countryByName/<n>')
def countryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	return render_template(
		'country.html',
		c = c,
		alist=alist)

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
		w = w[0:page_size],alist=alist)
#all deleted country will be back on the list after restarting the server

@app.route('/editcountryByName/<n>')
def editcountryByNamePage(n):
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	#c=c.replace(' ','_')
	return render_template(
		'country-edit.html',
		c = c)

@app.route('/updatecountrybyname')
def updatecountryByNamePage():
	n=request.args.get('name')
	n=n.replace('_',' ')
	c = None
	for x in w:
		if x['name'] == n:
			c = x
	c['capital']=request.args.get('capital')
	c['continent']=request.args.get('continent') 
	c['area']=int(request.args.get('area'))
	c['population']=int(request.args.get('population'))
	c['gdp']=int(request.args.get('gdp'))
	return render_template(
		'country.html',
		c = c, alist=alist)

@app.route('/searchbyalphabet/<ab>')
def searchByAlphabet(ab):
	ab=ab.upper()
	alph=[]
	for i in w:
		name=i['name']
		if(name[0]==ab):
			alph.append(i)	
	return render_template(
		'search.html',
		length_of_alph = len(alph),
		alph = alph,
		ab = ab,
		alist=alist)

app.run(host='0.0.0.0', port=5645, debug=True)
