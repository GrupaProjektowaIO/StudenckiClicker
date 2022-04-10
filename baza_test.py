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
    email = input("Podaj email: ")
    password = input("Podaj haslo: ")
    try:
        auth.sign_in_with_email_and_password(email, password)
        print("Pomyslny login")
    except:
        print("Zly login lub haslo")


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
    special_characters = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    data = {'nick': username, 'email': email}
    users = db.child('users').order_by_child("nick").equal_to(data['nick']).get()
    if len(users.val())>0:
        announcement = "Ten nick już istnieje."
        print(announcement)
    elif any(character in special_characters for character in username):
        announcement = "Nick nie moze miec znakow specjalnych."
        print(announcement)
    else:
        db.child("users").push(data)
        # tworzenie informacji o osiagnieciach w bazie danych
        achievementData = {'nick': username, 1: 'F', 2: 'F', 3: 'F'}
        db.child("achievements").push(achievementData)

def dbPushAchievement(username,achievementNum):
    data = {'nick': username, achievementNum: 'T'}
    users = db.child('achievements').order_by_child("nick").equal_to(data['nick']).get()
    for user in users.each():
        db.child("achievements").child(user.key()).update({achievementNum: 'T'})
# login()
# signUp()
# dbPushHighscore()
# dbGetHighscore()
#dbPushUsername('siema1','siema1@gmail.com')
dbPushAchievement('siema1',2)