#!/usr/bin/env python
# Pour lancer directement l'exécution à partidi sur sell si le fichier a les droits d'exécution
# Exemple de jeu simple en pygame : le jeu pong

# Utilisation de pygame avec un préfixe plus simple
import pygame as pg

# Variable globale pour débug
pause = False # Si vrai, met le jeux en pause

# Définition du jeu en lui même
class Pong:
    def __init__(self,screen: pg.Surface):
        """ Création des attribut du jeux """
        # Conserve le lien vers l'objet surface ecran du jeux
        self.screen = screen

        # Crée une surface pour le fond du jeu de même taille que la fenêtre
        self.background = pg.Surface(self.screen.get_size())
        self.background.fill("purple")

        # Dessine le font d'écran une première fois
        self.screen.blit(self.background,(0,0))

        # Objet sous groupe pour avoir la liste des sprites et automatiser la mise à jour par update()
        # Automatise aussi l'affichage : draw() par défaut affiche dans l'écran image à la position rect
        self.all = pg.sprite.RenderUpdates()

        # Creation de la raquette de gauche et droite
        self.paddleL = Paddle()
        self.paddleR = Paddle()
        # Positionnement des raquettes
        self.paddleL.setLoc(0,0,self.screen.get_height())
        # Il faut dépplacer vers la gauche pour tenir compte de la taille de la raquette
        self.paddleR.setLoc(self.screen.get_width()-self.paddleR.rect.width,0,self.screen.get_height())

        # Ajoute au groupe pour l'envois des messages update() et draw()
        self.all.add(self.paddleL,self.paddleR)

        # Création de la balle
        self.ball = Ball()
        # Définit la zone de jeux
        self.ball.setPlayground(self.screen.get_rect())
        # Ajoute la balle à la liste des sprites
        self.all.add(self.ball)

        # Initialisation des scores des deux joueurs
        self.score = Score()
        # Place le score au centre de l'écran
        self.score.setLoc(self.screen.get_rect().midtop)
        # Ajoute le score à la liste des sprites
        self.all.add(self.score)

        # Initialise le score gagant
        self.winScore = 5
        # Vrai si le jeu est fini
        self.isEnded = False

    def isRunning(self):
        """ 
        Examine l'état du jeux et les actions pour savoir si le jeux continu
        Retourne vrai si le jeu n'est pas terminé
        """
        global pause
        if self.isEnded:
            return False
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    # On ferme la fenêtre
                    return False
                # Un appui sur une touche
                case pg.KEYDOWN:
                    match event.key:
                        case pg.K_ESCAPE:
                            return False
                        case pg.K_f:
                            # Touche 'f' passe en fullscreen ou revient en mode window
                            pg.display.toggle_fullscreen()
                        case pg.K_EQUALS:
                            # alterne la pause
                            pause = not pause
        return True

    def update(self,dt : int):
        """
        Met à jour l'état du jeux en fonction du temps dt écoulé 
        """
        global pause
        if pause:
            return
        # Calcule la table de toutes les touches du clavier présées
        keystate = pg.key.get_pressed()

        # Fait bouger les raquettes en fonction des touches pressées
        if keystate[pg.K_a]:
            self.paddleL.up()
        elif keystate[pg.K_q]:
            self.paddleL.down()
        else:
            self.paddleL.stop()

        if keystate[pg.K_p]:
            self.paddleR.up()
        elif keystate[pg.K_m]:
            self.paddleR.down()
        else:
            self.paddleR.stop()

        # Met à jours tous les sprites
        self.all.update(dt)

        # Test la collision avec les raquettes
        if pg.sprite.collide_rect(self.paddleL,self.ball):
            # Fait rebondir la balle sur la raquette
            self.ball.bounce(self.paddleL)
        if pg.sprite.collide_rect(self.paddleR,self.ball):
            self.ball.bounce(self.paddleR)

        # test si la balle est sortie de l'aire du jeux
        if not self.screen.get_rect().contains(self.ball.rect):
            if self.ball.rect.left <= 0:
                # Sortie à gauche
                self.score.add(1,0)
                self.serveL()
            else:
                # Sortie à droite
                self.score.add(0,1)
                self.serveR()
            # Est-ce la fin du jeux ?
            if self.score.scoreL >= self.winScore:
                print("Left payer wins !")
                self.isEnded = True
            if self.score.scoreR >= self.winScore:
                print("Right payer wins !")
                self.isEnded = True

            

        # Vide l'écran en replacant le background
        self.all.clear(self.screen, self.background)

        # Dessine tous les sprites dans la surface de l'écran
        dirty = self.all.draw(self.screen)
        # Remplace le background des zones modifiées par le mouvement des sprites
        pg.display.update(dirty)

    def serveL(self):
        """ Fait un service à gauche """
        self.ball.setR(self.paddleL,(0.5,0.5))

    def serveR(self):
        """ Fait un service à droite """
        self.ball.setL(self.paddleR,(-0.5,-0.5))

class Paddle(pg.sprite.Sprite):
    """ Les raquettes du jeux """
    # Variables de classes pour toutes les raquettes
    # Taille largeur, hauteur des raquettes, fixes
    size = (40,80)

    def __init__(self,*groups):
        # Appel du constructeur la super classe
        pg.sprite.Sprite.__init__(self, *groups)
        # Chaque sprite doit avoir son attribut de type Surface.image pour s'afficher
        # et Surface.rect pour se positionner
        # ATTENTION : size ici est un attribut de classe !
        self.image = pg.Surface(self.size)
        # Recupère le rectangle de la surface du Sprite
        self.rect = self.image.get_rect()
        # Donne une couleur à la raquette
        self.image.fill("green")
        # Initialise une vitesse en pixels par millisecondes
        self.speed = 0.8
        # Mouvement : 0 immobile, +1 descent, ou -1 monte
        self.movement = 0

    def setLoc(self,x, min, max):
        """ Definit les positions horizontale en x, et min et max en vertical """
        self.min = min
        self.max = max
        # Change la position horizontal du rectangle qui définit la position
        self.rect.move_ip((x,0))

    def update(self,dt):
        """ Met à jour la position du paddle """
        # Déplace la position de la raquette en fonction du mouvement demandé
        # Calcule le déplacement
        depl = self.speed * self.movement * dt
        # Modifie la position de la raquette
        self.rect.move_ip((0,depl))
        # Regarde si le déplacement est possible et corrige à la position min ou max
        # ATTENTION : on ne maitise pas le nombre de pixels exact du déplacement donc
        # cette manière de calculer permet à la raquette de toujours aller aux valeurs min et max
        if self.rect.top <= self.min:
            self.rect.top = self.min
        if self.rect.bottom >= self.max:
            self.rect.bottom = self.max            

    def up(self):
        """ Demande de déplacer la raquette vers le haut """
        self.movement = -1

    def down(self):
        """ Demande de déplacer la raquette vers le bas """
        self.movement = 1

    def stop(self):
        """ Demande de garder la raquette immobile """
        self.movement = 0



class Ball(pg.sprite.Sprite):
    """ Une balle qui rebondit """
    # Taille largeur, hauteur de la balle
    size = (20,20)

    def __init__(self,*groups):
        # Appel du constructeur la super classe
        pg.sprite.Sprite.__init__(self, *groups)
        # La surface (image) à afficher de ce sprite
        self.image = pg.Surface(self.size)
        # Recupère le rectangle de la surface du Sprite
        self.rect = self.image.get_rect()
        # Donne une couleur
        self.image.fill("blue")
        # Vecteur de mouvement
        self.movement = pg.Vector2(0.5,0.6)

    def setPlayground(self,rect : pg.Rect):
        """ Définit le rectangle de la zone de mouvement de la balle """
        self.playground = rect

    def setL(self,sprite,velocity):
        """ Positionne la balle au centre gauche du sprite, et initialise son vecteur vitesse """
        pos = sprite.rect.midleft
        x = pos[0] - self.size[0]
        y = pos[1] - self.size[1]/2
        self.rect.update((x,y),self.size)
        self.movement =  pg.Vector2(velocity)

    def setR(self,sprite,velocity):
        """ Positionne la balle au centre droit du sprite, et initialise son vecteur vitesse """
        pos = sprite.rect.midright
        x = pos[0] + self.size[0]
        y = pos[1] + self.size[1]/2
        self.rect.update((x,y),self.size)
        self.movement =  pg.Vector2(velocity)

    def update(self,dt):
        """ Met à jour la position de la balle  """
        # Déplace la position de la raquette en fonction du veteur de mouvement
        # Calcule le vecteur déplacement
        depl = self.movement * dt
        # Modifie la position
        self.rect.move_ip(depl)
        # Calcule les rebonts sur le haut et le bas
        if self.rect.top <= self.playground.top:
            # Rebond du haut
            self.rect.top = self.playground.top
            self.movement.reflect_ip((0,1))
        if self.rect.bottom >= self.playground.bottom:
            # Rebond du bas
            self.rect.bottom = self.playground.bottom
            self.movement.reflect_ip((0,-1))

    def bounce(self, sprite):
        """ La balle rebondit sur le sprite """
        # Simplification du problème : on considère que l'objet a une epaisseur nulle
        # Il suffit alors simplement de savoir si le rebond est sur la gauche ou la droite
        # C'est en fonction de l'orientation du vecteur vitesse par rapport à la vecticale
        # Le produit scalaire calcul le cosinus de l'angle par rapport à la verticale
        orientation = self.movement.dot((0,-1))
        # D'ou vient la balle par rapport au sprite ?
        if orientation > 0:
            # vient de la gauche
            self.movement.reflect_ip((-1,0))
        else:
            # vient de la droite
            self.movement.reflect_ip((1,0))

class Score(pg.sprite.Sprite):
    """ Score des deux joueurs et son affichage """
    def __init__(self,*groups):
        # Appel du constructeur la super classe
        pg.sprite.Sprite.__init__(self, *groups)
        # Initialisation du score du joueur gauche et droit
        self.scoreL = 0
        self.scoreR = 0
        # Crée un objet avec la font par défaut
        self.font = pg.font.Font(None,200)
        # La surface (image) à afficher de ce sprite
        self.image = self.font.render(f'{self.scoreL} {self.scoreR}',True,"green")
        # Recupère le rectangle de la surface à afficher
        self.rect = self.image.get_rect()
    
    def setLoc(self,midtop):
        """ Positionne le score """
        self.loc = midtop
        # Recalcule le rectangle de l'image
        self.rect = self.image.get_rect()
        # Positionne
        self.rect.midtop = midtop
    
    def add(self,l,r):
        """ Ajoute un point à gauche et/ou à droite """
        self.scoreL += l
        self.scoreR += r
        # Recalcule l'image
        self.image = self.font.render(f'{self.scoreL} {self.scoreR}',True,"green")
        self.rect = self.image.get_rect()
        self.rect.midtop = self.loc

# Fonction principale : pas de varaibles globales
def main():
    # Initialisation de pygame
    pg.init()
    # Initalisation du module de gestion des fonts
    pg.font.init()
    # Donne un nom à la fenêtre 
    pg.display.set_caption("PONG")
    # Taille de l'écran imposée
    screenSize = (1024,768)
    # Crée la surface qui va servir de surface de jeu
    screen = pg.display.set_mode(screenSize)
    # Creé un objet horloge pour gerer le temps entre deux images
    clock = pg.time.Clock()
    # Nombre de millisecondes entre deux images 
    dt = 0

    # Création d'une instance du jeu
    pong = Pong(screen)

    # Boucle de jeu
    while pong.isRunning():

        # Limite la vitesse à 6O images max par secondes
        # Calcule le temps réel entre deux images en millisecondes
        dt = clock.tick(60)

        # Met à jour le jeu sachant que dt millisecondes se sont écoulées
        pong.update(dt)

        # Affiche le nouvel état de l'écran
        pg.display.flip()

    # Fin utilisation de pygame
    pg.quit()


# Appel automatiquement la fonction main si pas utilisé comme module
if __name__ == "__main__":
    main()