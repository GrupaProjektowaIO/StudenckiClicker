import pygame
import pyrebase
import re
firebaseConfig = {
    "apiKey": "AIzaSyCr7nFZ_7LNowZtxN_jWAaYbjND4RCc4p4",
    "authDomain": "studencki-clicker.firebaseapp.com",
    "databaseURL": "https://studencki-clicker-default-rtdb.europe-west1.firebasedatabase.app/",
    "projectId": "studencki-clicker",
    "storageBucket": "studencki-clicker.appspot.com",
    "messagingSenderId": "310176660017",
    "appId": "1:310176660017:web:1754698f1e580d13e37310",
    "measurementId": "G-YYBMKEH9J3"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()

# Auth
# Login


def login(email,password):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    try:
        if re.fullmatch(regex,email):
            auth.sign_in_with_email_and_password(email, password)
            print("Pomyslny login")
    except:
        print("Zly login lub haslo")

# Rejestracja


def signUp(email,password):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    print("Rejestracja")
    try:
        if re.fullmatch(regex, email):
            auth.create_user_with_email_and_password(email, password)
            print("Pomyslnie zarejestrowano")
    except:
        print("Email juz istnieje")

# Baza danych


def dbPushHighscore(username):
    data = {'nick': username, 'highscore': 101}
    highscores = db.child('highscores').order_by_child(
        "nick").equal_to(data['nick']).get()
    print(highscores.val())
    if (len(highscores.val()) > 0):
        for highscore in highscores.each():
            db.child("highscores").child(highscore.key()).update(
                {"highscore": data['highscore']})
    else:
        db.child("highscores").push(data)


def dbGetHighscore():
    highscores = db.child("highscores").order_by_child(
        "highscore").limit_to_last(100).get()
    for highscore in reversed(highscores.each()):
        print(highscore.val())
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

objective_title_color = (56, 0, 0)

# objective pastelowe w kolorze statow
# przy ryzyku przegranej, wystapi minigierka, ktora pozwoli odzyskac troche statystyki (gierka a la dinozaur z Chroma)
# kiedy pasek postepu czynnosci to krysztalki zostaja przeniesione do odpowiedniej statystyki
# dbamy glownie o czas, a statystyki 1. i 2. sluza jako buffor
# SESJA

# tutoriale: formatowanie textu, maski, sound effects, przejscia pomiedzy ekranami,

pygame.init()
screen = pygame.display.set_mode([1920 / 2, 1080 / 2], pygame.RESIZABLE)
pygame.display.set_caption("Clicker")
pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()

#fonty
font = pygame.font.SysFont('Comic Sans MS, Arial, Times New Roman', 16, bold=True, italic=True, )
font_title = pygame.font.SysFont('Arial', 24, bold=True)
font_desc = pygame.font.SysFont('Arial', 16)
font_menu_button = pygame.font.SysFont('Arial', 24)
text_play = font_menu_button.render("Nowa Gra", True, (0, 0, 0))
text_login = font_menu_button.render("Logowanie", True, (0, 0, 0))
text_username = font_menu_button.render("Login: ", True, (0, 0, 0))
text_password = font_menu_button.render("Hasło: ", True, (0, 0, 0))
text_log_in = font_menu_button.render("Zaloguj się", True, (0, 0, 0))
text_register2 = font_menu_button.render("Zarejestruj się", True, (0, 0, 0))
text_register = font_menu_button.render("Zarejestruj się...", True, (0, 0, 0))
text_achievements = font_menu_button.render("Osiągnięcia", True, (0, 0, 0))
text_back = font_menu_button.render("Powrót", True, (0, 0, 0))
text_exit = font_menu_button.render("Wyjście", True, (0, 0, 0))

text_block_container = pygame.image.load("sprites/bar.png")

#sprites - main menu
main_menu_background = pygame.image.load("sprites/main_menu_background.png")
title = pygame.image.load("sprites/title.png")
menu_button = pygame.image.load("sprites/menu_button.png")

#sprites - game
game_background = pygame.image.load("sprites/game_background.png")
board = pygame.image.load("sprites/board.png")

healthbar = pygame.image.load("sprites/bar.png")
sanitybar = pygame.image.load("sprites/bar.png")
timebar = pygame.image.load("sprites/bar.png")
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
objective_progress_bar = pygame.image.load("sprites/objective_progress_bar.png")
crystal_red = pygame.image.load("sprites/crystal_red.png")
crystal_green = pygame.image.load("sprites/crystal_green.png")
crystal_blue = pygame.image.load("sprites/crystal_blue.png")

party = pygame.image.load("sprites/objective_icons/party.png")

book = pygame.image.load("sprites/power_ups/book.png")
clock = pygame.image.load("sprites/power_ups/clock.png")
coffee = pygame.image.load("sprites/power_ups/coffee.png")
dumbell = pygame.image.load("sprites/power_ups/dumbell.png")
energy_drink = pygame.image.load("sprites/power_ups/energy_drink.png")

#audio
clickSound = pygame.mixer.Sound('audio/click.wav')
winclickSound = pygame.mixer.Sound('audio/winclick.wav')
midclickSound = pygame.mixer.Sound('audio/midclick.wav')

#animations
class Animation:
    def __init__(self, name, frame_count, fps):
        self.timer = 0
        self.next = 1000 / fps
        self.index = 0
        self.frames = []
        for i in range(1, frame_count + 1):
            self.frames.append(pygame.image.load("animations/" + name + "/" + name + str(i) + ".png"))
    def play(self):
        self.timer += timer.get_time()
        if self.timer >= self.next:
            self.timer -= self.next
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
        return self.frames[self.index]
matrix = Animation("matrix", 22, 12)
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
    def clicked(self):
        midclickSound.play()

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
    "walk": ObjectiveType("Spacer", "Czas na ruch", HEALTH, LOW),
    "healthy_food": ObjectiveType("Zdrowy Posiłek", "Masz ochotę na zdrowe jedzonko!", HEALTH, MEDIUM),
    "gym": ObjectiveType("Siłownia", "Przypakuj na siłce!", HEALTH, HIGH),
    "music": ObjectiveType("Muzyka", "Muzyka łagodzi obyczaje", SANITY, LOW),
    "learn": ObjectiveType("Nauka", "Pora zakuwać", SANITY, MEDIUM),
    "party": ObjectiveType("Impreza!", "Czas na małą imprezkę!", SANITY, HIGH),
    "no_break": ObjectiveType("Bez Przerwy", "Na co komu odpoczynek?", TIME, LOW),
    "speed_boots": ObjectiveType("Szybkie buty", "Szybkość jest wszystkim!", TIME, MEDIUM),
    "multitasking": ObjectiveType("Multitasking", "Wiele spraw na raz", TIME, HIGH)
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

objectives[0].objectiveType = "walk"
objectives[1].objectiveType = "learn"
objectives[2].objectiveType = "speed_boots"
objectives[3].objectiveType = "gym"
objectives[4].objectiveType = "music"
objectives[5].objectiveType = "no_break"

health_max = 100
health_current = 100
health_drain = 0.1

sanity_max = 100
sanity_current = 100
sanity_drain = 0.1

time_max = 100
time_current = 100
time_drain = 0.1

active_text_box = ""
text_boxes = {
    "username": "",
    "password": ""
}


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
def renderTextBox(index, rect):
    global active_text_box
    text = text_boxes[index]
    renderScaled(text_block_container, rect)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            m = pygame.mouse.get_pos()
            if rect.collidepoint(m[0], m[1]):
                active_text_box = index
            else:
                if active_text_box == index:
                    active_text_box = ""
        elif e.type == pygame.KEYDOWN:
            if active_text_box == index:
                if e.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += e.unicode
        pygame.event.post(e)
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (rect.x + 5, rect.y + 5))
    text_boxes[index] = text
def renderObjectivePanel(percent_y=0.5, offset_x=0, index=0, reversed=False):
    panel = objective_panel
    o_type = objectiveTypes[objectives[index].objectiveType]
    if reversed:
        panel = objective_panel_reversed
    renderScaled(panel, centerAnchor(256, 128, reversed, percent_y, (1 - reversed * 2) * (256 // 2) * offset_x))

    renderScaled(o_type.renderedTitle, centerAnchor(128+64, 48, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x, -44))
    renderScaled(o_type.renderedDesc, centerAnchor(128 + 64, 48, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x, 36))

    crystal_white = timeicon_white
    crystal_black = timeicon_black

    if objectives[index].crystalType == 0:
        renderScaled(crystal_red, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
        crystal_white = healthicon_white
        crystal_black = healthicon_black
    elif objectives[index].crystalType == 1:
        renderScaled(crystal_blue, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
        crystal_white = sanityicon_white
        crystal_black = sanityicon_black
    else:
        renderScaled(crystal_green, centerAnchor(32, 32, reversed, percent_y, (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact == HIGH:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)), -32))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)), -32))

    if o_type.statImpact >= MEDIUM:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (288 - (256 // 2) * (1 - offset_x))))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (288 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact >= LOW:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)), 32))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)), 32))

    renderScaled(objective_progress_bar, centerAnchor(192, 32, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x))
def renderMainMenu():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(title, centerAnchor(384, 128, 0.5, 0, 0, 128 // 2 + 30))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.25, 0, 128 // 2))
    renderScaled(text_play, centerAnchor(221, 70, 0.5, 0.25, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.40, 0, 128 // 2))
    renderScaled(text_login, centerAnchor(221, 70, 0.5, 0.40, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.55, 0, 128 // 2))
    renderScaled(text_achievements, centerAnchor(221, 70, 0.5, 0.55, 0, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 80, 0.5, 0.70, 0, (128 // 2) * 1.62))
    renderScaled(text_exit, centerAnchor(221, 70, 0.5, 0.70, 0, (128 // 2) * 1.62))
def renderLoginPanel():
    renderScaled(matrix.play(), centerAnchor(1920, 1080))
    renderScaled(title, centerAnchor(576, 512, 0.5, 0.225, 0, 128 // 2))
    renderScaled(text_username, centerAnchor(128, 70, 0.5, 0.075, 0, 128 // 2 - 70))
    renderTextBox("username", centerAnchor(256, 70, 0.5, 0.075, 0, 128 // 2))
    renderScaled(text_password, centerAnchor(128, 70, 0.5, 0.225, 0, 128 // 2 - 100))
    renderTextBox("password", centerAnchor(256, 70, 0.5, 0.225, 0, 128 // 2 - 30))
    renderScaled(menu_button, centerAnchor(256, 70, 0.5, 0.3, 0, 128 // 2 - 30))
    renderScaled(text_log_in, centerAnchor(157, 60, 0.5, 0.3, 0, 128 // 2 - 30))
    renderScaled(menu_button, centerAnchor(256, 70, 0.5, 0.4, -136, 128 // 2))
    renderScaled(text_register, centerAnchor(157, 60, 0.5, 0.4, -136, 128 // 2))
    renderScaled(menu_button, centerAnchor(256, 70, 0.5, 0.4, 136, 128 // 2))
    renderScaled(text_back, centerAnchor(157, 60, 0.5, 0.4, 136, 128 // 2))
    #login(text_boxes['username'],text_boxes['password'])

def renderRegisterPanel():
    renderScaled(matrix.play(), centerAnchor(1920, 1080))
    renderScaled(title, centerAnchor(576, 512, 0.5, 0.225, 0, 128 // 2))
    renderScaled(text_username, centerAnchor(128, 70, 0.5, 0.075, 0, 128 // 2 - 70))
    renderTextBox("username", centerAnchor(256, 70, 0.5, 0.075, 0, 128 // 2))
    renderScaled(text_password, centerAnchor(128, 70, 0.5, 0.225, 0, 128 // 2 - 100))
    renderTextBox("password", centerAnchor(256, 70, 0.5, 0.225, 0, 128 // 2 - 30))
    renderScaled(menu_button, centerAnchor(256, 70, 0.5, 0.3, 0, 128 // 2 - 30))
    renderScaled(text_register2, centerAnchor(157, 60, 0.5, 0.3, 0, 128 // 2 - 30))
    renderScaled(menu_button, centerAnchor(256, 70, 0.5, 0.4, 0, 128 // 2))
    renderScaled(text_back, centerAnchor(157, 60, 0.5, 0.4, 0, 128 // 2))
    #signUp(text_boxes['username'], text_boxes['password'])
def renderAchievements():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
def renderGame():
    renderScaled(game_background, centerAnchor(1920, 1080))
    renderScaled(board, centerAnchor(512, 256, 0.5, 0, 0, 256 // 2 + 20))
    renderScaled(healthbar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 - 70))
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
    timer.tick(60)
    if gameState == "main_menu":
        renderMainMenu()
    elif gameState == "login_panel":
        renderLoginPanel()
    elif gameState == "register_panel":
        renderRegisterPanel()
    #elif gamestate == "achievements":
        #renderAchievements()
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
                #elif centerAnchor(256, 80, 0.5, 0.55, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    #gameState = "achievements"
                elif centerAnchor(221, 70, 0.5, 0.70, 0, (128 // 2) * 1.62).collidepoint(mouse[0], mouse[1]):
                    running = False
            elif gameState == "login_panel":
                if centerAnchor(256, 70, 0.5, 0.4, 136, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
                elif centerAnchor(256, 70, 0.5, 0.4, -136, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "register_panel"
            elif gameState == "game":
                if centerAnchor(256, 128, 0, 0.25, (1 - 0 * 2) * (256 // 2) * 1).collidepoint(mouse[0], mouse[1]):
                    objectives[0].clicked()
                elif centerAnchor(256, 128, 0, 0.5, (1 - 0 * 2) * (256 // 2)).collidepoint(mouse[0], mouse[1]):
                    objectives[1].clicked()
                elif centerAnchor(256, 128, 0, 0.75, (1 - 0 * 2) * (256 // 2)).collidepoint(mouse[0], mouse[1]):
                    objectives[2].clicked()
                elif centerAnchor(256, 128, 1, 0.25, (1 - 1 * 2) * (256 // 2)).collidepoint(mouse[0], mouse[1]):
                    objectives[3].clicked()
                elif centerAnchor(256, 128, 1, 0.5, (1 - 1 * 2) * (256 // 2)).collidepoint(mouse[0], mouse[1]):
                    objectives[4].clicked()
                elif centerAnchor(256, 128, 1, 0.75, (1 - 1 * 2) * (256 // 2)).collidepoint(mouse[0], mouse[1]):
                    objectives[5].clicked()

        elif event.type == pygame.QUIT:
            running = False

pygame.quit()