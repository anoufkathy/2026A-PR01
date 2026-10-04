# ======================== platforms.py ========================

import os
import random
import pygame
from config import ASSETS_DIR, PLATFORM_SIZE, MOVING_PLATFORM_SPEED

# Chargement des différentes images de plateformes
platform_green_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_green.png"))
platform_green_img = pygame.transform.scale(platform_green_img, PLATFORM_SIZE)

platform_blue_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_blue.png"))
platform_blue_img = pygame.transform.scale(platform_blue_img, PLATFORM_SIZE)

platform_brown_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_brown.png"))
platform_brown_img = pygame.transform.scale(platform_brown_img, PLATFORM_SIZE)

platform_spring_img = pygame.image.load(os.path.join(ASSETS_DIR, "platform_spring.png"))
platform_spring_img = pygame.transform.scale(platform_spring_img, (PLATFORM_SIZE[0], PLATFORM_SIZE[1] + 10))

# Dictionnaire d'accès aux images selon le type de plateforme
platform_images = {
    "green": platform_green_img,
    "blue": platform_blue_img,
    "brown": platform_brown_img,
    "spring": platform_spring_img
}


# ======================== PARTIE 2.1 ========================
def create_platform(x, y, platform_type="green"):
    """
    Crée et retourne un dictionnaire représentant une plateforme.

    Le dictionnaire ci-dessous représente pour l'instant correctement une
    plateforme verte. Votre travail consiste à le généraliser afin qu'il
    représente aussi correctement les plateformes bleues, marron et à ressort.
    """

    platform = {
        "x": float(x),
        "y": float(y),
        "type": platform_type,              # TODO(Fait) #permet de recevoir n'importe quel type de plateforme(green, blue, brown, spring)
        "image": platform_images[platform_type],  # TODO(Fait) #on va chercher l'image correspondante dans le dictionnaire platform_images)
        "vx": MOVING_PLATFORM_SPEED if platform_type=="blue" else 0.0,                          # TODO (fait) # vx est la vitesse horizontale de la plateforme. Pour les plateformes bleues, elle doit être égale à MOVING_PLATFORM_SPEED, et pour les autres plateformes, elle doit être égale à 0.
        "active": True,                     #on ne change pas 
        "width": PLATFORM_SIZE[0],          # le width reste pareille pour toutes les plateformes
        "height": PLATFORM_SIZE[1] + 10 if platform_type=="spring" else PLATFORM_SIZE[1],         # TODO(fait) # condition que la platefome à ressort à 10 pixels de plus en hauteur
    }

    # TODO(fait): Modifiez le dictionnaire ci-dessus pour qu'il dépende réellement
    # de l'argument platform_type.
    #
    # Contraintes :
    # - l'image doit être obtenue à partir de platform_images ;
    # - une plateforme bleue se déplace à MOVING_PLATFORM_SPEED ;
    # - une plateforme à ressort est 10 pixels plus haute ;
    # - les autres plateformes sont immobiles et gardent la hauteur normale.

    return platform

# ===========================================================


# ======================== PARTIE 2.2 ========================
def choose_platform_type(green_probability, blue_probability, spring_probability):
    """
    Choisit aléatoirement un type de plateforme.

    Les trois paramètres donnent les probabilités respectives des plateformes
    verte, bleue et à ressort. La probabilité restante correspond à une
    plateforme marron.
    """ 
    r=random.random()                  # addition cumulatif--> permet de faire aussi de intervalles 
    if r < green_probability:
        return "green"
    elif r < green_probability+ blue_probability:
        return "blue"
    elif r < green_probability+ blue_probability+ spring_probability:
        return "spring"
    else :
        return "brown"
   

    # TODO(fait) : Utilisez random.random() et les probabilités reçues en paramètres
    # pour retourner l'une des chaînes suivantes :
    # "green", "blue", "spring" ou "brown".
    #
    # Attention : les seuils utilisés avec random.random() doivent être
    # cumulatifs.

      
      

# ===========================================================

