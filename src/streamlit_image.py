r"""
Created on 21/9/2021 5:27 PM
@author: jiahuei

streamlit run streamlit_image.py
"""
import numpy as np
import cv2
import streamlit as st
from utils import streamlit_uploaded_file_to_cv2

MIN_MATCH_COUNT = 10


def match(query, gallery):
    # Initiate SIFT detector
    sift = cv2.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(query, None)
    kp2, des2 = sift.detectAndCompute(gallery, None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = [m for m, n in matches if m.distance < 0.7 * n.distance]
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w, d = query.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        gallery = cv2.polylines(gallery, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        gallery = None
    return gallery


def main():
    st.title("OpenCV Feature Matching + Homography")

    # Query image
    upload_help = "Provide a query image"
    uploaded_file = st.sidebar.file_uploader(upload_help)
    if uploaded_file is None:
        st.info(f"{upload_help}, by uploading it in the sidebar")
        return
    query_img = streamlit_uploaded_file_to_cv2(uploaded_file)

    # Gallery / training image
    upload_help = "Provide a gallery image (that potentially contains the query image)"
    uploaded_file = st.sidebar.file_uploader(upload_help)
    if uploaded_file is None:
        st.info(f"{upload_help}, by uploading it in the sidebar")
        return
    gallery_img = streamlit_uploaded_file_to_cv2(uploaded_file)

    # Main panel
    with st.spinner("Computing ..."):
        gallery_img = match(query_img, gallery_img)

    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        st.header("Query image")
        st.image(query_img, channels="BGR")

    with col2:
        st.header("Gallery image (output)")
        st.image(gallery_img, channels="BGR")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
