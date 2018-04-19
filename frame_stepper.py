import pygame
import dlib
from skimage import io

import json
import argparse

parser = argparse.ArgumentParser(description='Correlation tracker playground')
parser.add_argument('-f', '--filename', type=str, help='Correlation JSON to load')
args = parser.parse_args()

pygame.init()
screenWidth = 1920
screenHeight = 1080
startFrame = 557
nowFrame = 557

# input directory is directory with image sequence
# in this example it'd be ./bowl_in/00001.png through whatever
inputDirectory = './bowl_in/'

screen = pygame.display.set_mode((screenWidth, screenHeight))

red = (255, 0, 0)

running = True

currentFrame = pygame.image.load(inputDirectory + '%05d.png' % startFrame)
selecting = False
selection_start = [0, 0]
selection_end = [0, 0]

def draw_rect(screen, color, start, end, width=1):
    pygame.draw.rect(screen,
                     color,
                     (start[0], start[1], end[0] - start[0], end[1] - start[1]),
                     width)
    return

def get_tracker(nowFrame, start, end):
    tracker = {'start': start, 'end': end, 'currentStart': start, 'currentEnd': end, 'startFrame': nowFrame, 'endFrame': False}

    img = io.imread(inputDirectory + '%05d.png' % nowFrame)
    tracker['tracker'] = dlib.correlation_tracker()
    tracker['tracker'].start_track(img, dlib.rectangle(tracker['start'][0],
                                                       tracker['start'][1],
                                                       tracker['end'][0],
                                                       tracker['end'][1]))
    print("tracker added at start: %s end: %s and frame: % i" % (tracker['start'], tracker['end'], nowFrame))
    return tracker

def get_next_frame(trackers, startFrame, nowFrame):
    nowFrame += 1
    print('current frame: %i' % nowFrame)
    img = io.imread(inputDirectory + '%05d.png' % nowFrame)
    for tracker in trackers:
        if tracker['startFrame'] > nowFrame:
            continue
        elif tracker['startFrame'] == nowFrame:
            trackie = get_tracker(nowFrame, tracker['start'], tracker['end'])
            tracker['tracker'] = trackie['tracker']
            tracker['currentStart'] = tracker['start']
            tracker['currentEnd'] = tracker['end']
        else:
            tracker['tracker'].update(img)
            pos = tracker['tracker'].get_position()
            tracker['currentStart'] = [int(pos.left()), int(pos.top())]
            tracker['currentEnd'] = [int(pos.right()), int(pos.bottom())]
    return trackers, nowFrame

def save_trackers(trackers):
    # delete tracker objects
    for tracker in trackers:
        del tracker['tracker']
    with open('trackers.json', 'w') as out:
        json.dump(trackers, out, indent=4)
    print('wrote trackers to disk')
    return

def load_trackers(filename):
    with open(filename) as json_file:
        trackers = json.load(json_file)
        for tracker in trackers:
            tracker['currentStart'] = tracker['start']
            tracker['currentEnd'] = tracker['end']
        return trackers

if args.filename:
    trackers = load_trackers(args.filename)
else:
    trackers = []

while running:
    screen.blit(currentFrame, (0,0))
    for tracker in trackers:
        if nowFrame >= tracker['startFrame']:
            draw_rect(screen, red, tracker['currentStart'], tracker['currentEnd'], 1)
    if selecting:
        draw_rect(screen, red, selection_start, selection_end, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not selecting:
                selecting = True
                selection_start = event.pos
                selection_end = event.pos
        elif event.type == pygame.MOUSEMOTION:
            if selecting:
                selection_end = event.pos
                draw_rect(screen, red, selection_start, selection_end, 1)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if selecting:
                selecting = False
                trackers.append(get_tracker(nowFrame, selection_start, selection_end))
        elif event.type == pygame.KEYUP and event.key == ord('z'):
            trackers = trackers[:-1]
        elif event.type == pygame.KEYUP and event.key == ord('n'):
            trackers, nowFrame = get_next_frame(trackers, startFrame, nowFrame)
            currentFrame = pygame.image.load(inputDirectory + '%05d.png' % nowFrame)
        elif event.type == pygame.KEYUP and event.key == ord('s'):
            save_trackers(trackers)
    pygame.display.flip()
