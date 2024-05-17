
from flask import Flask,flash,redirect,render_template,url_for,request,jsonify,session,abort
from flask_session import Session
#from flask_mysqldb import MySQL
from datetime import date
from datetime import datetime
from sdmail import sendmail
from tokenreset import token
from stoken1 import token1
from stoken2 import token2
from database import execute_query

import os
from datetime import datetime
import datetime

from itsdangerous import URLSafeTimedSerializer
from key import *

#import stripe
#stripe.api_key='sk_test_51MzcVYSDVehZUuDTkwGUYe8hWu2LGN0krI8iO5QOAEqoRYXx3jgRVgkY7WzXqQmpN62oMWM59ii76NKPrRzg3Gtr005oVpiW82'
app=Flask(__name__)
app.secret_key='hello'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)




import random
def genotp():
    u_c=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    l_c=[chr(i) for i in range(ord('a'),ord('z')+1)]
    otp=''
    for i in range(3):
        otp+=random.choice(u_c)
        otp+=str(random.randint(0,9))
        otp+=random.choice(l_c)
    return otp
@app.route('/')
def home():
    places=execute_query('select * from places')
    return render_template('home.html',places=places)
@app.route('/homepage/<place_id>')
def homepage(place_id):
    #print('================',place_id)
    hdetails=execute_query('select * from hotels where place_id=%s',[place_id])
    tdetails=execute_query('select * from trip_package where place_id=%s',[place_id])
    bdetails=execute_query('select * from blogs where place_id=%s',[place_id])
    #print('================',hdetails)
    
    return render_template('homepage.html',h=hdetails,t=tdetails,b=bdetails)
#=========================================Blogs login and register
@app.route('/viewblogbyblogadmin')
def viewblog():
    if session.get('user'):
        details=execute_query('select * from blogs where user_id=%s',[session['user']])
        return render_template('viewblogsbyadmin.html',d=details)
    return redirect(url_for('ulogin'))
@app.route('/ulogin',methods=['GET','POST'])
def ulogin():
    if session.get('user'):
        return redirect(url_for('blogs_dashboard'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        # cursor = mydb.cursor(buffered=True)
        count=execute_query('SELECT count(*) as count from user where username=%s and password=%s',[username,password])[0]
        # count=cursor.fetchone()[0]
        if count==(1,):
            session['user']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for("blogs_dashboard"))
        else:
            flash('Invalid username or password')
            return render_template('ulogin.html')
    return render_template('ulogin.html')

@app.route('/uregistration',methods=['GET','POST'])
def uregistration():
    if request.method=='POST':
        username = request.form['username']
        
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        password = request.form['password']
        
        
        #cursor = mydb.cursor(buffered=True)
        count = execute_query('select count(*) from user where username=%s',[username])[0]
        #count=cursor.fetchone()[0]
        count1 = execute_query('select count(*) from user where email=%s',[email])[0]
        #count1=cursor.fetchone()[0]
        #cursor.close()
        if count==(1,):
            flash('username already in use')
            return render_template('uregistration.html')
        elif count1==(1,):
            flash('hotel_email already in use')
            return render_template('uregistration.html')
        
        data={'username':username,'email':email,'phone':phone,'address':address,'password':password}
        subject='hotel_email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('uconfirm',token=token(data,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('uregistration'))
    
    return render_template('uregistration.html')
@app.route('/uconfirm/<token>')
def uconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        #cursor = mydb.cursor(buffered=True)
        id1=data['username']
        count = execute_query('select count(*) from user where username=%s',[id1])[0]
        #count=cursor.fetchone()[0]
        if count==(1,):
            #cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('ulogin'))
        else:
            execute_query('INSERT INTO user (username,email,phone_number,address,password) VALUES (%s,%s,%s,%s,%s)',[data['username'],data['email'],data['phone'],data['address'], data['password']],commit=True)

            # mydb.commit()
            # cursor.close()
            flash('Details registered!')
            return redirect(url_for('ulogin'))

@app.route('/forget',methods=['GET','POST'])
def uforgot():
    if request.method=='POST':
        id1=request.form['id1']
        #cursor = mydb.cursor(buffered=True)
        count=execute_query('select count(*) from user where username=%s',[id1])[0]
        # count=cursor.fetchone()[0]
        # cursor.close()
        if count==(1,):
            #cursor = mydb.cursor(buffered=True)

            hotel_email=execute_query('SELECT email from user where username=%s',[id1])[0]
            #hotel_email=cursor.fetchone()[0]
            # cursor.close()
            subject='Forget Password'
            confirm_link=url_for('ureset',token=token(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=hotel_email,body=body,subject=subject)
            flash('Reset link sent check your hotel_email')
            return redirect(url_for('ulogin'))
        else:
            flash('Invalid hotel_email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def ureset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                # cursor = mydb.cursor(buffered=True)
                execute_query('update user set password=%s where username=%s',[newpassword,id1],commit=True)
                # mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('ulogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/ulogout')
def ulogout():
    if session.get('user'):
        session.pop('user')
        flash('Successfully loged out')
        return redirect(url_for('ulogin'))
    else:
        return redirect(url_for('ulogin'))
@app.route('/blogs_dashboard')
def blogs_dashboard():
    if session.get('user'):
        return render_template('blogs_dashboard.html')
    return redirect(url_for('ulogin'))

@app.route('/createblog',methods=['GET','POST'])
def createblog():
    if session.get('user'):
        places=execute_query('select * from places')
        if request.method=="POST":
            title=request.form['title']
            content=request.form['content']
            place=request.form['place']
            place_id_result = execute_query('SELECT place_id FROM places WHERE place_name = %s', [place])

            if place_id_result:
                tplace = place_id_result[0][0]
            else:
                flash(f'The place {place} does not exist. Please add it first.')
                return redirect(url_for('createblog'))
            #print('=========================',tplace)
            execute_query('insert into blogs (title,content,user_id,place_id) values (%s,%s,%s,%s)',[title,content,session['user'],tplace],commit=True)
            flash(f'{title} added sucessfully')
            return redirect(url_for('createblog'))

        return render_template('createblogs.html',places=places)
    return redirect(url_for('ulogin'))

@app.route('/addnewplace_b',methods=['GET','POST'])
def addnewplace_b():
    if session.get('user'):
        if request.method=="POST":
            id_pic=genotp()
            place=request.form['place']
            image=request.files['image']
            count_result = execute_query('SELECT COUNT(*) FROM places WHERE place_name = %s', [place])
            count = count_result[0][0] if count_result else 0
        
            if count > 0:
                flash(f'The place {place} is already added. Please check again.')
                return redirect(url_for('addnewplace'))
            else:
                filename=id_pic+'.jpg'#picture
                execute_query('insert into places (place_name,place_pic,added_by) values(%s,%s,%s)',[place,id_pic,session['user']],commit=True)
                path=r"C:\Users\user\Desktop\trip_planner (1)\trip_planner\static"            
                image.save(os.path.join( path, filename))
                flash(f'{place} added successfully')
                return redirect(url_for('addnewplace'))
        return render_template('addnewplace.html')
    return redirect(url_for('ulogin'))
#=================================anyone can view the trip packages
@app.route('/viewtripsanyone')
def viewtrips():
    trips=execute_query('select * from trip_package')
    #print("=========================",trips)
    return render_template('viewtrips_u.html',d=trips)
#====================================anyone can view the blogs
@app.route('/viewblogsanyone')
def viewblogsanyone():
    details=execute_query('select * from blogs')
    return render_template('viewblogs_u.html',b=details)



#==========================anyone can view the hotel details
# @app.route('/viewhotels')
# def viewhotels():
#     hotels=execute_query('select * from hotels')
#     places=execute_query('select * from places')
#     return render_template('viewhotels.html',detail=hotels,p=places)
from flask import request

@app.route('/viewhotels', methods=['GET', 'POST'])
def viewhotels():
    if request.method == 'POST':
        search_query = request.form['search_query']
        query = "SELECT * FROM hotels WHERE address_details LIKE '%" + search_query + "%'"
        hotels = execute_query(query)
    else:
        hotels = execute_query('SELECT * FROM hotels')
    places = execute_query('SELECT * FROM places')
    return render_template('viewhotels.html', detail=hotels, p=places)

#============================== hotel registration
@app.route('/hlogin',methods=['GET','POST'])
def hlogin():
    if session.get('hotel'):
        return redirect(url_for('hotel_dashboard'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        # cursor = mydb.cursor(buffered=True)
        count=execute_query('SELECT count(*)  from hotel_registration where hotel_username=%s and password=%s',[username,password])[0]
        # count=cursor.fetchone()[0]
        #print('===============================================',count)
        if count==(1,):
            session['hotel']=username
            return redirect(url_for('hotel_dashboard'))
        else:
            flash('Invalid username or password')
            return render_template('hlogin.html')
    return render_template('hlogin.html')

@app.route('/hregistration',methods=['GET','POST'])
def hregistration():
    if request.method=='POST':
        name=request.form['hotel_name']
        hotel_place=request.form['hotel_place']
        hotel_email=request.form['hotel_email']
        phone=request.form['hotel_phone_number']
        username=request.form['hotel_username']
        password=request.form['password']
        
        
        
        # cursor = mydb.cursor(buffered=True)
        count=execute_query('select count(*) from hotel_registration where hotel_username=%s',[username])[0]
        # count=cursor.fetchone()[0]
        count1=execute_query('select count(*) from hotel_registration where hotel_email=%s',[hotel_email])[0]
        # count1=cursor.fetchone()[0]
        # cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('hregister.html')
        elif count1==1:
            flash('hotel_email already in use')
            return render_template('hregister.html')
        
        data1={'name':name,'place':hotel_place,'hotel_email':hotel_email,'phone':phone,'username':username,'password':password}
        subject='hotel_email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('hconfirm',token=token1(data1,salt),_external=True)}"
        sendmail(to=hotel_email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('hregistration'))
    
    return render_template('hregister.html')
@app.route('/hconfirm/<token>')
def hconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        # cursor = mydb.cursor(buffered=True)
        id1=data['username']
        count=execute_query('select count(*) from hotel_registration where hotel_username=%s',[id1])[0]
        # count=cursor.fetchone()[0]
        if count==1:
            # cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('hotel_dashboard'))
        else:
            execute_query('INSERT INTO hotel_registration (hotel_email,hotel_phone_number,hotel_name,hotel_place,password,hotel_username) VALUES (%s, %s, %s,%s, %s, %s)', [data['hotel_email'],data['phone'],data['name'],   data['place'],data['password'],data['username']],commit=True)

            # mydb.commit()
            # cursor.close()
            flash('Details registered!')
            return redirect(url_for('hlogin'))
@app.route('/hforget',methods=['GET','POST'])
def hforgot():
    if request.method=='POST':
        id1=request.form['id1']
        # cursor = mydb.cursor(buffered=True)
        #print("Executing SQL query:", 'select count(*) as count from hotel_registration where hotel_username=%s', [id1])

        count=execute_query('select count(*) as count from hotel_registration where hotel_username=%s',[id1])[0]
        #print("Query Result (count):", count)
        # count=cursor.fetchone()[0]
        # cursor.close()
        #print('===================================',count)
        if count==(1,):
            # cursor = mydb.cursor(buffered=True)

            hotel_email=execute_query('SELECT hotel_email from hotel_registration where hotel_username=%s',[id1])[0]
            # hotel_email=cursor.fetchone()[0]
            # cursor.close()
            subject='Forget Password'
            confirm_link=url_for('hreset',token=token1(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=hotel_email,body=body,subject=subject)
            flash('Reset link sent check your hotel_email')
            return redirect(url_for('hlogin'))
        else:
            flash('Invalid hotel username id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/hreset/<token>',methods=['GET','POST'])
def hreset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                # cursor = mydb.cursor(buffered=True)
                execute_query('update hotel_registration set password=%s where hotel_username=%s',[newpassword,id1],commit=True)
                # mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('hlogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/hlogout')
def hlogout():
    if session.get('hotel'):
        session.pop('hotel')
        flash('Successfully loged out')
        return redirect(url_for('hlogin'))
    else:
        return redirect(url_for('hlogin'))
@app.route('/booktohotel/<hid>',methods=['GET','POST'])
def booktohotel(hid):
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        rooms=request.form['rooms']
        execute_query('insert into bookings (name,email,contact_number,number_of_rooms,hotel_id) values (%s,%s,%s,%s,%s)',[name,email,phone,rooms,hid],commit=True)
        flash('you will get the notification to the email ')
        subject='Room Booking'
        body=f"{name} Thanks for booking up\n\n our management contact with you"
        sendmail(to=email,subject=subject,body=body)
        return redirect(url_for('home'))

    return render_template('bookhotel.html')
@app.route('/booktrip/<tid>', methods=['GET', 'POST'])
def booktrip(tid):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        package_id = tid  # Assuming tid corresponds to package_id
        execute_query('INSERT INTO trip_bookings (name, email, contact_number, package_id) VALUES (%s, %s, %s, %s)',
                      [name, email, phone, package_id], commit=True)
        flash('Your trip has been booked successfully!')
        subject = 'Trip Booking Confirmation'
        body = f"Dear {name},\n\nThank you for booking the trip with us. We look forward to serving you.\n\nRegards,\n[Your Trip Planner]"
        sendmail(to=email, subject=subject, body=body)
        return redirect(url_for('home'))

    trip_details = execute_query('SELECT * FROM trip_package WHERE trip_id = %s', [tid])
    return render_template('booktrip.html', trip=trip_details)


@app.route('/hotel_dashboard')
def hotel_dashboard():
    if session.get('hotel'):
        return render_template('hotel_dashboard.html')
    else:
        return redirect(url_for('hlogin'))
@app.route('/hotelcreate',methods=['GET','POST'])
def createhotel():
    if session.get('hotel'):
        places=execute_query('select * from places')
        if request.method=="POST":
            hid=genotp()#hotel images
            rid=genotp()#room images
            name=request.form['hotel_name']
            email=request.form['email']
            picture=request.files['hotel_picture']
            number = request.form['contact_number']
            address=request.form['address_details']
            timings=request.form['timings']
            total_rooms=request.form['total_rooms']
            cost=request.form['room_cost']
            description=request.form['hotel_description']
            images= request.files['room_images']
            availability=request.form['room_availability']
            available_rooms=request.form['available_rooms']
            place=request.form['place']
            place_id_result = execute_query('SELECT place_id FROM places WHERE place_name = %s', [place])
            if place_id_result:
                hplace = place_id_result[0][0]
            else:
                flash(f'The place {place} does not exist. Please add it first.')
                return redirect(url_for('createhotel'))
            filename=hid+'.jpg'#picture
            filename1=rid+'.jpg'#room images
            execute_query('INSERT INTO hotels (hotel_name, hotel_picture, contact_number, email,address_details, timings, total_rooms, room_cost, hotel_description, room_images, room_availability, available_rooms, place_id, added_by) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                      [name,hid, number,email, address, timings, total_rooms, cost, description, rid, availability, available_rooms, hplace, session['hotel']],commit=True)
            path=r"C:\Users\user\Desktop\trip_planner (1)\trip_planner\static"
            picture.save(os.path.join(path, filename))#hotel images
            images.save(os.path.join(path, filename1))#room images

            flash(f'{name} hotel added successfully')
            return redirect(url_for('createhotel'))
        return render_template('createhotel.html',places=places)
    else:
        return redirect(url_for('hlogin'))

@app.route('/addnewplace',methods=['GET','POST'])
def addnewplace():
    if session.get('hotel'):
        if request.method=="POST":
            id_pic=genotp()
            place=request.form['place']
            image=request.files['image']
            count_result = execute_query('SELECT COUNT(*) FROM places WHERE place_name = %s', [place])
            count = count_result[0][0] if count_result else 0
        
            if count > 0:
                flash(f'The place {place} is already added. Please check again.')
                return redirect(url_for('addnewplace'))
            else:
                filename=id_pic+'.jpg'#picture
                execute_query('insert into places (place_name,place_pic,added_by) values(%s,%s,%s)',[place,id_pic,session['hotel']],commit=True)
                path=r"C:\Users\user\Desktop\trip_planner (1)\trip_planner\static"              
                image.save(os.path.join(path, filename))
                flash(f'{place} added successfully')
                return redirect(url_for('addnewplace'))
        return render_template('addnewplace.html')
    return redirect(url_for('hlogin'))
#=======================hotel admin view his hotel details

@app.route('/viewhotel_hotel', methods=['GET', 'POST'])
def viewhotel_hotel():
    if session.get('hotel'):
        print(session.get('hotel'))
        details = execute_query('select * from hotels where added_by=%s', [session['hotel']])
        try:
            place_query_result = execute_query('select place_id from hotels where added_by=%s', [session['hotel']])
            place = place_query_result[0][0]
            place_details = execute_query('select * from places where added_by=%s', [place])
            return render_template('viewhotel_hoteladmin.html', detail=details, p=place_details)
        except IndexError:
            # Handle the case where the query result is empty
            # You can redirect the user or render a specific error page
            # For example:
            return "nothing to display"
    return redirect(url_for('hlogin'))
@app.route('/update_hotel/<int:hotel_id>', methods=['GET', 'POST'])
def update_hotel(hotel_id):
    if request.method == 'POST':
        # Fetching form data
        hotel_name = request.form['hotel_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        timings = request.form['timings']
        total_rooms = request.form['total_rooms']
        room_cost = request.form['room_cost']
        description = request.form['description']
        rooms_availability = request.form['rooms_availability']
        available_rooms = request.form['available_rooms']
            
        # Update the database with the new details
        execute_query('UPDATE hotels SET hotel_name=%s, contact_number=%s, email=%s, address_details=%s, timings=%s, total_rooms=%s, room_cost=%s, hotel_description=%s, room_availability=%s, available_rooms=%s WHERE hotel_id=%s',
                      (hotel_name, contact_number, email, address, timings, total_rooms, room_cost, description, rooms_availability, available_rooms, hotel_id),
                      commit=True)  # Commit the transaction
        
        # Redirect to a success page or back to the update page
        return "done"
        
    # Fetch hotel details from the database based on session 'hotel' value
    details = execute_query('SELECT * FROM hotels WHERE hotel_id=%s', (hotel_id,))
    print(details)
    return render_template('hotel_update.html', details=details)

@app.route('/update_trips/<int:package_id>', methods=['GET', 'POST'])
def update_trips(package_id):
    if request.method == 'POST':
        # Extract modified data from the form
        package_name = request.form['package_name']
        description = request.form['description']
        price = request.form['price']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        duration = request.form['duration']
        includes = request.form['includes']
        excludes = request.form['excludes']
        
        # Update the specific trip package with the given ID
        execute_query('UPDATE trip_package SET package_name=%s, description=%s, price=%s, start_date=%s, end_date=%s, duration_days=%s, includes_amenities=%s, excludes_amenities=%s WHERE package_id=%s ',
                      (package_name, description, price, start_date, end_date, duration, includes, excludes, package_id),
                      commit=True)  # Commit the transaction
        
        # Redirect to a success page or back to the update page
        return "Trip package updated successfully"
        
    # Fetch details of the specific trip package with the given ID
    details = execute_query('SELECT * FROM trip_package WHERE package_id=%s', (package_id,))

    
    return render_template('trip_update.html', details=details)
    


@app.route('/update_blog/<int:blog_id>', methods=['GET', 'POST'])
def update_blog(blog_id):
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_content = request.form['blog-content']
        execute_query('UPDATE blogs SET title=%s, content=%s WHERE blog_id=%s', (blog_title, blog_content, blog_id), commit=True)
        return "Blog updated successfully"

    # Retrieve blog details based on blog_id
    blog_details = execute_query('SELECT * FROM blogs WHERE blog_id=%s', (blog_id,))
    

    return render_template('update_blog.html', details=blog_details)

    
@app.route('/delete_blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    if session.get('user'):
        # Delete the blog entry from the database
        execute_query('DELETE FROM blogs WHERE blog_id=%s', (blog_id,), commit=True)

        # Redirect to a relevant page after deletion, for example, the blogs dashboard
        return redirect(url_for('blogs_dashboard'))
    else:
        # Redirect to login page or any other relevant page if user is not authenticated
        return redirect(url_for('login'))



@app.route('/delete_hotel/<int:hotel_id>')
def delete_hotel(hotel_id):
    # Delete related bookings
    execute_query('DELETE FROM bookings WHERE hotel_id=%s', [hotel_id], commit=True)
    # Delete the hotel
    execute_query('DELETE FROM hotels WHERE hotel_id=%s', [hotel_id], commit=True)
    return redirect(url_for('viewhotel_hotel'))  # Redirect to view hotels page after deletion

@app.route('/delete_trips/<company_name>', methods=['GET', 'POST'])
def delete_trips(company_name):
    if request.method == 'POST':
        # Delete associated bookings first
        execute_query('DELETE FROM trip_bookings WHERE package_id IN (SELECT package_id FROM trip_package WHERE company_name = %s)',
                      (company_name,),
                      commit=True)
        
        # Then delete the trip
        execute_query('DELETE FROM trip_package WHERE company_name = %s',
                      (company_name,),
                      commit=True)
        
        return redirect(url_for('tripplanner_dashboard'))
    else:
        return "nope"
    #=================================trip packages planners
@app.route('/tlogin',methods=['GET','POST'])
def tlogin():
    if session.get('trip'):
        return redirect(url_for('tripplanner_dashboard'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        # cursor = mydb.cursor(buffered=True)
        count=execute_query('SELECT count(*)  from tripplanner_registration where username=%s and password=%s',[username,password])[0]
        # count=cursor.fetchone()[0]
        #print('===============================================',count)
        if count==(1,):
            session['trip']=username
            return redirect(url_for('tripplanner_dashboard'))
        else:
            flash('Invalid username or password')
            return render_template('tlogin.html')
    return render_template('tlogin.html')

@app.route('/tregistration',methods=['GET','POST'])
def tregistration():
    if request.method=='POST':
        name=request.form['username']
        email=request.form['email']
        phone=request.form['phone_number']
        address=request.form['address']
        password=request.form['password']
        
        
        
        # cursor = mydb.cursor(buffered=True)
        count=execute_query('select count(*) from tripplanner_registration where username=%s',[name])[0]
        # count=cursor.fetchone()[0]
        count1=execute_query('select count(*) from tripplanner_registration where email=%s',[email])[0]
        # count1=cursor.fetchone()[0]
        # cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('tregister.html')
        elif count1==1:
            flash('hotel_email already in use')
            return render_template('tregister.html')
        
        data2={'name':name,'email':email,'phone':phone,'address':address,'password':password}
        subject='hotel_email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('tconfirm',token=token2(data2,salt),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('tregistration'))
    
    return render_template('tregister.html')
@app.route('/tconfirm/<token>')
def tconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        # cursor = mydb.cursor(buffered=True)
        id1=data['name']
        count=execute_query('select count(*) from tripplanner_registration where username=%s',[id1])[0]
        # count=cursor.fetchone()[0]
        if count==1:
            # cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('tripplanner_dashboard'))
        else:
            execute_query('INSERT INTO tripplanner_registration (username,email,phone_number,address,password) VALUES (%s, %s, %s, %s, %s)', [data['name'],data['email'],data['phone'],   data['address'],data['password']],commit=True)

            # mydb.commit()
            # cursor.close()
            flash('Details registered!')
            return redirect(url_for('tlogin'))
@app.route('/tforget',methods=['GET','POST'])
def tforgot():
    if request.method=='POST':
        id1=request.form['id1']
        # cursor = mydb.cursor(buffered=True)
        #print("Executing SQL query:", 'select count(*) as count from hotel_registration where hotel_username=%s', [id1])

        count=execute_query('select count(*) as count from tripplanner_registration where username=%s',[id1])[0]
        #print("Query Result (count):", count)
        # count=cursor.fetchone()[0]
        # cursor.close()
        #print('===================================',count)
        if count==(1,):
            # cursor = mydb.cursor(buffered=True)

            hotel_email=execute_query('SELECT email from tripplanner_registration where username=%s',[id1])[0]
            # hotel_email=cursor.fetchone()[0]
            # cursor.close()
            subject='Forget Password'
            confirm_link=url_for('treset',token=token2(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=hotel_email,body=body,subject=subject)
            flash('Reset link sent check your hotel_email')
            return redirect(url_for('tlogin'))
        else:
            flash('Invalid hotel username id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/treset/<token>',methods=['GET','POST'])
def treset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                # cursor = mydb.cursor(buffered=True)
                execute_query('update tripplanner_registration set password=%s where username=%s',[newpassword,id1],commit=True)
                # mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('tlogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/tlogout')
def tlogout():
    if session.get('trip'):
        session.pop('trip')
        flash('Successfully loged out')
        return redirect(url_for('tlogin'))
    else:
        return redirect(url_for('tlogin'))
@app.route('/tripplanner_dashboard')
def tripplanner_dashboard():
    if session.get('trip'):
        return render_template('tripplanner_dashboard.html')
    else:
        return redirect(url_for('tlogin'))
@app.route('/viewtrip_members')
def viewtrip_members():
    if session.get('trip'):
        # Fetch the package_id associated with the current user (assuming 'anu' is the username)
        package_id_result = execute_query('SELECT package_id FROM trip_package WHERE username=%s', [session['trip']])
        if package_id_result:
            package_id = package_id_result[0][0]  # Extracting package_id from the result
            print("Package ID:", package_id)  # Debugging: Print the package_id
            
            # Fetch bookings related to the package_id
            bookings = execute_query('SELECT * FROM trip_bookings WHERE package_id = %s', [package_id])
            print("Bookings:", bookings)  # Debugging: Print the bookings
            
            if bookings is not None:
                return render_template('viewtrip_members.html', bookings=bookings)
            else:
                print("No bookings found.")
        else:
            print("No package_id found for the user.")
        
    # Redirect to the login page if session['trip'] is not set or if no package is associated with the user
    return redirect(url_for('tlogin'))

    
    # Redirect to the login page if session['trip'] is not set or if no package is associated with the user
    return redirect(url_for('tlogin'))
@app.route('/viewbookings')
def viewbookings():
    if session.get('hotel'):
        hid=execute_query('select hotel_id from hotels where added_by=%s',[session['hotel'],])[0][0]
        details=execute_query('select * from bookings where hotel_id=%s',[hid])
        return render_template('viewbookingshotel.html',b=details)
    return redirect(url_for('hlogin'))
@app.route('/createtrip', methods=['GET', 'POST'])
def createtrip():
    if session.get('trip'):
        places = execute_query('SELECT * FROM places')
        if request.method == "POST":
            cname = request.form['cname']
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            includes_amenities = request.form['includes_amenities']
            excludes_amenities = request.form['excludes_amenities']
            place = request.form['place']
            
            # Retrieve the place_id from the places table based on the selected place_name
            place_id_result = execute_query('SELECT place_id FROM places WHERE place_name = %s', [place])

            if place_id_result:
                place_id = place_id_result[0][0]
            else:
                flash(f'The place {place} does not exist. Please add it first.')
                return redirect(url_for('createhotel'))

            # Insert the trip package into the trip_package table
            execute_query('INSERT INTO trip_package (place_id, package_name, description, price, start_date, end_date, includes_amenities, excludes_amenities, company_name, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                          [place_id, name, description, price, start_date, end_date, includes_amenities, excludes_amenities, cname, session['trip']], commit=True)
            flash(f'{name} added successfully')
            return redirect(url_for('createtrip'))

        return render_template('createtrip_package.html', places=places)
    return redirect(url_for('tlogin'))
@app.route('/viewtrip_admin')
def viewtrip_admin():
    if session.get('trip'):
        details=execute_query('select * from trip_package where username=%s',[session['trip']])
        print('-------------------',details)
        return render_template('viewtrips.html',detail=details)
    return redirect(url_for('tlogin'))

@app.route('/addnewplace_t',methods=['GET','POST'])
def addnewplace_t():
    if session.get('trip'):
        if request.method=="POST":
            id_pic=genotp()
            place=request.form['place']
            image=request.files['image']
            count_result = execute_query('SELECT COUNT(*) FROM places WHERE place_name = %s', [place])
            count = count_result[0][0] if count_result else 0
        
            if count > 0:
                flash(f'The place {place} is already added. Please check again.')
                return redirect(url_for('addnewplace'))
            else:
                filename=id_pic+'.jpg'#picture
                execute_query('insert into places (place_name,place_pic,added_by) values(%s,%s,%s)',[place,id_pic,session['trip']],commit=True)
                path=r"C:\Users\user\Desktop\trip_planner (1)\trip_planner\static"              
                image.save(os.path.join( path, filename))
                flash(f'{place} added successfully')
                return redirect(url_for('addnewplace'))
        return render_template('addnewplace.html')
    return redirect(url_for('tlogin'))

app.run(use_reloader=True,debug=True)