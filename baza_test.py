import pyrebase

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
storage = firebase.storage()


# Auth
# Login


def login():
    email = "test1337@gmail.com"
    password = "test1337"
    auth.sign_in_with_email_and_password(email, password)
    print("Pomyslny login")
    users = db.child('users').order_by_child("email").equal_to(email).get()
    for user in users.each():
        username = user.val()['nick']


# Rejestracja


def signUp():
    print("Rejestracja")
    email = input("Podaj email: ")
    password = input("Podaj haslo: ")
    confirmPassword = input("Potwierdz haslo: ")
    if password == confirmPassword:
        try:
            auth.create_user_with_email_and_password(email, password)
            print("Pomyslnie zarejestrowano")
        except:
            print("Email juz istnieje")


# Baza danych


def dbPushHighscore():
    data = {'nick': 'qwerty', 'highscore': 101}
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


def dbPushUsername(username, email):
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
        db.child("users").push(data)
        # tworzenie informacji o osiagnieciach w bazie danych
        achievementData = {'nick': username, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
        db.child("achievements").push(achievementData)

def signUp(email, username, password):
    global logged_username
    global gameState
    global announcement
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
            gameState = "main_menu"
    except Exception as e:
        print(e)
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



def dbPushAchievement(username, achievementNum, achievementTier):
    users = db.child('achievements').order_by_child("nick").equal_to(username).get()
    for user in users.each():
        db.child("achievements").child(user.key()).update({achievementNum: achievementTier})

def dbGetAchievements(username):
    users = db.child('achievements').order_by_child("nick").equal_to(username).get()
    for user in users.each():
        return user.val()

login()
# signUp()
# dbPushHighscore()
# dbGetHighscore()
# dbPushUsername('siema1','siema1@gmail.com')
achievements = dbGetAchievements("test1337")
print(achievements)
dbPushAchievement('siema1', 2, 1)
