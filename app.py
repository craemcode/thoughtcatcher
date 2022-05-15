from flask import Flask, redirect, render_template, request
from model import db,Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


#controller code

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an accident'
    else:
        tasks = Todo.query.order_by(Todo.date).all()
        
        return render_template('index.html', tasks=tasks )

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
