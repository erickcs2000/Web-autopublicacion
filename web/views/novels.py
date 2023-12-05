from flask import Blueprint, app, jsonify, make_response, render_template, request, redirect, url_for, session, abort, flash, current_app
from sqlalchemy import func
from models import db, Novels, Categories, Tags, Users, Chapters, Followers, ReadLater, LikeNovel, Libraries, LibraryNovel
from werkzeug.utils import secure_filename
import os

from models.readfiles import extract_text_from_docx, extract_text_from_pdf


novels_blueprint = Blueprint('novels', __name__)

@novels_blueprint.route('/create', methods=['GET', 'POST'])
def create_novel():
    if request.method == 'POST':
        title = request.form['title']
        synopsis = request.form['synopsis']

        category_names = request.form.getlist('category')  

        tag_objects = []
        tags = request.form['tags']
        tag_names = tags.split(',')

        for tag_name in tag_names:
            tag = Tags.query.filter_by(name=tag_name.strip()).first()
            if tag is None:
                tag = Tags(name=tag_name.strip())
                db.session.add(tag)

            tag_objects.append(tag)

        category_objects = [Categories.query.filter_by(name=category_name).first() for category_name in category_names]

        db.session.commit()
        cover = request.files['cover']
        filename = secure_filename(cover.filename)        

        novel = Novels(title=title, synopsis=synopsis, categories=category_objects, tags=tag_objects, cover=filename, author_id=session['user_id'])
        db.session.add(novel)
        db.session.commit()
        novel_id = novel.id

        novel_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(novel_id))
        if not os.path.exists(novel_folder):
            os.makedirs(novel_folder)

        cover = request.files['cover']
        filename = secure_filename(cover.filename)
        cover.save(os.path.join(novel_folder, filename))

        cover_route = os.path.join(str(novel_id), filename)
        novel.cover = "uploads/" + cover_route.replace("\\", "/")
        novel.likes = 0
        novel.followers = 0
        novel.rating = 0
        novel.views = 0
        print(novel.cover)
        db.session.commit()

        
        return redirect(url_for('home'))
    resp = make_response(render_template('create.html', is_authenticated=('username' in session)))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    return resp

@novels_blueprint.route('/signout')
def signout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@novels_blueprint.route('/novel/<int:novel_id>')
def view_novel(novel_id):
    novel = Novels.query.get(novel_id)
    if novel is None:
        abort(404)
    novel.views += 1
    novel.followers = Followers.query.filter_by(novel_id=novel.id).count()
    if 'username' in session:
        user = Users.query.filter_by(username=session['username']).first()
        is_following = Followers.query.filter_by(user_id=user.id, novel_id=novel.id).first() is not None
        is_read_later = ReadLater.query.filter_by(user_id=user.id, novel_id=novel.id).first() is not None
        is_liked = LikeNovel.query.filter_by(user_id=user.id, novel_id=novel.id).first() is not None

    else:
        is_following = False
        is_read_later = False
        is_liked = False
    chapters = Chapters.query.filter_by(novel_id=novel_id).order_by(Chapters.number_chapter).all()
    db.session.commit()

    cover_path = os.path.join('uploads', novel.cover)
    print(novel.followers)
    return render_template('novel.html', novel=novel, is_following=is_following, is_read_later=is_read_later, is_liked=is_liked, chapters=chapters)

@novels_blueprint.route('/follow_novel/<novel_id>', methods=['POST'])
def follow_novel(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user and novel:
        novel.followers += 1

        follower = Followers(user_id=user.id, novel_id=novel.id)
        db.session.add(follower)

        db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))

@novels_blueprint.route('/unfollow_novel/<int:novel_id>', methods=['POST'])
def unfollow_novel(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user is None or novel is None:
        abort(404)

    follower = Followers.query.filter_by(user_id=user.id, novel_id=novel.id).first()
    if follower is None:
        abort(404)

    db.session.delete(follower)
    db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))
@novels_blueprint.route('/add_read_later/<novel_id>', methods=['POST'])
def add_read_later(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user and novel:
        read_later = ReadLater(user_id=user.id, novel_id=novel.id)
        db.session.add(read_later)
        db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))

@novels_blueprint.route('/remove_read_later/<int:novel_id>', methods=['POST'])
def remove_read_later(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user is None or novel is None:
        abort(404)

    read_later = ReadLater.query.filter_by(user_id=user.id, novel_id=novel.id).first()
    if read_later is None:
        abort(404)

    db.session.delete(read_later)
    db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))


@novels_blueprint.route('/like_novel/<novel_id>', methods=['POST'])
def like_novel(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user and novel:
        novel.likes += 1  
        like_novel = LikeNovel(user_id=user.id, novel_id=novel.id)
        db.session.add(like_novel)
        db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))

@novels_blueprint.route('/unlike_novel/<int:novel_id>', methods=['POST'])
def unlike_novel(novel_id):
    user = Users.query.filter_by(username=session['username']).first()
    novel = Novels.query.get(novel_id)

    if user is None or novel is None:
        abort(404)

    like_novel = LikeNovel.query.filter_by(user_id=user.id, novel_id=novel.id).first()
    if like_novel is None:
        abort(404)

    novel.likes -= 1  
    db.session.delete(like_novel)
    db.session.commit()

    return redirect(url_for('novels.view_novel', novel_id=novel_id))

@novels_blueprint.route('/create_library', methods=['POST'])
def create_library():
    user = Users.query.filter_by(username=session['username']).first()
    library_name = request.form.get('library_name')

    new_library = Libraries(name=library_name, user_id=user.id)
    db.session.add(new_library)
    db.session.commit()
    
    return jsonify({'message': 'Library created successfully', 'library_id': new_library.id})



@novels_blueprint.route('/novel/<int:novel_id>/libraries', methods=['GET'])
def get_novel_libraries(novel_id):
    user_id = session.get('user_id')
    libraries = Libraries.query.filter_by(user_id=user_id).all()
    libraries_data = [{'id': lib.id, 'name': lib.name} for lib in libraries]
    return jsonify({'libraries': libraries_data})

@novels_blueprint.route('/novel/<int:novel_id>/add_to_library/<int:library_id>', methods=['POST'])
def add_novel_to_library(novel_id, library_id):
    try:
        existing_relation = LibraryNovel.query.filter_by(novel_id=novel_id, library_id=library_id).first()
        if existing_relation:
            return jsonify({'message': 'The novel is already in the library'}), 400
        
        new_relation = LibraryNovel(library_id=library_id, novel_id=novel_id)
        db.session.add(new_relation)
        db.session.commit()
        return jsonify({'message': 'Novel added to library successfully'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@novels_blueprint.route('/novel/<int:novel_id>/add_chapter')
def add_chapter(novel_id):
    novel = Novels.query.get(novel_id)
    total_chapters = db.session.query(func.count(Chapters.id)).filter(Chapters.novel_id == novel_id).scalar()
    return render_template('add_chapter.html', novel=novel, total_chapters=total_chapters)

@novels_blueprint.route('/novel/<int:novel_id>/save_chapter', methods=['POST'])
def save_chapter(novel_id):
    title = request.form.get('title')
    text = request.form.get('content')
    file = request.files.get('file')
    chapter_num = request.form.get('chapter_num')
    if (text and file) or (not text and not file):
        flash('Por favor, introduce contenido en el editor o sube un archivo, pero no ambas cosas.')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        _, ext = os.path.splitext(filename)
        if ext.lower() == '.pdf':
            text = extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif ext.lower() in ['.doc', '.docx']:
            text = extract_text_from_docx(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif ext.lower() == '.txt':
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                text = f.read()
        else:
            flash('Formato de archivo no permitido. Solo se aceptan PDF, DOC/DOCX, TXT.')
            return redirect(request.url)
    print(chapter_num)
    chapter = Chapters(title=title, text=text, novel_id = novel_id, number_chapter=chapter_num)
    db.session.add(chapter)
    db.session.commit()

    flash('Capítulo guardado correctamente.')
    return redirect(url_for('novels.chapter', novel_id=novel_id, number_chapter=chapter.number_chapter, ))

@novels_blueprint.route('/novel/<int:novel_id>/chapter/<int:number_chapter>', methods=['GET'])
def chapter(novel_id, number_chapter):
    chapter = Chapters.query.filter_by(novel_id=novel_id, number_chapter=number_chapter).first()
    if not chapter:
        abort(404)
    novel = Novels.query.get(novel_id)
    next_chapter = Chapters.query.filter_by(novel_id=novel_id, number_chapter=number_chapter + 1).first()
    prev_chapter = Chapters.query.filter_by(novel_id=novel_id, number_chapter=number_chapter - 1).first() if number_chapter > 1 else None
    all_chapters = Chapters.query.filter_by(novel_id=novel_id).order_by(Chapters.number_chapter).all()
    return render_template('chapter.html', chapter=chapter, next_chapter=next_chapter, prev_chapter=prev_chapter, all_chapters = all_chapters, novel_title = novel.title)