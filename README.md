![mii](assets/miis/right%20mii.png)
# 6 Feet Apart 
# How close are we? 

## About
Find the shortest chain of mutual follows between Twitch Users

## How to Run 
1. Download the dataset from https://snap.stanford.edu/data/twitch_gamers.html 
2. Unzip and place dataset in the 6 Feet Apart folder, no need for subfolders. 
3. Install dependencies: `pip install flask'`
4. Run the server: `.venv\Scripts\python.exe flask_app.py`
5. Open `index.html` with the Live Server extension 

## Dependencies 
- Backend: Python + Flask 
- Frontend: HTML/CSS/JS
- Visualization: vis.js

## Known Issues 
- Music + SFX not playing in demo 
- Flask needs to output a local host link before opening index.html 
