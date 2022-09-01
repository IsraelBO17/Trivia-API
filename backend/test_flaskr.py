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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student",'localhost:5432', self.database_name
            )
        setup_db(self.app, self.database_path)
        self.new_question = {'question': "What is the name of Nigeria's President?",'answer':'Muhammadu Buhari','category':4,'difficulty':1}
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        """Test get_categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])


    def test_get_paginated_questions(self):
        """Test get_questions endpoint"""
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_get_paginated_questions_error(self):
        """Test get_questions endpoint for 404 error"""
        res = self.client().get('/questions?page=5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    # def test_delete_question(self):
    #     """Test delete_question endpoint"""
    #     res = self.client().delete('/questions/5')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['question_id'], 5)

    def test_create_question(self):
        """Test create_question endpoint"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])

    def test_search_question(self):
        """Test search_question endpoint"""
        res = self.client().post('/questions', json={'searchTerm':'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_search_question_error(self):
        """Test search_question endpoint for searhTerm not found"""
        res = self.client().post('/questions', json={'searchTerm':'whatergarri'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_get_category_question(self):
        """Test get_category_question endpoint"""
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_get_category_question_for_invalid_category(self):
        """Test get_category_question endpoint for invalid category"""
        res = self.client().get('/categories/15/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_play_quiz(self):
        """Test play_quiz endpoint"""
        res = self.client().post('/quizzes', json={'previous_questions':[5,9],'quiz_category': {'type': 'History', 'id': 4}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_play_quiz_for_error(self):
        """Test play_quiz endpoint for error"""
        res = self.client().post('/quizzes', json={'previous_questions':[2,4,6],'quiz_category': {'type': 'Entertainment', 'id': 5}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()