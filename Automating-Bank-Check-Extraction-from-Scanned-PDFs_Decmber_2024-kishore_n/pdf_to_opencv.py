from pdf2image import convert_from_path
import cv2
import os

# PDF and output directories
pdf_path = r"C:\Users\chikk_3\Downloads\pdf images.pdf"
output_dir = r"C:\Users\chikk_3\Desktop\op image"
poppler_path = r"C:\Users\chikk_3\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i, image in enumerate(images):
   
    page_output_dir = os.path.join(output_dir, f"page_{i+1}")
    if not os.path.exists(page_output_dir):
        os.makedirs(page_output_dir)
    
    image_path = os.path.join(page_output_dir, f"page_{i+1}.jpg")
    image.save(image_path, "JPEG")
    print(f"Saved: {image_path}")
    
  
    img = cv2.imread(image_path)
    img = cv2.resize(img, (600, 800)) 

    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        if area > 1000 and area < 50000:  
       
            x, y, w, h = cv2.boundingRect(contour)

            aspect_ratio = w / float(h)

            if 1.5 < aspect_ratio < 3.5: 
             
                check_img = img[y:y+h, x:x+w]
                check_image_path = os.path.join(page_output_dir, f"check_{idx+1}.jpg")
                cv2.imwrite(check_image_path, check_img)
                print(f"Saved check image: {check_image_path}")

    # Optionally, display the processed image with bounding boxes for checks
    # cv2.imshow(f"Processed Page {i+1}", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


