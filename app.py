from ensurepip import bootstrap
from flask import Flask, redirect, render_template, request
from model import db,Todo
from flask_bootstrap import Bootstrap
from forms import UserForm

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
        name = form.name.data
        form.name.data = ''
        
    return render_template('index.html', form=form, name=name )

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
