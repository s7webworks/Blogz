
from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:simplepassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    btitle = db.Column(db.String(120))
    bpost = db.Column(db.String(400))
    
    def __init__(self, btitle, bpost):
        self.btitle = btitle
        self.bpost = bpost

@app.route('/newpost', methods=['GET', 'POST'])
def newpost(): 
    
    blogs = Blog.query.all()
    
    if request.method == 'POST':
        new_btitle = request.form['new_btitle']
        new_bpost = request.form['new_bpost']
        new_blog = Blog(new_btitle, new_bpost)
        db.session.add(new_blog)
        db.session.commit()
        return redirect("/")
        
    return render_template("newpost.html", blogs=blogs)

        

    
    

@app.route('/blog')
def blog():
    blog_id = request.args.get('blog_id')
    

    if blog_id != None:
        blog_id = int(blog_id)
        blogs = Blog.query.get(blog_id)
        return render_template('single.html', blogs=blogs)

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs )


@app.route('/', methods=['GET', 'POST'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)



if __name__ == '__main__':  
    app.run()