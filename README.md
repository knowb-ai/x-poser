# 📢 XPosay

> “When they post propaganda, we post receipts.”

XPosé is an open-source, real-time fact-checking and counter-narrative toolkit for monitoring specific accounts on Twitter/X, detecting disinformation or propaganda, and publicly replying with factual corrections powered by LLMs.

This project is designed as a peaceful resistance tool — to expose falsehoods, amplify truth, and hold digital empires accountable.


## 📜 Philosophical Goals
	•	Expose, don’t censor: We fight disinformation by shining a light on it, not by silencing it.
	•	Whistleblower spirit: Truth is not neutral. False narratives must be publicly corrected, not merely “balanced.”
	•	Automation with purpose: Technology should not amplify the powerful — it should empower the powerless.
	•	Radical transparency: Receipts over rhetoric. Always cite, always verify.


## ⚡ Project Structure

```bash
Xposay/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI server entrypoint
│   ├── config.py              # API keys and configs
│   ├── twitter_client.py      # Monitoring Twitter accounts
│   ├── factchecker.py         # Fact-checking and LLM prompts
│   ├── retriever.py           # (Optional) Fact retrieval augmentation
│   └── responder.py           # Formulate and post replies
├── data/
│   └── sources/               # Static reference sources (Wikipedia dumps, CSVs, etc.)
├── requirements.txt           # Project dependencies
├── README.md                  # You're here
└── .env                       # Local environment variables (never commit)
```

## 🛠️ Installation and Setup

### 1.	Clone the repository:
```
git clone https://github.com/yourusername/XPose.git
cd XPosay
```

### 2. Set up your environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3.	Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables:
Create a .env file in the root directory:
```bash
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the bot:
```bash
uvicorn app.main:app --reload
```

This will start a FastAPI server and launch your monitoring system.

## ⚙️ How It Works
	•	Monitoring: Watches specified Twitter/X accounts for new tweets.
	•	Analysis: Uses an LLM (like GPT-4) to fact-check tweet content.
	•	Replying: Posts an automated, concise, cited reply if necessary.
	•	Retrieval (optional): Pulls from preloaded factual datasets to ground LLM responses.

## 🚨 Important Warning and Disclaimer

Use responsibly.

XPosay is a toolkit. It is powerful enough to be used for:
	•	Mass counter-propaganda efforts
	•	Real-time rebuttal and fact-based disruption
	•	Potentially overwhelming or “crippling” narrative control from malicious actors

However, misuse of this tool — including violating Twitter/X Terms of Service (TOS), harassing individuals, or engaging in prohibited automated activity — can result in account suspension, legal action, or worse.

We strongly advise:
	•	Always label bot activity clearly (e.g., “Automated Fact-Checker” in your bio).
	•	Always cite credible sources when fact-checking.
	•	Do not target private individuals.
	•	Review the Twitter Automation Rules and Platform Manipulation Policy.

You are solely responsible for how you deploy this software. We provide XPosay for educational, ethical activism, and academic purposes only.

## 🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

MIT License

## ✊ Final Word

They lied. We coded. Welcome to the counter-narrative.