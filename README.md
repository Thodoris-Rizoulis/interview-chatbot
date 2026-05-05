# Interview Chatbot 🤖

A Streamlit-powered mock interview preparation chatbot that uses OpenAI's GPT model to simulate an HR interviewer and provide personalized feedback.

## Features

- **Personalized setup** — Enter your name, age, experience, and skills before starting
- **Targeted practice** — Choose your seniority level, role, and target company
- **AI-driven interview** — Chat with a simulated HR executive for up to 5 questions
- **Automated feedback** — Receive an overall score and detailed feedback on your performance after the session

## Demo

![Setup screen](https://via.placeholder.com/800x400?text=Setup+Screen)

## Requirements

- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Installation

```bash
git clone https://github.com/your-username/interview-chatbot.git
cd interview-chatbot
pip install -r requirements.txt
```

## Configuration

Create a `.streamlit/secrets.toml` file in the project root:

```toml
OPENAI_API_KEY = "sk-..."
```

> This file is gitignored by default — never commit your API key.

## Usage

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

1. Fill in your personal info and target role on the setup screen
2. Click **Start Interview Preparation**
3. Ask up to 5 questions to the AI interviewer
4. Click **Provide Feedback** to receive your performance score and feedback

## Project Structure

```
interview-chatbot/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── secrets.toml     # API keys (not committed)
└── README.md
```

## License

MIT
