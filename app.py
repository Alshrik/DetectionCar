from flask import Flask,render_template,request,redirect,url_for, flash
from extra import *
import psycopg2
import psycopg2.extras


app=Flask(__name__)
app.secret_key='cairocoders-ednalan'
# Connected with Database................
DB_HOST='localhost'
DB_NAME='Detection'
DB_USER='postgres'
DB_PASS='@Aa1@Aa1@'
conn=psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Return Home Page....................
@app.route('/')
@app.route('/home',methods=['GET','POST'])
def goHome():
    return render_template('home.html',navbar=True)

# Return All Data From Database And Show All Data In AllData Page.
@app.route('/allData',methods=['GET','POST'])
def allData():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM cars")
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return render_template('allData.html',data=data,navbar=True)

# Search in Database And Return The Result in result page.
@app.route('/srch',methods=['POST','GET'])
def search():
    plate_number=request.form['plate_number']
    if plate_number:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM cars WHERE plate_number=%s",(plate_number,))
        data = cur.fetchall()
        cur.close()
        if data:
            return render_template('results.html', data=data, navbar=True)
        else:
            return render_template('results.html', plate_number=plate_number, navbar=True)
    else:
        return render_template('home.html')
    
# Take the image and send it to extract_number function then show the result extraction.
@app.route('/extract',methods=['GET','POST'])
def extract():
    image = request.files['picture']
    if 'picture' in request.files:
        file=request.files['picture']
        nparr=np.frombuffer(file.read(),np.uint8)
        image=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        result = extract_number(image)
        location = request.form['location']
        return redirect(url_for('save', result=result,location=location))
    return render_template('extractPlate.html', result=result, location=location, navbar=True)

# Return The Index Page.
@app.route('/indexs',methods=['GET','POST'])
def indexs():
    return render_template('insert.html',navbar=True)
# Return The About Page.
@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html',navbar=True)
# Recive Data from extractPlate Then save the data in database . 
@app.route('/save',methods=['GET','POST'])
def save():
    result=request.args.get('result')
    location=request.args.get('location')
    if request.method == 'POST':
        result=request.form['result']
        location=request.form['location']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO cars (plate_number, location)  VALUES(%s, %s)",(result, location))
        conn.commit()
        cur.close()
        flash('Car number added successfly')
    return render_template('save.html', result=result, location=location, navbar=True)

if __name__=='__main__':
    app.run()    