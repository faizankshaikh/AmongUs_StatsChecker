[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/faizankshaikh/amongus_statschecker/main/app.py)

# AmongUs_StatsChecker
Given a screenshot of official statistics, shows your individual performance and ranks you among the peers

## How to try out Statistics Checker

If you just want to get up-and-running with the project, you can check out [the hosted website using Streamlit Share](https://share.streamlit.io/faizankshaikh/amongus_statschecker/main/app.py). You can use the website as shown in the video below

![Demo](demo.gif)

If you are unsure of the screenshot to upload, you can find the official stats by logging in to the game and clicking on the button as shown  below

![steps_to_get_stats](steps_to_get_stats.jpeg)

On the other hand, if you are technically savvy, open the code in google Colab [by clicking on this link](https://colab.research.google.com/github/faizankshaikh/AmongUs_StatsChecker/blob/main/GetYourStats.ipynb), run all the cells in sequential order to host the website, and use the weblink created at the end of the notebook. 

You can change the code and try to print/plot more detailed stats using the pandas dataframe "df"

## How to collaborate on the Project

### For non-technical collaborators

If you want to collaborate on the project, you can help make the image parsing algorithm better by submitting your screenshot of the official stats. The more screenshots we have, the better we can train the algorithm. Please [submit your screenshots here](https://forms.gle/knaupar22huD2uJo8)

### For technical collaborators

Please refer CONTRIBUTING.md

Along with this, if you have any general suggestions / feedback, you can create a github issue or contact me directly on faizankshaikh at gmail.

## Acknowledgement

This project is built on the shoulders of awesome tools (and their dependencies ofcourse)

* [Streamlit](https://github.com/streamlit/streamlit)
* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [Pandas](https://github.com/pandas-dev/pandas)
