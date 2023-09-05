import pygame

pygame.init()
pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

image = pygame.image.load("data/images/entities/character1/idle/idle_1.png")

# Convert the image to a Pygame surface with alpha transparency
image = image.convert_alpha()

# Get the bounding rectangle of non-empty pixels
bounding_rect = image.get_bounding_rect()

# Create a new surface with the dimensions of the bounding rectangle
cropped_image = pygame.Surface((bounding_rect.width, bounding_rect.height), pygame.SRCALPHA)

# Blit the original image onto the new surface, aligning it to the top-left corner
cropped_image.blit(image, (0, 0), bounding_rect)

# Save or display the cropped image as needed
pygame.image.save(cropped_image, "cropped_image.png")