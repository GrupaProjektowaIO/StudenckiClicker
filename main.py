import pygame

#enums
HEALTH = 0
SANITY = 1
TIME = 2

LOW = 10
MEDIUM = 25
HIGH = 40

HEALTH_COLOR = (155, 0, 0)
SANITY_COLOR = (0, 4, 155)
TIME_COLOR = (2, 155, 0)

objective_title_color = (255, 255, 230)

#test
#test2
#test3
#test4

# objective pastelowe w kolorze statow
# przy ryzyku przegranej, wystapi minigierka, ktora pozwoli odzyskac troche statystyki (gierka a la dinozaur z Chroma)
# kiedy pasek postepu czynnosci to krysztalki zostaja przeniesione do odpowiedniej statystyki
# dbamy glownie o czas, a statystyki 1. i 2. sluza jako buffor
# SESJA

# tutoriale: formatowanie textu, maski, sound effects, przejscia pomiedzy ekranami,

pygame.init()
screen = pygame.display.set_mode([1920 / 2, 1080 / 2], pygame.RESIZABLE)
pygame.display.set_caption("Studencki")
pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

#fonty
font = pygame.font.SysFont('Comic Sans MS, Arial, Times New Roman', 16, bold=True, italic=True, )
font_title = pygame.font.SysFont('Arial', 18, bold=True)
font_desc = pygame.font.SysFont('Arial', 16)
text_play = font.render("Nowa Gra", True, (255, 255, 255))

#text = font.render("Zadania", True, (255, 255, 255))

#sprites - main menu
title = pygame.image.load("sprites/title.png")
menu_button = pygame.image.load("sprites/menu_button.png")

#sprites - game
board = pygame.image.load("sprites/board.png")

healthbar = pygame.image.load("sprites/health_bar.png")
sanitybar = pygame.image.load("sprites/sanity_bar.png")
timebar = pygame.image.load("sprites/time_bar.png")
healthicon = pygame.image.load("sprites/health_icon.png")
sanityicon = pygame.image.load("sprites/sanity_icon.png")
timeicon = pygame.image.load("sprites/time_icon.png")
statbar_mask = pygame.Surface(pygame.image.load("sprites/stat_bar_mask.png").get_size()).convert_alpha()
statbar_mask.fill((255,255,255))

objective_panel = pygame.image.load("sprites/objective_panel.png")
objective_panel_reversed = pygame.image.load("sprites/objective_panel_reversed.png")
crystal_white = pygame.image.load("sprites/crystal_white.png")
crystal_black = pygame.image.load("sprites/crystal_black.png")
crystal_red = pygame.image.load("sprites/crystal_red.png")
crystal_green = pygame.image.load("sprites/crystal_green.png")
crystal_blue = pygame.image.load("sprites/crystal_blue.png")

party = pygame.image.load("sprites/objective_icons/party.png")

#audio
clickSound = pygame.mixer.Sound('audio/click.wav')
winclickSound = pygame.mixer.Sound('audio/winclick.wav')
midclickSound = pygame.mixer.Sound('audio/midclick.wav')

class Objective:
    def __init__(self):
        self.points = 0
        self.pointsToComplete = 100
        self.crystalType = 0
        self.addStat = 0
        self.objectiveType = ""
        self.isCompleted = False
    def setType(self, type_name):
        o_type = objectiveTypes[type_name]
        self.objectiveType = o_type
        self.points = 0
        self.pointsToComplete = o_type.statImpact // 2
        self.crystalType = o_type.statType
        self.addStat = o_type.statImpact
        self.isCompleted = False

class ObjectiveType:
    def __init__(self, title, desc, statType, statImpact):
        self.title = title
        self.desc = desc
        self.statType = statType
        self.statImpact = statImpact
        self.renderedTitle = False
        self.renderedDesc = False

objectiveTypes =\
{
    "walk": ObjectiveType("Spacer", "Krótki spacer poprawi krążenie.", HEALTH, LOW),
    "healthy_food": ObjectiveType("Zdrowy Posiłek", "Masz ochotę na zdrowe jedzonko!", HEALTH, MEDIUM),
    "gym": ObjectiveType("Wyjście na Siłownię", "Przypakuj na siłce!", HEALTH, HIGH),
    "music": ObjectiveType("Muzyka", "Postanawiasz posłuchać paru swoich ulubionych kawałków.", SANITY, LOW),
    "learn": ObjectiveType("Nauka", "Masz czas, by trochę się trochę pouczyć.", SANITY, MEDIUM),
    "party": ObjectiveType("Impreza!", "Czas na małą imprezkę!", SANITY, HIGH),
    "no_break": ObjectiveType("Bez Krótkiej Przerwy", "Na co komu odpoczynek?", TIME, LOW),
    "speed_boots": ObjectiveType("Szybkie buty", "Zakup Szybkich Butów pozwoli ci zaoszczędzić trochę czasu. Logiczne, prawda?", TIME, MEDIUM),
    "multitasking": ObjectiveType("Multitasking", "Twoje zdolności zarządzania czasem zwiększają się!", TIME, HIGH)
}

for k in objectiveTypes:
    objectiveTypes[k].renderedTitle = font_title.render(objectiveTypes[k].title, True, objective_title_color)
    objectiveTypes[k].renderedDesc = font_desc.render(objectiveTypes[k].desc, True, objective_title_color)

objectives =\
[
    Objective(), Objective(), Objective(),
    Objective(), Objective(), Objective()
]

objectives[0].crystalType = HEALTH
objectives[1].crystalType = SANITY
objectives[2].crystalType = TIME
objectives[3].crystalType = HEALTH
objectives[4].crystalType = SANITY
objectives[5].crystalType = TIME

objectives[0].objectiveType = "party"
objectives[1].objectiveType = "party"
objectives[2].objectiveType = "party"
objectives[3].objectiveType = "party"
objectives[4].objectiveType = "party"
objectives[5].objectiveType = "party"

health_max = 100
health_current = 100
health_drain = 0.1

sanity_max = 100
sanity_current = 100
sanity_drain = 0.1

time_max = 100
time_current = 100
time_drain = 0.1

def centerAnchor(width, height, percent_x=0.5, percent_y=0.5,
                 offset_x=0, offset_y=0):
    return pygame.Rect(screen.get_width() * percent_x - width / 2 + offset_x,
                       screen.get_height() * percent_y - height / 2 + offset_y,
                       width, height)
def renderObjectivePanel(percent_y=0.5, offset_x=0, index=0, reversed=False):
    panel = objective_panel
    o_type = objectiveTypes[objectives[index].objectiveType]
    if reversed:
        panel = objective_panel_reversed
    screen.blit(panel, centerAnchor(231, 123, reversed, percent_y, (1 - reversed * 2) * (231 // 2) * offset_x))

    panel.blit(o_type.renderedTitle, (panel.get_width() / 2 - o_type.renderedTitle.get_rect().width / 2, panel.get_height() / 2 - o_type.renderedTitle.get_rect().height / 2 - 40))
    panel.blit(o_type.renderedDesc, (20, panel.get_height() / 2 - o_type.renderedTitle.get_rect().height / 2 + 20))
    #panel.blit(text, (panel.get_width() / 2 - text.get_rect().width / 2, panel.get_height() / 2 - text.get_rect().height / 2))

    if objectives[index].crystalType == 0:
        screen.blit(crystal_red, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 // 2) * (1 - offset_x))))
    elif objectives[index].crystalType == 1:
        screen.blit(crystal_blue, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 // 2) * (1 - offset_x))))
    else:
        screen.blit(crystal_green, centerAnchor(25, 25, reversed, percent_y, (1 - reversed * 2) * (231 - (231 // 2) * (1 - offset_x))))

    if o_type.statImpact == HIGH:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 // 2) * (1 - offset_x)), -21))
    else:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 // 2) * (1 - offset_x)), -21))

    if o_type.statImpact >= MEDIUM:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (253 - (231 // 2) * (1 - offset_x))))
    else:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (253 - (231 // 2) * (1 - offset_x))))

    if o_type.statImpact >= LOW:
        screen.blit(crystal_white, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 // 2) * (1 - offset_x)), 21))
    else:
        screen.blit(crystal_black, centerAnchor(14, 14, reversed, percent_y, (1 - reversed * 2) * (248 - (231 // 2) * (1 - offset_x)), 21))

def renderMainMenu():
    screen.fill((36,36,36))
    screen.blit(title, centerAnchor(415, 128, 0.5, 0, 0, 128 // 2 + 30))
    screen.blit(menu_button, centerAnchor(257, 79, 0.5, 0.25, 0, 128 // 2))
    screen.blit(text_play, centerAnchor(257, 79, 0.5, 0.25, 0, 128 // 2))
    screen.blit(menu_button, centerAnchor(257, 79, 0.5, 0.40, 0, 128 // 2))
    screen.blit(menu_button, centerAnchor(257, 79, 0.5, 0.55, 0, (128 // 2) * 1.62))

def renderGame():
    screen.fill((0, 0, 0))
    screen.blit(board, centerAnchor(415, 256, 0.5, 0, 0, 256 // 2 + 20))

    stat_rect = centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 - 70)

    screen.blit(healthbar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 - 70))
    healthbar.blit(statbar_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    #pygame.draw.rect(screen, HEALTH_COLOR, stat_rect)

    screen.blit(sanitybar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timebar, centerAnchor(379, 70, 0.5, 0, 0, 256 // 2 + 20 + 70))
    screen.blit(healthicon, centerAnchor(56, 65, 0.5, 0, 0, 256 // 2 + 20 - 70))
    screen.blit(sanityicon, centerAnchor(57, 58, 0.5, 0, 0, 256 // 2 + 20))
    screen.blit(timeicon, centerAnchor(49, 56, 0.5, 0, 0, 256 // 2 + 20 + 70))

    renderObjectivePanel(0.25, 1, 0)  # od -1.5 do 1
    renderObjectivePanel(0.5, 1, 1)
    renderObjectivePanel(0.75, 1, 2)

    renderObjectivePanel(0.25, 1, 3, True)
    renderObjectivePanel(0.5, 1, 4, True)
    renderObjectivePanel(0.75, 1, 5, True)

gameState = "main_menu"
running = True
while running:

    if gameState == "main_menu":
        renderMainMenu()
    elif gameState == "game":
        renderGame()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if gameState == "main_menu":
                if centerAnchor(257, 79, 0.5, 0.25, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "game"
            elif gameState == "game":
                pass
                #if centerAnchor(257, 79, 0.5, 0.25, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):

        elif event.type == pygame.QUIT:
            running = False
pygame.quit()