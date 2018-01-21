# coding=utf-8
import itertools
import pygame
from pygame.color import THECOLORS
from pykinect import nui
from pykinect.nui import JointId
from random import randint

SIZE_WINDOW = (800, 600)

VIDEO_WINSIZE = SIZE_WINDOW
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


def draw_skeleton_data(pSkelton, index, positions, width=4):
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
        pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons=frame.SkeletonData))
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
    background = pygame.image.load('images/background.jpg');
    background = pygame.transform.scale(background, SIZE_WINDOW)
    backgroundrect = background.get_rect()

    # Chapeau du magicien
    hat = pygame.image.load('images/magicHat.png')
    hat = pygame.transform.scale(hat, (70, 70))
    hat = pygame.transform.rotate(hat, 180)
    hatrect = hat.get_rect()
    hatrect.center = (300, 360)

    abovehatrect = pygame.Rect(hatrect.x, hatrect.y - 100, 100, 100)

    stars = pygame.image.load('images/stars.gif')
    stars = pygame.transform.scale(stars, (100, 100))
    starsrect = stars.get_rect();
    srcImage = ' '

    # image nuage
    srcnuage = 'images/nuage.png'
    imgnuage = pygame.image.load(srcnuage)
    imgnuage = pygame.transform.scale(imgnuage, (140, 140))
    imgnuagerect = imgnuage.get_rect()

    # Controle
    wasInHat = False
    isAboveHat = False
    counter = 0  # temps d'affichage de l'objet magique sortie du chapeau
    timeMax = 60  # temps maximum d'affichage
    randomImage = 1
    delta = 0.5
    randomActif = False
    no = 1
    isHatOnHead = True
    timeToSwitchHead = 0
    timeToSwitchHeadMax = 60

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
        screen.blit(background, backgroundrect)
       # screen.blit(hat, hatrect)
        pygame.display.update()
        while not done:
            screen.blit(background, backgroundrect)
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                done = True
                break
            elif event.type == KINECTEVENT:
                skeletons = event.skeletons

                # Dessiner le squellette derrière le chapeau
                if(not isHatOnHead):
                    draw_skeletons(skeletons)

                for skeleton in skeletons:
                    if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                        leftHand = skeleton.SkeletonPositions[JointId.HandLeft];
                        rightHand = skeleton.SkeletonPositions[JointId.HandRight];
                        head = skeleton.SkeletonPositions[JointId.Head];

                        #Coordonnées des mains
                        leftHandCoords = skeleton_to_depth_image(leftHand, VIDEO_WINSIZE[0], VIDEO_WINSIZE[1])
                        rightHandCoords = skeleton_to_depth_image(rightHand, VIDEO_WINSIZE[0], VIDEO_WINSIZE[1])
                        headCoords = skeleton_to_depth_image(head, VIDEO_WINSIZE[0], VIDEO_WINSIZE[1])

                        if (isHatOnHead):
                            hatrect.center = (headCoords[0], headCoords[1] - 30)
                        else:
                            hatrect.center = (leftHandCoords[0], leftHandCoords[1])

                        #Chapeau sur la tête ou pas
                        if(isHatOnHead):
                            screen.blit(hat, hatrect)
                            if(hatrect.collidepoint(leftHandCoords) and timeToSwitchHead > timeToSwitchHeadMax):
                                timeToSwitchHead = 0;
                                hatrect.center = (leftHandCoords[0], leftHandCoords[1])
                                hat = pygame.transform.rotate(hat, 180)
                                isHatOnHead = False
                                counter = 0
                                wasInHat = False
                                isAboveHat = False
                                randomActif = True
                        else:
                            screen.blit(hat, hatrect)
                            if(hatrect.collidepoint(headCoords) and timeToSwitchHead > timeToSwitchHeadMax):
                                timeToSwitchHead = 0
                                isHatOnHead = True
                                hat = pygame.transform.rotate(hat, 180)
                            else:

                                # Le chapeau suit la main gauche
                                # hatrect.center = (leftHandCoords[0], leftHandCoords[1])
                                abovehatrect.center = (hatrect.x, hatrect.y - 100)

                                #Si on a la main dans le chapeau
                                if ((not wasInHat)and hatrect.collidepoint(rightHandCoords)):
                                    wasInHat = True
                                    randomActif = True
                                #Detecte si on change de trajectoires lorsque l'on sort la main du chapeau
                                if(wasInHat and (rightHandCoords[0] - hatrect.center[0] > delta) and hatrect.center[0] - rightHandCoords[0] > delta):
                                    wasInHat = False
                                #Si on est assez haut du chapeau, on fait apparaitre une image
                                if (wasInHat and (not isAboveHat ) and abovehatrect.collidepoint(rightHandCoords[0], rightHandCoords[1])):
                                    isAboveHat = True
                                    # tirage de l'image aléatoire
                                    if randomActif :
                                        no = randint(1, 8)
                                        randomActif = False
                                        # chemin d'accès de l'image
                                        srcImage = 'images/' + str(no) + '.png'
                                        img = pygame.image.load(srcImage)
                                        img = pygame.transform.scale(img, (75, 75))
                                        imgrect = img.get_rect()
                                # Si on a tiré un objet, on l'accroche a la main droite
                                if(isAboveHat and wasInHat):
                                    starsrect.center = (rightHandCoords[0], rightHandCoords[1])
                                    imgrect.center = (rightHandCoords[0], rightHandCoords[1])
                                    screen.blit(stars, starsrect)
                                    screen.blit(img, imgrect)
                                    # hatrect.center(LEFT_ARM)
                                    counter += 1
                                #Apres un certain temps, on reinitialise les variables pour pouvoir retirer un objet
                                if (counter > timeMax):
                                    imgnuagerect.center = (rightHandCoords[0], rightHandCoords[1])
                                    screen.blit(imgnuage, imgnuagerect)
                                    if(counter > timeMax + 20 ):
                                        counter = 0
                                        wasInHat = False
                                        isAboveHat = False
                                        randomActif = True

                        #screen.blit(hat, hatrect)
                if(isHatOnHead):
                    draw_skeletons(skeletons)
                timeToSwitchHead = timeToSwitchHead +1
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


if __name__ == '__main__':
    main()
