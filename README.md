# Analyticat
## Google analytics in real life

Analyticat was built during the StirHack 2017 [MLH](https://mlh.io) event, over the course of 24 hours.

## What is Analyticat designed to do?

- Register IoT video sources to gain analytics about your customers; including:
  - a measure of recurring customers on an individual, but anonymous level, using AWS-powered facial recognition (you will not be able to track individual customers)
  - _estimate_ demographics including gender, age etc.
- View analytics in a clean dashboard. You can view analytics over various discrete timesteps (hours, days, weeks, etc.) for your registered video sources (or groups thereof).
- Utilise our own REST API so that you can use your own analytics data for something more unique!

![user interface mockup](http://i.imgur.com/zmf3lQC.png)

## Current Functionality

- The [analyticat.net](https://analyticat.net) frontend mockup is available to view.
- Our REST API is somewhere in the region of 50% finished:
  - finished:
    - [X] emotional and sentiment analysis of people in uploaded images
    - [X] check similarity between two people in uploaded images
  - not finished:
    - demographic analysis (age, gender, etc.)
    - coordination and interfacing between the IoT layer, the front end and our AWS MySQL database
- We currently have a [camera watcher](https://github.com/AdamHirst/StirHack/blob/master/preproc/watcher.py) which continually watches over the default camera - whenever a face is detected the image is saved (but would be uploaded via our REST API upon completion).
