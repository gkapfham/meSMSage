"""Visualize a spaCy text categorization model using Streamlit."""

import spacy_streamlit  # type: ignore  noreorder
import typer


def main(models: str, default_text: str):
    """Display the model in an interactive browser dashboard created by spacy-streamlit."""
    models_list = [name.strip() for name in models.split(",")]
    spacy_streamlit.visualize(models_list, default_text, visualizers=["textcat"])


if __name__ == "__main__":
    try:
        typer.run(main)
    except SystemExit:
        pass
