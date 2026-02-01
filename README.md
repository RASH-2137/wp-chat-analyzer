# WhatsApp Chat Analyzer 💬

A simple Streamlit app to analyze your WhatsApp chat exports. See your messaging stats, most used words, emoji patterns, and activity timelines.

## What it does

Upload a WhatsApp chat export and get insights like:
- Total messages, words, media, and links shared
- Most active users (for group chats)
- Word cloud visualization
- Most common words
- Emoji usage stats
- Monthly and daily message timelines
- Activity patterns (which days/hours you chat most)
- Hourly activity heatmap

## Getting started

### Prerequisites

You'll need Python 3.7+ and pip installed.

### Installation

1. Clone this repo or download the files
2. Install the required packages:

```bash
pip install streamlit pandas matplotlib seaborn wordcloud urlextract emoji
```

### Running the app

```bash
streamlit run app.py
```

The app will open in your browser automatically.

## How to export your WhatsApp chat

1. Open WhatsApp on your phone
2. Go to the chat you want to analyze (individual or group)
3. Tap the three dots menu (top right)
4. Select "More" → "Export chat"
5. Choose "Without Media" (this keeps the file size small)
6. Save the file to your computer
7. Upload it in the app using the sidebar

**Note:** The app works with both `.txt` files (Android) and `.zip` files (iPhone exports).

## Features

### Overview Statistics
Quick stats showing total messages, words, media files, and links shared.

### Most Active Users
For group chats, see who sends the most messages and their contribution percentage.

### Word Cloud
Visual representation of the most frequently used words in your chats.

### Most Used Words
Top 20 words with frequency counts and bar charts.

### Emoji Analysis
See which emojis you use most often with frequency tables and pie charts.

### Timelines
- **Monthly timeline:** Message activity over months
- **Daily timeline:** Day-by-day message counts

### Activity Patterns
- **Weekly pattern:** Which days of the week are most active
- **Monthly pattern:** Which months had the most activity
- **Hourly heatmap:** See when you chat most throughout the day and week

## Project structure

```
.
├── app.py              # Main Streamlit app
├── preprocessor.py     # Handles chat file parsing
├── helper.py          # Analysis functions
├── stop_hinglish.txt  # Stop words for filtering
└── README.md          # This file
```

## How it works

1. **File upload:** The app accepts `.txt` or `.zip` WhatsApp exports
2. **Preprocessing:** Parses the chat format and extracts messages, users, dates, etc.
3. **Analysis:** Calculates stats and generates visualizations
4. **Display:** Shows everything in a clean dashboard layout

The app handles different WhatsApp export formats (Android vs iPhone) and tries multiple encodings to read the files correctly.

## Tips

- Export chats "Without Media" to keep file sizes manageable
- For very large chats, processing might take a few seconds
- You can analyze individual users or the entire group
- The word cloud filters out common stop words to show more meaningful results

## Troubleshooting

**File won't upload?**
- Make sure it's a `.txt` or `.zip` file exported from WhatsApp
- Try exporting again from WhatsApp

**Charts not showing?**
- Make sure you clicked the "Show Analysis" button after selecting a user
- Check that your chat file has actual messages (not just media)

**Encoding errors?**
- The app tries multiple encodings automatically
- If it still fails, try re-exporting the chat from WhatsApp

## Notes

- All processing happens locally in your browser - your chat data never leaves your computer
- The app filters out group notifications and media placeholders
- Stop words are filtered to show more meaningful word analysis

## License

Feel free to use this for personal projects or modify as needed.

---

Made with Streamlit. If you find any bugs or have suggestions, feel free to open an issue!
