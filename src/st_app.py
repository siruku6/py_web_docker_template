"""
# My first app
Here's our first attempt at using data to create a table:
"""
import streamlit as st
import numpy as np
from PIL import Image
import cv2


uploaded_file = st.file_uploader("Choose a image file (only `.jpg`)")


if uploaded_file is not None:
    image: Image = Image.open(uploaded_file)

    # Display original image
    st.write("Original Image")
    st.image(image, caption="Input", use_column_width=True)

    file_name: str = uploaded_file.name
    file_path: str = f"./tmp/{file_name}"
    img_array: np.ndarray = np.array(image)

    # processing

    # Write image on Disk as file
    cv2.imwrite(file_path, cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))

    # Display converted image on UI
    image: np.ndarray = cv2.cvtColor(
        cv2.imread(file_path), cv2.COLOR_BGR2RGB
    )
    st.write("Converted Image")
    st.image(image, caption="Output", use_column_width=True)
