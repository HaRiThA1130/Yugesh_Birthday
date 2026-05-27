import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

os.chdir(r'c:\Users\HP\OneDrive\Desktop\Yugesh_Birthday')

print("Creating Birthday Surprise Video for Yugesh...")
print("=" * 60)

# Video settings
video_width = 1920
video_height = 1080
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Create video writer
output_path = "birthday_surprise_video.mp4"
out = cv2.VideoWriter(output_path, fourcc, fps, (video_width, video_height))

def create_text_frame(text, duration_sec=3, bg_color=(102, 126, 234), text_color=(255, 255, 255), secondary_text=""):
    """Create frames with text"""
    frames = []
    frames_count = int(fps * duration_sec)

    for _ in range(frames_count):
        # Create blank frame
        frame = np.full((video_height, video_width, 3), bg_color, dtype=np.uint8)

        # Convert to PIL for better text rendering
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        # Try to use a nice font, fallback to default
        try:
            font_large = ImageFont.truetype("arial.ttf", 100)
            font_small = ImageFont.truetype("arial.ttf", 50)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Draw main text
        text_bbox = draw.textbbox((0, 0), text, font=font_large)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (video_width - text_width) // 2
        draw.text((text_x, video_height // 3), text, fill=text_color, font=font_large)

        # Draw secondary text if provided
        if secondary_text:
            try:
                text_bbox2 = draw.textbbox((0, 0), secondary_text, font=font_small)
                text_width2 = text_bbox2[2] - text_bbox2[0]
                text_x2 = (video_width - text_width2) // 2
                draw.text((text_x2, video_height * 2 // 3), secondary_text, fill=(200, 200, 200), font=font_small)
            except:
                pass

        # Convert back to OpenCV format
        frame_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        frames.append(frame_cv)

    return frames

def add_image_frames(image_path, duration_sec=4):
    """Add image with proper scaling"""
    frames = []

    if not os.path.exists(image_path):
        print("Image not found: " + image_path)
        return frames

    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Could not read: " + image_path)
            return frames

        # Get original dimensions
        h, w = img.shape[:2]
        aspect_ratio = w / h

        # Calculate new dimensions to fit in video
        if aspect_ratio > (video_width / video_height):
            new_w = video_width
            new_h = int(video_width / aspect_ratio)
        else:
            new_h = video_height
            new_w = int(video_height * aspect_ratio)

        # Resize image
        img_resized = cv2.resize(img, (new_w, new_h))

        # Create frame with black background
        frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)

        # Center the image
        x_offset = (video_width - new_w) // 2
        y_offset = (video_height - new_h) // 2

        frame[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = img_resized

        # Create multiple frames for duration
        frames_count = int(fps * duration_sec)
        for _ in range(frames_count):
            frames.append(frame.copy())

        print("  [OK] Added: " + image_path)
        return frames

    except Exception as e:
        print("Error processing " + image_path + ": " + str(e))
        return frames

print("\nScreen 1: Creating intro screen...")
frames = create_text_frame("ARE YOU YUGESH?", duration_sec=4,
                          bg_color=(102, 126, 234),
                          secondary_text="YES")
for frame in frames:
    out.write(frame)
print("[OK] Intro created")

print("\nScreen 2: Creating welcome screen...")
frames = create_text_frame("WELCOME YUGESH!", duration_sec=3,
                          bg_color=(102, 126, 234),
                          secondary_text="Your Birthday Surprise Awaits...")
for frame in frames:
    out.write(frame)
print("[OK] Welcome screen created")

print("\nScreen 3: Adding childhood photos...")
childhood_photos = ["child1.jpeg", "child2.jpeg"]
for photo in childhood_photos:
    frames = add_image_frames(photo, duration_sec=4)
    for frame in frames:
        out.write(frame)

print("\nScreen 4: Adding together photos...")
together_photos = ["me,y1.jpeg", "me,y2.jpeg", "me,y3.jpeg"]
for photo in together_photos:
    frames = add_image_frames(photo, duration_sec=4)
    for frame in frames:
        out.write(frame)

print("\nScreen 5: Adding Yugesh's photos...")
yugesh_photos = ["yugesh1.jpeg", "yugesh2.jpeg", "yugesh3.jpeg"]
for photo in yugesh_photos:
    frames = add_image_frames(photo, duration_sec=4)
    for frame in frames:
        out.write(frame)

print("\nScreen 6: Adding birthday messages...")
messages = [
    ("HAPPY BIRTHDAY YUGESH!", "Your Best Friend"),
    ("Another year older, infinitely wiser!", "Because you're awesome"),
    ("May your day be amazing!", "Wishing you the best"),
    ("Here's to being extraordinary!", "Forever grateful for you"),
]

for i, (message, author) in enumerate(messages):
    # Alternate colors for messages
    colors = [(240, 147, 251), (131, 56, 236), (255, 136, 117), (76, 175, 80)]
    frames = create_text_frame(message, duration_sec=3,
                              bg_color=colors[i % len(colors)],
                              secondary_text="~ " + author)
    for frame in frames:
        out.write(frame)
    print("  [OK] Added message: " + message[:40] + "...")

print("\nScreen 7: Creating final celebration screen...")
frames = create_text_frame("HAPPY BIRTHDAY!", duration_sec=5,
                          bg_color=(17, 153, 142),
                          secondary_text="May your year be filled with joy and success!")
for frame in frames:
    out.write(frame)
print("[OK] Final screen created")

# Release the video writer
out.release()

print("\n" + "=" * 60)
print("[SUCCESS] VIDEO CREATED!")
print("Location: " + os.path.abspath(output_path))
print("Duration: ~55 seconds")
print("Resolution: " + str(video_width) + "x" + str(video_height))
print("=" * 60)
print("\nReady to surprise Yugesh!\n")
