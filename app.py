from ensurepip import bootstrap
from flask import Flask, redirect, render_template, request, session, flash, url_for
from model import db,Todo,User,Topic,Thought
from flask_bootstrap import Bootstrap
from forms import UserForm, ThoughtForm
from sqlalchemy import desc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SECRET_KEY'] = 'JABAWABA2'
db.init_app(app)
bootstrap = Bootstrap(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Topic=Topic, Thought=Thought)

#controller code

#EPIPHANY: Create the route that the client will hit. Intercept their request. 
# if get:
#   do something
#   render template with requested data (In whatever format)
# else (if post):
#   do something
#   redirect to page
#
#
#
#
#
#
#
@app.route('/', methods = ['POST','GET'])

def index():
    
    name = None
    form = UserForm()
    
    if form.validate_on_submit():

        
        #check if user 
        user = User.query.filter_by(name=form.name.data).first()
        
        if user is None:
            """no new users
            #session['known'] = False
            nu_user = User(name=form.name.data)
            db.session.add(nu_user)
            db.session.commit()
            
            new_user = User.query.filter_by(name=form.name.data).first()
            session['id'] = new_user.id
            session['name'] = new_user.name
            """
            flash('Access Denied!')
            form.name.data = ''
            return redirect('/')
            

        else:
            #session['known'] = True
            #useful for adding topics in the /add_thought
            session['id'] = user.id
            session['name'] = user.name
            form.name.data = ''
            return redirect('/add_thought')
                 
    else:
        session['name']= ''
        #we dont want dirty dishes in the cookie

    
    
    return render_template('index.html', 
                            form1=form,
                            name=session.get('name'),
                            #known=session.get('known', False)
                            )


#this route is for adding thoughts in db. Check models.py for relationships
@app.route('/add_thought',methods=['POST','GET'])
def add_thought():

    topic = None
    thought = None
    form2 = ThoughtForm()    
    
    #If new topic, add topic to db, then get id...if old topic just add straight
    
    if form2.validate_on_submit():
       
       topic = Topic.query.filter_by(name=form2.topic.data).first()
       if topic is None:
           topic = Topic(name=form2.topic.data, user_id=session.get('id'))
           db.session.add(topic)
           db.session.commit()
           
           flash('new topic added')

           nu_topic = Topic.query.filter_by(name=form2.topic.data).first()
           thought = Thought(content=form2.thought.data, topic_id=nu_topic.id)
           db.session.add(thought)
           db.session.commit()
           flash('thought successfully added')
           return redirect('/add_thought')
           
       else:
            thought = Thought(content=form2.thought.data, topic_id=topic.id)
            db.session.add(thought)
            db.session.commit()
            form2.thought.data = ''
            flash('thought successfully added')
            return redirect('/add_thought')
       
       
    else:
        pass
    
    
    return render_template('add_thoughts.html', 
                                form2=form2,
                                name=session.get('name'))                                        



#New route. We want to show the user their thoughts. We will need about
#three queries. But we'll manage.

@app.route('/display_topics', methods=['GET'])
def get_thoughts():
    topics= None

    id=session.get('id')

    topics = Topic.query.filter_by(user_id=id).all()
    topics.reverse()
    return render_template('topic_display.html', topics=topics, name=session.get('name'))


@app.route('/show_thoughts/<int:id>&<string:topic_name>')
def show_topic(id,topic_name):

    thoughts = Thought.query.filter_by(topic_id=id).all()
     
    return render_template('thought.html', thoughts=thoughts, topic_name=topic_name,name=session.get('name'))


@app.route('/delete_topic/<int:id>')
def delete_topic(id):

    thought = Topic.query.filter_by(id=id).first()
    db.session.delete(thought)
    db.session.commit()
    flash('thought successfully deleted')
    return redirect('/display_topics')

if __name__ == "__main__":
    app.run(debug=True)
