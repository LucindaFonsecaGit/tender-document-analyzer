# Usage

## Command-Line Interface

### Demo Mode

Run the application without calling the AI model. This mode is useful for testing the application or exploring its functionality without requiring API credentials.

```bash
python -m app.main --demo
```

### AI Mode

Analyze a tender document using the configured Large Language Model (LLM).

```bash
python -m app.main
```

> Ensure your `.env` file is configured with your API key and model settings before running in AI mode.

## Web Interface

Launch the Streamlit application:

```bash
streamlit run app/streamlit_app.py
```

Open your browser and navigate to:

```
http://localhost:8501
```

Upload a tender document (PDF), click **Analyze**, and review the extracted structured information.

## Quality Assurance

This project includes automated tests using `pytest`.

Current test coverage includes:

- PDF reader error handling
- AI extraction in demo mode
- Validation of structured tender analysis output

GitHub Actions is configured to run tests automatically on push and pull requests.