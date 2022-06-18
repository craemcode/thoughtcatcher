from ensurepip import bootstrap
from flask import Flask, redirect, render_template, request, session, flash
from model import db,Todo,User,Topic,Thought
from flask_bootstrap import Bootstrap
from forms import UserForm, ThoughtForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SECRET_KEY'] = 'JABAWABA2'
db.init_app(app)
bootstrap = Bootstrap(app)


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
        #flash("Name successfully submitted")
        #beat the redirect
        
        user = User.query.filter_by(name=form.name.data).first()
        
        if user is None:
            #session['known'] = False
            flash('unkown user')
            session['name'] = form.name.data
            form.name.data = ''
            return redirect('/')
            
        else:
            #session['known'] = True
            session['id'] = user.id
            session['name'] = form.name.data
            form.name.data = ''
            return redirect('/add_thought')
                 
    else:
        pass
        #fix this my niggar

    
    
    return render_template('index.html', 
                            form1=form,
                            name=session.get('name'),
                            #known=session.get('known', False)
                            )

@app.route('/add_thought',methods=['POST','GET'])
def add_thought():

    topic = None
    thought = None
    form2 = ThoughtForm()    
    
    #If new topic, add topic to db, then get id...if old topic just add straight
    
    if form2.validate_on_submit():
       topic = Topic.query.filter_by(name=form2.topic.data).first()
       if topic is None:
           topic = Topic(name=form2.topic.data, user_id=session.get['id'])
           db.session.add(topic)
           db.session.commit()
           flash('new topic added')

           thought = Thought(name=form2.thought.data, topic_id=topic.id)
           db.session.add(thought)
           db.session.commit()
           flash('thought successfully added')
       else:
            thought = Thought(name=form2.thought.data, topic_id=topic.id)
            flash('thought successfully added')
    else:
        pass
    
    
    return render_template('thoughts.html', 
                                form2=form2,
                                name=session.get('name'))                                        






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
