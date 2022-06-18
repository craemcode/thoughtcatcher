from ensurepip import bootstrap
from flask import Flask, redirect, render_template, request, session, flash
from model import db,Todo,User,Topic,Thought
from flask_bootstrap import Bootstrap
from forms import UserForm, ThoughtForm
import time

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
        flash("Name successfully submitted")
        
        #check if user 
        user = User.query.filter_by(name=form.name.data).first()
        
        if user is None:
            #session['known'] = False
            nu_user = User(name=form.name.data)
            db.session.add(nu_user)
            db.session.commit()
            
            new_user = User.query.filter_by(name=form.name.data).first()
            session['id'] = new_user.id
            session['name'] = new_user.name
            flash('You have been registered!')
            form.name.data = ''
            return redirect('/add_thought')
            

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
    
    
    return render_template('thoughts.html', 
                                form2=form2,
                                name=session.get('name'))                                        

#I need a special function to handle the insertion of a new topic
# this is to avoid the problem that comes with doing two queries at once.

#New route. We want to show the user their thoughts. We will need about
#three queries. But we'll manage.

@app.route('/display_thoughts', methods=['GET'])
def get_thoughts():
    topics= None
    thought=None
    entrees= []
    

    topics= Topic.query.filter_by(user_id=session.get('id')).all()

    for topic in topics:
        topic_date=topic.date_created
        format_date=topic_date.strftime("%Y-%m-%d %H:%M")
        data = (topic.name, format_date)
        entrees.append(data)

    

    


    return render_template('display.html', entrees=entrees, name=session.get('name'))






@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an accident'

@app.route('/update/<int:id>',methods = ['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "An accident happened"
    else:
        return render_template('update.html', task=task)
    


if __name__ == "__main__":
    app.run(debug=True)
