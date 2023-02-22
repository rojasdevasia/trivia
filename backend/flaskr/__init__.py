import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
    questions=[]
    page=request.args.get('page',1,type=int)
    start=(page-1) * QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE

    questions=[question.format() for question in selection]
    current_questions=questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
   
    # Set up CORS. Allow '*' for origins
    CORS(app,resources={r"*" : {'origins': '*/api'}})

    #after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # GET Request - Fetches a dictionary of categories
    @app.route('/categories')
    def get_categories():
        data={}
        categories_list=Category.query.all()

        for category in categories_list:
            data[category.id]=category.type

        return jsonify({
            'success':True,
            'categories':data
        })

    #GET Request - Fetches a paginated set of questions, a total number of questions, all categories and current category string.    
    @app.route('/questions')
    def get_questions():
        # Fetch all questions
        selection=Question.query.all()
        current_questions= paginate_questions(request,selection)

        if len(current_questions) == 0:
            abort(404)

        # Fetch all categories 
        data={}
        categories_list=Category.query.all()

        for category in categories_list:
            data[category.id]=category.type    

        return jsonify({
            'success':True,
            'questions':current_questions,
            'totalQuestions':len(current_questions),
            'categories':data,
            'currentCategory':""
        })    


    # DELETE question using a question ID
    @app.route('/question/<int:question_id>',methods=['DELETE'])
    def delete_question(question_id):
        try:
            question=Question.query.order_by(Question.id).all()

            if question is None:
                abort(404)

            question.delete()
            selection=Question.query.all()
            current_questions=paginate_questions(request,selection)

            return jsonify({
                'success':True,
                'deleted':question_id
            })
        except:
            abort(422)

    # Create new question
    @app.route('/questions',methods=['POST'])
    def create_new_question():
        body=request.get_json()
        new_question=body.get('question',None)
        new_answer=body.get('answer',None)
        new_category=body.get('category',None)
        new_difficulty_score=body.get('difficulty',None)

        try:
            question=Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty_score)
            question.insert()

            selection=Question.query.all()
            current_questions=paginate_questions(request,selection)
        except:
            abort(422)    

    # Search
    @app.route('/questions',methods=['POST'])
    def search():
        body=request.get_json()
        searchVal=body.get('searchTerm')
        selection=Question.query.filter(Question.question.ilike('%'+'searchVal'+'%')).all()

        if len(selection) >0:
            current_questions=paginate_questions(request,selection)

            return jsonify({
                'success':True,
                'questions':current_questions,
                'total_questions':len(selection),
                'currentCategory':''
            })
        else:
            abort(404)    

    # GET questions based on category
    @app.route('/categories/<int:id>/questions')
    def questions_of_category(id):
        selection=Question.query.filter_by(category=id)

        if len(selection) >0:
            current_questions=paginate_questions(request,selection)

            return jsonify({
                'success':True,
                'questions':current_questions,
                'total_questions':len(selection),
                'currentCategory':''
            })
        else:
            abort(404)  

    # POST for quizzes
    @app.route('/quizzes',methods=['POST'])
    def play_quiz():
        body=request.get_json()
        selection=[]
        previous_questions=body.get('previous_questions',None)
        quiz_category=body.get('quiz_category',None)

        questions=Question.query.filter_by(category=quiz_category)

        for question in questions:
            if question.id not in previous_questions:
                selection.append(question)

        if len(selection) >0:
            current_questions=paginate_questions(request,selection)

            return jsonify({
                'success':True,
                'questions':current_questions,
                'previousQuestion':""
            })
        else:
            abort(404)        

    # Error handler for 404
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success':True,
            "error":404,
            "message":"Not found"
        })

    # Error handler for 422
    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            'success':True,
            "error":422,
            "message":"Unsupported"
        })    

    return app

