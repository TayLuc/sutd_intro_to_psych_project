import pandas as pd
from nrclex import NRCLex
import textblob.download_corpora
import nltk

# Ensure necessary corpora are downloaded
nltk.data.path.append('<custom path here>')
textblob.download_corpora.download_all()


def classify_emotions(text):
    """Returns a dictionary of emotion scores."""
    emotion_analysis = NRCLex(text)
    return emotion_analysis.raw_emotion_scores


def get_top_emotions(text):
    """Returns the top emotions for the text."""
    emotion_analysis = NRCLex(text)
    return emotion_analysis.top_emotions


def extract_keywords(file):
    """Processes combined columns for emotion analysis and tags results to the name."""
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file)

        # Check if required columns exist
        required_columns = ['engagement_reason', 'emotional_connection_reason', "additional_comments"]
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"The column '{col}' is missing from the file.")

        # Handle missing or empty values in the relevant columns
        for col in required_columns:
            df[col] = df[col].fillna('')  # Replace NaN with an empty string

        # Combine the relevant columns into one text field for analysis
        df['combined_text'] = df['agent_description'] + ' ' + df['engagement_reason'] + ' ' + df[
            'emotional_connection_reason'] + ' ' + df["additional_comments"]

        # Perform emotion analysis on the combined text
        df['top_emotions'] = df['combined_text'].apply(lambda x: get_top_emotions(str(x)))

        # Save the name and top emotions columns to a new Excel file
        output_file = "studygrpA_with_emotions4.xlsx"
        df[['name', 'top_emotions']].to_excel(output_file, index=False)

        # Print a summary of the processed data
        print(df[['top_emotions']].head())
        print(f"Processed file saved as: {output_file}")

    except FileNotFoundError:
        print(f"File not found: {file}")
    except KeyError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function with the Excel file path
extract_keywords("data/studygrpA.xlsx")
