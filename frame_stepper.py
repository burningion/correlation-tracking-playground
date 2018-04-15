import pygame
import dlib
from skimage import io

pygame.init()
screenWidth = 1920
screenHeight = 1080
startFrame = 199
nowFrame = 199

# input directory is directory with image sequence
inputDirectory = './bowl_in/'
screen = pygame.display.set_mode((screenWidth, screenHeight))

red = (255, 0, 0)

running = True

currentFrame = pygame.image.load(inputDirectory + '%05d.png' % startFrame)
selecting = False
selection_start = [0, 0]
selection_end = [0, 0]

def draw_rect(screen, color, start, end, width=1):
    pygame.draw.rect(screen, color, (start[0], start[1], end[0] - start[0], end[1] - start[1]), width)
    return

def get_next_frame(trackers, startFrame, nowFrame):
    # if same, we need to initialize trackers
    if startFrame == nowFrame:
        img = io.imread(inputDirectory + '%05d.png' % nowFrame)
        for tracker in trackers:
            tracker['tracker'] = dlib.correlation_tracker()
            tracker['tracker'].start_track(img, dlib.rectangle(tracker['start'][0],
                                tracker['start'][1],
                                tracker['end'][0],
                                tracker['end'][1]))
    nowFrame += 1
    img = io.imread(inputDirectory + '%05d.png' % nowFrame)
    for tracker in trackers:
        tracker['tracker'].update(img)
        pos = tracker['tracker'].get_position()
        tracker['start'] = [int(pos.left()), int(pos.top())]
        tracker['end'] = [int(pos.right()), int(pos.bottom())]
    return trackers, nowFrame

trackers = []

while running:
    screen.blit(currentFrame, (0,0))
    for tracker in trackers:
        draw_rect(screen, red, tracker['start'], tracker['end'], 1)
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
                trackers.append({'start': selection_start, 'end': selection_end})
        elif event.type == pygame.KEYUP and event.key == ord('z'):
            trackers = trackers[:-1]
        elif event.type == pygame.KEYUP and event.key == ord('n'):
            trackers, nowFrame = get_next_frame(trackers, startFrame, nowFrame)
            currentFrame = pygame.image.load(inputDirectory + '%05d.png' % nowFrame)
    pygame.display.flip()