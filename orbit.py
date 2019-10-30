import pygame

pygame.init()
pygame.display.set_caption('Orbit')

def main():
    # VARS
    running = True
    screen_width = 800
    screen_height = 600
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
                print("create obj")
            elif event.type == pygame.MOUSEBUTTONUP:
                draw_line = False
                print("release obj")

        # draw background
        screen.fill((0,0,0))

        # draw mouse indicator line
        if draw_line == True:
            pygame.draw.line(screen, (255,0,0), line_start, pygame.mouse.get_pos(), 2)


        # Flip the display each frame
        pygame.display.flip()

    # when while loop ends, exit game
    pygame.quit()


main()