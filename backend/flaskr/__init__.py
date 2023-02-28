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
    # CORS(app,resources={r"*" : {'origins': '*/api'}})
    CORS(app,resources={r"/" : {'origins': '*'}})

    #after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # GET Request - Fetches a dictionary of categories
    @app.route('/categories')
    def get_categories():
        try:
            data={}
            categories_list=Category.query.all()

            for category in categories_list:
                data[category.id]=category.type

            return jsonify({
                'success':True,
                'categories':data
            })
        except Exception as e:
            print(e)    

    #GET Request - Fetches a paginated set of questions, a total number of questions, all categories and current category string.    
    @app.route('/questions')
    def get_questions():
        try:
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
        except Exception as e:
            print(e)    


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
        except Exception as e:
            print(e)
            abort(422)

    # Create new question
    @app.route('/questions',methods=['POST'])
    @cross_origin()
    def create_question():
        body=request.get_json()
        new_question=body.get('question',None)
        new_answer=body.get('answer',None)
        new_category_id=body.get('category',None)
        new_difficulty_score=body.get('difficulty',None)

        try:
            question=Question(question=new_question,answer=new_answer,category=new_category_id,
                              difficulty=new_difficulty_score)
            question.insert()

            return jsonify({
                "success":True
            })

        except Exception as e:
            print(e)
            abort(422)    

    # Search
    @app.route('/questions',methods=['POST'])
    @cross_origin()
    def search():
        try:
            body=request.get_json()
            searchVal=body.get('searchTerm')
            print(searchVal)

            selection=Question.query.filter(Question.question.ilike('%'+searchVal+'%')).all()

            if len(selection) >0:
                current_questions=paginate_questions(request,selection)

                return jsonify({
                    'success':True,
                    'questions':current_questions,
                    'total_questions':len(selection),
                    'currentCategory':''
                })
        except Exception as e:
            print(e)
            abort(404)    

    # GET questions based on category
    @app.route('/categories/<int:id>/questions')
    def questions_of_category(id):
        try:
            selection=Question.query.filter_by(category=id).all()

            if len(selection) >0:
                current_questions=paginate_questions(request,selection)

                return jsonify({
                    'success':True,
                    'questions':current_questions,
                    'total_questions':len(selection),
                    'currentCategory':''
                })
        except Exception as e:
            print(e)
            abort(404)  

    # POST for quizzes
    @app.route('/quizzes',methods=['POST'])
    @cross_origin()
    def play_quiz():
        try:
            body=request.get_json()
            selection=[]
            previous_questions=body.get('previous_questions',None)
            quiz_category=body.get('quiz_category',None)

            # print(previous_questions)
            # print(quiz_category)

            # Selecting 'All'
            if quiz_category["id"] == 0:
                questions=Question.query.all()
            else:    
                questions=Question.query.filter_by(category=quiz_category["id"]).all()
            # print(questions)

            for question in questions:
                if question.id not in previous_questions:
                    selection.append(question)

            # print(selection)

            return jsonify({
                    'success':True,
                    'question':random.choice(selection).format()
                })
        except Exception as e:
            print(e)
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

