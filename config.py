"""
Configuration file for the annotation tool.
"""

# Application settings
APP_TITLE = "Word Recognition Annotation Tool"
APP_ICON = "📝"

# Data directories
SORTED_CROPS_DIR = "sorted_crops"
GROUND_TRUTH_DIR = "ground_truth"
ANNOTATIONS_DIR = "annotations"

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}

# UI settings
ITEMS_PER_PAGE = 10
DEFAULT_IMAGE_QUALITY = 95

# Export settings
EXPORT_DATE_FORMAT = "%Y-%m-%d_%H-%M-%S"

# Session settings
SESSION_TIMEOUT_MINUTES = 120

# Annotation settings
ENABLE_KEYBOARD_SHORTCUTS = True
AUTO_ADVANCE_ON_CORRECT = True
SHOW_ANNOTATION_HISTORY = True

# Admin settings
MAX_PREVIEW_ITEMS = 10
ENABLE_QUALITY_REVIEW = True
