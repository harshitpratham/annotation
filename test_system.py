#!/usr/bin/env python
"""
Test script to verify all components of the annotation tool.
"""

import sys
from pathlib import Path

print("=" * 60)
print("ANNOTATION TOOL - SYSTEM CHECK")
print("=" * 60)
print()

# Test 1: Import dependencies
print("1️⃣  Testing dependencies...")
try:
    import streamlit as st
    print("  ✅ streamlit")
except ImportError as e:
    print(f"  ❌ streamlit - {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("  ✅ pandas")
except ImportError as e:
    print(f"  ❌ pandas - {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("  ✅ Pillow (PIL)")
except ImportError as e:
    print(f"  ❌ Pillow - {e}")
    sys.exit(1)

print()

# Test 2: Import modules
print("2️⃣  Testing modules...")
try:
    from utils.data_loader import DataLoader
    print("  ✅ utils.data_loader")
except ImportError as e:
    print(f"  ❌ utils.data_loader - {e}")
    sys.exit(1)

try:
    from utils.storage import AnnotationStorage
    print("  ✅ utils.storage")
except ImportError as e:
    print(f"  ❌ utils.storage - {e}")
    sys.exit(1)

print()

# Test 3: Check directory structure
print("3️⃣  Checking directory structure...")
required_dirs = ['utils', 'pages', 'sorted_crops', 'ground_truth', 'annotations']
for dir_name in required_dirs:
    if Path(dir_name).exists():
        print(f"  ✅ {dir_name}/")
    else:
        print(f"  ⚠️  {dir_name}/ - not found")

print()

# Test 4: Check files
print("4️⃣  Checking required files...")
required_files = [
    'app.py',
    'requirements.txt',
    'README.md',
    'utils/data_loader.py',
    'utils/storage.py',
    'pages/annotate.py',
    'pages/admin.py'
]

for file_path in required_files:
    if Path(file_path).exists():
        print(f"  ✅ {file_path}")
    else:
        print(f"  ❌ {file_path} - MISSING!")
        sys.exit(1)

print()

# Test 5: Initialize storage
print("5️⃣  Testing storage initialization...")
try:
    storage = AnnotationStorage()
    print("  ✅ AnnotationStorage initialized")
    
    # Check if files were created
    if Path('annotations/users.json').exists():
        print("  ✅ users.json created")
    if Path('annotations/history.csv').exists():
        print("  ✅ history.csv created")
    if Path('annotations/history.json').exists():
        print("  ✅ history.json created")
except Exception as e:
    print(f"  ❌ Storage initialization failed - {e}")
    sys.exit(1)

print()

# Test 6: Initialize data loader
print("6️⃣  Testing data loader...")
try:
    data_loader = DataLoader()
    print("  ✅ DataLoader initialized")
    
    folders = data_loader.get_all_folders()
    print(f"  📁 Found {len(folders)} folder(s)")
    
    if folders:
        all_data = data_loader.load_all_data()
        print(f"  📷 Loaded {len(all_data)} image(s)")
    else:
        print("  ⚠️  No data folders found (run create_sample_data.py to create test data)")
    
except Exception as e:
    print(f"  ❌ DataLoader failed - {e}")
    sys.exit(1)

print()

# Test 7: Storage operations
print("7️⃣  Testing storage operations...")
try:
    # Register a test user
    storage.register_user("test_user", "annotator")
    users = storage.load_users()
    if len(users) > 0:
        print(f"  ✅ User registration works ({len(users)} user(s))")
    
    # Test annotation save
    storage.save_annotation({
        'image_path': 'test/path.jpg',
        'folder': 'test',
        'filename': 'path.jpg',
        'suggested_label': 'test',
        'is_correct': True,
        'corrected_label': '',
        'annotator': 'test_user'
    })
    
    history = storage.load_history()
    if len(history) > 0:
        print(f"  ✅ Annotation save works ({len(history)} annotation(s))")
    
    # Test stats
    stats = storage.get_user_stats('test_user')
    print(f"  ✅ Stats calculation works (total: {stats['total']})")
    
except Exception as e:
    print(f"  ❌ Storage operations failed - {e}")
    sys.exit(1)

print()

# Summary
print("=" * 60)
print("SYSTEM CHECK COMPLETE")
print("=" * 60)
print()
print("✅ All tests passed!")
print()
print("Next steps:")
print("  1. Run: streamlit run app.py")
print("  2. Login and start annotating")
print()
print("Optional:")
print("  - Run: python create_sample_data.py (to create test data)")
print("  - Run: python check_data.py (to verify data integrity)")
print()
