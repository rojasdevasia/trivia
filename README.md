Project README - TRIVIA APP

API Reference

Getting Started:

Base URL : At present , this app can only be run locally and is not hsoted as a base URL.The backend app is hosted at the 
default http://127.0.0.1:5000/ 

Authentication: No authentication required

Error Handling:

Errors are returned as JSON objects in hte following format:
  return jsonify({
            'success':status,
            "error":error code,
            "message":"message"
        })    


End points:

GET /categories

Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

GET '/questions?page=${integer}'

Fetches a paginated set of questions, a total number of questions, all categories and current category string.
Request Arguments: page - integer
Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}

GET '/categories/${id}/questions'

Fetches questions for a cateogry specified by id request argument
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}

DELETE '/questions/${id}'

Deletes a specified question using the id of the question
Request Arguments: id - integer
Returns: Does not need to return anything besides the appropriate HTTP status code.

POST '/quizzes'

Sends a post request in order to get the next question
Request Body:
{
    'previous_questions': [1, 4, 20, 15]
    quiz_category': 'current category'
 }
Returns: a single new question object
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer',
        'difficulty': 5,
        'category': 4
    }
}

POST '/questions'

Sends a post request in order to add a new question
Request Body:
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3,
}
Returns: Does not return any new data

POST '/questions'

Sends a post request in order to search for a specific question by search term
Request Body:
{
    'searchTerm': 'this is the term the user is looking for'
}

Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer',
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}
