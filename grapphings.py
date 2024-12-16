import pandas as pd
import matplotlib.pyplot as plt


# Function to parse the emotion column
def parse_emotion_column(emotion_column):
    """
    Parses a column of emotion tuples into a dictionary of emotions with their scores.
    Missing values are treated as zeros.
    """
    all_emotions = {}

    for row in emotion_column:
        if pd.notna(row):  # Skip NaN values
            for emotion, score in eval(row):  # Use eval to convert strings into tuples
                if emotion not in all_emotions:
                    all_emotions[emotion] = []
                all_emotions[emotion].append(score)
        else:
            # Handle missing rows by assigning zeros to all known emotions
            for emotion in all_emotions.keys():
                all_emotions[emotion].append(0)

    # Fill in zeros for any missing entries in the emotions dictionary
    max_length = max(len(scores) for scores in all_emotions.values())
    for emotion, scores in all_emotions.items():
        if len(scores) < max_length:
            all_emotions[emotion] += [0] * (max_length - len(scores))

    return pd.DataFrame.from_dict(all_emotions, orient='index').transpose()


# Function to compute mean scores
def compute_mean_scores(df):
    """
    Computes mean scores for each emotion in the given DataFrame.
    """
    return df.mean()


# Function to plot the emotion scores
def plot_emotion_scores(mean_scores, title):
    """
    Plots a bar chart of the mean emotion scores.
    """
    plt.figure(figsize=(10, 6))
    mean_scores.sort_values(ascending=False).plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title(title, fontsize=16)
    plt.xlabel('Emotion', fontsize=14)
    plt.ylabel('Average Score', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Main workflow
def process_and_plot_emotions(emotion_column, title):
    """
    Processes an emotion column and generates a bar chart.
    """
    parsed_df = parse_emotion_column(emotion_column)
    mean_scores = compute_mean_scores(parsed_df)
    plot_emotion_scores(mean_scores, title)


# Import your data (Run lexnalysis2.py first)
df_studygrpA = pd.read_excel("studygrpA_with_emotions4.xlsx")
df_studygrpB = pd.read_excel("studygrpB_with_emotions4.xlsx")

# Extract emotion columns
emocolumnA = df_studygrpA["top_emotions"]
emocolumnB = df_studygrpB["top_emotions"]

# Process and plot for each group
process_and_plot_emotions(emocolumnA, "Average Emotion (Group A)")
process_and_plot_emotions(emocolumnB, "Average Emotion (Group B)")
