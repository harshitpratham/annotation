# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

#### Option A: Use Sample Data (for testing)
```bash
python create_sample_data.py
```

#### Option B: Add Your Own Data
Organize your data as follows:
```
data-annotation/
├── sorted_crops/
│   ├── 31/
│   │   ├── 000.jpg
│   │   ├── 001.jpg
│   │   └── ...
│   └── 32/
│       └── ...
└── ground_truth/
    ├── 31.txt  (one label per line)
    └── 32.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📖 Usage Guide

### For Annotators

1. **Login**: Enter username, select "annotator" role
2. **View**: See word image with suggested label
3. **Annotate**:
   - Press **Enter** → Mark as correct
   - Press **Backspace** → Mark as incorrect (type correction)
   - Press **Ctrl+Enter** → Submit correction
4. **Navigate**: Use **← →** arrow keys
5. **Export**: Download your annotations from sidebar

### For Admins

1. **Login**: Enter username, select "admin" role
2. **Overview**: View system statistics
3. **Users**: Compare annotator performance
4. **Annotations**: Filter and review all annotations
5. **Export**: Download merged data with annotator attribution
6. **Quality Review**: Check inter-annotator agreement and conflicts

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Enter** | Mark correct & next image |
| **Backspace** | Mark incorrect (focus correction) |
| **Ctrl/Cmd+Enter** | Submit correction & next |
| **← Left Arrow** | Previous image |
| **→ Right Arrow** | Next image |

---

## 💡 Tips

### For Efficient Annotation
- ✅ Use keyboard shortcuts - much faster than clicking
- ✅ Enable "Show only unannotated" filter to focus on new images
- ✅ Take regular breaks to maintain accuracy
- ✅ Export your work periodically as backup

### For Quality Control (Admins)
- ✅ Check the Quality Review tab for disagreements
- ✅ Monitor correction rates per folder
- ✅ Review most common corrections to identify systematic issues
- ✅ Use inter-annotator agreement metrics to assess quality

---

## 📊 Understanding the Data

### Annotation Record Fields
- **annotation_id**: Unique identifier
- **image_path**: Full path to image file
- **folder**: Folder name (e.g., "31")
- **filename**: Image filename (e.g., "000.jpg")
- **suggested_label**: Original label from ground_truth
- **is_correct**: True/False
- **corrected_label**: User's correction (if incorrect)
- **annotator**: Username
- **timestamp**: When annotation was made

### Export Formats

#### CSV
- Excel compatible
- Easy to analyze in spreadsheets
- Best for bulk data processing

#### JSON
- Machine readable
- Preserves data types
- Best for programmatic access

---

## 🔧 Troubleshooting

### "No data found" error
**Solution**: Ensure `sorted_crops/` and `ground_truth/` folders exist with data

### Image/label count mismatch
**Solution**: Check admin dashboard → Overview → Data Folder Statistics

### Keyboard shortcuts not working
**Solution**: Click inside the Streamlit app window to focus it

### Export button disabled
**Solution**: You need at least one annotation to export

---

## 📁 Project Structure

```
data-annotation/
├── app.py                 # Main application
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── utils/
│   ├── data_loader.py    # Data loading logic
│   └── storage.py        # Annotation storage
├── pages/
│   ├── annotate.py       # Annotation interface
│   └── admin.py          # Admin dashboard
└── sorted_crops/         # Your image data
    ground_truth/         # Your label files
    annotations/          # Generated annotations
```

---

## 🆘 Need Help?

Check the main [README.md](README.md) for detailed documentation.
