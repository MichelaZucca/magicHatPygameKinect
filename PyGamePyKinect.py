import itertools
import pygame
from pygame.color import THECOLORS
from pykinect import nui
from pykinect.nui import JointId

VIDEO_WINSIZE = (640, 480)
KINECTEVENT = pygame.USEREVENT

screen = None
skeletons = []

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image


def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, VIDEO_WINSIZE[0], VIDEO_WINSIZE[1]) 
        curend = skeleton_to_depth_image(next, VIDEO_WINSIZE[0], VIDEO_WINSIZE[1])

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def draw_skeletons(skeletons):
    distance_min = 1000000
    index = -1
    for i, data in enumerate(skeletons):
        hip = data.SkeletonPositions[JointId.HipCenter]
        distance = (hip.x * hip.x) + (hip.y * hip.y) + (hip.z * hip.z)
        if (distance > 0) and (distance < distance_min):
            distance_min = distance
            index = i
    
    if index >= 0:
        data = skeletons[index]
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], VIDEO_WINSIZE[0], VIDEO_WINSIZE[1]) 
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)

        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM)
        draw_skeleton_data(data, index, RIGHT_ARM)
        draw_skeleton_data(data, index, LEFT_LEG)
        draw_skeleton_data(data, index, RIGHT_LEG)

def video_frame_ready(frame):
    frame.image.copy_bits(screen._pixels_address)
    draw_skeletons(skeletons)
    pygame.display.update()

def post_frame(frame):
    try:
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
    except:
        # event queue full
        pass

def main():
    """Initialize and run the game"""
    pygame.init()

    # Initialize PyGame
    global screen
    global skeletons
    screen = pygame.display.set_mode(VIDEO_WINSIZE, 0, 32)

    pygame.display.set_caption("PyKinect Video Example")
    background = pygame.image.load('project/images/background.jpg');
    background = pygame.transform.scale(background, (640, 480))
    backgroundrect = background.get_rect()

    
    angle = 0
    with nui.Runtime() as kinect:
        kinect.skeleton_engine.enabled = True
        kinect.video_frame_ready += video_frame_ready
        kinect.skeleton_frame_ready += post_frame
        # peut etre pas besoin
        # kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)        

        print('Controls: ')
        print('     u - Increase elevation angle')
        print('     j - Decrease elevation angle')
        
        # Main game loop
        done = False
        while not done:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == KINECTEVENT:
                skeletons = event.skeletons
                screen.blit(background, backgroundrect)
                draw_skeletons(skeletons)
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    break
                elif event.key == pygame.K_u:
                    kinect.camera.elevation_angle = kinect.camera.elevation_angle + 1
                elif event.key == pygame.K_j:
                    kinect.camera.elevation_angle = kinect.camera.elevation_angle - 1
                elif event.key == pygame.K_x:
                    kinect.camera.elevation_angle = 0
    
    pygame.quit()