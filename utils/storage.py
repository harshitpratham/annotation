"""
Storage module for annotation tool.
Handles user management and annotation persistence with full history.
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class AnnotationStorage:
    """Manages annotation storage with history tracking."""
    
    def __init__(self, annotations_dir: str = "annotations"):
        """
        Initialize AnnotationStorage.
        
        Args:
            annotations_dir: Base directory for all annotation data
        """
        self.annotations_dir = Path(annotations_dir)
        self.annotations_dir.mkdir(exist_ok=True)
        
        self.users_file = self.annotations_dir / "users.json"
        self.history_csv = self.annotations_dir / "history.csv"
        self.history_json = self.annotations_dir / "history.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize storage files if they don't exist."""
        # Initialize users file
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump([], f)
        
        # Initialize history CSV
        if not self.history_csv.exists():
            with open(self.history_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'annotation_id', 'image_path', 'folder', 'filename', 
                    'suggested_label', 'is_correct', 'corrected_label', 
                    'annotator', 'timestamp'
                ])
                writer.writeheader()
        
        # Initialize history JSON
        if not self.history_json.exists():
            with open(self.history_json, 'w') as f:
                json.dump([], f)
    
    def register_user(self, username: str, role: str = "annotator") -> bool:
        """
        Register a new user or update existing user.
        
        Args:
            username: Username
            role: User role ("annotator" or "admin")
            
        Returns:
            True if new user was created, False if user already existed
        """
        users = self.load_users()
        
        # Check if user already exists
        for user in users:
            if user['username'] == username:
                # Update role if changed
                if user['role'] != role:
                    user['role'] = role
                    self._save_users(users)
                return False
        
        # Add new user
        users.append({
            'username': username,
            'role': role,
            'created_at': datetime.now().isoformat()
        })
        
        self._save_users(users)
        return True
    
    def load_users(self) -> List[Dict]:
        """Load all registered users."""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users: List[Dict]):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username."""
        users = self.load_users()
        for user in users:
            if user['username'] == username:
                return user
        return None
    
    def save_annotation(self, annotation: Dict):
        """
        Save a single annotation to history (append-only).
        
        Args:
            annotation: Dictionary containing:
                - image_path: Path to image
                - folder: Folder name
                - filename: Image filename
                - suggested_label: Original suggested label
                - is_correct: Boolean indicating if label is correct
                - corrected_label: Corrected label if is_correct is False
                - annotator: Username of annotator
        """
        # Generate unique annotation ID
        annotation_id = self._generate_annotation_id()
        
        # Add metadata
        full_annotation = {
            'annotation_id': annotation_id,
            'timestamp': datetime.now().isoformat(),
            **annotation
        }
        
        # Append to CSV
        with open(self.history_csv, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'annotation_id', 'image_path', 'folder', 'filename', 
                'suggested_label', 'is_correct', 'corrected_label', 
                'annotator', 'timestamp'
            ])
            writer.writerow(full_annotation)
        
        # Append to JSON
        history = self.load_history()
        history.append(full_annotation)
        with open(self.history_json, 'w') as f:
            json.dump(history, f, indent=2)
    
    def _generate_annotation_id(self) -> str:
        """Generate a unique annotation ID."""
        history = self.load_history()
        return f"ANN_{len(history) + 1:06d}"
    
    def load_history(self) -> List[Dict]:
        """Load all annotation history."""
        with open(self.history_json, 'r') as f:
            return json.load(f)
    
    def load_history_df(self) -> pd.DataFrame:
        """Load annotation history as pandas DataFrame."""
        return pd.read_csv(self.history_csv)
    
    def get_user_annotations(self, username: str) -> List[Dict]:
        """Get all annotations by a specific user."""
        history = self.load_history()
        return [ann for ann in history if ann['annotator'] == username]
    
    def get_user_annotations_df(self, username: str) -> pd.DataFrame:
        """Get user annotations as DataFrame."""
        df = self.load_history_df()
        if df.empty:
            return df
        return df[df['annotator'] == username]
    
    def get_annotated_images(self, username: str) -> set:
        """Get set of image paths that user has already annotated."""
        annotations = self.get_user_annotations(username)
        return {ann['image_path'] for ann in annotations}
    
    def get_user_stats(self, username: str) -> Dict:
        """
        Get statistics for a specific user.
        
        Returns:
            Dictionary with stats:
                - total: Total annotations
                - correct: Number marked as correct
                - incorrect: Number marked as incorrect
                - correct_percentage: Percentage marked correct
        """
        annotations = self.get_user_annotations(username)
        
        if not annotations:
            return {
                'total': 0,
                'correct': 0,
                'incorrect': 0,
                'correct_percentage': 0.0
            }
        
        correct = sum(1 for ann in annotations if ann['is_correct'])
        incorrect = len(annotations) - correct
        
        return {
            'total': len(annotations),
            'correct': correct,
            'incorrect': incorrect,
            'correct_percentage': (correct / len(annotations) * 100) if annotations else 0.0
        }
    
    def get_all_user_stats(self) -> List[Dict]:
        """Get statistics for all users."""
        users = self.load_users()
        stats = []
        
        for user in users:
            username = user['username']
            user_stats = self.get_user_stats(username)
            stats.append({
                'username': username,
                'role': user['role'],
                **user_stats
            })
        
        return stats
    
    def export_to_csv(self, filepath: str, username: Optional[str] = None):
        """
        Export annotations to CSV file.
        
        Args:
            filepath: Output file path
            username: If provided, export only this user's annotations
        """
        if username:
            df = self.get_user_annotations_df(username)
        else:
            df = self.load_history_df()
        
        df.to_csv(filepath, index=False)
    
    def export_to_json(self, filepath: str, username: Optional[str] = None):
        """
        Export annotations to JSON file.
        
        Args:
            filepath: Output file path
            username: If provided, export only this user's annotations
        """
        if username:
            data = self.get_user_annotations(username)
        else:
            data = self.load_history()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_latest_annotation_for_image(self, image_path: str, username: str) -> Optional[Dict]:
        """Get the most recent annotation for a specific image by a user."""
        annotations = self.get_user_annotations(username)
        user_image_annotations = [ann for ann in annotations if ann['image_path'] == image_path]
        
        if not user_image_annotations:
            return None
        
        # Sort by timestamp and return latest
        return sorted(user_image_annotations, key=lambda x: x['timestamp'], reverse=True)[0]
