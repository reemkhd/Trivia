import os
import unittest
import json
from flaskr import create_app
from models import setup_db, Question, Category


class QuestionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://reem@localhost:5432/trivia'
        setup_db(self.app, self.database_path)
        self.search_term = 'reem'
        self.new_question = {
            'question': 'question1',
            'answer': 'answer1',
            'category': 3,
            'difficulty': 2
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
    '''
    def test_delete_question(self):
        res = self.client().delete('/questions/34')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted'])

    
    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
    '''
    
    def test_fail_delete_question(self):
        res = self.client().delete('/questions/7088')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
    
    def test_search_question(self):
        request_data = {'searchTerm': 'which'}
        res = self.client().post('/questions/search', data=json.dumps(request_data), content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    def test_play_quiz(self):
        res = self.client().post('/quizzes', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')
    
    '''
    def test_update_plant_primary_color(self):
        res = self.client().patch('/plants/2', json={'primary_color':'blue'})
        data = json.loads(res.data)
        plant = Plants.query.filter(Plants.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(plant.format()['primary_color'], 'blue')

    def test_400_for_failed_update(self):
        res = self.client().patch('/plants/5')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_plant(self):
        res = self.client().delete('/plants/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_fail_delete_plant(self):
        res = self.client().delete('/plants/334')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    '''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()