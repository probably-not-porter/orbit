import pygame
import random

pygame.init()
pygame.display.set_caption('Orbit')
gameIcon = pygame.image.load('orbitIcon.png')
pygame.display.set_icon(gameIcon)

screen_width = 800
screen_height = 600

# list for objects
sat_ls = []
stars_ls = []

for x in range(random.randint(20,40)):
    x_pos = random.randint(0,screen_width)
    y_pos = random.randint(0,screen_height)
    radius = random.randint(1,3)
    stars_ls.append([x_pos,y_pos,radius])


# data structure for objects
class Satellite:
    def __init__(self, x, y, v, r):
        self.x_pos = x
        self.y_pos = y
        self.velocity = v
        self.radius = r
        self.point_ls = []
        self.released = False

    def updatePosition(self):
        new_x = self.x_pos + self.velocity[0] // 2
        new_y = self.y_pos + self.velocity[1] // 2
        self.x_pos = new_x
        self.y_pos = new_y

    def updateVelocity(self):
        change_in_x = 0
        change_in_y = 0
        if self.x_pos < screen_width // 2:
            change_in_x = 1
        elif self.x_pos > screen_width // 2:
            change_in_x = -1
        
        if self.y_pos < screen_height // 2:
            change_in_y = 1
        elif self.y_pos > screen_height // 2:
            change_in_y = -1
    
        self.velocity = (self.velocity[0] + change_in_x, self.velocity[1] + change_in_y)

    def setVelocity(self, x_influence, y_influence):
        if x_influence > 100:
            x_influence = 100
        elif x_influence < -100:
            x_influence = -100
        if y_influence > 100:
            y_influence = 100
        elif y_influence < -100:
            y_influence = -100

        self.velocity = (x_influence // 10, y_influence // 10)


def main():
    # VARS
    running = True
    
    sun_radius = 20
    count = 0
    draw_line = False
    line_start = None

    # create game screen
    screen = pygame.display.set_mode([screen_width, screen_height])

    # main logic loop
    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                line_start = (x,y)
                draw_line = True
                sat_ls.append(Satellite(x,y,(0,0), 5))
                print("create obj")
            elif event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos
                sat_ls[-1].setVelocity(line_start[0] - x,line_start[1] - y)
                sat_ls[-1].released = True
                draw_line = False
                print("release obj")
        
        # DRAWING
        # draw background
        screen.fill((0,0,0))
        # draw mouse indicator line
        if draw_line == True:
            pygame.draw.line(screen, (255,0,0), line_start, pygame.mouse.get_pos(), 2)
        # draw sun
        pygame.draw.circle(screen, (50,50,50), (screen_width // 2, screen_height // 2), sun_radius+(count % 10))
        pygame.draw.circle(screen, (150,150,150), (screen_width // 2, screen_height // 2), sun_radius+(count % 5))
        pygame.draw.circle(screen, (200,200,200), (screen_width // 2, screen_height // 2), sun_radius+(count % 2))
        pygame.draw.circle(screen, (255,255,255), (screen_width // 2, screen_height // 2), sun_radius)

        # draw stars
        for star in stars_ls:
            pygame.draw.circle(screen, (150,150,150), (star[0],star[1]), star[2])

        # draw sats
        if count < 11:
            count = count + 1
        else:
            count = 0

        for sat in sat_ls:
            pygame.draw.circle(screen, (255,255,255), (sat.x_pos,sat.y_pos), sat.radius)

            # update position every nth frame
            if sat.released == True:
                if count == 10:
                    print(sat.velocity)
                    sat.updatePosition()
                    sat.updateVelocity()

        # Flip the display each frame
        pygame.display.flip()

    # when while loop ends, exit game
    pygame.quit()


main()