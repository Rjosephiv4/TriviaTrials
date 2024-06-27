from dotenv import load_dotenv
import os
import json
from openai import OpenAI


def triviaCreator():
    # Load environment variables from the .env file
    load_dotenv()

    # Get the OpenAI API key from the environment variables
    API_KEY = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI client
    client = OpenAI(api_key=API_KEY)

    # Define the prompt

    introToPrompt = """
    Generate a JSON array containing exactly 20 trivia questions. Each question should be formatted as a JSON object with the following structure: THE LIST OF OBJECTS MUST BE NAMED questions

    ```json
    questions[ 
    {
    "question": "Question text here?",
    "correct": "Correct answer here",
    "incorrect1": "First incorrect answer",
    "incorrect2": "Second incorrect answer",
    "incorrect3": "Third incorrect answer"
    }
    ]
    
    Ensure there are exactly 20 questions in total.
    The questions should be categorized into 5 very easy, 5 pretty easy, 5 medium difficulty, and 5 hard. Do not specify the difficulty level within the JSON objects.
    Shuffle the order of the questions randomly.
    Avoid questions about specific dates.
    Focus on questions related to people (e.g., identities, professions, roles in movies/shows/historical positions) and events (e.g., occurrences, notable figures).
    Each question should be between 80 and 150 characters in length.
    Each answer should be no longer than 23 characters.
    Ensure all questions are unique and do not share similar themes, subjects, or contexts.
    Example JSON format for a question:
    json
    {
    "question": "What is the capital city of France?",
    "correct": "Paris",
    "incorrect1": "Berlin",
    "incorrect2": "Rome",
    "incorrect3": "London"
    }

    Please provide exactly 20 unique trivia questions based on the guidelines above. The longest any question can be is 77 characters. THe longest any answer can be is 30 chraacters. 

    You must use the information below as a starting point, but branch off of it. Don't repeat the same content in any question. THE MOST IMPORTANT PART OF THIS IS NO REPEPETION. YOU HAVE FAILED IF THERE IS A SIMILIAR ANSWER QUESTION OR ANYTHING OF THE SORT.

    """

    with open("output.txt", "r") as file:
        data = file.read()


    prompt = f"{introToPrompt}{data}"



    # Call the API
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You're only job is to provide the user with EXACTLY 20 UNIQUE Trivia Questions based on thier request. IN json"},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" },
        model="gpt-4o",
        max_tokens=4096,
        temperature=1
    )


    # Extract the content from the response
        # Extract the message content from the first choice
    response_message = response.choices[0].message.content

    try:
        trivia_questions = json.loads(response_message)
        
        # Define the file path
        file_path = 'trivia_questions.json'
        
        # Write the trivia questions to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(trivia_questions, json_file, indent=4)
        
        print(f"Trivia questions have been written to {file_path}")

    except json.JSONDecodeError:
        print("Error decoding JSON response")