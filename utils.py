import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
import os
from datetime import datetime

# Create directory for saving images if it doesn't exist
IMAGES_DIR = "generated_images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def save_base64_image(base64_str: str, prefix: str = "image") -> str:
    """
    Save a base64 encoded image to file
    Args:
        base64_str: Base64 encoded image string
        prefix: Prefix for the filename (default: 'image')
    Returns:
        str: Path to the saved image file
    """
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(IMAGES_DIR, filename)
    
    # Decode and save image
    img_data = base64.b64decode(base64_str)
    with open(filepath, 'wb') as f:
        f.write(img_data)
    
    return filepath

def calculate_average(*numbers):
    """
    Calculate the average of given numbers
    Args:
        *numbers: Variable length argument of numbers
    Returns:
        float: Average of the numbers
    """
    return sum(numbers) / len(numbers)

def draw_sine_wave(amplitude=1.0, frequency=1.0) -> dict:
    """
    Draw a sine wave with given parameters
    Args:
        amplitude: Amplitude of the sine wave
        frequency: Frequency of the sine wave
    Returns:
        dict: Dictionary containing base64 image string and saved file path
    """
    x = np.linspace(0, 10, 1000)
    y = amplitude * np.sin(2 * np.pi * frequency * x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title(f'Sine Wave (Amplitude: {amplitude}, Frequency: {frequency})')
    plt.grid(True)
    
    # Save plot to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Convert to base64
    base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Save to file
    filepath = save_base64_image(base64_str, "sine_wave")
    
    return {
        "base64_image": base64_str,
        "saved_path": filepath
    }

def generate_color_gradient(start_color, end_color, width=300, height=100) -> dict:
    """
    Generate an image with a color gradient
    Args:
        start_color: Tuple of RGB values for start color
        end_color: Tuple of RGB values for end color
        width: Width of the image
        height: Height of the image
    Returns:
        dict: Dictionary containing base64 image string and saved file path
    """
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    for x in range(width):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * x / width)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * x / width)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * x / width)
        
        for y in range(height):
            pixels[x, y] = (r, g, b)
    
    # Convert to base64
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # Save to file
    filepath = save_base64_image(base64_str, "gradient")
    
    return {
        "base64_image": base64_str,
        "saved_path": filepath
    }

def list_generated_images() -> list:
    """
    List all generated images in the images directory
    Returns:
        list: List of image file paths
    """
    if not os.path.exists(IMAGES_DIR):
        return []
    return [os.path.join(IMAGES_DIR, f) for f in os.listdir(IMAGES_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]

def clear_generated_images() -> int:
    """
    Delete all generated images
    Returns:
        int: Number of files deleted
    """
    if not os.path.exists(IMAGES_DIR):
        return 0
    
    count = 0
    for file in os.listdir(IMAGES_DIR):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            os.remove(os.path.join(IMAGES_DIR, file))
            count += 1
    return count

def fibonacci(n):
    """
    Generate Fibonacci sequence up to n numbers
    Args:
        n: Number of Fibonacci numbers to generate
    Returns:
        list: List of Fibonacci numbers
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def text_statistics(text):
    """
    Analyze text and return various statistics
    Args:
        text: Input text string
    Returns:
        dict: Dictionary containing text statistics
    """
    words = text.split()
    return {
        'word_count': len(words),
        'char_count': len(text),
        'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
        'sentence_count': text.count('.') + text.count('!') + text.count('?')
    } 