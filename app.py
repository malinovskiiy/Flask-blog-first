from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False, default='N/A')
    date = db.Column(db.String(100), default=datetime.today().strftime("%m/%d/%Y %H:%M"))

    def __repr__(self):
        return 'Blog post ' + str(self.id)


# Routes
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date).all()
    return render_template('index.html', posts=posts)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        # Construct post from form data
        post = Post(title=title, content=content, author=author)

        # Add to the database
        db.session.add(post)
        # Save database
        db.session.commit()

        return redirect('/')
    else:
        posts = Post.query.order_by(Post.date).all()
    return render_template('posts.html', posts=posts)


# Delete post
@app.route('/posts/delete/<int:id>')
def delete(id):
    # Get post by id
    post = Post.query.get_or_404(id)
    # Delete
    db.session.delete(post)
    # Save
    db.session.commit()

    return redirect('/')


# Edit post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    # Get post by id
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        # Edit data
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']

        # Save
        db.session.commit()

        return redirect('/')
    else:
        return render_template('edit.html', post=post)





if __name__ == '__main__':
    app.run(debug=True)

