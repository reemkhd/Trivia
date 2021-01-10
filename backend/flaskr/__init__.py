import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import re 
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  #set up CORS
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  def pagination(request, questions):
    #get current page
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    #take the format of questions
    formatted_questions = [question.format() for question in questions]
    #make the questions in pages
    current_question = formatted_questions[start:end]
    return current_question


  #endpoint to handle GET requests for all available categories.
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    #get all categories
    categories = Category.query.all()
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in categories}
    })


  #endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    #get all questions
    questions = [question for question in Question.query.all()]
    #make them in pages
    current_paging = pagination(request, questions)
    #get all categories
    categories = Category.query.all()
    return jsonify({
      'success': True,
      'questions': current_paging,
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories}
    })
 

  #endpoint to DELETE question using a question ID.
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = False
    #get the question from the id
    question = Question.query.get(question_id)
    all_questions = Question.query.all()
    if question in all_questions:
      try:
        question.delete()
      except:
        error = True
    else:
      abort(404)
    return jsonify({
      'success': True,
      'deleted': question_id
    })
    
  
  #endpoint to POST a new question, 
  @app.route('/questions', methods=['POST'])
  def add_question():
    #get the question data
    question = request.json.get('question')
    answer = request.json.get('answer')
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')
    #if the data not complate, make error
    if not (question and answer and category and difficulty):
      return abort(400)
    #add the question to the table
    full_question = Question(question, answer, category, difficulty)
    full_question.insert()
    return jsonify({
      'success': True,
      'question': full_question.format()
    })

 
  #POST endpoint to get questions based on a search term.
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    #get the search term
    search_term = request.json.get('searchTerm', '')
    #ilike to be insensitive case, and % any leters before or after the search term
    all_questions = Question.query.filter(Question.question.ilike("%" + search_term + "%")).all()
    questions = [question.format() for question in all_questions]
    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(questions)
    })

  
  #GET endpoint to get questions based on category.
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_question_by_category(category_id):
    #get all question that involved to the given category
    questions =  Question.query.filter(Question.category==category_id)
    current_pagination = pagination(request, questions)
    return jsonify({
      'success': True,
      'questions': current_pagination,
      'total_questions': len(current_pagination)
    })
    

  #POST endpoint to get questions to play the quiz. 
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    #get previous questions & current category
    previous_questions = request.json.get('previous_questions')
    current_category = request.json.get('quiz_category')
    #get the id of the category
    category_id = current_category.get('id')
    #if the user choose 'All'
    if category_id == 0:
      questions = Question.query.all()
      #get the questions randomly
      question = random.choice(questions)
      return jsonify({
        'success': True,
        'question': question.format(),
        'previousQuestions': []
      })
    else:
      #if the user choose specific category, return just questions in same category & not repeat the previous questions
      questions = Question.query.filter(Question.category == category_id,~Question.id.in_(previous_questions)).all()
      #get the questions randomly
      question = random.choice(questions)      
      return jsonify({
        'success': True,
        'question': question.format(),
        'previousQuestions': []
      })    


  #error handlers for all expected errors 
  @app.errorhandler(400)
  def bad_request_error(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404

  @app.errorhandler(405)
  def not_allowed_error(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable_error(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

  return app

    