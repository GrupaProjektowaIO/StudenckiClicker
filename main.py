import pygame

# objective pastelowe w kolorze statow
# przy ryzyku przegranej, wystapi minigierka, ktora pozwoli odzyskac troche statystyki (gierka a la dinozaur z Chroma)
# kiedy pasek postepu czynnosci to krysztalki zostaja przeniesione do odpowiedniej statystyki
# dbamy glownie o czas, a statystyki 1. i 2. sluza jako buffor
# SESJA

# tutoriale: formatowanie textu, maski, sound effects, przejscia pomiedzy ekranami,

pygame.init()
screen = pygame.display.set_mode([1920/2, 1080/2], pygame.RESIZABLE)
pygame.display.set_caption("Studencki")
pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

board = pygame.image.load("sprites/board.png")

healthbar = pygame.image.load("sprites/health_bar.png")
sanitybar = pygame.image.load("sprites/sanity_bar.png")
timebar = pygame.image.load("sprites/time_bar.png")

healthicon = pygame.image.load("sprites/health_icon.png")
sanityicon = pygame.image.load("sprites/sanity_icon.png")
timeicon = pygame.image.load("sprites/time_icon.png")

objective_panel = pygame.image.load("sprites/objective_panel.png")
party = pygame.image.load("sprites/objective_icons/party.png")

objective_panel_arrow = pygame.image.load("sprites/objective_panel_arrow.png")

def centerAnchor(width, height, percent_x=0.5, percent_y=0.5,
                 offset_x=0, offset_y=0):
    return pygame.Rect(screen.get_width() * percent_x - width / 2 + offset_x,
                       screen.get_height() * percent_y - height / 2 + offset_y,
                       width, height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    screen.blit(board, centerAnchor(415, 256, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(healthbar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 - 70))
    screen.blit(sanitybar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timebar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 + 70))
    screen.blit(healthicon, centerAnchor(56, 65, 0.5, 0, 0, 256 // 2 + 20 - 70))
    screen.blit(sanityicon, centerAnchor(57, 58, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timeicon, centerAnchor(49, 56, 0.5, 0, 0, 256 // 2 + 20 + 70))

    #screen.blit(objective_panel, centerAnchor(207, 128, 0, 0.25, 270/2 + 10))
    #screen.blit(party, centerAnchor(32, 32, 0, 0.25, 270/2 + 10, -64))
    screen.blit(objective_panel_arrow, centerAnchor(778, 466, 0, 0.25, 778 / 2 + 10))

    screen.blit(objective_panel, centerAnchor(207, 128, 0, 0.5, 270 / 2 + 10))
    screen.blit(objective_panel, centerAnchor(207, 128, 0, 0.75, 270 / 2 + 10))

    screen.blit(objective_panel, centerAnchor(207, 128, 1, 0.25, -(270 / 2 + 10)))
    screen.blit(objective_panel, centerAnchor(207, 128, 1, 0.5, -(270 / 2 + 10)))
    screen.blit(objective_panel, centerAnchor(207, 128, 1, 0.75, -(270 / 2 + 10)))

    pygame.display.flip()
pygame.quit()