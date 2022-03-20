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

#fonty
font = pygame.font.SysFont('Comic Sans MS, Arial, Times New Roman', 16, bold=True, italic=True)
text = font.render("Zadania", True, (255, 255, 255))

board = pygame.image.load("sprites/board.png")

healthbar = pygame.image.load("sprites/health_bar.png")
sanitybar = pygame.image.load("sprites/sanity_bar.png")
timebar = pygame.image.load("sprites/time_bar.png")

healthicon = pygame.image.load("sprites/health_icon.png")
sanityicon = pygame.image.load("sprites/sanity_icon.png")
timeicon = pygame.image.load("sprites/time_icon.png")

objective_panel = pygame.image.load("sprites/objective_panel.png")
objective_panel_reversed = pygame.image.load("sprites/objective_panel_reversed.png")
crystal_white = pygame.image.load("sprites/crystal_white.png")
crystal_black = pygame.image.load("sprites/crystal_black.png")
crystal_red = pygame.image.load("sprites/crystal_red.png")
crystal_green = pygame.image.load("sprites/crystal_green.png")
crystal_blue = pygame.image.load("sprites/crystal_blue.png")

party = pygame.image.load("sprites/objective_icons/party.png")

#dzwiek
clickSound = pygame.mixer.Sound('click.wav')
winclickSound = pygame.mixer.Sound('winclick.wav')
midclickSound = pygame.mixer.Sound('midclick.wav')


#kolory
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


class Objective:
    def __init__(self):
        self.points = 0
        self.pointsToComplete = 100
        self.crystalType = 0
        self.addHealth = 0
        self.addSanity = 0
        self.addTime = 0

class ObjectiveType:
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

objectiveTypes = {}
objectiveTypes["party"] = ObjectiveType("Impreza!", "Czas na małą imprezkę")
objecives =\
[
    Objective(), Objective(), Objective(),
    Objective(), Objective(), Objective()
]

objecives[0].crystalType = 2
objecives[1].crystalType = 1
objecives[2].crystalType = 0
objecives[3].crystalType = 2
objecives[4].crystalType = 1
objecives[5].crystalType = 0
objecives[0].addHealth = 10
objecives[0].addSanity = -5
objecives[0].addTime = 5



def centerAnchor(width, height, percent_x=0.5, percent_y=0.5,
                 offset_x=0, offset_y=0):
    return pygame.Rect(screen.get_width() * percent_x - width / 2 + offset_x,
                       screen.get_height() * percent_y - height / 2 + offset_y,
                       width, height)
def renderObjectivePanel(percent_y=0.5, offset_x=0, index=0, reversed=False):
    panel = objective_panel
    if reversed:
        panel = objective_panel_reversed
    screen.blit(panel, centerAnchor(231, 123, reversed, percent_y, (1 - reversed * 2) * (231 / 2) * offset_x))

    panel.blit(text,(panel.get_width() / 2 - text.get_rect().width / 2, panel.get_height() / 2 - text.get_rect().height / 2))
    if objecives[index].crystalType == 0:
        screen.blit(crystal_red, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 / 2) * (1 - offset_x))))
    elif objecives[index].crystalType == 1:
        screen.blit(crystal_green, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 / 2) * (1 - offset_x))))
    else:
        screen.blit(crystal_blue, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 / 2) * (1 - offset_x))))

    if objecives[index].addHealth > 0:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 / 2) * (1 - offset_x)), -21))
    elif objecives[index].addHealth < 0:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 / 2) * (1 - offset_x)), -21))

    if objecives[index].addSanity > 0:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (253 - (231 / 2) * (1 - offset_x))))
    elif objecives[index].addSanity < 0:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (253 - (231 / 2) * (1 - offset_x))))

    if objecives[index].addTime > 0:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 / 2) * (1 - offset_x)), 21))
    elif objecives[index].addTime < 0:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 / 2) * (1 - offset_x)), 21))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            winclickSound.play()
            draw_green = True
            pos = pygame.mouse.get_pos()
        elif event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    screen.blit(board, centerAnchor(415, 256, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(healthbar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 - 70))
    screen.blit(sanitybar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timebar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 + 70))
    screen.blit(healthicon, centerAnchor(56, 65, 0.5, 0, 0, 256 // 2 + 20 - 70))
    screen.blit(sanityicon, centerAnchor(57, 58, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timeicon, centerAnchor(49, 56, 0.5, 0, 0, 256 // 2 + 20 + 70))

    renderObjectivePanel(0.25, 1, 0) # od -1.5 do 1
    renderObjectivePanel(0.5, 1, 1)
    renderObjectivePanel(0.75, 1, 2)

    renderObjectivePanel(0.25, 1, 3, True)
    renderObjectivePanel(0.5, 1, 4, True)
    renderObjectivePanel(0.75, 1, 5, True)


    pygame.display.flip()
pygame.quit()