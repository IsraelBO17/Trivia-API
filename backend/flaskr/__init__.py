import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_catagories = {}
        for category in categories:
            formatted_catagories[category.id] = category.type

        if len(formatted_catagories) == 0:
            abort(404)
        else:
            return jsonify({
                "categories" : formatted_catagories
            })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.category).all()
        formatted_questions = [question.format() for question in questions]
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        paginated_questions = formatted_questions[start:end]

        if len(paginated_questions) == 0:
            abort(404)
        else:
            try:
                categories = Category.query.order_by(Category.id).all()
                formatted_catagories = {}
                for category in categories:
                    formatted_catagories[category.id] = category.type
                
                currentCategory_id = paginated_questions[-1]['category']
                currentCategory = Category.query.filter(Category.id == currentCategory_id).one_or_none()

                return jsonify({
                    "questions": paginated_questions,
                    "totalQuestions": len(questions),
                    "categories": formatted_catagories,
                    "currentCategory": currentCategory.type
                })
            except:
                abort(500)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(422)
            else:
                question.delete()
                return jsonify({
                    "success": True,
                    "question_id": question_id,
                })
        except:
            abort(500)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def create_question():
        data = request.get_json()
        new_question_text = data.get("question", None)
        new_answer = data.get("answer", None)
        new_category = data.get("category", None)
        new_difficulty = data.get("difficulty", None)
        searchTerm = data.get("searchTerm", None)
    
        try:
            if searchTerm:
                searched_questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
                questions = [question.format() for question in searched_questions]
                currentCategory_id = questions[-1]['category']
                currentCategory = Category.query.filter(Category.id == currentCategory_id).one_or_none()
                
                return jsonify({
                    'questions': questions,
                    'totalQuestions': len(questions),
                    'currentCategory': currentCategory.type
                })
            else:
                new_question = Question(question=new_question_text,answer=new_answer,category=new_category,difficulty=new_difficulty)
                new_question.insert()

                return jsonify({
                    "success": True,
                    "created": new_question.id
                })
        except:
            abort(422)


    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # @app.route('/questions/search', methods=["POST"])
    # def search_question():
    #     searchTerm = request.get_json()['searchTerm']
    #     if searchTerm is None:
    #         abort(400)
    #     else:
    #         searched_questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()

    #         if len(searched_questions) > 0:
    #             questions = [question.format() for question in searched_questions]

    #             currentCategory_id = questions[-1]['category']
    #             currentCategory = Category.query.filter(Category.id == currentCategory_id).one_or_none()

    #             return jsonify({
    #                 'questions': questions,
    #                 'totalQuestions': len(questions),
    #                 'currentCategory': currentCategory.type
    #             })
    #         else:
    #             abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_category_question(category_id):
        try:
            # category = Category.query.filter(Category.id == category_id).one_or_none()
            # questions = Question.query.filter(Question.category == category_id).all()
            questions = Question.query.join('categories').filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]

            if len(formatted_questions) == 0:
                abort(404)
            else:
                return jsonify({
                    "questions": formatted_questions,
                    "totalQuestions": len(formatted_questions),
                    "currentCategory": category.type
                })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=["POST"])
    def play_quiz():
        try:
            previous_questions = request.get_json()['previous_questions']
            quiz_category = request.get_json()['quiz_category']

            category = Category.query.filter(Category.type == quiz_category).one_or_none()
            questions = Question.query.filter(Question.category == category.id).all()
            # questions = Question.query.join('categories').filter(Question.category == category_id).all()
            new_question = []

            for question in questions:
                if question.id in previous_questions:
                    continue
                else:
                    new_question.append(question)
                    break
            
            if len(new_question) > 0:
                return jsonify({
                    "question": new_question[0].format()
                })
        except:
            abort(422)
        
        
        



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def access_denied(error):
        return jsonify({
            "success" : False,
            "error" : 400,
            "message" : "Access Denied (Bad Request)"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success" : False,
            "error" : 404,
            "message" : "Resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success" : False,
            "error" : 422,
            "message" : "Unprocessable"
        }), 422
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success" : False,
            "error" : 500,
            "message" : "Internal Server Error"
        }), 500
    return app

