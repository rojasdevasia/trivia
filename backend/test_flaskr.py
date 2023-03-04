import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres/postgres".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question={
            'question':'Name the pink city of India',
            'answer':'Jaipur',
            'category': 'History',
            'difficulty':2
        }  

        self.testSearch="test";  
    
        self.quiz={
            'previous_questions':[1],
            'quiz_category':{
            'type':'Science',
            'id':'1'
            }
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Testcase for paginated questions

    def test_get_paginate_questions(self):
        response=self.client().get('/categories')
        data=json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['total_questions']))

    # Testcase for Get Categories

    def test_get_categories(self):
        response=self.client().get('/categories')
        data=json.loads(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["categories"])

    def test_get_categories_not_allowed(self):
        response= self.client().post('/categories')  
        data=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data["success"],False)
    
    # Testcase for create question
    def test_create_new_question(self):
        response=self.client().post('/question',json=self.new_question)
        data=json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        # Check if there is a value 'created' in response
        self.assertTrue(data['created'])
        # Check whether we are returning a list of questions
        self.assertTrue(len(data['questions']))

    # Testcase to check if 404 sent when requested beyond a valid page
    def test_404_sent_requesting_beyond_valid_page(self):
        # Including a json body but we will not be using that
        response=self.client() .get('/questions?page=100',json={'difficulty':1})
        data=json.loads(response.data)

        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Not Found')    

    # Testcase to delete question
    def test_delete_question(self):
        response=self.client().delete('/question/1')
        data=json.loads(response.data)
        question=Question.query.filter(Question.id==1).one_or_none()
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],1)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question,None)    

    def test_delete_question_not_found(self):
        response=self.client().delete('/question/131')
        data=json.loads(response.data)    
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)

    # Testcase for search end point
    def test_search(self):
        response=self.client().post('/questions',json=self.test_search)
        data=json.loads(response.data)  
        self.assertEqual(response.status_code,200)
        self.assertEqual(data['success'],True)

    def test_search_not_found(self):
        response=self.client().get('/questions',json=self.test_search)
        data=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(data['success'],False)

    # Testcase for getting questions based on category
    def test_questions_of_category(self):
        response=self.client().get('/categories/1/questions')
        data=json.loads(response.data)   
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])

    def test_questions_of_category_not_found(self):
        response=self.client().get('/categories/131/questions')
        data=json.loads(response.data)   
        self.assertEqual(response.status_code,404)
        self.assertEqual(data["success"],False)   

    # Testcase for /quizzes end point
    def test_quizzes(self):
        response=self.client().post('/quizzes',json=self.quiz)
        data=json.loads(response.data)   
        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])    

    def test_quizzes_not_found(self):
        response=self.client().post('/quizzes',json={'difficulty':1})
        data=json.loads(response.data)   
        self.assertEqual(response.status_code,404)
        self.assertEqual(data["success"],False)       

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()