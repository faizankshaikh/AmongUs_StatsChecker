The project as of now is simplistic and can be improved algorithmically / UI wise, or can have a better statistical analysis. If you're interested in collaboration, you can contribute to the improvements noted. Here's a non-exhaustive list of the TODOs

* UI improvements

- [ ] Better display of Individual Statistics
- [ ] Better display of Aggregate Statistics
- [ ] Separate page for Current Leaderboard (ranked according to win-rates)


* Algorithmic / Code Improvements

- [ ] As of now, the project uses a pretrained Deep Learning model (uses EasyOCR). In order to improve the performance, the model can be finetuned on this particular data which could give a substantial boost in the accurate detection of the numbers in the screenshots
- [ ] Hypothetically, an object oriented paradigm could make the code approachable for new contributions. At the moment, the code is simplistic and mainly functional


* Hosting and Security

- [ ] For now, the web service is hosted temporarily on Google Colab because of logistic difficulties (requirement of GPU system). Ideally it could be hosted on a cloud service for a permanent access to the website
- [ ] The code as of now has minimal unit testing, which is unthinkable for a deployable project
