# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


### API Reference

**Getting Started**
- Base URL:The backend app is hosted at the default, `http://127.0.0.1:5000/`.

**Error Handling**
- Errors are returned as JSON objects in the following format:
  {
      "success": False, 
      "error": 400,
      "message": "bad request"
  }
- The API will return four error types when requests fail:

  400: Access Denied (Bad Request)
  404: Resource Not Found
  422: Unprocessable
  500: Internal Server Error

**Endpoints**

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
'categories': {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
```

`GET '/questions?page=<int>'`

- Fetches a dictionary of questions from the database, and then paginates it based on the value of the `page` query parameter passed with it.
- Request Arguments: None
- Returns: An object with keys `questions` that contains a list of paginated questions, `totalQuestions` that contains the total number of questions in the database, `categories` that contains the an object of `id: category_string` key: value pairs, and `currentCategory` that contains the category of the last question in the list of questions returned.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "Geography",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
  ]
}
```

`DELETE '/questions/<int:question_id>'`

- Deletes the question with the id of the given request argument.
- Request argument: `question_id`
- Returns: an object with keys `success` indicating if it was successfully deleted and `question_id`, the id of the question deleted.

```json
{
  "success":True,
  "question_id":2
}
```

`POST '/questions'`

- Creates a new question into the database.
- Request argument: None
- Returns: an object with keys `success` identifying if it was successfully created and `created`, the id of the newly created question.

```json
{
  "success": True,
  "created": 4
}
```

`POST '/questions/search'`

- Fetches a list of questions based on a search term,for whom the search term is a substring of the question. The search term is passed as json data with the request.
- Request argument: None
- Returns: an object with keys `questions` that contains a list of questions for whom the search term is a substring of the question, `total_questions` that contains the number of questions that met the search term, and `current_category` that contains the category of the last question in the list of questions returned.

```json
{
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
  ],
  "total_questions": 2,
  "current_category": "Geography"
}
```

`GET '/categories/<int:category_id>/questions'`

- Fetches a list of questions based on catgory.
- Request argument: `category_id`
- Returns: an object with keys `questions` that contains alist of questions for the specified category, `totalQuestions` that contains the total number of questions in the specified category, `currentCategory` that contains the category of the last question in the list of questions returned.

```json
{
  "questions":  [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
  ],
  "totalQuestions": 10,
  "currentCategory": "Geography"
}
```

`POST '/quizzes'`

- Fetches a random question within the given category that has not been already answered.
- Request arguments: None
- Returns: an object with a single key `question` that contains a question object.

```json
{
  "question": {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
}
```