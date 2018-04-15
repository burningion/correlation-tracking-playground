# Correlation Tracking Playground

![example](https://github.com/burningion/correlation-tracking-playground/raw/master/images/example.png)

Playground for correlation tracking in dlib with Pygame

This is a work in progress, and will go along with a blog post on doing correlation tracking in Python with dlib.

In the meantime, if you want to take a look, this project will open up a directory with an image sequence created with ffmpeg (something like `ffmpeg -i yourvideo outputdirectory/%05d.png`), and let you see how selected regions will be tracked.

You click and drag to create selection rectangles, and press `z` to delete the most recent selection rectangle. 

Once you've selected some regions to track, press `n` to move to the next frame.

I'm using this playground to explore video with automatic masking, something like what's in [this](https://www.instagram.com/p/BhNlkD-jvm1/) instagram post, along with Mask R-CNN.
