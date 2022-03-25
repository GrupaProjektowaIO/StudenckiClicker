import pygame

#enums
HEALTH = 0
SANITY = 1
TIME = 2

LOW = 10
MEDIUM = 25
HIGH = 40
# test2
HEALTH_COLOR = (155, 0, 0)
SANITY_COLOR = (0, 4, 155)
TIME_COLOR = (2, 155, 0)

objective_title_color = (255, 255, 230)

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
font_menu_button = pygame.font.SysFont('Arial', 14)
text_play = font_menu_button.render("Nowa Gra", True, (0, 0, 0))

#text = font.render("Zadania", True, (255, 255, 255))

#sprites - main menu
main_menu_background = pygame.image.load("sprites/main_menu_background.png")
title = pygame.image.load("sprites/title.png")
menu_button = pygame.image.load("sprites/menu_button.png")

#sprites - game
game_background = pygame.image.load("sprites/game_background.png")
board = pygame.image.load("sprites/board.png")

healthbar = pygame.image.load("sprites/health_bar.png")
sanitybar = pygame.image.load("sprites/sanity_bar.png")
timebar = pygame.image.load("sprites/time_bar.png")
healthicon = pygame.image.load("sprites/health_icon.png")
sanityicon = pygame.image.load("sprites/sanity_icon.png")
timeicon = pygame.image.load("sprites/time_icon.png")
deathicon = pygame.image.load("sprites/death_icon.png")

healthicon_white = pygame.image.load("sprites/health_icon_white.png")
healthicon_black = pygame.image.load("sprites/health_icon_black.png")
sanityicon_white = pygame.image.load("sprites/sanity_icon_white.png")
sanityicon_black = pygame.image.load("sprites/sanity_icon_black.png")
timeicon_white = pygame.image.load("sprites/time_icon_white.png")
timeicon_black = pygame.image.load("sprites/time_icon_black.png")

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

book = pygame.image.load("sprites/power_ups/book.png")
clock = pygame.image.load("sprites/power_ups/clock.png")
coffe = pygame.image.load("sprites/power_ups/coffe.png")
dumbell = pygame.image.load("sprites/power_ups/dumbell.png")
energy_drink = pygame.image.load("sprites/power_ups/energy_drink.png")

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
    x_scale = screen.get_width() / 1920
    y_scale = screen.get_height() / 1080
    return pygame.Rect(screen.get_width() * percent_x - width / 2 * x_scale + offset_x * x_scale,
                       screen.get_height() * percent_y - height / 2 * y_scale + offset_y * y_scale,
                       width * x_scale, height * y_scale)
def renderScaled(sprite, rect):
    scaled = pygame.transform.scale(sprite, (rect.w, rect.h))
    screen.blit(scaled, rect)
def renderObjectivePanel(percent_y=0.5, offset_x=0, index=0, reversed=False):
    panel = objective_panel
    o_type = objectiveTypes[objectives[index].objectiveType]
    if reversed:
        panel = objective_panel_reversed
    renderScaled(panel, centerAnchor(256, 128, reversed, percent_y, (1 - reversed * 2) * (256 // 2) * offset_x))

    panel.blit(o_type.renderedTitle, (panel.get_width() / 2 - o_type.renderedTitle.get_rect().width / 2, panel.get_height() / 2 - o_type.renderedTitle.get_rect().height / 2 - 40))
    panel.blit(o_type.renderedDesc, (20, panel.get_height() / 2 - o_type.renderedTitle.get_rect().height / 2 + 20))
    #panel.blit(text, (panel.get_width() / 2 - text.get_rect().width / 2, panel.get_height() / 2 - text.get_rect().height / 2))

    if objectives[index].crystalType == 0:
        renderScaled(crystal_red, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
    elif objectives[index].crystalType == 1:
        renderScaled(crystal_blue, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
    else:
        renderScaled(crystal_green, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact == HIGH:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x)), -21))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x)), -21))

    if o_type.statImpact >= MEDIUM:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact >= LOW:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x)), 21))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x)), 21))

def renderMainMenu():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(title, centerAnchor(384, 128, 0.5, 0, 0, 128 // 2 + 30))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.25, 0, 128 // 2))
    renderScaled(text_play, centerAnchor(221, 80, 0.5, 0.25, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.40, 0, 128 // 2))
    renderScaled(text_play, centerAnchor(221, 80, 0.5, 0.40, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.55, 0, (128 // 2) * 1.62))
def renderLoginPanel():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.15, 0, 128 // 2))
    renderScaled(text_play, centerAnchor(221, 80, 0.5, 0.15, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.30, 0, 128 // 2))
    renderScaled(text_play, centerAnchor(221, 80, 0.5, 0.30, 0, 128 // 2))
def renderGame():
    renderScaled(game_background, centerAnchor(1920, 1080))
    renderScaled(board, centerAnchor(512, 256, 0.5, 0, 0, 256 // 2 + 20))

    stat_rect = centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 - 70)

    renderScaled(healthbar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 - 70))
    #healthbar.blit(statbar_mask, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    #pygame.draw.rect(screen, HEALTH_COLOR, stat_rect)

    renderScaled(sanitybar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20))
    renderScaled(timebar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 + 70))
    renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20 - 70))
    renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20))
    renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20 + 70))
    renderScaled(healthicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20 - 70))
    renderScaled(sanityicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20))
    renderScaled(timeicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20 + 70))

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
    elif gameState == "login_panel":
        renderLoginPanel()
    elif gameState == "game":
        renderGame()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if gameState == "main_menu":
                if centerAnchor(256, 80, 0.5, 0.25, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "game"
                elif centerAnchor(256, 80, 0.5, 0.40, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "login_panel"
            elif gameState == "game":
                pass
                #if centerAnchor(257, 79, 0.5, 0.25, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):

        elif event.type == pygame.QUIT:
            running = False
pygame.quit()