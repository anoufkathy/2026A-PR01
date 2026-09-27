# ======================== game.py ========================

import pygame
import random
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, JUMP_VELOCITY, SPRING_JUMP_VELOCITY,
    DOODLE_SPEED, DOODLE_WIDTH, DOODLE_HEIGHT, PLATFORM_WIDTH,
    MIN_PLATFORM_GAP, MAX_PLATFORM_GAP, CAMERA_SCROLL_THRESHOLD,
    PLATFORMS, doodle_dict, DOODLE_START_X, DOODLE_START_Y, LIVES
)
from platforms import create_platform, choose_platform_type
from doodle import doodle_left_img, doodle_right_img
from window import generate_initial_platforms


# ======================== PARTIE 3.1 ========================
def apply_gravity():
    """
    Applique la gravité au Doodle en augmentant progressivement sa vitesse verticale (vel_y).
    Met à jour la position verticale (y) du Doodle.
    """
    # TODO(fait): Mettez à jour la vitesse verticale puis la position verticale
    # du Doodle à partir de GRAVITY.
    doodle_dict["vel_y"] += GRAVITY # chaque image--> la gravité accélère un peu plus la chute du doodle. GRAVITY--> nb+==> vas vers le bas . ralenti en montant,atteint 0, et tombe 
    doodle_dict["y"] += doodle_dict["vel_y"] #position(verticale) change selon vel_y(vitesse verticale). Si vel_y est nég, le doodle monte, y diminue --> monte à l'écran

    return

# ===========================================================


# ======================== PARTIE 1.2 ========================
def move_doodle():
    """
    Gère le déplacement horizontal du Doodle selon les touches pressées (Flèches ou A/D).
    Implémente le passage fluide d'un côté de l'écran à l'autre (Screen Wrap).
    """
    keys = pygame.key.get_pressed()

    # TODO : Gérez les déplacements gauche/droite et mettez à jour
    # simultanément la direction et l'image du Doodle.



    # TODO : Implémentez le Screen Wrap pour qu'une partie du Doodle puisse
    # sortir d'un côté avant de réapparaître de l'autre.
    # N'utilisez pas de dimensions numériques écrites directement.



    return

# ===========================================================


# ======================== PARTIE 2.3 ========================
def move_platforms():
    """
    Déplace horizontalement les plateformes mobiles ("blue").
    Fait rebondir les plateformes lorsqu'elles atteignent les bords de la fenêtre.
    """
    # TODO : Parcourez les plateformes et gérez le déplacement des plateformes
    # bleues encore actives. Elles doivent rester dans la fenêtre en inversant
    # leur vitesse lorsqu'elles atteignent un bord.

    for platform in PLATFORMS: # on parcourt toutes les plateformes stockées
        if platform["type"] == "blue" and platform["active"]: # on veut seulement toucher aux plateformes bleues
            platform["x"] +=platform["vx"] # fait avancer la plateforme d'un petit pas horizontal à chaque image du jeu.
            if platform["x"] <= 0 or platform["x"] + platform["width"] >= SCREEN_WIDTH:
                platform["vx"] = -platform["vx"] # Pour chacune, on la déplace de vx, puis on regarde si elle a touché un bord. Si oui, on inverse vx (positif devient négatif et inversement), et elle repart dans l'autre sens
    return

# ===========================================================


# ======================== PARTIE 3.2 ========================
def check_platform_collisions():
    """
    Détecte si le Doodle atterrit sur une plateforme.
    Le rebond ne se produit QUE lorsque le Doodle descend (vel_y > 0)
    et qu'il arrive sur le dessus d'une plateforme.
    """
    # TODO(fait): Implémentez la détection d'un atterrissage.
    #
    # Contraintes :
    # - aucun rebond pendant la montée ;
    # - ignorer les plateformes inactives ;
    # - utiliser rects_collide(...) pour le chevauchement des rectangles ;
    # - un simple chevauchement ne suffit pas : le Doodle doit arriver par
    #   le dessus de la plateforme. Pour le vérifier, comparez la position
    #   actuelle de ses pieds à leur position approximative à l'image
    #   précédente à l'aide de vel_y. Une tolérance de 14 pixels est permise ;
    # - spring : SPRING_JUMP_VELOCITY ;
    # - brown : JUMP_VELOCITY puis désactivation de la plateforme ;
    # - green/blue : JUMP_VELOCITY.

    if doodle_dict["vel_y"] <=0 :   #si le doodle est entrain de monter--> pas besoin d'atterir
        return

    doodle_rect =(doodle_dict["x"], doodle_dict["y"], DOODLE_WIDTH, DOODLE_HEIGHT) #construit le rectangle du doodle sous la forme que rects_collide attend(x,y,largeur,hauteur)

    feet_y= doodle_dict["y"] +DOODLE_HEIGHT # y est le haut du doodle --> en ajoutant sa hauteur, on a la position de ses pieds
    previous_feet_y = feet_y - doodle_dict["vel_y"] #reprend la position des pieds de l'image précédente 

    for platform in PLATFORMS:   # on regarde chaque plateforme 
        if not platform["active"]: 
            continue             # so la plateforme n'est pas active, on passe à la prochaine 

        platform_rect= (platform["x"], platform["y"], platform["width"], platform["height"]) #on construit un rectangle pour rects_collide

        if not rects_collide(doodle_rect, platform_rect): # si les deux rectanges( du doodle et de la plateforme) ne se touche pas--> pas d'atterisage
            continue

        if previous_feet_y <= platform["y"] + 14:    # test qui distingue un vrai atterissage d'un simple passage à travers--> il faut donc que le doodle soit au dessus( marge de 14 pixels) avant d'entrer en collision. Ainsi, si le doodle vient directement par en dessous, ce n'est pas valide 
            if platform["type"] in ("green", "blue"): #rebond normal 
                doodle_dict["vel_y"] = JUMP_VELOCITY

            elif platform["type"] == "spring":          #rebond plus fort 
                doodle_dict["vel_y"] = SPRING_JUMP_VELOCITY

            elif platform["type"] == "brown":           # rebond normal, mais devient plus active, donc un seul rebond permis 
                doodle_dict["vel_y"]= JUMP_VELOCITY
                platform["active"]= False

            return # retourne dans le if pour valider les atterrissage 


    return

# ===========================================================


# ======================== PARTIE 3.3 ========================
def scroll_camera():
    """
    Fait défiler le monde lorsque le Doodle dépasse CAMERA_SCROLL_THRESHOLD.
    Met à jour le score et maintient les plateformes visibles.
    """
    # TODO(fait) : Lorsque le Doodle dépasse le seuil de caméra, il doit rester
    # visuellement au seuil pendant que les plateformes sont déplacées vers
    # le bas de la même distance.
    #
    # Le score doit représenter la distance verticale ainsi parcourue et le
    # meilleur score doit être mis à jour. Les plateformes sorties sous
    # l'écran doivent être retirées, puis de nouvelles plateformes générées.
    if doodle_dict["y"] < CAMERA_SCROLL_THRESHOLD:  # déclenche le scroll, car seuil atteint(doodle est monté au dessus du seuil)
        scroll_distance= CAMERA_SCROLL_THRESHOLD- doodle_dict["y"] # le nb de pixel que le doodle dépassé depuis le seuil 

        doodle_dict["y"] = CAMERA_SCROLL_THRESHOLD # on remet le doodle exactement au seuil pour qu'il rest visuellement à la même hauteur

        for platform in PLATFORMS: 
            platform["y"] += scroll_distance   # on vient descendre chaque plateforme de la même distance 

        doodle_dict["score"] += int(scroll_distance)  # score augmente selon la distance parcouru vers le haut 
        if doodle_dict["score"] < doodle_dict["high_score"] : # met à jour le nouveau meilleur score
            doodle_dict["high_score"] = doodle_dict["score"] 

        PLATFORMS[:] =[ p for p in PLATFORMS if p["y"] < SCREEN_HEIGHT] # garde seulement les plateformes visbles ou proche de l'écran et retire les autres--> nouvelle liste pour ne pas changer les références

        generate_new_platforms()            

    return

# ===========================================================


# ======================== PARTIE 3.4 ========================
def generate_new_platforms():
    """
    Génère de nouvelles plateformes au-dessus du haut de l'écran pour maintenir
    un flux continu lorsque la caméra défile.
    """
    # TODO : Complétez cette fonction en vous inspirant de la logique de
    # génération initiale, sans la recopier inutilement.
    #
    # Vous devrez partir de la plateforme actuellement la plus haute et
    # continuer à ajouter des plateformes tant que nécessaire. Utilisez
    # choose_platform_type(...) avec les probabilités indiquées dans le README.
    

    return

# ===========================================================


def check_game_over():
    """
    Vérifie si le Doodle tombe sous le bas de l'écran.
    Si oui, réduit les vies.
    Retourne True si la partie est terminée.
    """
    if doodle_dict["y"] > SCREEN_HEIGHT:
        doodle_dict["lives"] -= 1
        return True
    return False


def restart_game():
    """
    Réinitialise la partie : position du Doodle, vitesse, score et plateformes.
    """
    doodle_dict["x"] = DOODLE_START_X
    doodle_dict["y"] = DOODLE_START_Y
    doodle_dict["vel_y"] = 0.0
    doodle_dict["direction"] = "right"
    doodle_dict["image"] = doodle_right_img
    doodle_dict["score"] = 0
    doodle_dict["lives"] = LIVES

    generate_initial_platforms()


def rects_collide(r1, r2):
    """
    Vérifie si deux rectangles (x, y, largeur, hauteur) se chevauchent.
    Cette fonction est fournie et ne doit pas être modifiée.
    """
    return not (
        r1[0] + r1[2] <= r2[0] or r1[0] >= r2[0] + r2[2] or
        r1[1] + r1[3] <= r2[1] or r1[1] >= r2[1] + r2[3]
    )
