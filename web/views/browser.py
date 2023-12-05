
from flask import Blueprint, app, jsonify, make_response, render_template, request, redirect, url_for, session, abort, flash
from models import db, Novels, Categories, Tags, Users, Chapters, Followers, ReadLater, LikeNovel, Libraries, LibraryNovel, NovelCategory, NovelTag



browser_blueprint = Blueprint('browser', __name__)

@browser_blueprint.route('/browser')
def browser():
    query = request.args.get('query')
    tag_name = request.args.get('tag')
    category_id = request.args.get('category')
    pressed = request.args.get('pressed')
    print(tag_name)
    if query or tag_name or category_id:
        base_query = Novels.query

        if query:
            base_query = base_query.filter(
                Novels.title.like('%' + query + '%') | 
                Novels.synopsis.like('%' + query + '%')
            )

        if tag_name:
            tag = Tags.query.filter(Tags.name == tag_name).first()
            base_query = base_query.join(NovelTag).filter(NovelTag.tag_id == tag.id)

        if category_id:
            base_query = base_query.join(NovelCategory).filter(NovelCategory.category_id == category_id)

        searchResults = base_query.all()
        print(category_id)
        print(searchResults)

        return render_template('partials/search_results.html', results=searchResults)
    elif pressed:
        base_query = Novels.query
        searchResults = base_query.all()
        return render_template('partials/search_results.html', results=searchResults)
    else:
        categories = Categories.query.all()
        tags = Tags.query.all()
        return render_template('browser.html', categories=categories, tags=tags)