import os
import cv2
import easyocr
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


from glob import glob
from enum import Enum
from typing import Union
from io import BytesIO, StringIO
from scipy.stats import norm, percentileofscore

st.set_option("deprecation.showfileUploaderEncoding", False)

FILE_TYPES = ["png", "jpeg", "jpg"]
reader = easyocr.Reader(["en"])
PAGE_CONFIG = {"page_title": "StColab.io", "layout": "centered"}
st.set_page_config(**PAGE_CONFIG)
DATA_DIR = "/content/AmongUs_StatsChecker"


class FileType(Enum):
    IMAGE = "Image"


def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    if isinstance(file, BytesIO):
        return FileType.IMAGE


def get_segment_crop(img, tol=0, mask=None):
    if mask is None:
        mask = img > tol
    return img[np.ix_(mask.any(1), mask.any(0))]


def preprocess_image(user_name, img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    # Blur the image
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)

    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # find contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    mask = np.ones(img.shape[:2], dtype="uint8") * 255
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 0.2 * img.shape[0] * img.shape[1]:
            cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 0, 255), -1)

    res_final = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(mask))
    mask_out = cv2.subtract(cv2.bitwise_not(mask), thresh_inv)

    result = get_segment_crop(img, mask=cv2.bitwise_not(mask))

    width = 600
    height = 650
    dim = (width, height)

    # resize image
    result = cv2.resize(result, dim, interpolation=cv2.INTER_AREA)

    result = result[:-30, int(0.666 * result.shape[1]) :]

    # cv2_imshow(result)
    cv2.imwrite("processed_images/" + user_name + ".jpeg", result)


def get_reply(user_name, img_path):

    preprocess_image(user_name, img_path)

    result = reader.readtext(
        "processed_images/" + user_name + ".jpeg",
        decoder="greedy",
        detail=0,
        text_threshold=0.6,
        low_text=0.339,
        mag_ratio=2.5
    )

    stats = [user_name]
    for r in result:
        if r.isnumeric():
            stats.append(int(r))

    assert len(stats) == 19
    stats = stats + list(np.zeros(6, dtype="int"))
    df = pd.read_csv(os.path.join(DATA_DIR, "info.csv"))
    df = df.append(pd.Series(stats, df.columns), ignore_index=True)

    df["Tasks Completion Rate"] = df["All Tasks Completed"] * 100 / df["Games Started"]
    df["Game completion rate"] = df["Games Finished"] * 100 / df["Games Started"]
    df["Impostor win rate"] = (
        (
            df["Impostor Vote Wins"]
            + df["Impostor Kill Wins"]
            + df["Impostor Sabotage Wins"]
        )
        * 100
        / df["Times Impostor"]
    )
    df["Crewmate win rate"] = (
        (df["Crewmate Vote Wins"] + df["Crewmate Task Wins"])
        * 100
        / df["Times Crewmate"]
    )
    df["Total win rate"] = (
        (
            df["Crewmate Vote Wins"]
            + df["Crewmate Task Wins"]
            + df["Impostor Vote Wins"]
            + df["Impostor Kill Wins"]
            + df["Impostor Sabotage Wins"]
        )
        * 100
        / df["Games Started"]
    )
    df["Ejection Rate"] = df["Times Ejected"] * 100 / df["Games Started"]

    df.sort_values("Total win rate", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)

    row = df.loc[df["Player Name"] == user_name]

    "Info for Player", row["Player Name"].values[0]

    "Total win rate:", round(row["Total win rate"].values[0], 2)

    "Impostor win rate:", round(row["Impostor win rate"].values[0], 2)

    "Crewmate win rate:", round(row["Crewmate win rate"].values[0], 2)

    "All tasks completion rate:", round(row["Tasks Completion Rate"].values[0], 2)

    st.text("---\n\n")

    personal_winrate = row["Total win rate"].values[0]

    mean, stdev = (
        df[["Total win rate"]].mean().values[0],
        df[["Total win rate"]].std().values[0],
    )

    fig, ax = plt.subplots(1)

    x = range(30, 81)
    y = norm.pdf(x, mean, stdev)
    ax.plot(x, y)
    ax.fill_between(x, 0, y, color="cyan")
    ax.axvline(personal_winrate, color="red", linestyle="dashed", linewidth=1)
    ax.set_yticklabels([])
    ax.set_xlabel("Win Rate of Players")

    st.pyplot(fig, figsize=(10,10))

    percentile = percentileofscore(df[["Total win rate"]], personal_winrate)

    "You are better than", round(percentile), "% of the players"


def main():
    st.title("Among Us Stats Checker")
    menu = ["Home", "Leaderboard", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        user_name = st.text_input("Username", "")
        file = st.file_uploader("Upload file", type=FILE_TYPES)
        show_file = st.empty()
        if not file:
            show_file.info("Please upload a file of type: " + ", ".join(FILE_TYPES))
            return

        file_type = get_file_type(file)

        img_path = user_name + ".jpeg"

        f = open(img_path, "wb")
        f.write(file.getvalue())

        file.close()
        f.close()

        get_reply(user_name, img_path)


if __name__ == "__main__":
    main()
