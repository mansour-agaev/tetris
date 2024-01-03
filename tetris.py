import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
largeur, hauteur = 300, 600
taille_bloc = 30
fenetre = pygame.display.set_mode((largeur, hauteur))
clock = pygame.time.Clock()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)
couleurs = [(0, 255, 255), (255, 165, 0), (128, 0, 128),
            (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]

# Formes des pièces
tetriminos = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]]  # Z
]


def cree_grille_vide():
    return [[noir for _ in range(largeur // taille_bloc)] for _ in range(hauteur // taille_bloc)]


def affiche_grille(grille):
    for y, row in enumerate(grille):
        for x, color in enumerate(row):
            pygame.draw.rect(fenetre, color, (x * taille_bloc,
                             y * taille_bloc, taille_bloc, taille_bloc), 0)
            pygame.draw.rect(fenetre, blanc, (x * taille_bloc,
                             y * taille_bloc, taille_bloc, taille_bloc), 1)


def cree_piece():
    forme = random.choice(tetriminos)
    couleur = random.choice(couleurs)
    piece = {
        'forme': forme,
        'couleur': couleur,
        'x': largeur // 2 // taille_bloc - len(forme[0]) // 2,
        'y': 0
    }
    return piece


def collision(grille, piece):
    for y, row in enumerate(piece['forme']):
        for x, bloc in enumerate(row):
            if bloc:
                if piece['y'] + y >= hauteur // taille_bloc or piece['x'] + x < 0 or piece['x'] + x >= largeur // taille_bloc or grille[piece['y'] + y][piece['x'] + x] != noir:
                    return True
    return False


def ajoute_piece_grille(grille, piece):
    for y, row in enumerate(piece['forme']):
        for x, bloc in enumerate(row):
            if bloc:
                grille[piece['y'] + y][piece['x'] + x] = piece['couleur']


def efface_ligne_complete(grille):
    lignes_a_supprimer = [i for i, row in enumerate(grille) if noir not in row]
    for index in lignes_a_supprimer:
        del grille[index]
        grille.insert(0, [noir for _ in range(largeur // taille_bloc)])


def main():
    grille = cree_grille_vide()
    piece_actuelle = cree_piece()
    jeu = True
    vitesse_chute = 0.5
    temps_ecoule = 0

    while jeu:
        fenetre.fill(noir)
        temps_ecoule += clock.get_rawtime()
        clock.tick()

        if temps_ecoule / 1000 > vitesse_chute:
            temps_ecoule = 0
            piece_actuelle['y'] += 1
            if collision(grille, piece_actuelle):
                piece_actuelle['y'] -= 1
                ajoute_piece_grille(grille, piece_actuelle)
                efface_ligne_complete(grille)
                piece_actuelle = cree_piece()
                if collision(grille, piece_actuelle):
                    jeu = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_actuelle['x'] -= 1
                    if collision(grille, piece_actuelle):
                        piece_actuelle['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    piece_actuelle['x'] += 1
                    if collision(grille, piece_actuelle):
                        piece_actuelle['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    piece_actuelle['y'] += 1
                    if collision(grille, piece_actuelle):
                        piece_actuelle['y'] -= 1

        affiche_grille(grille)
        for y, row in enumerate(piece_actuelle['forme']):
            for x, bloc in enumerate(row):
                if bloc:
                    pygame.draw.rect(fenetre, piece_actuelle['couleur'], (piece_actuelle['x'] * taille_bloc + x *
                                     taille_bloc, piece_actuelle['y'] * taille_bloc + y * taille_bloc, taille_bloc, taille_bloc), 0)
                    pygame.draw.rect(fenetre, blanc, (piece_actuelle['x'] * taille_bloc + x * taille_bloc,
                                     piece_actuelle['y'] * taille_bloc + y * taille_bloc, taille_bloc, taille_bloc), 1)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
