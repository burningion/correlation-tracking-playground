# Correlation Tracking Playground

![example](https://github.com/burningion/correlation-tracking-playground/raw/master/images/example.png)

Playground for correlation tracking in dlib with Pygame

This is a work in progress, and will go along with a blog post on doing correlation tracking in Python with dlib.

In the meantime, if you want to take a look, this project will open up a directory with an image sequence created with ffmpeg (something like `ffmpeg -i yourvideo outputdirectory/%05d.png`), and let you see how selected regions will be tracked.

You click and drag to create selection rectangles, and press `z` to delete the most recent selection rectangle. 

Once you've selected some regions to track, press `n` to move to the next frame.

Once you're okay with the correlation trackers and their tracking over time, press `s` to save out a JSON file with the coordinates and frame numbers of your trackers.

```json
[
    {
        "start": [
            78,
            17
        ],
        "end": [
            306,
            145
        ],
        "startFrame": 199,
        "endFrame": false
    },
    {
        "start": [
            1066,
            61
        ],
        "end": [
            1111,
            95
        ],
        "startFrame": 217,
        "endFrame": false
    }
]
```

I'm using this playground to explore video with automatic masking, something like what's in [this](https://www.instagram.com/p/BhNlkD-jvm1/) instagram post, along with Mask R-CNN.
