#!/usr/bin/env python
"""
Data integrity checker for the annotation tool.
Run this script to verify your data structure before starting annotation.
"""

import os
from pathlib import Path
from utils.data_loader import DataLoader


def check_data_integrity():
    """Check data integrity and report issues."""
    print("=" * 60)
    print("DATA INTEGRITY CHECK")
    print("=" * 60)
    print()
    
    data_loader = DataLoader()
    
    # Check directories exist
    print("📁 Checking directories...")
    sorted_crops_exists = data_loader.sorted_crops_dir.exists()
    ground_truth_exists = data_loader.ground_truth_dir.exists()
    
    if not sorted_crops_exists:
        print("  ❌ sorted_crops/ directory not found")
        return False
    else:
        print("  ✅ sorted_crops/ directory found")
    
    if not ground_truth_exists:
        print("  ❌ ground_truth/ directory not found")
        return False
    else:
        print("  ✅ ground_truth/ directory found")
    
    print()
    
    # Get all folders
    folders = data_loader.get_all_folders()
    
    if not folders:
        print("❌ No subfolders found in sorted_crops/")
        return False
    
    print(f"📂 Found {len(folders)} folder(s): {', '.join(folders)}")
    print()
    
    # Check each folder
    print("🔍 Checking each folder...")
    print()
    
    all_ok = True
    total_images = 0
    total_labels = 0
    mismatches = []
    
    for folder in folders:
        print(f"  Folder: {folder}")
        
        # Get images
        images = data_loader.get_images_in_folder(folder)
        num_images = len(images)
        total_images += num_images
        print(f"    📷 Images: {num_images}")
        
        # Get labels
        labels = data_loader.load_ground_truth(folder)
        num_labels = len(labels)
        total_labels += num_labels
        print(f"    🏷️  Labels: {num_labels}")
        
        # Check match
        if num_images == num_labels:
            print(f"    ✅ Match!")
        else:
            print(f"    ❌ MISMATCH! Difference: {abs(num_images - num_labels)}")
            mismatches.append(folder)
            all_ok = False
        
        # Check for empty labels
        empty_labels = [i for i, label in enumerate(labels) if not label.strip()]
        if empty_labels:
            print(f"    ⚠️  Warning: {len(empty_labels)} empty label(s) at line(s): {empty_labels}")
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total folders: {len(folders)}")
    print(f"Total images: {total_images}")
    print(f"Total labels: {total_labels}")
    print()
    
    if all_ok:
        print("✅ All checks passed! Data is ready for annotation.")
        print()
        print("Next steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Login and start annotating!")
        return True
    else:
        print("❌ Issues found!")
        print()
        print(f"Folders with mismatches: {', '.join(mismatches)}")
        print()
        print("Please fix the following:")
        for folder in mismatches:
            images = data_loader.get_images_in_folder(folder)
            labels = data_loader.load_ground_truth(folder)
            print(f"  - {folder}: {len(images)} images vs {len(labels)} labels")
            
            if len(images) > len(labels):
                print(f"    → Add {len(images) - len(labels)} more label(s) to ground_truth/{folder}.txt")
            else:
                print(f"    → Remove {len(labels) - len(images)} label(s) from ground_truth/{folder}.txt")
        
        return False


if __name__ == "__main__":
    try:
        success = check_data_integrity()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)
