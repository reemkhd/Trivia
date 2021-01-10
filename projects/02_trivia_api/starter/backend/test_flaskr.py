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
        self.database_path = 'postgresql://reem@localhost:5432/trivia'
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
    def test_fail_get_all_questions(self):
        res = self.client().get('/question')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)


    def test_add_new_question(self):
        new_question = {
            'question': 'question2',
            'answer': 'answer1',
            'category': 3,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    def test_fail_add_new_question(self):
        new_question = {
            'question': 'question2',
            'answer': '',
            'category': 3,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
    

    def test_delete_question(self):
        res = self.client().delete('/questions/61')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])
    def test_fail_delete_question(self):
        res = self.client().delete('/questions/58')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
   
    
    def test_search_question(self):
        request_data = {'searchTerm': 'which'}
        res = self.client().post('/questions/search', data=json.dumps(request_data), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    def test_fail_search_question(self):
        request_data = {'searchTerm': 'which'}
        res = self.client().post('/questions', data=json.dumps(request_data), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)


    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    def test_fail_get_questions_by_category(self):
        res = self.client().get('/categories/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()