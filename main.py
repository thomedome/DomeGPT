import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
import sys

from modules import analyse

def attemptAnalysis():
    analyse.analyseImage()

def saveImage():
    drawing_area = pygame.Rect(0, 125, windowWidth, 350)
    drawing_surface = screen.subsurface(drawing_area).copy()

    try:
        pygame.image.save(drawing_surface, "cDraw.png")
    except Exception as e:
        print(f"Failed to save image: {e}")
        
# Init Pygame window
pygame.init()
windowWidth, windowHeight = 800, 600
screen = pygame.display.set_caption("DomeGPT")
screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()

# Setup Page
BackgroundCol = (0, 0, 0)
CircleCol = (255, 255, 255)
TextCol = (200, 200, 200)

drawn_points = []
circSize = 15

slider = Slider(screen, 400, 45, 300, 15, min=5, max=20, step=1, initial=15, handleRadius=10)

# Game Loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                drawn_points.clear()
            elif event.key == pygame.K_q:
                pygame.quit()
                running = False
            elif event.key == pygame.K_a:
                saveImage()
                attemptAnalysis()

    # Check if mouse down
    mousebuttons = pygame.mouse.get_pressed()

    if mousebuttons[0]:
        cPos = pygame.mouse.get_pos()
        if cPos[1] > 150 and cPos[1] < 500:
            drawn_points.append([cPos, circSize])

    screen.fill(BackgroundCol)

    # Draw all points
    for point, size in drawn_points:
        pygame.draw.circle(screen, CircleCol, point, radius=size)

    slider.draw()

    font = pygame.font.SysFont(None, 24)
    instructions = font.render("LMB to draw. C to clear page. Q to quit, A to Analyse.", True, TextCol)
    screen.blit(instructions, (15, 15))
    sizeNoti = font.render(f"Current Draw Size: {circSize}px", True, TextCol)
    screen.blit(sizeNoti, (15, 45))

    circSize = slider.getValue()
    # Tick at 240hz & process events
    pygame.display.flip()
    pygame_widgets.update(pygame.event.get())

    clock.tick(120)

pygame.quit()
sys.exit()