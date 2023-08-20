"""
# My first app
Here's our first attempt at using data to create a table:
"""
from typing import List
import numpy as np
import streamlit as st
from PIL import Image
import cv2


def image_uploading_func():
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


# Using object notation
with st.sidebar:
    sidebar_selectbox = st.selectbox(
        "What would you like to do?",
        ("Touch select box", "Upload image", "Mobile phone")
    )
    st.write("You selected: ", sidebar_selectbox)


if sidebar_selectbox == "Upload image":
    uploaded_file = st.file_uploader("Choose a image file (only `.jpg`)")
    if uploaded_file is not None:
        image_uploading_func()


if sidebar_selectbox == "Touch select box":
    option = st.selectbox(
        "select box:",
        [1, 2, 3]
    )
    st.write("You selected: ", f"{option}: {sidebar_selectbox}")

    names: List[str] = ["Lita", "Kile", "Judy", "Phoenix", "Popo"]
    checkboxes = {
        name: None
        for name in names
    }
    for name in names:
        checkboxes[name] = st.checkbox(name)

    msg: str = "Hello, "
    for name in names:
        if checkboxes[name]:
            msg += name + ", "

    st.write(msg)
