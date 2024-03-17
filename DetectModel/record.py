from ultralytics import YOLO
import easyocr
import cv2
import os
import time
from os import listdir
from pathlib import Path

reader = easyocr.Reader(['en'], gpu=True)

def perform_ocr_on_image(img):
  try:
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    results = reader.readtext(gray_img)

    text = ""
    if len(results) == 1:
      text = results[0][1] 
    elif results:  
      for res in results:
        if res[2] > 0.2: 
          text = res[1]
          break  

    return text
  except Exception as e:
    print(f"Error performing OCR: {e}")
    return ""  
  

base_folder = "runs/detect"
def find_newest_folder(base_folder):

  folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
  

  folders.sort(key=lambda f: os.path.getmtime(os.path.join(base_folder, f)), reverse=True)
  
  if folders:
    return os.path.join(base_folder, folders[0])
  else:
    return None

def process_images(folder_path):
  # Loop through each subfolder
  for subfolder in os.listdir(folder_path):
    subfolder_path = os.path.join(folder_path, subfolder)
    
    # Check if it's a directory
    if os.path.isdir(subfolder_path):
      # Recursively process images within the subfolder
      process_images(subfolder_path)
    else:
      # Check if it's an image based on extension (modify as needed)
      if subfolder.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(folder_path, subfolder)
        img = cv2.imread(image_path)  # Load the image using OpenCV
        if img is None:
            print(f"Error reading image: {image_path}")
            continue  # Skip to the next image if loading fails
        try:
            extracted_text = perform_ocr_on_image(img)  # Pass the loaded image
            print(extracted_text)
        except Exception as e:
            print(f"Error processing image: {image_path}\n{e}")

if __name__ == "__main__":
  while True:
    newest_folder_path = find_newest_folder(base_folder)
    if newest_folder_path:
        process_images(newest_folder_path)
    else:
        print("No new folder found.")

