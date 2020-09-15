# Real Time Background Substitution

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Requires.io](https://img.shields.io/requires/github/umangraval/Real-time-background-masking)

There many situations in daily life that people had to
move to a particular place to do a video call when it's
really important to do one. But not always we find a place
when it's an emergency. We use a video capturing device (
camera/ webcam in this case ) to acquire images for real-
time analysis and processing. Histogram Equalization is
used to enhance the video quality as the frames might have
low contrast and resolution. Segmentation is done to
identify the foreground and masking is done to replace the
background with another background of our choice.
<p align="center">
  <img align="center" width="500" height="450" src="./app/static/vector.png">
</p>

## Running App

Activate virtual environment
```
python3 -m venv env
source env/bin/activate
```

Install Dependancies
```
pip install -r requirements
python app.py
```

## Testing BG-code

```
python test.py
```

## Results
### Background mask
<img src="app/static/Screenshot from 2020-06-06 10-54-23.png" width="300">

### After Applying mask
<img src="app/static/Screenshot from 2020-06-06 10-50-05.png" width="300">

### After Histogram Equalization
<img src="app/static/Screenshot from 2020-06-06 11-43-00.png" width="300">
