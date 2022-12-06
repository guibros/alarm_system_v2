


import pygame
import math
import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config
from datetime import datetime,timedelta
import time
import smtplib
from RPiSim import GPIO
# import RPi.GPIO as GPIO  # Import GPIO Library

#configuration du board raspberry
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#bloc declaration des variables de gpio pin
ALARM_PIN = 22
SENSOR_PIN = 6

#initiation des pin du board
#GPIO.setup(ALARM_PIN, GPIO.OUT, initial=GPIO.LOW)
#GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(ALARM_PIN, GPIO.MODE_OUT, initial=GPIO.LOW)
GPIO.setup(SENSOR_PIN, GPIO.MODE_IN, pull_up_down=GPIO.PUD_UP)


#bloc-config de la fonction d'evenements en provenance du raspberry
def getEvent():
    if GPIO.input(SENSOR_PIN) == False:
        print ('getEvent true')
        return True

#bloc config couleur
BLEU = (0, 0, 255)
ROUGE = (100, 0, 0)
JAUNE = (200, 200, 0)
VERT = (0, 100, 0)
BLANC = (255, 255, 255)
GRIS = (50, 50, 50)
NOIR = (0, 0, 0)

#bloc pour config de la class keyboard pour affichage de clavier
class keyboard():
    #config des variables initiales de la classe
    def __init__(self, couleur, x, y, rayon, police=''):
        self.couleur = couleur
        self.x = x
        self.y = y
        self.rayon = rayon
        self.police = police

    #methode pour config l'affichage des differents boutons
    def dessiner(self, screen, posX, posY, texte):
        font = pygame.font.SysFont(self.police, self.rayon+10)
        pygame.draw.circle(screen, self.couleur, (posX, posY), self.rayon)
        txtBtn = font.render(texte, True, (250, 250, 250))
        rectBtn = txtBtn.get_rect()
        rectBtn.center = (posX, posY)
        screen.blit(txtBtn, rectBtn)

    #methode pour definir l'organisation et l'affichage du keyboard
    def board(self,screen):
        btn1 = self.dessiner(screen,self.x, self.y, '1')
        btn2 = self.dessiner(screen,self.x+80, self.y, '2')
        btn3 = self.dessiner(screen,self.x+160, self.y, '3')
        btn4 = self.dessiner(screen,self.x, self.y+80, '4')
        btn5 = self.dessiner(screen,self.x+80, self.y+80, '5')
        btn6 = self.dessiner(screen,self.x+160, self.y+80, '6')
        btn7 = self.dessiner(screen,self.x, self.y+160, '7')
        btn8 = self.dessiner(screen,self.x+80, self.y+160, '8')
        btn9 = self.dessiner(screen,self.x+160, self.y+160, '9')
        btnX = self.dessiner(screen,self.x, self.y+240, 'x')
        btn0 = self.dessiner(screen,self.x+80, self.y+240, '0')
        btnOK = self.dessiner(screen,self.x+160, self.y+240, 'ok')

    #methode pour rendre les boutons actifs avec un retour de valeur selon l'identité du bouton
    def event(self, posSouris):
        if self.isOverBouton(posSouris, self.x, self.y):
            return "1"
        elif self.isOverBouton(posSouris, self.x+80, self.y):
            return "2"
        elif self.isOverBouton(posSouris, self.x+160, self.y):
            return "3"
        elif self.isOverBouton(posSouris, self.x, self.y+80):
            return "4"
        elif self.isOverBouton(posSouris, self.x+80, self.y+80):
            return "5"
        elif self.isOverBouton(posSouris, self.x+160, self.y+80):
            return "6"
        elif self.isOverBouton(posSouris, self.x, self.y+160):
            return "7"
        elif self.isOverBouton(posSouris, self.x+80, self.y+160):
            return "8"
        elif self.isOverBouton(posSouris, self.x+160, self.y+160):
            return "9"
        elif self.isOverBouton(posSouris, self.x, self.y+240):
            return "x"
        elif self.isOverBouton(posSouris, self.x+80, self.y+240):
            return "0"
        elif self.isOverBouton(posSouris, self.x+160, self.y+240):
            return "ok"

    #methode pour la config de l'activation des boutons
    def isOverBouton(self, posSouris, posX, posY):
        xSouris = posSouris[0]
        ySouris = posSouris[1]

        absX = (posX - xSouris) ** 2
        absY = (posY - ySouris) ** 2

        return (math.sqrt(absX + absY) < self.rayon)

#bloc pour config de class objBouton pour afficher les boutons individuelle
class objBouton():
    def __init__(self, couleur, x, y, rayon, texte=''):
        self.couleur = couleur
        self.x = x
        self.y = y
        self.rayon = rayon
        self.texte = texte

    def dessiner(self, screen):
        font = pygame.font.SysFont('twcen', 36)
        pygame.draw.circle(screen, self.couleur, (self.x, self.y), self.rayon)
        txtBtn = font.render(self.texte, True, (0, 0, 0))
        rectBtn = txtBtn.get_rect()
        rectBtn.center = (self.x, self.y)
        screen.blit(txtBtn, rectBtn)

    def isOverBouton(self, posSouris):
        xSouris = posSouris[0]
        ySouris = posSouris[1]

        absX = (self.x - xSouris) ** 2
        absY = (self.y - ySouris) ** 2

        return (math.sqrt(absX + absY) < self.rayon)


#bloc-config de la fonction de l'envoi courriel
def emailMe():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("popocoagulecole@gmail.com", "Popo21popo21ecole")

        subject = 'Alarm was triggerd'
        body = f'Your home alarm was triggered on'

        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail("popocoagulecole@gmail.com", "popocoagul@gmail.com", msg)

#bloc-config de la fonction pour l'alarme
def protocolAlarm():
    #GPIO.output(ALARM_PIN, GPIO.HIGH)
    print('sonnerie')
    if nowAlarm % 2 == 0:
        GPIO.output(ALARM_PIN, GPIO.HIGH)
    elif nowAlarm % 2 != 0:
        GPIO.output(ALARM_PIN, GPIO.LOW)
    #print("protocolAlarm return " + etat)
#     print("send email")
#     emailMe()

#bloc-config pour la fonction fermeture d'alarme
def alarmOff():
    GPIO.output(ALARM_PIN, GPIO.LOW)

#bloc config de la fonction pour acquisition de données meteo
def getMeteo():
    global txtMeteo
    global txtMeteo2
    imageMeteo = f"http://openweathermap.org/img/wn/{w.weather_icon_name}.png"
    response = requests.get(imageMeteo)
    file = open("meteo_image.png", "wb")
    file.write(response.content)
    file.close()
    txtMeteo = "Temperature: " + str(w.temperature('celsius')['temp'])+' celsius'
    txtMeteo2 = str(w.detailed_status)

#bloc-config pour la fonction d'affichage des details meteo
def afficheMeteo():
    font = pygame.font.SysFont('twcen', 20)
    texte = font.render(txtMeteo, True, BLANC)
    texte2 = font.render(txtMeteo2, True, BLANC)
    rectBtn = texte.get_rect()
    rectBtn.center = (225, 325)
    screen.blit(texte, rectBtn)
    rectBtn2 = texte2.get_rect()
    rectBtn2.center = (225, 350)
    screen.blit(texte2, rectBtn2)

#bloc-config de la fonction affichage horloge
def clockTime():
    font = pygame.font.SysFont('twcen', 50)
    t = datetime.now()
    time_render = font.render(f'{t:%H: %M: %S}', True, BLANC, GRIS)
    screen.blit(time_render, (150, 150))
    clock.tick(20)

#bloc-config de la fonction affichages messages variés
def afficheTexte(txt):
    font = pygame.font.SysFont('arialblack', 100)
    txt = str(txt)
    texte = font.render(txt, True, BLANC)
    rectBtn = texte.get_rect()
    rectBtn.center = (400, 450)
    screen.blit(texte, rectBtn)

#bloc-config de la fonction affichage code password entré
def afficheCode():
    font = pygame.font.SysFont('twcen', 40)
    txt = codeAffichage
    texte = font.render(txt, True, BLANC)
    rectBtn = texte.get_rect()
    rectBtn.center = (400, 75)
    screen.blit(texte, rectBtn)


#bloc des fonction d'affichages sur ecrans selon les etats
def screenStart():
    afficheCode()
    btnActivation.dessiner(screen)
    getMeteo()
    screen.blit(img,rect)
    clockTime()
    afficheMeteo()
    afficheTexte('DÉSARMÉ')

def screenArming():
    key.board(screen)
    btnArming.dessiner(screen)
    afficheCode()

def screenArmingDelay():
    getMeteo()
    screen.blit(img, rect)
    clockTime()
    afficheMeteo()
    btnUnarming.dessiner(screen)
    x = str(deltaX-datetime.now())
    x = x[5:7]
    afficheCode()
    afficheTexte(x)

def screenArmed():
    getMeteo()
    screen.blit(img, rect)
    clockTime()
    afficheMeteo()
    btnUnarming.dessiner(screen)
    afficheTexte('SYSTÈME ARMÉ')

def screenDisarming():
    key.board(screen)
    btnDeactivating.dessiner(screen)
    afficheCode()

def screenTrigger():
    key.board(screen)
    btnDeactivating.dessiner(screen)
    x = str(deltaTrigX - datetime.now())
    x = x[5:7]
    afficheCode()
    afficheTexte(x)

def screenAlarm():
    getMeteo()
    screen.blit(img, rect)
    clockTime()
    afficheMeteo()
    btnUnarming.dessiner(screen)
    afficheTexte('ALARME DÉCLENCHÉE')


#bloc config des differents boutons
btnArming = objBouton(ROUGE,200, 250, 100, "Armer")
btnDeactivating = objBouton(ROUGE,200, 250, 100, "Désarmer")
btnUnarming = objBouton(JAUNE,575, 250, 100, "Désactiver")
btnActivation = objBouton(VERT,575, 250, 100, "Activer")

#bloc config meteo openweathermedia
config_dict = get_default_config()
config_dict['language'] = 'fr'
owm = OWM('f29f5d4679785c63240b83b42f050dd8', config_dict)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Montreal,CA')
w = observation.weather
getMeteo()

#config du tableau d'affichage
screen = pygame.display.set_mode([800, 550])

#config de l'affichage de l'image meteo
img = pygame.image.load("meteo_image.png")
img.convert()
img = pygame.transform.rotozoom(img, 0, 4)
rect = img.get_rect()
rect.center = 225, 245

#config de l'horloge
clock = pygame.time.Clock()

#config des parametres du keyboard
key = keyboard(GRIS, 450, 160, 30, 'twcen')

#initialisation des variables string pour password et code
password = '1'
code = ''
codeAffichage = ''
#liste des etats = unarmed, arming, armingDelay, armed, disarming, triggerDelay, alarm
etat = 'unarmed'
running = True
#declaration des variables d'entroposages pour les fonctions de temps
delta = 0
deltaX = 0
deltaTrig = 0
deltaTrigX = 0
deltaAffichage = 0
now = 0

while running:
    pygame.init()

#acquisition de la donnée pour le temps
    now = datetime.now()
    now = now.strftime('%H:%M:%S')
    nowAlarm = int(now[7:8])

    porte = getEvent()

    screen.fill(GRIS)

#declaration des affichages selon les etats
    if etat == 'unarmed':
        screenStart()
    elif etat == 'arming':
        screenArming()
    elif etat == 'armingDelay':
        screenArmingDelay()
    elif etat == 'armed':
        screenArmed()
    elif etat == 'disarming':
        screenDisarming()
    elif etat == 'triggerDelay':
        screenTrigger()
    elif etat == 'alarm':
        screenAlarm()
        print('alarm')
        protocolAlarm()
        

#premiere boucle de delai
    if delta == now:
        etat = 'armed'
        print('deltaPush ' + etat)

#deuxieme boucle de delai
    if deltaTrig == now:
        etat = 'alarm'
        print('deltaTrigPush ' + etat)

#boucle de delai pour reset d'affichage
    if deltaAffichage == now:
        codeAffichage = ''
        code = ''
        
#declaration des evenement souris en fonction des differents ecrans
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mousepressed')
            xSouris, ySouris = pygame.mouse.get_pos()
            if etat == 'unarmed':
                if btnActivation.isOverBouton((xSouris,ySouris)):
                    etat = 'arming'
                    print(etat)
            elif etat == 'arming':
                if key.event((xSouris,ySouris)):
                    if key.event((xSouris,ySouris)) == 'x':
                        if codeAffichage == '':
                            etat = 'unarmed'
                            print('return')
                        else:
                            code = ''
                            codeAffichage = ''
                            print('resetX')
                    elif key.event((xSouris,ySouris)) == 'ok':
                        print("ca fonctionne ok")
                        if code == password:
                            etat = 'armingDelay'
                            deltaX = datetime.now() + timedelta(seconds=11)
                            delta = deltaX.strftime('%H:%M:%S')
                            code = ''
                            codeAffichage = ''
                            print('password success, arming delay')
                            print(delta)
                            time.sleep(0.2)
                        else:
                            codeAffichage = 'invalid password'
                            deltaAffichage = datetime.now() + timedelta(seconds=2)
                            deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
                            print(deltaAffichage)
                            print('password invalid')
                    else:
                        print("ca marche")
                        print(key.event((xSouris,ySouris)))
                        a = key.event((xSouris,ySouris))
                        print(a)
                        code = code+a
                        codeAffichage = codeAffichage+'*'
                        afficheCode()
                        print(code)
                elif btnArming.isOverBouton((xSouris,ySouris)):
                    print("ca fonctionne")
                    if code == password:
                        etat = 'armingDelay'
                        code = ''
                        codeAffichage = ''
                        deltaX = datetime.now() + timedelta(seconds=11)
                        delta = deltaX.strftime('%H:%M:%S')
                        print(delta)
                        print('password success, arming delay')
                    else:
                        codeAffichage = 'invalid password'
                        print('password invalid')
                        deltaAffichage = datetime.now() + timedelta(seconds=2)
                        deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
                        print(deltaAffichage)
            elif etat == 'armingDelay':
                if btnUnarming.isOverBouton((xSouris,ySouris)):
                    etat = 'unarmed'
                    delta = 0
                    print(str(delta) + etat)
            elif etat == 'armed':
                if btnUnarming.isOverBouton((xSouris,ySouris)):
                    etat = 'disarming'
                    code = ''
                    codeAffichage = ''
                    print(etat)
            elif etat == 'disarming':
                if key.event((xSouris, ySouris)):
                    if key.event((xSouris, ySouris)) == 'x':
                        if codeAffichage == '':
                            etat = 'armed'
                            print('return')
                        else:
                            code = ''
                            codeAffichage = ''
                            print('resetX')
                    elif key.event((xSouris, ySouris)) == 'ok':
                        print("ca fonctionne ok")
                        if code == password:
                            etat = 'unarmed'
                            code = ''
                            codeAffichage = ''
                            print('password success, disarming now')
                            time.sleep(0.2)
                        else:
                            codeAffichage = 'invalid password'
                            print('password invalid')
                            deltaAffichage = datetime.now() + timedelta(seconds=2)
                            deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
                    else:
                        print("ca marche")
                        print(key.event((xSouris, ySouris)))
                        a = key.event((xSouris, ySouris))
                        print(a)
                        code = code + a
                        codeAffichage = codeAffichage + '*'
                        afficheCode()
                        print(code)
                elif btnDeactivating.isOverBouton((xSouris, ySouris)):
                    print("ca fonctionne")
                    if code == password:
                        etat = 'unarmed'
                        code = ''
                        codeAffichage = ''
                        print('password success, disarming trigger')
                    else:
                        codeAffichage = 'invalid password'
                        print('password invalid')
                        deltaAffichage = datetime.now() + timedelta(seconds=2)
                        deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
            elif etat == 'triggerDelay':
                if key.event((xSouris, ySouris)):
                    if key.event((xSouris, ySouris)) == 'x':
                        code = ''
                        codeAffichage = ''
                        print('code resetx')
                    elif key.event((xSouris, ySouris)) == 'ok':
                        print("ca fonctionne ok")
                        if code == password:
                            etat = 'unarmed'
                            code = ''
                            codeAffichage = ''
                            deltaTrig = 0
                            print('password success, disarming trigger')
                            time.sleep(0.2)
                        else:
                            codeAffichage = 'invalid password'
                            print('password invalid')
                            deltaAffichage = datetime.now() + timedelta(seconds=2)
                            deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
                    else:
                        print("ca marche")
                        print(key.event((xSouris, ySouris)))
                        a = key.event((xSouris, ySouris))
                        print(a)
                        code = code + a
                        codeAffichage = codeAffichage + '*'
                        afficheCode()
                        print(code)
                elif btnArming.isOverBouton((xSouris, ySouris)):
                    print("ca fonctionne")
                    if code == password:
                        etat = 'unarmed'
                        code = ''
                        codeAffichage = ''
                        deltaTrig = 0
                        print('password success, disarming now')
                    else:
                        codeAffichage = 'invalid password'
                        print('password invalid')
                        deltaAffichage = datetime.now() + timedelta(seconds=2)
                        deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
            elif etat == 'alarm':
                if btnUnarming.isOverBouton((xSouris,ySouris)):
                    etat= 'unarmed'
                    print('alarm deactivating')
                    alarmOff()


#declaration des evenements du boards en fonctions des etats
    if porte == True:
        print(porte)
        if etat == 'armed':
            etat = 'triggerDelay'
            deltaTrigX = datetime.now() + timedelta(seconds=11)
            deltaTrig = deltaTrigX.strftime('%H:%M:%S')
            print('triggerDelay ' + str(deltaTrig))
        if etat == 'disarming':
            etat = 'triggerDelay'
            deltaTrigX = datetime.now() + timedelta(seconds=11)
            deltaTrig = deltaTrigX.strftime('%H:%M:%S')
            print('triggerDelay ' + str(deltaTrig))
        if etat == 'armingDelay':
            print(porte)
            codeAffichage = 'FERMEZ PORTE'
            deltaAffichage = datetime.now() + timedelta(seconds=2)
            deltaAffichage= deltaAffichage.strftime('%H:%M:%S')
            etat = 'unarmed'
            delta = 0



    pygame.display.flip()

pygame.quit()
print("Fin du test")
