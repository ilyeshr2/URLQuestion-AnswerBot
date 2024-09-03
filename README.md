# URL Question & Answer Bot

This project is a web application that allows users to enter a URL, then ask questions about the content of the page. The application scrapes the content of the URL, processes it to create embeddings, and then stores these embeddings in Pinecone. Users can interact with the bot via a chat interface to get answers to their questions based on the content of the scraped URL.


![urlgif2](https://github.com/user-attachments/assets/a17e374d-2939-4bde-ac0f-1e3cacb9af75)


## Features

- **URL Scraping**: Extracts and processes the text content from a user-provided URL.
- **Embedding & Storage**: Creates embeddings from the text content and stores them in a Pinecone index.
- **Question Answering**: Allows users to ask questions about the URL content, retrieves relevant information, and provides answers via a chat interface.
- **Real-Time Interaction**: Streams the response from the backend in real-time as the bot generates the answer.

## Technology Stack

- **Frontend**: React
  - Manages the user interface for entering URLs and interacting with the chat bot.
  - Uses state and effects to control the transition between input and chat interfaces.
- **Backend**: Flask
  - Provides the API for handling URL submissions, processing text, and managing interactions with Pinecone and OpenAI.
  - Integrates with various services like Pinecone for storage and OpenAI for generating embeddings and answers.

## Installation


### Prerequisites

- Python 3.x
- Node.js & npm
- Pipenv (optional but recommended)

### Backend Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ilyeshr2/URLQuestion-AnswerBot.git
    cd URLQuestion-AnswerBot
    ```

2. Set up a virtual environment:

    ```bash
    py -3 -m venv .venv
    .venv\Scripts\activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your API keys:

    ```makefile
    OPENAI_API_KEY=your_openai_api_key
    PINECONE_API_KEY=your_pinecone_api_key
    ```

5. Run the Flask server:

    ```bash
    python run.py
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install the required npm packages:

    ```bash
    npm install
    ```

3. Run the React app:

    ```bash
    npm start
    ```

The frontend will be accessible at [http://localhost:3000](http://localhost:3000).

## Usage

1. **Start the Backend**: Run the Flask server to make the API available.
2. **Start the Frontend**: Open the React app in your browser.
3. **Enter a URL**: In the URL input field, enter a website URL and click "Submit."
4. **Interact with the Bot**: Once the URL content is processed, ask the bot any questions related to the URL content.

## File Structure

- `app/` - Contains the backend code including API routes, services, and utilities.
- `frontend/` - Contains the React frontend code with components for URL input and chat interface.
- `requirements.txt` - Lists the Python dependencies.
- `run.py` - Entry point for running the Flask server.

## Contributing

Feel free to submit issues or pull requests if you want to contribute to this project.

## License

This project is licensed under the MIT License.
