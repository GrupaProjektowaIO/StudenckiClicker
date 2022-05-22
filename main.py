import pygame
import pyrebase
import re
import random
import json
import sys, traceback

# KONIEC GRY:
# PODSTAWOWE: WYNIK JAKO LICZBA UKONCZONYCH SESJI;
# ENDLESS MODE: WYNIK JAKO CZAS PRZETRWANY;
# EKRANY ZALICZENIA GIER;
# DODANIE ELEMENTOW DO 1. POKOJU;
# OSIAGNIECIA POWIAZANE Z BAZA DANYCH I WYSKAKUJACE INFORMACJE;
# RANKING TRYBU ENDLESS;

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

logged_username = ""
dbAchievements = []

def login(email, password):
    global logged_username
    global gameState
    global announcement
    global dbAchievements
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Pomyslny login")
        users = db.child('users').order_by_child("email").equal_to(email).get()
        for user in users.each():
            logged_username = user.val()['nick']
        dbAchievements = dbGetAchievements(logged_username)
        print(dbAchievements)
        gameState = "main_menu"
    except Exception as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        print(error)
        # INVALID_PASSWORD
        # INVALID_EMAIL
        # EMAIL_NOT_FOUND
        # MISSING_PASSWORD
        if error == "MISSING_PASSWORD":
            announcement = "Nie wpisano hasła!"
        elif error == "INVALID_PASSWORD" or error == "INVALID_EMAIL":
            announcement = "Niepoprawny login lub hasło!"
        elif error == "EMAIL_NOT_FOUND":
            announcement = "E-mail nie istnieje!"
        else:
            announcement = "Niepoprawny login!"
            print(error)


# Rejestracja


def signUp(email, username, password):
    global logged_username
    global gameState
    global announcement
    global dbAchievements
    print("Rejestracja")
    try:
        special_characters = " \"#$%&'()*+,/:;<=>?@[\]^`{|}~"
        data = {'nick': username, 'email': email}
        users = db.child('users').order_by_child("nick").equal_to(data['nick']).get()
        if len(users.val()) > 0:
            announcement = "Ten nick już istnieje."
            print(announcement)
        elif any(character in special_characters for character in username):
            announcement = "Nick nie moze miec znakow specjalnych."
            print(announcement)
        else:
            auth.create_user_with_email_and_password(email, password)
            db.child("users").push(data)
            # tworzenie informacji o osiagnieciach w bazie danych
            achievementData = {'nick': username, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
            db.child("achievements").push(achievementData)
            print("Pomyslnie zarejestrowano")
            logged_username = username
            dbAchievements = dbGetAchievements(logged_username)
            gameState = "main_menu"
    except Exception as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        print(error)
        # WEAK_PASSWORD : Password should be at least 6 characters
        # EMAIL_EXISTS
        if error == "EMAIL_EXISTS":
            announcement = "E-mail jest już użyty!"
        elif error == "MISSING_PASSWORD":
            announcement = "Nie wpisano hasła!"
        elif error == "INVALID_PASSWORD" or error == "INVALID_EMAIL":
            announcement = "Niepoprawny login lub hasło!"
        elif error == "WEAK_PASSWORD : Password should be at least 6 characters":
            announcement = "Hasło powinno zawierać przynajmniej 6 znaków!"
        else:
            announcement = "Niepoprawny login!"
            print(error)


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


def dbPushAchievement(username, achievementNum, achievementTier):
    users = db.child("achievements").order_by_child("nick").equal_to(username).get()
    for user in users.each():
        db.child("achievements").child(user.key()).update({achievementNum: achievementTier})

def dbGetAchievements(username):
    users = db.child('achievements').order_by_child("nick").equal_to(username).get()
    for user in users.each():
        print("!!!" + str(user.val()) + "!!!")
        ach = str(user.val()).split(":")
        i = 0
        for a in ach:
            if 13 > i > 0:
                print(a)
                achievements[i - 1].setTier(ord(a[1]) - 48)
            i += 1
        return user.val()

# enums
HEALTH = 0
SANITY = 1
TIME = 2
BIRET = 3

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
pygame.mouse.set_visible(False)
# pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
# screen = pygame.display.set_mode([1920, 1080])
screen = pygame.display.set_mode([1920, 1080], pygame.FULLSCREEN)
pygame.display.set_caption("Clicker")
# pygame.font.Font("freesansbold.ttf", 16)
pygame.font.Font("fonts/PressStart2P-Regular.ttf", 16)
timer = pygame.time.Clock()

# fonty
# font = pygame.font.SysFont('Comic Sans MS, Arial, Times New Roman', 16, bold=True, italic=True, )
# font_title = pygame.font.SysFont('Arial', 24, bold=True)
# font_desc = pygame.font.SysFont('Arial', 16)VT323-Regular
# font_menu_button = pygame.font.SysFont('Arial', 24)

font = pygame.font.Font('fonts/VT323-Regular.ttf', 30, bold=True, italic=True)
font_title = pygame.font.Font('fonts/VT323-Regular.ttf', 24, bold=True)
font_desc = pygame.font.Font('fonts/VT323-Regular.ttf', 16)
font_menu_button = pygame.font.Font('fonts/VT323-Regular.ttf', 24)

text_play = font_menu_button.render("Nowa Gra", False, (0, 0, 0))
text_login = font_menu_button.render("Logowanie", False, (0, 0, 0))
text_username = font_menu_button.render("Login: ", False, (144, 164, 174))
text_nick = font_menu_button.render("Nick: ", False, (144, 164, 174))
text_password = font_menu_button.render("Hasło: ", False, (144, 164, 174))
text_log_in = font_menu_button.render("Zaloguj się", False, (0, 0, 0))
text_register2 = font_menu_button.render("Zarejestruj się", False, (0, 0, 0))
text_register = font_menu_button.render("Zarejestruj się...", False, (0, 0, 0))
text_achievements = font_menu_button.render("Osiągnięcia", False, (0, 0, 0))
text_back = font_menu_button.render("Powrót", False, (0, 0, 0))
text_exit = font_menu_button.render("Wyjście", False, (0, 0, 0))

dialog0 = font_menu_button.render("W końcu zdałem maturę!", False, (255, 255, 0))
dialog1 = font_menu_button.render("Studia stoją przede mną otworem.", False, (255, 255, 0))
dialog2 = font_menu_button.render("To będzie najlepszy czas w moim życiu.", False, (255, 255, 0))
dialog3 = font_menu_button.render("(Prawda?)", False, (255, 255, 0))
dialog_adv = font_menu_button.render("Kliknij, by przejść dalej", False, (0, 0, 0))

dialog0_endless = font_menu_button.render("* otwierasz oczy *", False, (255, 255, 0))
dialog1_endless = font_menu_button.render("* widzisz przed sobą książki i kraty *", False, (255, 255, 0))
dialog2_endless = font_menu_button.render("* właśnie zaczyna się twój studencki koszmar *", False, (255, 255, 0))
dialog3_endless = font_menu_button.render("* powodzenia >:D *", False, (255, 255, 0))
dialog_adv_endless = font_menu_button.render("Kliknij, by przejść dalej", False, (255, 0, 0))

text_podyplomowe = font_menu_button.render("Studia Podyplomowe", False, (0, 0, 0))  # poziom latwy
text_informatyka = font_menu_button.render("Studia Informatyczne", False, (0, 0, 0))  # poziom medium
text_medycyna = font_menu_button.render("Studia Medyczne", False, (0, 0, 0))  # poziom hard

text_dummy = font_title.render("WYBIERZ POZIOM", False, (255, 255, 255))

text_level_desc_1_dif = font_title.render("Poziom: Łatwy", False, (255, 255, 255))
text_level_desc_2_dif = font_title.render("Poziom: Średni", False, (255, 255, 255))
text_level_desc_3_dif = font_title.render("Poziom: Trudny", False, (255, 255, 255))
text_level_desc_4_dif = font_title.render("Poziom: Zabójczy", False, (255, 255, 255))

text_level_desc_1_len = font_title.render("Długość: 3 lata", False, (255, 255, 255))
text_level_desc_2_len = font_title.render("Długość: 5 lat", False, (255, 255, 255))
text_level_desc_3_len = font_title.render("Długość: 6 lat", False, (255, 255, 255))
text_level_desc_4_len = font_title.render("Długość: Nieskończona", False, (255, 255, 255))

text_level_desc_1_boost = font_title.render("Nagroda: Bonus do Czasu", False, (255, 255, 255))
text_level_desc_2_boost = font_title.render("Nagroda: Bonus do Zdrowia Psychicznego", False, (255, 255, 255))
text_level_desc_3_boost = font_title.render("Nagroda: Bonus do Zdrowia Fizycznego", False, (255, 255, 255))
text_level_desc_4_boost = font_title.render("Nagroda: Chwała i sława na wieczność", False, (255, 255, 255))

text_block_container = pygame.image.load("sprites/text_container.png")

# sprites - main menu
pixel = pygame.image.load("sprites/pixel.png")
pixel_white = pygame.image.load("sprites/pixel_white.png")
warning_login = pygame.image.load("sprites/warning_login.png")
text_warning_login = font_title.render(" W celu zdobycia osiągnięć musisz być zalogowany! ", False, (255, 0, 0))
cursor = pygame.image.load("sprites/cursor.png")
x_button = pygame.image.load("sprites/x_button.png")
x_button_p = pygame.image.load("sprites/x_button_p.png")
main_menu_background = pygame.image.load("sprites/main_menu_background.png")
title = pygame.image.load("sprites/title.png")
menu_button = pygame.image.load("sprites/menu_button.png")
login_button = pygame.image.load("sprites/login_button.png")
new_game_button = pygame.image.load("sprites/new_game_button.png")
achievements_button = pygame.image.load("sprites/achievements_button.png")
back_button = pygame.image.load("sprites/back_button.png")
register_button = pygame.image.load("sprites/register_button.png")
exit_button = pygame.image.load("sprites/exit_button.png")
login_button_p = pygame.image.load("sprites/login_button_p.png")
new_game_button_p = pygame.image.load("sprites/new_game_button_p.png")
achievements_button_p = pygame.image.load("sprites/achievements_button_p.png")
back_button_p = pygame.image.load("sprites/back_button_p.png")
register_button_p = pygame.image.load("sprites/register_button_p.png")
exit_button_p = pygame.image.load("sprites/exit_button_p.png")
logout_button = pygame.image.load("sprites/logout_button.png")
logout_button_p = pygame.image.load("sprites/logout_button_p.png")
login_panel = pygame.image.load("sprites/login_panel.png")
# sprites - difficulty options
informatyczne_button = pygame.image.load("sprites/informatyczne_button.png")
informatyczne_button_p = pygame.image.load("sprites/informatyczne_button_p.png")
podyplomowe_button = pygame.image.load("sprites/podyplomowe_button.png")
podyplomowe_button_p = pygame.image.load("sprites/podyplomowe_button_p.png")
medyczne_button = pygame.image.load("sprites/medyczne_button.png")
medyczne_button_p = pygame.image.load("sprites/medyczne_button_p.png")
endless_button = pygame.image.load("sprites/endless_button.png")
endless_button_p = pygame.image.load("sprites/endless_button_p.png")
endless_button_i = pygame.image.load("sprites/endless_button_p.png")
# sprites - game
game_background = pygame.image.load("sprites/game_background.png")
Computer_science_difficulty = pygame.image.load("sprites/Computer_science_difficulty.png")
Medic_school_difficulty = pygame.image.load("sprites/Medic_school_difficulty.png")
endless_background = pygame.image.load("sprites/endless_background.png")
game_background_opening = pygame.image.load("sprites/game_background.png")
Computer_science_difficulty_opening = pygame.image.load("sprites/game_background.png")
Medic_school_difficulty_opening = pygame.image.load("sprites/game_background.png")
session_overlay = pygame.image.load("sprites/overlay_red.png")
board = pygame.image.load("sprites/board.png")
sesja = pygame.image.load("sprites/sesja.png")
current_game_background = game_background
# sprite - legend
notebook_background = pygame.image.load("sprites/notebook.png")
end_game_button = pygame.image.load("sprites/end_game_button.png")
end_game_button_p = pygame.image.load("sprites/end_game_button_p.png")
win_game_button = pygame.image.load("sprites/end_game_button.png")
win_game_button_p = pygame.image.load("sprites/end_game_button_p.png")
tooltip_button = pygame.image.load("sprites/tooltip_button.png")
tooltip_button_p = pygame.image.load("sprites/tooltip_button_p.png")
try_again_button = pygame.image.load("sprites/try_again_button.png")
try_again_button_p = pygame.image.load("sprites/try_again_button_p.png")

text_legend_stats = font_menu_button.render("Statystyki", False, (0, 0, 0))
text_legend_stats_desc = font_menu_button.render("Podczas rozgrywki należy śledzić widzoczne poniżej ikony.", False,
                                                 (0, 0, 0))
text_legend_stats_desc2 = font_menu_button.render("Kiedy jedna z nich spadnie do zera, to następuje koniec gry.", False,
                                                  (0, 0, 0))
text_legend_stats_health = font_menu_button.render("Twoje Zdrowie Fizyczne  ", False, (0, 0, 0))
text_legend_stats_sanity = font_menu_button.render("Twoje Zdrowie Psychiczne", False, (0, 0, 0))
text_legend_stats_time = font_menu_button.render("Upływający Czas         ", False, (0, 0, 0))
text_legend_stats_biret = font_menu_button.render("Sesja                   ", False, (0, 0, 0))

text_legend_premie_lotne = font_menu_button.render("Premie Lotne", False, (0, 0, 0))
text_legend_premie_lotne_desc = font_menu_button.render("W trakcie gry napotkasz dodatkowe atrybuty studenta.", False,
                                                        (0, 0, 0))
text_legend_premie_lotne_desc2 = font_menu_button.render("Kliknięcie na nie ułatwi lub utrudni rozgrywkę.", False,
                                                         (0, 0, 0))
text_legend_premie_lotne_book = font_menu_button.render("Książka: Nieznacznie wypełnia cele", False, (0, 0, 0))
text_legend_premie_lotne_antibook = font_menu_button.render("AntyKsiążka: Nieznacznie zmniejsza cele", False, (0, 0, 0))
text_legend_premie_lotne_clock = font_menu_button.render("Zegar: Zatrzymuje Czas ", False, (0, 0, 0))
text_legend_premie_lotne_anticlock = font_menu_button.render("AntyZegar: Przyspiesza Czas", False, (0, 0, 0))
text_legend_premie_lotne_coffe = font_menu_button.render("Kawa: Zwiększa moc klikania", False, (0, 0, 0))
text_legend_premie_lotne_anticoffe = font_menu_button.render("AntyKawa: Zmniejsza moc klikania", False, (0, 0, 0))
text_legend_premie_lotne_dumbell = font_menu_button.render("Hantel: Zmniejsza poziom zadań", False, (0, 0, 0))
text_legend_premie_lotne_antidumbell = font_menu_button.render("AntyHantel: Zwiększa poziom zadań", False, (0, 0, 0))
text_legend_premie_lotne_energy_drink = font_menu_button.render("Energetyk: Możesz klikać gdzie chcesz", False,
                                                                (0, 0, 0))
text_legend_premie_lotne_antienergy_drink = font_menu_button.render("AntyEnergetyk: Paraliż na klikanie", False,
                                                                    (0, 0, 0))

# sprite - achievements
notebook_achievements_background = pygame.image.load("sprites/notebook_achievements.png")
trophy_none = pygame.image.load("sprites/trophy_none.png")
trophy_bronze = pygame.image.load("sprites/trophy_bronze.png")
trophy_silver = pygame.image.load("sprites/trophy_silver.png")
trophy_gold = pygame.image.load("sprites/trophy_gold.png")

text_achievements_hidden = font_menu_button.render("???", False, (0, 0, 0))
text_achievements_hidden_desc = font_menu_button.render("????? ???", False, (0, 0, 0))
text_achievements_1 = font_menu_button.render("Nazwa", False, (0, 0, 0))
text_achievements_1_desc = font_menu_button.render("Opis", False, (0, 0, 0))

healthbar = pygame.image.load("sprites/bar.png")
sanitybar = pygame.image.load("sprites/bar.png")
timebar = pygame.image.load("sprites/bar.png")
health_filler = pygame.image.load("sprites/health_filler.png")
sanity_filler = pygame.image.load("sprites/sanity_filler.png")
time_filler = pygame.image.load("sprites/time_filler.png")
biret_filler = pygame.image.load("sprites/biret_filler.png")
healthicon = pygame.image.load("sprites/health_icon.png")
sanityicon = pygame.image.load("sprites/sanity_icon.png")
timeicon = pygame.image.load("sprites/time_icon.png")
bireticon = pygame.image.load("sprites/biret_icon.png")
deathicon = pygame.image.load("sprites/death_icon.png")
diffuculty_progress_bar_easy = pygame.image.load('sprites/difficulty_bar_easy.png')
diffuculty_progress_bar_medium = pygame.image.load('sprites/difficulty_bar_medium.png')
diffuculty_progress_bar_hard = pygame.image.load('sprites/difficulty_bar_hard.png')

statbar_mask = pygame.Surface(pygame.image.load("sprites/stat_bar_mask.png").get_size()).convert_alpha()
statbar_mask.fill((255, 255, 255))

objective_paper_normal = pygame.image.load("sprites/paper.png")
objective_paper_endless = pygame.image.load("sprites/endless_paper.png")
objective_paper = objective_paper_normal
objective_progress_bar = pygame.image.load("sprites/objective_progress_bar.png")
crystal_red = pygame.image.load("sprites/crystal_red.png")
crystal_green = pygame.image.load("sprites/crystal_green.png")
crystal_blue = pygame.image.load("sprites/crystal_blue.png")
crystal_black = pygame.image.load("sprites/crystal_black.png")
party = pygame.image.load("sprites/objective_icons/party.png")

book = pygame.image.load("sprites/power_ups/book.png")
clock = pygame.image.load("sprites/power_ups/clock.png")
coffee = pygame.image.load("sprites/power_ups/coffee.png")
dumbell = pygame.image.load("sprites/power_ups/dumbell.png")
energy_drink = pygame.image.load("sprites/power_ups/energy_drink.png")
antibook = pygame.image.load("sprites/power_ups/antibook.png")
anticlock = pygame.image.load("sprites/power_ups/anticlock.png")
anticoffee = pygame.image.load("sprites/power_ups/anticoffee.png")
antidumbell = pygame.image.load("sprites/power_ups/antidumbell.png")
antienergy_drink = pygame.image.load("sprites/power_ups/antienergy_drink.png")

# audio
clickSound = pygame.mixer.Sound('audio/click.wav')
winclickSound = pygame.mixer.Sound('audio/winclick.wav')
midclickSound = pygame.mixer.Sound('audio/midclick.wav')
achievementgetSound = pygame.mixer.Sound('audio/winclick.wav')

# animations
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

    def reset(self):
        self.index = 0


cloud = Animation("cloud", 6, 2.5)
sun = Animation("Sun", 2, 3)
smoke = Animation("Smoke", 4, 2)
bird = Animation("bird", 8, 2)
game_opening_easy = Animation("game_opening_easy", 6, 3)
game_opening_medium = Animation("game_opening_medium", 6, 3)
game_opening_hard = Animation("game_opening_hard", 6, 3)
game_opening_endless = Animation("game_opening_endless", 5, 3)
gameover_background = Animation("gameover_background", 23, 2)
win_background = Animation("win_background", 6, 3)


class Objective:
    def __init__(self):
        self.objectiveType = ""
        self.points = 0
        self.pointsToComplete = 100
        self.crystalType = 0
        self.addStat = 0
        self.isCompleted = False
        self.timer = 0
        self.drain_cooldown = 0

    def isSession(self):
        if self.crystalType == BIRET:
            return True
        else:
            return False

    def setType(self, type_name, session=False):
        o_type = 0
        if session:
            o_type = objectiveTypesSession[type_name]
        else:
            o_type = objectiveTypes[type_name]
        self.objectiveType = type_name
        self.points = 0
        if o_type.statImpact == LOW:
            self.pointsToComplete = o_type.statImpact
            self.drain_cooldown = 0.5
        elif o_type.statImpact == MEDIUM:
            self.pointsToComplete = o_type.statImpact / 1.25
            self.drain_cooldown = 2
        elif o_type.statImpact == HIGH:
            self.pointsToComplete = o_type.statImpact / 1.5
            self.drain_cooldown = 5
        self.drain_cooldown *= 1000
        self.crystalType = o_type.statType
        self.addStat = o_type.statImpact
        self.isCompleted = False
        self.timer = self.drain_cooldown

    def setRandom(self, sesja=False):
        if sesja:
            if self.objectiveType == "egzamin":
                self.setType("egzamin", True)
            else:
                self.setType(random.choice(list(objectiveTypesSession.keys())[1:]), True)
        else:
            self.setType(random.choice(list(objectiveTypes.keys())))

    def setLower(self, sesja=False):
        if sesja:
            pass
        else:
            if self.objectiveType == "gym":
                self.setType("healthy_food")
            elif self.objectiveType == "healthy_food":
                self.setType("walk")
            elif self.objectiveType == "party":
                self.setType("learn")
            elif self.objectiveType == "learn":
                self.setType("music")
            elif self.objectiveType == "multitasking":
                self.setType("speed_boots")
            elif self.objectiveType == "speed_boots":
                self.setType("no_break")

    def update(self):
        global premie_lotne_timer
        global premie_lotne_sprite_timer
        global premie_lotne_x, premie_lotne_y
        if self.timer < 0:
            self.points -= timer.get_time() / 1000
            if self.points < 0:
                self.points = 0
        else:
            self.timer -= timer.get_time()
        if self.isCompleted:
            self.setRandom(self.isSession())
        if premie_lotne_timer <= 0:
            resetPowerUps()
        else:
            premie_lotne_timer -= timer.get_time() / 3
        if premie_lotne_sprite_timer > 0:
            premie_lotne_sprite_timer -= timer.get_time() / 3
        if premie_lotne_sprite_timer <= 0:
            premie_lotne_x = 100000
            premie_lotne_y = 100000

    def clicked(self):
        global premie_lotne_x
        global premie_lotne_y
        global premie_lotne_type
        global premie_lotne_sprite_timer
        global premie_lotne_sprite_timer_duration
        global premie_lotne_is_negative
        if premie_lotne_sprite_timer <= 0 and premie_lotne_timer <= 0 and random.random() * 100 < premie_lotne_chance:
            premie_lotne_is_negative = random.randrange(0, 100) < premie_lotne_negative_chance
            premie_lotne_x = 0.4 + random.random() / 5
            premie_lotne_y = 0.4 + random.random() / 5
            premie_lotne_type = random.choice(range(premie_lotne_type_amount))
            premie_lotne_sprite_timer = premie_lotne_sprite_timer_duration
        self.timer = self.drain_cooldown
        if coffee_activated:
            if premie_lotne_is_negative:
                self.points += 0.5
            else:
                self.points += 2
        else:
            self.points += 1
        if self.points >= self.pointsToComplete:
            winclickSound.play()
            self.isCompleted = True
            if self.crystalType == HEALTH:
                global health_current
                global health_max
                health_current += self.addStat
                if health_current > health_max:
                    health_current = health_max
            elif self.crystalType == SANITY:
                global sanity_current
                global sanity_max
                sanity_current += self.addStat
                if sanity_current > sanity_max:
                    sanity_current = sanity_max
            elif self.crystalType == BIRET:
                global biret_current
                global biret_max
                biret_current += self.addStat
                if biret_current > biret_max:
                    biret_current = biret_max
            else:
                global time_current
                global time_max
                time_current += self.addStat
                if time_current > time_max:
                    time_current = time_max
        else:
            clickSound.play()


class ObjectiveType:
    def __init__(self, title, desc, statType, statImpact):
        self.title = title
        self.desc = desc
        self.statType = statType
        self.statImpact = statImpact
        self.renderedTitle = False
        self.renderedDesc = False


objectiveTypes = \
    {
        "walk": ObjectiveType("Spacer", "Czas na ruch", HEALTH, LOW),
        "healthy_food": ObjectiveType("Zdrowy Posiłek", "Masz ochotę na zdrowe jedzonko!", HEALTH, MEDIUM),
        "gym": ObjectiveType("Siłownia", "Przypakuj na siłce!", HEALTH, HIGH),
        "music": ObjectiveType("Muzyka", "Muzyka łagodzi obyczaje", SANITY, LOW),
        "learn": ObjectiveType("Nauka", "Pora zakuwać", SANITY, MEDIUM),
        "party": ObjectiveType("Impreza!", "Czas na małą imprezkę!", SANITY, HIGH),
        "no_break": ObjectiveType("Bez Przerwy", "Na co komu odpoczynek?", TIME, LOW),
        "speed_boots": ObjectiveType("Szybkie buty", "Szybkość jest wszystkim!", TIME, MEDIUM),
        "multitasking": ObjectiveType("Multitasking", "Wiele spraw na raz", TIME, HIGH),
    }
objectiveTypesSession = \
    {
        "egzamin": ObjectiveType("Egzamin", "", BIRET, HIGH),
        "grupowy": ObjectiveType("Projekt", "", BIRET, LOW),
        "prezentacja": ObjectiveType("Prezentacja", "", BIRET, LOW),
        "projekt": ObjectiveType("Projekt Grupowy", "", BIRET, LOW),
        "test": ObjectiveType("Test", "", BIRET, MEDIUM),
        "kolokwium": ObjectiveType("Kolokwium", "", BIRET, MEDIUM),
        "odpytka": ObjectiveType("Odpytka", "", BIRET, MEDIUM)
    }

for k in objectiveTypes:
    objectiveTypes[k].renderedTitle = font_title.render(objectiveTypes[k].title, False, objective_title_color)
    objectiveTypes[k].renderedDesc = font_desc.render(objectiveTypes[k].desc, False, objective_title_color)

for k in objectiveTypesSession:
    objectiveTypesSession[k].renderedTitle = font_title.render(objectiveTypesSession[k].title, False,
                                                               objective_title_color)
    objectiveTypesSession[k].renderedDesc = font_desc.render(objectiveTypesSession[k].desc, False,
                                                             objective_title_color)

objectives = [
    Objective(), Objective(), Objective()
]

objectives[0].setRandom()
objectives[1].setRandom()
objectives[2].setRandom()

health_max = 100
health_current = 100
health_drain = 1

sanity_max = 100
sanity_current = 100
sanity_drain = 1.15

time_max = 100
time_current = 100
time_drain = 1.175

biret_max = 100
biret_current = 50
biret_drain = 5

biret_current_loops = 0
biret_loops = 6

game_time = 0
session_errors = 0
session_delay = 1.05 * 1000 * 60
session_duration = .5 * 1000 * 60
isSession = False

clock_activated = False
coffee_activated = False
energy_drink_activated = False
premie_lotne_type_amount = 5
premie_lotne_timer = 0
premie_lotne_base_duration = 5000
premie_lotne_chance = 100
premie_lotne_negative_chance = 50
premie_lotne_is_negative = False
premie_lotne_x = 0
premie_lotne_y = 0
premie_lotne_type = 0
premie_lotne_sprite_timer = 0
premie_lotne_sprite_timer_duration = 2000

endless_time = 0

def getPowerUpSprite(t):
    global clock_activated
    global coffee_activated
    global energy_drink_activated
    if premie_lotne_is_negative:
        if t == 0:
            return anticlock
        elif t == 1:
            return anticoffee
        elif t == 2:
            return antienergy_drink
        elif t == 3:
            return antibook
        elif t == 4:
            return antidumbell
    else:
        if t == 0:
            return clock
        elif t == 1:
            return coffee
        elif t == 2:
            return energy_drink
        elif t == 3:
            return book
        elif t == 4:
            return dumbell


def activatePowerUp(t):
    global clock_activated
    global coffee_activated
    global energy_drink_activated
    global premie_lotne_sprite_timer
    global premie_lotne_timer
    global premie_lotne_is_negative
    global premie_lotne_x
    global premie_lotne_y
    premie_lotne_x = 100000
    premie_lotne_y = 100000
    premie_lotne_timer = premie_lotne_base_duration
    premie_lotne_sprite_timer = -1
    if t == 0:
        clock_activated = True
        achievements[3].addScore()
    elif t == 1:
        coffee_activated = True
        achievements[1].addScore()
    elif t == 2:
        energy_drink_activated = True
        achievements[0].addScore()
    elif t == 3:
        achievements[2].addScore()
        if premie_lotne_is_negative:
            objectives[0].points = 0
            objectives[1].points = 0
            objectives[2].points = 0
        else:
            objectives[0].points = 10000
            objectives[1].points = 10000
            objectives[2].points = 10000
            objectives[0].clicked()
            objectives[1].clicked()
            objectives[2].clicked()
    elif t == 4:
        achievements[4].addScore()
        objectives[0].setLower()
        objectives[1].setLower()
        objectives[2].setLower()
    premie_lotne_sprite_timer = 0


def resetPowerUps():
    global clock_activated
    global coffee_activated
    global energy_drink_activated
    clock_activated = False
    coffee_activated = False
    energy_drink_activated = False


active_text_box = ""
text_boxes = {
    "username": "",
    "nick": "",
    "password": ""
}


def refreshGame():
    global endless_time
    global health_max
    global health_current
    global health_drain
    global sanity_max
    global sanity_current
    global sanity_drain
    global time_max
    global time_current
    global time_drain
    global current_game_background
    global objectives
    global clock_activated
    global coffee_activated
    global energy_drink_activated
    global premie_lotne_timer
    global premie_lotne_sprite_timer_duration
    global premie_lotne_chance
    global game_time
    global biret_loops
    global objective_paper
    global session_errors
    global birret_current_loops
    global dialog
    endless_time = 0
    dialog = 0
    birret_current_loops = 0
    session_errors = 0
    objective_paper = objective_paper_normal
    biret_loops = 6
    game_time = 0
    resetPowerUps()
    objectives[0].setRandom()
    objectives[1].setRandom()
    objectives[2].setRandom()
    health_max = 100
    health_current = 100
    health_drain = 1.25
    sanity_max = 100
    sanity_current = 100
    sanity_drain = 1.5
    time_max = 100
    time_current = 100
    time_drain = 1.75
    current_game_background = Computer_science_difficulty
    clock_activated = False
    coffee_activated = False
    energy_drink_activated = False
    premie_lotne_timer = 0
    premie_lotne_sprite_timer = 0
    premie_lotne_sprite_timer_duration = 1000
    premie_lotne_chance = 2


current_difficulty = 0


def setDifficulty(level):
    global health_drain
    global sanity_drain
    global time_drain
    global premie_lotne_sprite_timer_duration
    global premie_lotne_chance
    global current_game_background
    global biret_loops
    global objective_paper
    global current_difficulty
    global isSession
    isSession = False
    current_difficulty = level
    playMusic("gametheme")
    health_drain = 1
    sanity_drain = 1.15
    time_drain = 1.175
    premie_lotne_sprite_timer_duration = 2000
    premie_lotne_chance = 2
    if level == 0:
        health_drain *= 0.95
        sanity_drain *= 0.95
        time_drain *= 0.95
        current_game_background = game_background
        premie_lotne_sprite_timer_duration *= 1.5
        premie_lotne_chance *= 2
        biret_loops = 6
    elif level == 2:
        health_drain *= 1.25
        sanity_drain *= 1.25
        time_drain *= 1.25
        current_game_background = Medic_school_difficulty
        premie_lotne_sprite_timer_duration *= 1
        premie_lotne_chance *= 1
        biret_loops = 6
    elif level == 3:
        health_drain *= 1.25
        sanity_drain *= 1.25
        time_drain *= 1.25
        current_game_background = endless_background
        premie_lotne_sprite_timer_duration *= 1
        premie_lotne_chance *= 1
        biret_loops = 9999999
        objective_paper = objective_paper_endless
        playMusic("endlesstheme")


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


text_timer = 0
last_key = 0

text_caret = 0


def renderTextBox(index, rect, encrypted=False):
    global active_text_box
    global text_timer
    global last_key
    global text_caret
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
        # elif e.type == pygame.KEYDOWN:
        # if active_text_box == index:
        # if e.key == pygame.K_BACKSPACE:
        # text = text[:-1]
        # else:
        # text += e.unicode
        pygame.event.post(e)
    ks = pygame.key.get_pressed()
    if active_text_box == index:
        if text_caret < 250:
            renderScaled(pixel, pygame.Rect(rect.x + 12 + min(len(text), 32) * 12, rect.y + 12, 4, rect.h - 24))
        text_caret += timer.get_time()
        if text_caret > 500:
            text_caret = 0
        # for k in range(97, 123):
        for k in range(0, 127):
            if ks[k]:
                if last_key != k:
                    if ks[pygame.K_BACKSPACE]:
                        text = text[:-1]
                    else:
                        if ks[pygame.K_LSHIFT]:
                            if k == 50:
                                text += "@"
                            else:
                                text += chr(k - 32)
                        else:
                            text += chr(k)
                    text_timer = 250
                    last_key = k
                elif text_timer < 0:
                    if ks[pygame.K_BACKSPACE]:
                        text = text[:-1]
                    else:
                        if ks[pygame.K_LSHIFT]:
                            if k == 50:
                                text += "@"
                            else:
                                text += chr(k - 32)
                        else:
                            text += chr(k)
                    text_timer = 50
                    last_key = k
                break
    if text_timer >= 0:
        text_timer -= timer.get_time()

    render = 0
    s = ""
    if encrypted:
        for i in range(len(text)):
            s = s + "*"
    else:
        s = text
    s = s[-32:]
    render = font.render(s, False, (0, 0, 0))
    screen.blit(render, (rect.x + 10, rect.y + 5))
    text_boxes[index] = text


class Button:
    def __init__(self, sprite, sprite_p, width, height, percent_x, percent_y, offset_x=0, offset_y=0):
        self.pressed = False

        self.offset_y = offset_y
        self.offset_x = offset_x
        self.percent_y = percent_y
        self.percent_x = percent_x
        self.height = height
        self.width = width
        self.sprite = sprite
        self.sprite_p = sprite_p
        self.sprite_t = self.sprite
        self.centerAnchor = centerAnchor(self.width, self.height, self.percent_x, self.percent_y, self.offset_x,
                                         self.offset_y)

    def draw(self):
        renderScaled(self.sprite_t, self.centerAnchor)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.centerAnchor.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.sprite_t = self.sprite_p
                self.pressed = True
            else:
                if self.pressed == True:
                    self.pressed = False
                    self.sprite_t = self.sprite
        else:
            self.sprite_t = self.sprite


#
x_b = Button(x_button, x_button_p, 64, 64, 1, 0, -32, 32)
podyplomowe_b = Button(podyplomowe_button, podyplomowe_button_p, 384 * 2, 89 * 1.5, 0.75, 0.25)
informatyczne_b = Button(informatyczne_button, informatyczne_button_p, 384 * 2, 89 * 1.5, 0.75, 0.4)
medyczne_b = Button(medyczne_button, medyczne_button_p, 384 * 2, 89 * 1.5, 0.75, 0.55)
endless_b = Button(endless_button, endless_button_p, 384 * 2, 89 * 1.5, 0.75, 0.7)
# main menu
new_game_b = Button(new_game_button, new_game_button_p, 256, 80, 0.5, 0.30, 0, 128 // 2)
login_enter_b = Button(login_button, login_button_p, 256, 80, 0.5, 0.40, 0, 128 // 2)
exit_b = Button(exit_button, exit_button_p, 256, 80, 0.5, 0.70, 0, 128 // 2)
achievements_b = Button(achievements_button, achievements_button_p, 256, 80, 0.5, 0.6, 0, 128 // 2)
# login
login_b = Button(login_button, login_button_p, 157, 60, 0.5, 0.3, 0, 128 // 2 - 30 + 32)
login_back_b = Button(back_button, back_button_p, 256, 70, 0.5, 0.4, 136, 128 // 2 + 32)
register_enter_b = Button(register_button, register_button_p, 256, 70, 0.5, 0.4, -136, 128 // 2 + 32)
logout_b = Button(logout_button, logout_button_p, 60, 60, 0, 0, 80 + len(logged_username) * 6.5 + 17 * 6.5, 80)

# register
register_b = Button(register_button, register_button_p, 256, 70, 0.5, 0.45, 0, 128 // 2 - 30 + 32)
register_back_b = Button(back_button, back_button_p, 256, 70, 0.5, 0.55, 0, 128 // 2 + 32)

# legend
tooltip_b = Button(tooltip_button, tooltip_button_p, 256, 80, 0.5, 0.5, 0, 128 // 2)
try_again_b = Button(try_again_button, try_again_button_p, 256 + 96, 80, 0.5, 1, -256-128, -64)
end_game_b = Button(end_game_button, end_game_button_p, 256, 80, 0.5, 1, 256+128, -64)


win_game_b = Button(win_game_button, win_game_button_p, 256, 80, 0.5, 1, 0, -64)

def renderObjectivePaper(index=0):
    o_type = 0
    if objectives[index].isSession():
        o_type = objectiveTypesSession[objectives[index].objectiveType]
    else:
        o_type = objectiveTypes[objectives[index].objectiveType]
    offset_x = 0
    if index == 0:
        offset_x = -82 * 3.5 - 50
    elif index == 1:
        offset_x = 0
    else:
        offset_x = 82 * 3.5 + 50

    renderScaled(objective_paper, centerAnchor(82 * 3.5, 102 * 3.5, 0.5, 1, offset_x, -102 * 1.75))

    renderScaled(o_type.renderedTitle,
                 centerAnchor(128 + 64, 48, 0.5, 1, offset_x, -102 * 1.75 - 150 + 35))
    # renderScaled(o_type.renderedDesc,
    # centerAnchor(128 + 64 + 32, 48, 0.5, 1, offset_x, -102 * 1.75 - 50))

    filler = time_filler

    if objectives[index].crystalType == 0:
        renderScaled(crystal_red, centerAnchor(32, 32, 0.5, 1, offset_x, -170 - 12))
        filler = health_filler
    elif objectives[index].crystalType == 1:
        renderScaled(crystal_blue, centerAnchor(32, 32, 0.5, 1, offset_x, -170 - 12))
        filler = sanity_filler
    elif objectives[index].crystalType == 3:
        renderScaled(crystal_black, centerAnchor(32, 32, 0.5, 1, offset_x, -170 - 12))
        filler = biret_filler
    else:
        renderScaled(crystal_green, centerAnchor(32, 32, 0.5, 1, offset_x, -170 - 12))

    objectives[index].update()
    fill = objectives[index].points / objectives[index].pointsToComplete
    renderScaled(filler, centerAnchor(192 * fill, 32, 0.5, 1,
                                      -192 / 2 + (192 * fill / 2) + offset_x, -275 + 35))
    renderScaled(objective_progress_bar, centerAnchor(192, 32, 0.5, 1, offset_x, -275 + 35))

    if o_type.statImpact == HIGH:
        renderScaled(diffuculty_progress_bar_hard, centerAnchor(96 * 2.5, 8 * 4, 0.5, 1, offset_x, -125))
    elif o_type.statImpact == MEDIUM:
        renderScaled(diffuculty_progress_bar_medium, centerAnchor(96 * 2.5, 8 * 4, 0.5, 1, offset_x, -125))
    else:
        renderScaled(diffuculty_progress_bar_easy, centerAnchor(96 * 2.5, 8 * 4, 0.5, 1, offset_x, -125))


def renderObjectivePanel(percent_y=0.5, offset_x=0, index=0, reversed=False):
    panel = objective_panel
    o_type = objectiveTypes[objectives[index].objectiveType]
    if reversed:
        panel = objective_panel_reversed
    renderScaled(panel, centerAnchor(256, 128, reversed, percent_y, (1 - reversed * 2) * (256 // 2) * offset_x))

    renderScaled(o_type.renderedTitle,
                 centerAnchor(128 + 64, 48, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x, -44))
    renderScaled(o_type.renderedDesc,
                 centerAnchor(128 + 64, 48, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x, 36))

    crystal_white = timeicon_white
    crystal_black = timeicon_black
    filler = time_filler

    if objectives[index].crystalType == 0:
        renderScaled(crystal_red, centerAnchor(32, 32, reversed, percent_y,
                                               (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
        crystal_white = healthicon_white
        crystal_black = healthicon_black
        filler = health_filler
    elif objectives[index].crystalType == 1:
        renderScaled(crystal_blue, centerAnchor(32, 32, reversed, percent_y,
                                                (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))
        crystal_white = sanityicon_white
        crystal_black = sanityicon_black
        filler = sanity_filler
    else:
        renderScaled(crystal_green, centerAnchor(32, 32, reversed, percent_y,
                                                 (1 - reversed * 2) * (256 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact == HIGH:
        renderScaled(crystal_white,
                     centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)),
                                  -32))
    else:
        renderScaled(crystal_black,
                     centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)),
                                  -32))

    if o_type.statImpact >= MEDIUM:
        renderScaled(crystal_white, centerAnchor(16, 16, reversed, percent_y,
                                                 (1 - reversed * 2) * (288 - (256 // 2) * (1 - offset_x))))
    else:
        renderScaled(crystal_black, centerAnchor(16, 16, reversed, percent_y,
                                                 (1 - reversed * 2) * (288 - (256 // 2) * (1 - offset_x))))

    if o_type.statImpact >= LOW:
        renderScaled(crystal_white,
                     centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)),
                                  32))
    else:
        renderScaled(crystal_black,
                     centerAnchor(16, 16, reversed, percent_y, (1 - reversed * 2) * (272 - (256 // 2) * (1 - offset_x)),
                                  32))

    objectives[index].update()
    fill = objectives[index].points / objectives[index].pointsToComplete  # -192 / 2 * (1 - fill)
    renderScaled(filler, centerAnchor(192 * fill, 32, reversed, percent_y,
                                      (1 - reversed * 2) * (256 // 2 - 16) * offset_x - 192 / 2 * (1 - fill)))
    renderScaled(objective_progress_bar,
                 centerAnchor(192, 32, reversed, percent_y, (1 - reversed * 2) * (256 // 2 - 16) * offset_x))


def renderMainMenu():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(sun.play(), centerAnchor(48 * 4, 48 * 4, 0.1, 0.2))
    renderScaled(title, centerAnchor(384, 256, 0.5, 0.05, 0, 128 // 2 + 30))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.7, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.9, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.8, 0.4))
    renderScaled(smoke.play(), centerAnchor(48 * 4, 48 * 4, 0.955, 0.45))
    new_game_b.draw()
    login_enter_b.draw()
    tooltip_b.draw()
    exit_b.draw()
    achievements_b.draw()
    if not logged_username == "":
        render = font.render("Zalogowano jako: " + logged_username, False, (0, 0, 0))
        screen.blit(render, centerAnchor(100, 20, 0, 0, 70, 20))
        logout_b.draw()
    else:
        render = font.render("Nie zalogowano", False, (0, 0, 0))
        screen.blit(render, centerAnchor(100, 20, 0, 0, 70, 20))


announcement = ""


def renderLoginPanel():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(sun.play(), centerAnchor(48 * 4, 48 * 4, 0.1, 0.2))
    renderScaled(title, centerAnchor(384, 256, 0.5, 0.05, 0, 128 // 2 + 30))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.7, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.9, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.8, 0.4))
    renderScaled(smoke.play(), centerAnchor(48 * 4, 48 * 4, 0.955, 0.45))
    renderScaled(login_panel, centerAnchor(750, 768, 0.5, 0.3375, 0, 128 // 2))
    renderScaled(text_username, centerAnchor(128, 70, 0.5, 0.075, 0, 128 // 2 - 70 + 32))
    renderTextBox("username", centerAnchor(512, 70, 0.5, 0.075, 0, 128 // 2 + 32))
    renderScaled(text_password, centerAnchor(128, 70, 0.5, 0.225, 0, 128 // 2 - 100 + 32))
    renderTextBox("password", centerAnchor(512, 70, 0.5, 0.225, 0, 128 // 2 - 30 + 32), True)
    login_b.draw()
    login_back_b.draw()
    register_enter_b.draw()
    if register_enter_b.pressed:
        a = font.render(" ", False, (200, 0, 0))
        renderScaled(a, centerAnchor(550, 100, 0.5, 0, 0, 128 // 2 + 600))
    if announcement != "":
        a = font.render(announcement, False, (200, 0, 0))
        renderScaled(a, centerAnchor(550, 100, 0.5, 0, 0, 128 // 2 + 600))


def renderRegisterPanel():
    renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(sun.play(), centerAnchor(48 * 4, 48 * 4, 0.1, 0.2))
    renderScaled(title, centerAnchor(384, 128, 0.5, 0.05, 0, 128 // 2 + 30))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.7, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.9, 0.2))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.8, 0.4))
    renderScaled(smoke.play(), centerAnchor(48 * 4, 48 * 4, 0.955, 0.45))
    renderScaled(login_panel, centerAnchor(750, 768, 0.5, 0.3375, 0, 128 // 2))
    renderScaled(text_username, centerAnchor(128, 70, 0.5, 0.075, 0, 128 // 2 - 70 + 32))
    renderTextBox("username", centerAnchor(512, 70, 0.5, 0.075, 0, 128 // 2 + 32))
    renderScaled(text_nick, centerAnchor(128, 70, 0.5, 0.225, 0, 128 // 2 - 100 + 32))
    renderTextBox("nick", centerAnchor(512, 70, 0.5, 0.225, 0, 128 // 2 - 30 + 32))

    renderScaled(text_password, centerAnchor(128, 70, 0.5, 0.375, 0, 128 // 2 - 130 + 32))
    renderTextBox("password", centerAnchor(512, 70, 0.5, 0.375, 0, 128 // 2 - 60 + 32), True)
    register_b.draw()
    register_back_b.draw()
    if register_back_b.pressed:
        a = font.render(" ", False, (200, 0, 0))
        renderScaled(a, centerAnchor(550, 100, 0.5, 0, 0, 128 // 2 + 600))
    # renderScaled(register_button, centerAnchor(256, 70, 0.5, 0.3, 0, 128 // 2 - 30))
    # renderScaled(text_register2, centerAnchor(157, 60, 0.5, 0.3, 0, 128 // 2 - 30))
    # renderScaled(back_button, centerAnchor(256, 70, 0.5, 0.4, 0, 128 // 2))

    # renderScaled(text_back, centerAnchor(157, 60, 0.5, 0.4, 0, 128 // 2))
    # signUp(text_boxes['username'], text_boxes['password'])
    if announcement != "":
        a = font.render(announcement, False, (200, 0, 0))
        renderScaled(a, centerAnchor(550, 100, 0.5, 0, 0, 128 // 2 + 600))


def renderLegend():
    renderScaled(notebook_background, centerAnchor(1920, 1080))
    x_b.draw()
    renderScaled(text_legend_stats, centerAnchor(256, 48, 0.25, 0, 0, 64))
    renderScaled(text_legend_stats_desc, centerAnchor(800, 32, 0.25, 0, 0, 128))
    renderScaled(text_legend_stats_desc2, centerAnchor(800, 32, 0.25, 0, 0, 128 + 32))

    renderScaled(healthicon, centerAnchor(128, 128, 0.25, 0, -320, 256 + 64))
    renderScaled(text_legend_stats_health, centerAnchor(500, 32, 0.25, 0, 100, 256 + 64))

    renderScaled(sanityicon, centerAnchor(128, 128, 0.25, 0, -320, 384 + 128))
    renderScaled(text_legend_stats_sanity, centerAnchor(500, 32, 0.25, 0, 100, 384 + 128))

    renderScaled(timeicon, centerAnchor(128, 128, 0.25, 0, -320, 512 + 192))
    renderScaled(text_legend_stats_time, centerAnchor(500, 32, 0.25, 0, 100, 512 + 192))

    renderScaled(bireticon, centerAnchor(128, 128, 0.25, 0, -320, 512 + 128 + 256))
    renderScaled(text_legend_stats_biret, centerAnchor(500, 32, 0.25, 0, 100, 512 + 128 + 256))

    renderScaled(text_legend_premie_lotne, centerAnchor(256, 48, 0.75, 0, 0, 64))
    renderScaled(text_legend_premie_lotne_desc, centerAnchor(800, 32, 0.75, 0, 0, 128))
    renderScaled(text_legend_premie_lotne_desc2, centerAnchor(800, 32, 0.75, 0, 0, 128 + 32))

    renderScaled(book, centerAnchor(128, 128, 0.75, 0, -360, 256 + 64))
    renderScaled(text_legend_premie_lotne_book, centerAnchor(550, 32, 0.75, 0, 162, 256 + 32))
    renderScaled(antibook, centerAnchor(128, 128, 0.75, 0, -216, 256 + 64))
    renderScaled(text_legend_premie_lotne_antibook, centerAnchor(550, 32, 0.75, 0, 162, 256 + 72))

    renderScaled(clock, centerAnchor(128, 128, 0.75, 0, -360, 384 + 64))
    renderScaled(text_legend_premie_lotne_clock, centerAnchor(550, 32, 0.75, 0, 162, 384 + 56))
    renderScaled(anticlock, centerAnchor(128, 128, 0.75, 0, -216, 384 + 64))
    renderScaled(text_legend_premie_lotne_anticlock, centerAnchor(550, 32, 0.75, 0, 162, 384 + 96))

    renderScaled(coffee, centerAnchor(128, 128, 0.75, 0, -360, 512 + 64))
    renderScaled(text_legend_premie_lotne_coffe, centerAnchor(550, 32, 0.75, 0, 162, 512 + 56))
    renderScaled(anticoffee, centerAnchor(128, 128, 0.75, 0, -216, 512 + 64))
    renderScaled(text_legend_premie_lotne_anticoffe, centerAnchor(550, 32, 0.75, 0, 162, 512 + 96))

    renderScaled(dumbell, centerAnchor(128, 128, 0.75, 0, -360, 640 + 64))
    renderScaled(text_legend_premie_lotne_dumbell, centerAnchor(550, 32, 0.75, 0, 162, 640 + 56))
    renderScaled(antidumbell, centerAnchor(128, 128, 0.75, 0, -216, 640 + 64))
    renderScaled(text_legend_premie_lotne_antidumbell, centerAnchor(550, 32, 0.75, 0, 162, 640 + 96))

    renderScaled(energy_drink, centerAnchor(128, 128, 0.75, 0, -360, 768 + 64))
    renderScaled(text_legend_premie_lotne_energy_drink, centerAnchor(550, 32, 0.75, 0, 162, 768 + 56))
    renderScaled(antienergy_drink, centerAnchor(128, 128, 0.75, 0, -216, 768 + 64))
    renderScaled(text_legend_premie_lotne_antienergy_drink, centerAnchor(550, 32, 0.75, 0, 162, 768 + 96))

achievementCount = 0
achievement_popup_index = 0
achievement_popup_time = 0
def showAchievementPopup(index):
    global achievement_popup_time, achievement_popup_index
    achievement_popup_time = 3 * 1000
    achievement_popup_index = index
    achievementgetSound.play()
    dbPushAchievement(logged_username, index, achievements[index].getTier())
class Achievement:
    def __init__(self, title1, desc, bronze_prize, silver_prize, gold_prize):
        global achievementCount
        self.title = title1
        self.desc = desc
        self.score = 0
        self.bronze_prize = bronze_prize
        self.silver_prize = silver_prize
        self.gold_prize = gold_prize
        self.index = achievementCount
        achievementCount += 1

    def getTitle(self):
        if logged_username == "":
            return "?????????"
        else:
            return self.title

    def getDesc(self, level):
        if logged_username == "":
            return "?????????????????"
        else:
            if self.score >= self.gold_prize:
                return "       MAX       "
            elif self.score >= self.silver_prize:
                return self.desc.replace("~", str(self.gold_prize))
            elif self.score >= self.bronze_prize:
                return self.desc.replace("~", str(self.silver_prize))
            else:
                return self.desc.replace("~", str(self.bronze_prize))

    def getTrophy(self):
        if logged_username == "":
            return trophy_none
        else:
            if self.score >= self.gold_prize:
                return trophy_gold
            elif self.score >= self.silver_prize:
                return trophy_silver
            elif self.score >= self.bronze_prize:
                return trophy_bronze
            else:
                return trophy_none

    def setTier(self, tier):
        if tier == 3:
            self.score = self.gold_prize
        elif tier == 2:
            self.score = self.silver_prize
        elif tier == 1:
            self.score = self.bronze_prize
        else:
            self.score = 0
    def getTier(self):
        if self.score >= self.gold_prize:
            return 3
        elif self.score >= self.silver_prize:
            return 2
        elif self.score >= self.bronze_prize:
            return 1
        else:
            return 0
    def addScore(self, instagold=False):
        if logged_username != "":
            tier = self.getTier()
            if instagold:
                self.setTier(3)
            else:
                self.score += 1
            if self.getTier() > tier:
                showAchievementPopup(self.index)
    def addScoreEndless(self, time):
        if logged_username != "":
            tier = self.getTier()
            if time / 60000 > self.score:
                self.score = time / 60000
            if self.getTier() > tier:
                showAchievementPopup(self.index)


achievements =\
[
    Achievement("Czysta Energia", "Podczas rozgrywki użyj ~ Energetyków", 5, 25, 50),
    Achievement("Kawa to moje paliwo", "Podczas rozgrywki użyj ~ Kaw", 5, 25, 50),
    Achievement("Mól książkowy", "Podczas rozgrywki użyj ~ Książek", 5, 25, 50),
    Achievement("Zegarmistrz", "Podczas rozgrywki użyj ~ Zegarów", 5, 25, 50),
    Achievement("Trening na pełnej", "Podczas rozgrywki użyj ~ Hantli", 5, 25, 50),
    Achievement("Bananowy Student", "Przejdź do następnej sesji z 2 ubytkami", 1, 2, 3),
    Achievement("Warunkowy Student", "Przejdź do następnej sesji z 1 ubytkiem", 1, 2, 3),
    Achievement("Licencjat", "Ukończ studia podyplomowe", 1, 2, 3),
    Achievement("Anonymous", "Ukończ studia informatyczne", 1, 2, 3),
    Achievement("Doktor House", "Ukończ studia medyczne", 1, 2, 3),
    Achievement("Pilny Student", "Przejdź 1 kierunek studiów bez ubytków", 1, 2, 3),
    Achievement("Wieczny Student", "Przeżyj ~ minut w trybie nieskończonym", 5, 10, 20),
]
def isEndlessUnlocked():
    return achievements[7].getTier() == 3 and achievements[8].getTier() and achievements[9].getTier()

def renderAchievements():
    renderScaled(notebook_achievements_background, centerAnchor(1920, 1080))
    x_b.draw()
    renderScaled(text_achievements, centerAnchor(256, 48, 0.25, 0, 0, 64))
    renderScaled(text_achievements, centerAnchor(256, 48, 0.75, 0, 0, 64))
    for i in range(6):
        renderScaled(achievements[i].getTrophy(), centerAnchor(896, 128, 0.25, 0, 0, 192 + i * 140))
        renderScaled(font_title.render(achievements[i].getTitle(), False, (0, 0, 0)),
                     centerAnchor(400, 64, 0.25, 0, 100, 192 + i * 140 - 32))
        renderScaled(font_title.render(achievements[i].getDesc(0), False, (0, 0, 0)),
                     centerAnchor(600, 64, 0.25, 0, 100, 192 + i * 140 + 32))
    for i in range(6):
        renderScaled(achievements[i + 6].getTrophy(), centerAnchor(896, 128, 0.75, 0, 0, 192 + i * 140))
        renderScaled(font_title.render(achievements[i + 6].getTitle(), False, (0, 0, 0)),
                     centerAnchor(400, 64, 0.75, 0, 100, 192 + i * 140 - 32))
        renderScaled(font_title.render(achievements[i + 6].getDesc(0), False, (0, 0, 0)),
                     centerAnchor(600, 64, 0.75, 0, 100, 192 + i * 140 + 32))


def renderGame():
    renderScaled(current_game_background, centerAnchor(1920, 1080))
    global game_time, biret_current
    global biret_max
    global health_current
    global sanity_current
    global time_current
    global gameState
    global birret_current_loops
    global isSession
    global achievement_popup_time
    global achievement_popup_index
    global endless_time
    game_time += timer.get_time()
    renderScaled(board, centerAnchor(512, 256, 0.5, 0, 0, 256 // 2 + 20))
    if game_time > session_delay:
        if not objectives[0].isSession():
            biret_current = 50
            objectives[0].setRandom(True)
            objectives[1].setType("egzamin", True)
            objectives[2].setRandom(True)
            setDifficulty(current_difficulty)
        if not isSession:
            isSession = True
            playMusic("redthemeclock")
        renderScaled(session_overlay, centerAnchor(1920, 1080))
        renderScaled(board, centerAnchor(512, 256, 0.5, 0, 0, 256 // 2 + 20))
        fill = biret_current / biret_max
        renderScaled(biret_filler, centerAnchor(384 * fill, 64, 0.5, 0, -384 / 2 * (1 - fill), 256 // 2 + 20))
        renderScaled(sanitybar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20))
        renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20))
        renderScaled(bireticon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20))
        time_delta = timer.get_time()
        if clock_activated:
            if premie_lotne_is_negative:
                time_delta *= 2
            else:
                time_delta = 0
        biret_current -= biret_drain * (time_delta / 1000)

        if biret_current <= 0:
            gameState = "game_over"
            playMusic("endtheme")
            health_current = 100
            sanity_current = 100
            time_current = 100
            biret_current = 50
    else:
        fill = health_current / health_max
        renderScaled(health_filler, centerAnchor(384 * fill, 64, 0.5, 0, -384 / 2 * (1 - fill), 256 // 2 + 20 - 70))
        renderScaled(healthbar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 - 70))
        fill = sanity_current / sanity_max
        renderScaled(sanity_filler, centerAnchor(384 * fill, 64, 0.5, 0, -384 / 2 * (1 - fill), 256 // 2 + 20))
        renderScaled(sanitybar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20))
        fill = time_current / time_max
        renderScaled(time_filler, centerAnchor(384 * fill, 64, 0.5, 0, -384 / 2 * (1 - fill), 256 // 2 + 20 + 70))
        renderScaled(timebar, centerAnchor(384, 64, 0.5, 0, 0, 256 // 2 + 20 + 70))

        renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20 - 70))
        renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20))
        renderScaled(deathicon, centerAnchor(32, 32, 0.5, 0, -216, 256 // 2 + 20 + 70))
        renderScaled(healthicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20 - 70))
        renderScaled(sanityicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20))
        renderScaled(timeicon, centerAnchor(32, 32, 0.5, 0, 216, 256 // 2 + 20 + 70))
        time_delta = timer.get_time()
        if clock_activated:
            if premie_lotne_is_negative:
                time_delta *= 2
            else:
                time_delta = 0
        health_current -= health_drain * (time_delta / 1000)
        sanity_current -= sanity_drain * (time_delta / 1000)
        time_current -= time_drain * (time_delta / 1000)
        if health_current <= 0 or sanity_current <= 0 or time_current <= 0:
            gameState = "game_over"
            gameover_background.reset()
            playMusic("endtheme")  # dodać muzykę końca gry
            health_current = 100
            sanity_current = 100
            time_current = 100
            biret_current = 50

    renderObjectivePaper(0)
    renderObjectivePaper(1)
    renderObjectivePaper(2)

    x_b.draw()

    if premie_lotne_sprite_timer > 0:
        renderScaled(getPowerUpSprite(premie_lotne_type), centerAnchor(128, 128, premie_lotne_x, premie_lotne_y))
    if 60 * 1000 - 5000 < session_delay - game_time < 60 * 1000:
        renderScaled(sesja, centerAnchor(196 * 3, 64 * 3, 1, 0, -196, 540))
    if game_time > session_duration + session_delay:
        global biret_current_loops
        global session_errors
        objectives[0].setRandom()
        objectives[1].setRandom()
        objectives[2].setRandom()
        setDifficulty(current_difficulty)
        game_time = 0
        biret_current_loops += 1
        if biret_current < biret_max * 0.5:
            gameState = "game_over"
            gameover_background.reset()
            playMusic("endtheme")
            health_current = 100
            sanity_current = 100
            time_current = 100
            biret_current = 50
        elif biret_current < biret_max * 0.625:
            session_errors += 2
            achievements[5].addScore(True)
        elif biret_current < biret_max * 0.75:
            session_errors += 1
            achievements[6].addScore(True)
        if biret_current_loops == biret_loops:
            gameState = "win"
            playMusic("wintheme")
            if session_errors == 0:
                achievements[10].addScore(True)
            if current_difficulty == 0:
                achievements[7].addScore(True)
            elif current_difficulty == 1:
                achievements[8].addScore(True)
            elif current_difficulty == 2:
                achievements[9].addScore(True)

    if current_difficulty == 3:
        endless_time += timer.get_time()
        achievements[11].addScoreEndless(endless_time)
    if achievement_popup_time > 0:
        achievement_popup_time -= timer.get_time()
        renderScaled(achievements[achievement_popup_index].getTrophy(), centerAnchor(224 * 3, 64 * 1.5, 0, 0.1, 224 * 1.5))
        renderScaled(font_title.render(achievements[achievement_popup_index].getTitle(), False, (0, 0, 0)), centerAnchor(300, 64 * 1.5 / 2, 0, 0.1, 380, -24))
        renderScaled(font_title.render("Zdobyto osiągnięcie!", False, (0, 0, 0)), centerAnchor(300, 64 * 1.5 / 2, 0, 0.1, 380, 16))

def renderDifficultySetter():
    mouse = pygame.mouse.get_pos()
    if centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.25).collidepoint(mouse[0], mouse[1]):
        renderScaled(game_background, centerAnchor(1920, 1080))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.4).collidepoint(mouse[0], mouse[1]):
        renderScaled(Computer_science_difficulty, centerAnchor(1920, 1080))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.55).collidepoint(mouse[0], mouse[1]):
        renderScaled(Medic_school_difficulty, centerAnchor(1920, 1080))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.7).collidepoint(mouse[0], mouse[1]) and isEndlessUnlocked():
        renderScaled(endless_background, centerAnchor(1920, 1080))
    else:
        renderScaled(main_menu_background, centerAnchor(1920, 1080))
    renderScaled(board, centerAnchor(415 * 2, 256 * 2, 0.25, 0.5, 128, -64))
    if logged_username == "":
        renderScaled(warning_login, centerAnchor(640+256+256+256, 128, 0.5, 0.075))
        renderScaled(text_warning_login, centerAnchor(620+256+256+256, 118, 0.5, 0.075))

    if centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.25).collidepoint(mouse[0], mouse[1]):
        renderScaled(text_level_desc_1_dif, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -126))
        renderScaled(text_level_desc_1_len, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -64))
        renderScaled(text_level_desc_1_boost, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -2))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.4).collidepoint(mouse[0], mouse[1]):
        renderScaled(text_level_desc_2_dif, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -126))
        renderScaled(text_level_desc_2_len, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -64))
        renderScaled(text_level_desc_2_boost, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -2))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.55).collidepoint(mouse[0], mouse[1]):
        renderScaled(text_level_desc_3_dif, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -126))
        renderScaled(text_level_desc_3_len, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -64))
        renderScaled(text_level_desc_3_boost, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -2))
    elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.7).collidepoint(mouse[0], mouse[1]) and isEndlessUnlocked():
        renderScaled(text_level_desc_4_dif, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -126))
        renderScaled(text_level_desc_4_len, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -64))
        renderScaled(text_level_desc_4_boost, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -2))

    else:
        renderScaled(text_dummy, centerAnchor(380 * 2, 32 * 2, 0.25, 0.5, 128, -64))

    podyplomowe_b.draw()
    informatyczne_b.draw()
    medyczne_b.draw()
    if isEndlessUnlocked():
        endless_b.draw()
    else:
        renderScaled(endless_button_i, centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.7))
    x_b.draw()


dialog = 0


def renderOpening():
    global gameState
    if current_difficulty == 0:
        renderScaled(game_opening_easy.play(), centerAnchor(1920, 1080))
    elif current_difficulty == 1:
        renderScaled(game_opening_medium.play(), centerAnchor(1920, 1080))
    elif current_difficulty == 2:
        renderScaled(game_opening_hard.play(), centerAnchor(1920, 1080))
    elif current_difficulty == 3:
        renderScaled(game_opening_endless.play(), centerAnchor(1920, 1080))
    if current_difficulty == 3:
        renderScaled(pixel_white, centerAnchor(175 * 4, 75 * 0.618 * 4, 0.5, 1, 0, -550))
        renderScaled(pixel, centerAnchor(170 * 4, 70 * 0.618 * 4, 0.5, 1, 0, -550))
        renderScaled(dialog_adv_endless, centerAnchor(120 * 4, 84, 0.5, 1, 0, -425))
        if dialog == 0:
            renderScaled(dialog0_endless, centerAnchor(160 * 4, 98, 0.5, 1, 0, -550))
        elif dialog == 1:
            renderScaled(dialog1_endless, centerAnchor(160 * 4, 64, 0.5, 1, 0, -550))
        elif dialog == 2:
            renderScaled(dialog2_endless, centerAnchor(160 * 4, 64, 0.5, 1, 0, -550))
        elif dialog == 3:
            renderScaled(dialog3_endless, centerAnchor(160 * 4, 98, 0.5, 1, 0, -550))
        elif dialog == 4:
            gameState = "game"
    else:
        renderScaled(pixel_white, centerAnchor(130 * 4, 55 * 0.618 * 4, 1, 1, -260, -400))
        renderScaled(pixel, centerAnchor(125 * 4, 50 * 0.618 * 4, 1, 1, -260, -400))
        renderScaled(dialog_adv, centerAnchor(90 * 4, 64, 1, 1, -260, -300))
        if dialog == 0:
            renderScaled(dialog0, centerAnchor(115 * 4, 98, 1, 1, -260, -400))
        elif dialog == 1:
            renderScaled(dialog1, centerAnchor(120 * 4, 64, 1, 1, -260, -400))
        elif dialog == 2:
            renderScaled(dialog2, centerAnchor(120 * 4, 64, 1, 1, -260, -400))
        elif dialog == 3:
            renderScaled(dialog3, centerAnchor(120 * 4, 98, 1, 1, -260, -400))
        elif dialog == 4:
            gameState = "game"


def renderGameOver():
    global endless_time
    global current_difficulty
    global font_title
    renderScaled(gameover_background.play(), centerAnchor(1920, 1080))
    try_again_b.draw()
    end_game_b.draw()
    if current_difficulty == 3: #256, 80, 0.5, 1, 256+128, -64
        renderScaled(font_title.render(str(endless_time // 1000), False, (255, 255, 255)), centerAnchor(256+64, 80, 0.5, 1, 0, -64))

def renderWin():
    global achievement_popup_time, achievement_popup_index
    renderScaled(win_background.play(), centerAnchor(1920, 1080))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.3, 0.8))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.1, 0.8))
    renderScaled(cloud.play(), centerAnchor(96 * 4, 96 * 4, 0.2, 0.6))
    renderScaled(bird.play(), centerAnchor(19 * 4, 17 * 4, 0.9, 0.7, bird.index * -20))
    renderScaled(bird.play(), centerAnchor(19 * 4, 17 * 4, 0.95, 0.75, bird.index * -20))
    renderScaled(bird.play(), centerAnchor(19 * 4, 17 * 4, 0.96, 0.66, bird.index * -20))
    win_game_b.draw()
    if achievement_popup_time > 0:
        achievement_popup_time -= timer.get_time()
        renderScaled(achievements[achievement_popup_index].getTrophy(), centerAnchor(224 * 3, 64 * 1.5, 0, 0.1, 224 * 1.5))
        renderScaled(font_title.render(achievements[achievement_popup_index].getTitle(), False, (0, 0, 0)), centerAnchor(300, 64 * 1.5 / 2, 0, 0.1, 380, -24))
        renderScaled(font_title.render("Zdobyto osiągnięcie!", False, (0, 0, 0)), centerAnchor(300, 64 * 1.5 / 2, 0, 0.1, 380, 16))



gameState = "main_menu"
running = True
infoObject = pygame.display.Info()


def playMusic(name):
    pass
    pygame.mixer.music.load("audio/" + name + ".wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)


playMusic("maintheme")

while running:
    timer.tick(60)
    if gameState == "main_menu":
        renderMainMenu()
    elif gameState == "login_panel":
        renderLoginPanel()
    elif gameState == "register_panel":
        renderRegisterPanel()
    elif gameState == "difficulty_setter":
        renderDifficultySetter()
    elif gameState == "legend":
        renderLegend()
    elif gameState == "achievements":
        renderAchievements()
    elif gameState == "game_over":
        renderGameOver()
    elif gameState == "game":
        renderGame()
    elif gameState == "opening":
        renderOpening()
    elif gameState == "win":
        renderWin()
    mpose = pygame.mouse.get_pos()
    if infoObject.current_w == 1920:  # zamienilem ">" na "==" bo u mnie w zlym miejscu jest ten kursor ~KubaK xD
        renderScaled(cursor, centerAnchor(64, 64, 0, 0, mpose[0] + 32, mpose[1] + 32))
    else:
        renderScaled(cursor, centerAnchor(64, 64, 0, 0, mpose[0] * 1.25 + 32, mpose[1] * 1.25 + 32))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if gameState == "main_menu":
                if logged_username != "" and centerAnchor(160, 64, 0, 0, 80 + len(logged_username) * 6.5 + 17 * 6.5, 80).collidepoint(mouse[0], mouse[1]):
                    logged_username = ""
                    text_boxes["username"] = ""
                    text_boxes["password"] = ""
                    text_boxes["nick"] = ""
                if centerAnchor(256, 80, 0.5, 0.30, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "difficulty_setter"  # difficulty_setter
                    announcement = ""
                elif centerAnchor(256, 80, 0.5, 0.40, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "login_panel"
                    announcement = ""
                elif centerAnchor(256, 80, 0.5, 0.50, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "legend"
                elif centerAnchor(256, 80, 0.5, 0.60, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    gameState = "achievements"
                elif centerAnchor(256, 80, 0.5, 0.70, 0, 128 // 2).collidepoint(mouse[0], mouse[1]):
                    running = False
            elif gameState == "login_panel":
                if centerAnchor(256, 70, 0.5, 0.4, 136, 128 // 2 + 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
                elif centerAnchor(157, 60, 0.5, 0.3, 0, 128 // 2 - 30 + 32).collidepoint(mouse[0], mouse[1]):
                    login(text_boxes['username'], text_boxes['password'])
                elif centerAnchor(256, 70, 0.5, 0.4, -136, 128 // 2 + 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "register_panel"
            elif gameState == "register_panel":
                if centerAnchor(256, 70, 0.5, 0.55, 0, 128 // 2 + 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "login_panel"
                    announcement = ""
                elif centerAnchor(256, 70, 0.5, 0.45, 0, 128 // 2 - 30 + 32).collidepoint(mouse[0], mouse[1]):
                    signUp(text_boxes['username'], text_boxes['nick'], text_boxes['password'])
            elif gameState == "difficulty_setter":
                if centerAnchor(64, 64, 1, 0, -32, 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
                elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.25).collidepoint(mouse[0], mouse[1]):
                    refreshGame()
                    setDifficulty(0)
                    gameState = "opening"
                elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.4).collidepoint(mouse[0], mouse[1]):
                    refreshGame()
                    setDifficulty(1)
                    gameState = "opening"
                elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.55).collidepoint(mouse[0], mouse[1]):
                    refreshGame()
                    setDifficulty(2)
                    gameState = "opening"
                elif centerAnchor(384 * 2, 89 * 1.5, 0.75, 0.7).collidepoint(mouse[0], mouse[1]) and isEndlessUnlocked():
                    refreshGame()
                    setDifficulty(3)
                    gameState = "opening"
            elif gameState == "opening":
                dialog += 1
            elif gameState == "win":
                if centerAnchor(256, 80, 0.5, 1, 0, -64).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
                    playMusic("maintheme")
            elif gameState == "legend":
                if centerAnchor(64, 64, 1, 0, -32, 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
            elif gameState == "achievements":
                if centerAnchor(64, 64, 1, 0, -32, 32).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
            elif gameState == "game_over":
                if centerAnchor(256 + 96, 80, 0.5, 1, -256-128, -64).collidepoint(mouse[0], mouse[1]):
                    gameState = "difficulty_setter"
                    playMusic("maintheme")
                if centerAnchor(256, 80, 0.5, 1, 256+128, -64).collidepoint(mouse[0], mouse[1]):
                    gameState = "main_menu"
                    playMusic("maintheme")
            elif gameState == "game":
                if energy_drink_activated:
                    if centerAnchor(64, 64, 1, 0, -32, 32).collidepoint(mouse[0], mouse[1]):
                        gameState = "main_menu"
                        playMusic("maintheme")
                    else:
                        if not premie_lotne_is_negative:
                            objectives[0].clicked()
                            objectives[1].clicked()
                            objectives[2].clicked()

                else:
                    if centerAnchor(82 * 3.5, 102 * 3.5, 0.5, 1, -82 * 3.5 - 50, -102 * 1.75).collidepoint(mouse[0],
                                                                                                           mouse[
                                                                                                               1]) and not energy_drink_activated:
                        objectives[0].clicked()
                    elif centerAnchor(82 * 3.5, 102 * 3.5, 0.5, 1, 0, -102 * 1.75).collidepoint(mouse[0], mouse[
                        1]) and not energy_drink_activated:
                        objectives[1].clicked()
                    elif centerAnchor(82 * 3.5, 102 * 3.5, 0.5, 1, 82 * 3.5 + 50, -102 * 1.75).collidepoint(mouse[0],
                                                                                                            mouse[
                                                                                                                1]) and not energy_drink_activated:
                        objectives[2].clicked()
                    elif centerAnchor(64, 64, 1, 0, -32, 32).collidepoint(mouse[0], mouse[1]):
                        gameState = "main_menu"
                        playMusic("maintheme")
                    elif centerAnchor(128, 128, premie_lotne_x, premie_lotne_y).collidepoint(mouse[0], mouse[1]):
                        activatePowerUp(premie_lotne_type)

        elif event.type == pygame.QUIT:
            running = False

pygame.quit()
