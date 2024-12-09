import pandas as pd
from nrclex import NRCLex
import textblob.download_corpora
import nltk
nltk.data.path.append("E:\\psych\\py\\venv\\nltk_data")
print(nltk.data.path)

# Ensure necessary corpora are downloaded
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
    """Processes specified columns for emotion analysis and tags results to the name."""
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file)

        # Check if required columns exist
        required_columns = ['name', 'agent_description', 'engagement_reason', 'emotional_connection_reason']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"The column '{col}' is missing from the file.")

        # Handle missing or empty values in the relevant columns
        for col in required_columns:
            df[col] = df[col].fillna('')  # Replace NaN with an empty string

        # Perform emotion classification for each of the specified columns
        emotion_columns = ['agent_description', 'engagement_reason', 'emotional_connection_reason']
        for col in emotion_columns:
            emotion_score_col = f"{col}_emotion_scores"
            top_emotion_col = f"{col}_top_emotions"

            df[emotion_score_col] = df[col].apply(lambda x: classify_emotions(str(x)))
            df[top_emotion_col] = df[col].apply(lambda x: get_top_emotions(str(x)))

        # Save the updated DataFrame to a new Excel file
        output_file = "data/studygrpB_with_emotions.xlsx"
        df.to_excel(output_file, index=False)

        # Print a summary of the processed data
        print(df[['name', 'agent_description_emotion_scores', 'engagement_reason_emotion_scores',
                  'emotional_connection_reason_emotion_scores']].head())

        print(f"Processed file saved as: {output_file}")

    except FileNotFoundError:
        print(f"File not found: {file}")
    except KeyError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function with the Excel file path
extract_keywords("data/studygrpB.xlsx")
