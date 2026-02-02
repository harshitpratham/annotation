# Example: Creating sample data for testing

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def create_sample_data():
    """Create sample data structure for testing the annotation tool."""
    
    # Create directories
    base_dir = Path(__file__).parent
    sorted_crops = base_dir / "sorted_crops"
    ground_truth = base_dir / "ground_truth"
    
    sorted_crops.mkdir(exist_ok=True)
    ground_truth.mkdir(exist_ok=True)
    
    # Sample words for each folder
    sample_data = {
        "31": ["hello", "world", "test", "sample", "data"],
        "32": ["python", "code", "streamlit", "annotation", "tool"],
        "33": ["word", "image", "label", "correct", "incorrect"]
    }
    
    # Create sample images and ground truth files
    for folder_name, words in sample_data.items():
        # Create folder
        folder_path = sorted_crops / folder_name
        folder_path.mkdir(exist_ok=True)
        
        # Create images
        for idx, word in enumerate(words):
            # Create a simple image with text
            img = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw text (using default font)
            text_position = (10, 15)
            draw.text(text_position, word, fill='black')
            
            # Save image
            img_path = folder_path / f"{idx:03d}.jpg"
            img.save(img_path)
            print(f"Created: {img_path}")
        
        # Create ground truth file
        gt_path = ground_truth / f"{folder_name}.txt"
        with open(gt_path, 'w') as f:
            f.write('\n'.join(words))
        print(f"Created: {gt_path}")
    
    print("\n✅ Sample data created successfully!")
    print(f"📁 Images: {sorted_crops}")
    print(f"📄 Labels: {ground_truth}")
    print("\nYou can now run: streamlit run app.py")

if __name__ == "__main__":
    create_sample_data()
