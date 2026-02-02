# Word Recognition Annotation Tool

A multi-user Streamlit application for annotating word images with ground truth labels. Built for efficient word recognition dataset labeling with keyboard shortcuts, progress tracking, and admin dashboard.

## Features

### For Annotators
- 🖼️ **Image viewer** with suggested labels from ground truth
- ✅ **Mark correct/incorrect** with option to provide corrections
- ⌨️ **Keyboard shortcuts** for faster annotation
- 📊 **Personal progress tracking** and statistics
- 💾 **Export** annotations in CSV or JSON format
- 🔍 **Filters** to show only unannotated or incorrect images

### For Admins
- 👥 **User management** and progress overview
- 📈 **System-wide statistics** and visualizations
- 📝 **View all annotations** with filtering options
- 📦 **Merged exports** with annotator attribution
- 📊 **Data quality monitoring** (image/label count verification)

### Technical Features
- 🔄 **Multi-user support** with role-based access
- 📜 **Full annotation history** (append-only storage)
- 💾 **Dual format storage** (CSV + JSON)
- 🚀 **Session persistence** (resume where you left off)
- ⚡ **Fast navigation** with jump-to-image functionality

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Structure

Organize your data as follows:

```
data-annotation/
├── sorted_crops/          # Image folders
│   ├── 31/
│   │   ├── 000.jpg
│   │   ├── 001.jpg
│   │   └── ...
│   ├── 32/
│   │   └── ...
│   └── ...
├── ground_truth/          # Label files (one per folder)
│   ├── 31.txt            # One label per line
│   ├── 32.txt
│   └── ...
└── annotations/           # Auto-generated annotation storage
    ├── users.json
    ├── history.csv
    └── history.json
```

**Important**: 
- Each subfolder in `sorted_crops/` should have a corresponding `.txt` file in `ground_truth/`
- Images in each folder should be named sequentially (e.g., 000.jpg, 001.jpg)
- Labels in `.txt` files should match the order of images (one label per line)

## Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### First Time Setup

1. **Login Screen**: Enter a username and select your role
   - **Annotator**: For labeling images
   - **Admin**: For viewing all annotations and user statistics

2. **Returning Users**: Click on your username button to login quickly

### Annotator Workflow

1. **View Image**: Current word image is displayed with suggested label
2. **Review Label**: Check if the suggested label is correct
3. **Annotate**:
   - If correct: Click "✅ Correct & Next" or press **Enter**
   - If incorrect: Select "❌ Incorrect", type correction, then click "💾 Submit & Next" or press **Ctrl+Enter**
4. **Navigate**: Use Previous/Next buttons or **Arrow keys** (← →)
5. **Track Progress**: View stats in the sidebar
6. **Export**: Download your annotations as CSV or JSON

### Keyboard Shortcuts

- **Enter**: Mark as correct and move to next image
- **Backspace**: Mark as incorrect (focuses correction input)
- **Ctrl/Cmd + Enter**: Submit correction and move to next
- **← Arrow**: Previous image
- **→ Arrow**: Next image

### Admin Dashboard

Admins have access to four main tabs:

1. **Overview**: System statistics and data folder verification
2. **Users**: User progress comparison and metrics
3. **Annotations**: Filterable view of all annotations
4. **Export**: Download merged annotations with annotator attribution

## Storage Format

### Annotation History (CSV/JSON)

Each annotation record contains:
- `annotation_id`: Unique identifier
- `image_path`: Full path to image
- `folder`: Folder name (e.g., "31")
- `filename`: Image filename (e.g., "000.jpg")
- `suggested_label`: Original label from ground truth
- `is_correct`: Boolean (True/False)
- `corrected_label`: User's correction (if incorrect)
- `annotator`: Username
- `timestamp`: ISO format timestamp

### Multi-Annotation Handling

- Same image can be annotated multiple times by same/different users
- All annotations are preserved (append-only)
- Latest annotation per user available via API
- Export includes all annotations with annotator column

## Project Structure

```
data-annotation/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # Image/label loading logic
│   └── storage.py        # Annotation persistence
├── pages/
│   ├── annotate.py       # Annotator interface
│   └── admin.py          # Admin dashboard
├── sorted_crops/         # Your image data
├── ground_truth/         # Your label files
└── annotations/          # Auto-generated storage
    ├── users.json
    ├── history.csv
    └── history.json
```

## Tips for Efficient Annotation

1. **Use keyboard shortcuts** - Much faster than clicking
2. **Enable filters** - Focus on unannotated images first
3. **Regular exports** - Download backups of your work
4. **Check progress** - Monitor accuracy in the sidebar
5. **Jump navigation** - Use "Jump to image" for reviewing specific images

## Troubleshooting

### No data found error
- Ensure `sorted_crops/` and `ground_truth/` folders exist
- Verify folder structure matches the expected format
- Check that image files have valid extensions (.jpg, .jpeg, .png)

### Image/label count mismatch
- Admin dashboard will show warnings for mismatches
- Verify `.txt` files have correct number of lines
- Check for missing images or labels

### Export not working
- Ensure you have annotated at least one image
- Check browser's download settings

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.
