from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.now())

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/',methods=['GET','POST'])
def firstPage():
    if request.method == 'POST':
        title = request.form['title'].lstrip()
        desc = request.form['desc'].lstrip()
        if title=="" or desc=="":
            return redirect('/')
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    allTodo = Todo.query.all()
    return render_template('index.html',todoList=allTodo)

@app.route('/update/<int:sno>',methods=['GET','POST'])
def updateData(sno):
    if request.method == 'POST':
        title = request.form['title'].lstrip()
        desc = request.form['desc'].lstrip()
        if title=="" or desc=="":
            return redirect('/')
        updateTodo = Todo.query.filter_by(sno=sno).first()
        updateTodo.title = title
        updateTodo.desc = desc
        db.session.add(updateTodo)
        db.session.commit()
        return redirect('/')
    updateTodo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=updateTodo)


@app.route('/delete/<int:sno>')
def deleteData(sno):
    delTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delTodo)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)