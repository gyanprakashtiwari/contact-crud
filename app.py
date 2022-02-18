from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fxdxgpuikiuvkm:b75b4d4b1e8fc07ffb5e5edbaaebeff9bfbb9acba4f48ae9387fdeca803b35ca@ec2-44-192-245-97.compute-1.amazonaws.com:5432/ddv7raue5vqncn"


app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    phone_no = db.Column(db.String(15),nullable = False)

    def __repr__(self) -> str :
        return f"{self.name} {self.email} {self.phone_no}"


@app.route("/",methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['input_email']
        phone_no = request.form['phone_no']
        user1 = User(name=name,email = email, phone_no = phone_no)
        db.session.add(user1)
        db.session.commit()

    allUsers = User.query.all()
    return render_template('index.html',allUsers = allUsers)



@app.route("/edit/<int:id>",methods = ['GET','POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['input_email']
        phone_no = request.form['phone_no']
        user = User.query.filter_by(id = id).first()
        user.name = name
        user.email = email
        user.phone_no = phone_no
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    user = User.query.filter_by(id = id).first()
    return render_template('edit.html',user = user)
    



@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id = id).first()
    db.session.delete(user)
    db.session.commit()      
    return redirect("/")


@app.route("/search/<s>",methods = ['POST'])
def search(s):
    s = request.form['input_s']

    users = User.query.filter(func.lower(User.name) == func.lower(s)).all()
    find = User.query.filter(func.lower(User.name) == func.lower(s)).first()
    if find is not None:
        return render_template('search_result.html',allUsers = users)
    else:
        users = User.query.filter(func.lower(User.email) == func.lower(s)).all()

        return render_template('search_result.html',allUsers = users)
    
 
        



if __name__ == '__main__':
    app.run(debug=True)


