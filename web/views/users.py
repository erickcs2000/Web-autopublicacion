from flask import Blueprint, app, jsonify, make_response, render_template, request, redirect, url_for, session, abort, flash
from sqlalchemy import func
from models import db, Users, Novels, Followers, ReadLater, LikeNovel
from werkzeug.utils import secure_filename
import os
import base64
from flask import current_app as app
from PIL import Image
import io


users_blueprint = Blueprint('users', __name__)

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size

    if width > height:
        left = (width - height) / 2
        top = 0
        right = (width + height) / 2
        bottom = height
    else:
        left = 0
        top = (height - width) / 2
        right = width
        bottom = (height + width) / 2

    cropped_image = original_image.crop((left, top, right, bottom))

    resized_image = cropped_image.resize((size, size), Image.ANTIALIAS)
    resized_image.save(output_image_path)


@users_blueprint.route('/user/<id>', methods=['GET', 'POST'])
def user(id):
    user = Users.query.filter_by(id=id).first_or_404()

    own_novels_ids_tuples = db.session.query(Novels.id).filter_by(author_id=user.id).all()
    own_novels_ids = [id_tuple[0] for id_tuple in own_novels_ids_tuples]
    own_novels = Novels.query.filter(Novels.id.in_(own_novels_ids)).all()

    followed_novels_ids_tuples = db.session.query(Followers.novel_id).filter_by(user_id=user.id).all()
    followed_novels_ids = [id_tuple[0] for id_tuple in followed_novels_ids_tuples]
    followed_novels = Novels.query.filter(Novels.id.in_(followed_novels_ids)).all()

    readlater_novels_ids_tuples = db.session.query(ReadLater.novel_id).filter_by(user_id=user.id).all()
    readlater_novels_ids = [id_tuple[0] for id_tuple in readlater_novels_ids_tuples]
    readlater_novels = Novels.query.filter(Novels.id.in_(readlater_novels_ids)).all()

    liked_novel_ids_tuples = db.session.query(LikeNovel.novel_id).filter_by(user_id=user.id).all()
    liked_novel_novels_ids = [id_tuple[0] for id_tuple in liked_novel_ids_tuples]
    liked_novel_novels = Novels.query.filter(Novels.id.in_(liked_novel_novels_ids)).all()
    return render_template('user.html', user=user, own_novels=own_novels, followed_novels=followed_novels, readlater_novels=readlater_novels, liked_novel_novels=liked_novel_novels)

@users_blueprint.route('/user/<id>/update_profile', methods=['POST'])
def update_profile(id):
    data = request.get_json()
    user = Users.query.filter_by(id=id).first()
    bg_color = data.get('bg_color')
    image_profile64 = data.get('image')
    new_username = data.get('username')
    description = data.get('description')
    if new_username:
        user.username = new_username

    if image_profile64:
        image_profile = base64.b64decode(image_profile64)
        image = Image.open(io.BytesIO(image_profile))
        filename = secure_filename(f"{id}_profile_pic.png")

        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'users', str(user.id))
        os.makedirs(user_dir, exist_ok=True)

        filepath = os.path.join(user_dir, filename)
        image.save(filepath)
        # Añadir aquí el código para redimensionar la imagen
        resized_filepath = os.path.join(user_dir, filename)
        resize_image(filepath, resized_filepath, 200)
        print(resized_filepath)
        user.image_profile = filepath
    if bg_color:
        user.bg_color = bg_color
    
    if description:
        user.description = description
    db.session.flush()
    db.session.commit()
    flash('Profile updated successfully', 'success')
    session['username'] = user.username
    return redirect(url_for('users.user', id=user.id))


