import json
from flask import Blueprint, app, jsonify, make_response, render_template, request, redirect, url_for, session, abort, flash
from models import db, CategoryPost, Post, Response, Users, Novels, VotePost, VoteResponse, CategoryPostRelationship

forum_blueprint = Blueprint('forum', __name__)

@forum_blueprint.route('/forum')
def show_forum():
    categories = CategoryPost.query.all()
    recent_posts = Post.query.order_by(Post.id.desc()).limit(10) 
    return render_template('forum.html', categories=categories, recent_posts=recent_posts)

@forum_blueprint.route('/forum/post', methods=['POST'])
def create_post():
    if 'username' not in session:
        return redirect(url_for('login'))

    title = request.form.get('title')
    content = request.form.get('content')
    category_ids = json.loads(request.form.get('categories')) 
    novel_id = request.form.get('novelId')
    if novel_id:
        novel_id = int(novel_id)  
    else:
        novel_id = None  
    user = Users.query.filter_by(username=session['username']).first()

    new_post = Post(title=title, content=content, user_id=user.id, novel_id=novel_id)
    db.session.add(new_post)
    db.session.flush() 

    for category_id in category_ids:
        category_post_relation = CategoryPostRelationship(category_id=category_id, post_id=new_post.id)
        db.session.add(category_post_relation)

    db.session.commit()

    return redirect(url_for('forum.show_forum'))

def load_nested_responses(response):
    response.children = Response.query.filter_by(parent_id=response.id).all()
    for child_response in response.children:
        load_nested_responses(child_response)  

@forum_blueprint.route('/forum/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    responses = Response.query.filter_by(post_id=post.id, parent_id=None).all()

    for response in responses:
        load_nested_responses(response)

    return render_template('post_detail.html', post=post, responses=responses)


@forum_blueprint.route('/forum/response', methods=['POST'])
def post_response():
    user = Users.query.filter_by(username=session['username']).first()
    post_id = request.form.get('post_id')
    content = request.form.get('content')

    new_response = Response(content=content, user_id=user.id, post_id=post_id)
    db.session.add(new_response)
    db.session.commit()

    return redirect(url_for('view_post', post_id=post_id))

@forum_blueprint.route('/api/posts')
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).limit(10)  
    posts_data = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,  
        }
        posts_data.append(post_data)
    
    return jsonify(posts_data)

@forum_blueprint.route('/api/forum/categories')
def api_categories():
    categories = CategoryPost.query.all()
    categories_data = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(categories_data)

@forum_blueprint.route('/api/novels')
def api_novels():
    novels = Novels.query.all()
    novels_data = []
    for novel in novels:
        author = Users.query.get(novel.author_id)  
        author_name = author.username if author else 'Desconocido'  
        novel_data = {
            'id': novel.id,
            'title': novel.title,
            'author': author_name,
            'cover': novel.cover
        }
        novels_data.append(novel_data)
    return jsonify(novels_data)

@forum_blueprint.route('/api/vote/post/<int:post_id>', methods=['POST'])
def vote_post(post_id):
    user_id = Users.query.filter_by(username=session['username']).first()
    is_upvote = request.json.get('is_upvote')
    existing_vote = VotePost.query.filter_by(user_id=user_id, post_id=post_id).first()

    if existing_vote:
        existing_vote.is_upvote = is_upvote
    else:
        new_vote = VotePost(user_id=user_id, post_id=post_id, is_upvote=is_upvote)
        db.session.add(new_vote)

    db.session.commit()
    return jsonify({'message': 'Voto registrado'})

@forum_blueprint.route('/api/vote/response/<int:response_id>', methods=['POST'])
def vote_response(response_id):
    user_id = Users.query.filter_by(username=session['username']).first()
    is_upvote = request.json.get('is_upvote')
    existing_vote = VoteResponse.query.filter_by(user_id=user_id, response_id=response_id).first()

    if existing_vote:
        existing_vote.is_upvote = is_upvote
    else:
        new_vote = VoteResponse(user_id=user_id, response_id=response_id, is_upvote=is_upvote)
        db.session.add(new_vote)

    db.session.commit()
    return jsonify({'message': 'Voto registrado'})

@forum_blueprint.route('/api/respond', methods=['POST'])
def respond():
    user  = Users.query.filter_by(username=session['username']).first()
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    data = request.get_json()
    content = data.get('content')
    post_id = data.get('post_id', None)
    parent_id = data.get('parent_id', None)

    new_response = Response(content=content, user_id=user.id, post_id=post_id, parent_id=parent_id)
    db.session.add(new_response)
    db.session.commit()
    print(new_response.id)
    return jsonify({'message': 'Respuesta registrada', 'username': user.username, 'response_id': new_response.id})
