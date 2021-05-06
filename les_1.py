from flask import Flask, render_template,request, url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

myApp=Flask(__name__)
myApp.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///site.db'
db=SQLAlchemy(myApp)


class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(150), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    story = db.Column(db.Text , nullable=False)
    data_ = db.Column(db.DateTime, default=datetime.utcnow())
    def __repr__(self):
        return'Blog %r'%self.id
@myApp.route('/index')
@myApp.route('/')
def intex():
    notes = Blog.query.all()
    notes=notes[::-1]
    return render_template('index.html', notes=notes)

@myApp.route('/about', methods=['POST','GET'])
def about():
    if request.method=='POST':
        title=request.form['title']
        intro=request.form['intro']
        story=request.form['story']
        blog=Blog(title=title, intro=intro, story=story)
        try:
            db.session.add(blog)
            db.session.commit()
            return redirect("/")
        except:
            return 'error'
    else:
        return render_template('articles.html')

@myApp.route('/other')
def other():
        return render_template('about.html')

@myApp.route('/sign', methods=['POST','GET'])
def sign():
    if request.method=='POST':
        names=request.form['login']
        passes=request.form['password']
        return names,passes
    return render_template('sign_in.html')
@myApp.route('/post/<int:id>')
def det_post(id):
    lyubiy_object =Blog.query.get(id)
    return render_template("post.html",obj=lyubiy_object)

@myApp.route('/post/<int:id>/delete')
def delet(id):
    d_art=Blog.query.get_or_404(id)
    try:
        db.session.delete(d_art)
        db.session.commit()
        return redirect('/')
    except:
        return ('ПОМИЛКА!')

if __name__=='__main__':
    myApp.run(debug=True)

