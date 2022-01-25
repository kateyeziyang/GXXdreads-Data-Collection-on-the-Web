"""
Main file for web app.
"""

from flask import Flask, request, render_template, Response, redirect
import json
import db_functions
app = Flask(__name__)


@app.route('/')
def index():
    """
    Place holder.
    :return: A placeholder page.
    """
    return render_template("form.html")
    # return 'Hi! Here is the main page.'


@app.route('/advance/<and_or>/<field>/<collection>', methods=['GET'])
def advance(and_or, field, collection):
    """
    APIs that supports arithmetic operations: And & OR
    :param and_or: "and" or "or"
    :param field: field name
    :param collection: collection name
    :return: json formatted response
    """
    # try: http://127.0.0.1:5000/advance/and/title/books?a=algorithm&b=program
    is_and = 1 if and_or == "and" else 0
    result = db_functions.advanced_search(request.args, is_and, field, collection)
    if result:
        return Response(json.dumps(result), mimetype='application/json')
    else:
        return "Sorry, nothing found!"


@app.route('/book', methods=['POST', 'DELETE'])
def book():
    """
    Support insert one book and delete one book.
    :return: json formatted response
    """
    if request.method == 'POST':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.add_entries(data, 0, "books")
        return "Finished"
    elif request.method == 'DELETE':
        db_functions.del_entries(request.args, "books")
        return "Finished"
    return "Nothing"


@app.route('/books', methods=['GET', 'PUT', 'POST'])
def books():
    """
    Support get filtered books, insert many book and update one book.
    :return: json formatted response
    """
    # try: http://127.0.0.1:5000/books/?title=computer
    if request.method == 'PUT':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.update_entries(data, request.args, "books")
        return "Finished"
    elif request.method == 'POST':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.add_entries(data, 1, "books")
        return "Finished"
    else:
        if request.args:
            result = db_functions.get_entries(request.args, "books")
            if result:
                return Response(json.dumps(result), mimetype='application/json')
            else:
                return "Sorry, nothing found!"
        else:
            result = db_functions.get_all_books("books")
            return render_template("table_template.html", my_dict=result)


@app.route('/new_book', methods=['POST'])
def new_book():
    """
    Get new book form here.
    :return: message
    """
    book_form = request.form
    new_dic = {"title": book_form['book_title'], "author": book_form["book_author"], "book_id": book_form["book_id"]}
    db_functions.add_entries(new_dic, 0, "books")
    return "Finished!"


@app.route('/search_book_id', methods=['POST'])
def search_book_id():
    """
    Redirect to book page
    :return: another page
    """
    new_url = "/book/"+request.form["search_book_id"]
    return redirect(new_url)


@app.route('/book/<book_id>', methods=['GET'])
def book_page(book_id):
    """
    The book page
    :return: a rendered html
    """
    new_dic = {"book_id": book_id}
    result = db_functions.get_entries(new_dic, "books")
    return render_template("table_template.html", my_dict=result)


@app.route('/delete_this_book', methods=['GET', 'POST'])
def delete_this_book():
    """
    Get delete form here.
    :return: message
    """
    new_dic = {"book_id": request.form["delete_book_id"]}
    db_functions.del_entries(new_dic, "books")
    return "Finished!"


@app.route('/update_this_book', methods=['GET', 'POST'])
def update_this_book():
    """
    Get update form here.
    :return: message
    """
    doc = {request.form["field_name"]: request.form["value_name"]}
    args = {"book_id": request.form["update_book_id"]}
    db_functions.update_entries(doc, args, "books")
    return "Finished!"


@app.route('/author', methods=['POST', 'DELETE'])
def author():
    """
    Support insert one author and delete one author.
    :return: json formatted response
    """
    if request.method == 'POST':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.add_entries(data, 0, "authors")
        return "Finished"
    elif request.method == 'DELETE':
        db_functions.del_entries(request.args, "authors")
        return "Finished"
    return "Nothing"


@app.route('/authors', methods=['GET', 'PUT', 'POST'])
def authors():
    """
    Support get filtered authors, insert many author and update one author.
    :return: json formatted response
    """
    if request.method == 'PUT':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.update_entries(data, request.args, "authors")
        return "Finished"
    elif request.method == 'POST':
        data = request.json
        if data is None:
            return Response(status=415)
        db_functions.add_entries(data, 1, "authors")
        return "Finished"
    else:
        if request.args:
            result = db_functions.get_entries(request.args, "authors")
            if result:
                return Response(json.dumps(result), mimetype='application/json')
            else:
                return "Sorry, nothing found!"
        else:
            result = db_functions.get_all_authors("authors")
            return render_template("table_template.html", my_dict=result)


@app.route('/new_author', methods=['POST'])
def new_author():
    """
    Get new author form here.
    :return: message
    """
    author_form = request.form
    new_dic = {"name": author_form['author_name'], "author_id": author_form["author_id"]}
    db_functions.add_entries(new_dic, 0, "authors")
    return "Finished!"


@app.route('/search_author_id', methods=['POST'])
def search_author_id():
    """
    Redirect to author page
    :return: another page
    """
    new_url = "/author/"+request.form["search_author_id"]
    return redirect(new_url)


@app.route('/author/<author_id>', methods=['GET'])
def author_page(author_id):
    """
    The author page
    :return: a rendered html
    """
    new_dic = {"author_id": author_id}
    result = db_functions.get_entries(new_dic, "authors")
    return render_template("table_template.html", my_dict=result)


@app.route('/delete_this_author', methods=['GET', 'POST'])
def delete_this_author():
    """
    Get delete form here.
    :return: message
    """
    new_dic = {"author_id": request.form["delete_author_id"]}
    db_functions.del_entries(new_dic, "authors")
    return "Finished!"


@app.route('/update_this_author', methods=['GET', 'POST'])
def update_this_author():
    """
    Get update form here.
    :return: message
    """
    doc = {request.form["author_field_name"]: request.form["author_value_name"]}
    args = {"author_id": request.form["update_author_id"]}
    db_functions.update_entries(doc, args, "authors")
    return "Finished!"


@app.route('/query/most-book-authors')
def most_book_author():
    """
    Find the author that has the most books stored in your database.
    :return: the page of that author
    """
    return render_template("table_template.html", my_dict=db_functions.get_most_similar_authors())


@app.route('/query/most-similar-books')
def most_similar_books():
    """
    Find the book that has the most similar books stored in your database.
    :return: the page of that book
    """
    return render_template("table_template.html", my_dict=db_functions.get_most_similar_books())


if __name__ == '__main__':
    app.debug = True
    app.run()
