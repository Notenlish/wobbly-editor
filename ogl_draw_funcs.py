import pygame


def draw_circle(args: tuple) -> pygame.Surface:
    surf_size = (args[1] * 2, args[1] * 2)
    print(surf_size)
    #surf = pygame.Surface(surf_size, pygame.SRCALPHA).convert_alpha()
    surf = pygame.image.load("assets/brush/test.png").convert_alpha()
    inp = list(args)
    inp.insert(1, (0, 0))
    #pygame.draw.circle(surf, *inp)
    return surf
