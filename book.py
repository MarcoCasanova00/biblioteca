from flask import Blueprint, request, session
from bson import ObjectId
from db import db

book_bp = Blueprint("books", __name__)

@book_bp.route("/books", methods=["GET"])
def get_books():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Non autorizzato"}, 401

    books = list(db.books.find({"added_by": ObjectId(user_id)}))
    for b in books:
        b["_id"] = str(b["_id"])
        b["added_by"] = str(b["added_by"])
    return books

@book_bp.route("/books", methods=["POST"])
def add_book():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Non autorizzato"}, 401

    data = request.get_json()
    book = {
        "titolo": data.get("titolo"),
        "autore": data.get("autore"),
        "anno": data.get("anno"),
        "genere": data.get("genere"),
        "riassunto": data.get("riassunto"),
        "added_by": ObjectId(user_id),
        "valutazioni": []
    }
    result = db.books.insert_one(book)
    return {"message": "Libro aggiunto", "book_id": str(result.inserted_id)}

@book_bp.route("/books/<book_id>/rate", methods=["POST"])
def rate_book(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Non autorizzato"}, 401

    voto = request.get_json().get("voto")
    if not isinstance(voto, int) or not (1 <= voto <= 5):
        return {"error": "Voto non valido (1-5)"}, 400

    result = db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$push": {"valutazioni": {"utente": ObjectId(user_id), "voto": voto}}}
    )

    if result.matched_count == 0:
        return {"error": "Libro non trovato"}, 404

    return {"message": "Voto salvato"}
