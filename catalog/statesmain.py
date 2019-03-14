from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from StatesData_Setup import Base, States, StatesName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///statesdatabase.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "States Details"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
tss_det = session.query(States).all()


# login#completed
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    tss_det = session.query(States).all()
    tsh = session.query(StatesName).all()
    return render_template('login.html',
                           STATE=state, tss_det=tss_det, tsh=tsh)
    '''return render_template('home.html', STATE=state
     tss_det=tss_det,tsh=tsh)'''


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions#completed
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
# Home


@app.route('/')
@app.route('/home')
def home():
    tss_det = session.query(States).all()
    return render_template('home.html', tss_det=tss_det)


# states Category for admins


@app.route('/StatesStore')
def StatesStore():
    try:
        if login_session['username']:
            name = login_session['username']
            tss_det = session.query(States).all()
            tds = session.query(States).all()
            tsh = session.query(StatesName).all()
            return render_template('home.html', tss_det=tss_det,
                                   tds=tds, tsh=tsh, uname=name)
    except:
        return redirect(url_for('showLogin'))
# Showing states based


@app.route('/StatesStore/<int:sid>/AllStates')
def showstates(sid):
    tss_det = session.query(States).all()
    tds = session.query(States).filter_by(id=sid).one()
    tsh = session.query(StatesName).filter_by(statesid=sid).all()
    try:
        if login_session['username']:
            return render_template('showStatesDetails.html', tss_det=tss_det,
                                   tds=tds, tsh=tsh,
                                   uname=login_session['username'])
    except:
        return render_template('showStatesDetails.html',
                               tss_det=tss_det, tds=tds, tsh=tsh)
# Add New states


@app.route('/StatesStore/addstates', methods=['POST', 'GET'])
def addstates():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        company = States(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('StatesStore'))
    else:
        return render_template('addStatesDetails.html', tss_det=tss_det)
# Edit  Statename


@app.route('/StatesStore/<int:sid>/edit', methods=['POST', 'GET'])
def editStates(sid):
    if 'username' not in login_session:
        return redirect('/login')
    editedstate = session.query(States).filter_by(id=sid).one()
    creator = getUserInfo(editedstate.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this states Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('StatesStore'))
    if request.method == "POST":
        if request.form['name']:
            editedstate.name = request.form['name']
        session.add(editedstate)
        session.commit()
        flash("states Edited Successfully")
        return redirect(url_for('StatesStore'))
    else:
        # tss_det is global variable we can them in entire application
        return render_template('editStatesDetails.html',
                               sd=editedstate, tss_det=tss_det)


# Delete State
@app.route('/StatesStore/<int:sid>/delete', methods=['POST', 'GET'])
def deleteStates(sid):
    if 'username' not in login_session:
        return redirect('/login')
    sd = session.query(States).filter_by(id=sid).one()
    creator = getUserInfo(sd.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this state Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('StatesStore'))
    if request.method == "POST":
        session.delete(sd)
        session.commit()
        flash("States Category Deleted Successfully")
        return redirect(url_for('StatesStore'))
    else:
        return render_template(
            'deleteStatesDetails.html', sd=sd, tss_det=tss_det)

# Add New distict


@app.route('/StatesStore/addstate/adddistrict/<string:sname>/add',
           methods=['GET', 'POST'])
def adddistrict(sname):
    if 'username' not in login_session:
        return redirect('/login')
    tds = session.query(States).filter_by(name=sname).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(tds.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('StatesStore', sid=tds.id))
    if request.method == 'POST':
        district = request.form['district']
        headquartes = request.form['headquartes']
        revenue_division = request.form['revenue_division']
        mandals = request.form['mandals']
        population = request.form['population']
        area = request.form['area']
        density = request.form['density']
        statedetails = StatesName(
            district=district, headquartes=headquartes,
            revenue_division=revenue_division, mandals=mandals,
            population=population, area=area, density=density,
            statesid=tds.id, user_id=login_session['user_id'])
        session.add(statedetails)
        session.commit()
        return redirect(url_for('showstates', sid=tds.id))
    else:
        return render_template('adddistrict.html',
                               sname=tds.name, tss_det=tss_det)

# Edit distict details


@app.route('/StatesStore/<int:sid>/<string:dname>/edit',
           methods=['GET', 'POST'])
def editdistrict(sid, dname):
    t = session.query(States).filter_by(id=sid).one()
    statedetails = session.query(StatesName).filter_by(district=dname).one()
    creator = getUserInfo(t.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showstates', sid=t.id))
    # POST methods
    if request.method == 'POST':
        statedetails.district = request.form['district']
        statedetails.headquartes = request.form['headquartes']
        statedetails.revenue_division = request.form['revenue_division']
        statedetails.mandals = request.form['mandals']
        statedetails.population = request.form['population']
        statedetails.area = request.form['area']
        statedetails.density = request.form['density']
        session.add(statedetails)
        session.commit()
        flash("distict Edited Successfully")
        return redirect(url_for('showstates', sid=sid))
    else:
        return render_template(
            'editdistict.html',
            sid=sid, statedetails=statedetails, tss_det=tss_det)


# Delte district Edit
@app.route('/StatesStore/<int:sid>/<string:dname>/delete',
           methods=['GET', 'POST'])
def deletedistrict(sid, dname):
    sd = session.query(States).filter_by(id=sid).one()
    statedetails = session.query(StatesName).filter_by(district=dname).one()
    creator = getUserInfo(sd.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this states"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showstates', sid=sd.id))
    if request.method == "POST":
        session.delete(statedetails)
        session.commit()
        flash("Deleted distict Successfully")
        return redirect(url_for('showstates', sid=sid))
    else:
        return render_template(
            'deletedistict.html',
            sid=sid, statedetails=statedetails, tss_det=tss_det)
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={
                      'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Json

@app.route('/states/JSON')
def allStatesJSON():
    states = session.query(States).all()
    category_dict = [c.serialize for c in states]
    for c in range(len(category_dict)):
        names = [i.serialize for i in session.query(
                 StatesName).filter_by(
                     statesid=category_dict[c]["id"]).all()]
        if names:
            category_dict[c]["name"] = names
            return jsonify(States=category_dict)


@app.route('/States/states/JSON')
def categoriesJSON():
    names = session.query(States).all()
    return jsonify(states=[c.serialize for c in names])


@app.route('/States/name/JSON')
def itemsJSON():
    items = session.query(StatesName).all()
    return jsonify(states=[i.serialize for i in items])


@app.route('/States/<path:state_name>/names/JSON')
def categoryItemsJSON(state_name):
    states1 = session.query(States).filter_by(name=state_name).one()
    names = session.query(StatesName).filter_by(states=states1).all()
    return jsonify(stateEdtion=[i.serialize for i in names])


@app.route('/States/<path:state_name>/<path:edition_name>/JSON')
def ItemJSON(state_name, edition_name):
    states1 = session.query(States).filter_by(name=state_name).one()
    stateEdition = session.query(StatesName).filter_by(
           district=edition_name, states=states1).one()
    return jsonify(stateEdition=[stateEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=4444)
