"""
Pong Game

Controls:
- Left Paddle: W (up), S (down)
- Right Paddle: UP arrow (up), DOWN arrow (down)
"""

import pygame
import sys

import random

# Initialize Pygame and mixer for sound effects
pygame.init()
pygame.mixer.init()
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Particle settings
particles = []
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Generate stars
def generate_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        stars.append((x, y))
    return stars

# Draw stars
def draw_stars(stars):
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 2)
hit_sound = pygame.mixer.Sound("hit.wav")
hit_sound.set_volume(0.001)  # Set volume to 1% (99% quieter)
score_sound = pygame.mixer.Sound("score.wav")
score_sound.set_volume(0.001)  # Set volume to 1% (99% quieter)
wall_hit_sound = pygame.mixer.Sound("wall_hit.wav")
wall_hit_sound.set_volume(0.001)  # Set volume to 1% (99% quieter)

# Placeholder colors for paddles and ball
left_paddle_color = (0, 0, 255)  # Blue
right_paddle_color = (255, 0, 0)  # Red
ball_color = (255, 255, 0)  # Yellow
hit_sound = pygame.mixer.Sound("hit.wav")
score_sound = pygame.mixer.Sound("score.wav")
score_sound.set_volume(0.001)  # Set volume to 30% (70% quieter)
wall_hit_sound = pygame.mixer.Sound("wall_hit.wav")

# Particle settings
particles = []
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Scoring
left_score = 0
right_score = 0

# Winning score
WINNING_SCORE = 11

# Paddle positions
left_paddle = pygame.Rect(10, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position
ball = pygame.Rect((WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2, BALL_SIZE, BALL_SIZE)

# Load rocket image
try:
    rocket_image = pygame.image.load("rocket.png")
    rocket_image = pygame.transform.scale(rocket_image, (20, 100))
except FileNotFoundError:
    print("Warning: 'rocket.png' not found. The obstacle will not be displayed.")
    rocket_image = None
obstacle_speed = 5

# Main game loop
def main():
    global BALL_SPEED_X, BALL_SPEED_Y, left_score, right_score, particles, obstacle_speed
    global stars
    global obstacle
    clock = pygame.time.Clock()
    obstacle = pygame.Rect((WIDTH - 20) // 2, (HEIGHT - 100) // 2, 20, 100)
    stars = generate_stars(100)
    font = pygame.font.Font(None, 74)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if left_score >= WINNING_SCORE or right_score >= WINNING_SCORE:
            winner_text = "Left Player Wins!" if left_score >= WINNING_SCORE else "Right Player Wins!"
            winner_surface = font.render(winner_text, True, WHITE)
            screen.fill(BLACK)
            screen.blit(winner_surface, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        # Move the rocket obstacle every 3 points
        if (left_score + right_score) % 3 == 0 and (left_score + right_score) != 0:
            obstacle.y += obstacle_speed
            if obstacle.top <= 0 or obstacle.bottom >= HEIGHT:
                obstacle_speed *= -1

        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            wall_hit_sound.play()
            BALL_SPEED_Y *= -1
        if ball.left <= 0:
            right_score += 1
            ball.x, ball.y = (WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2
            BALL_SPEED_X *= -1
            score_sound.play()
            particles.append([ball.x, ball.y, BALL_SPEED_X * 0.5, BALL_SPEED_Y * 0.5, 5])  # Add velocity and initial size
        elif ball.right >= WIDTH:
            left_score += 1
            ball.x, ball.y = (WIDTH - BALL_SIZE) // 2, (HEIGHT - BALL_SIZE) // 2
            BALL_SPEED_X *= -1
            score_sound.play()
            particles.append([ball.x, ball.y, BALL_SPEED_X * 0.5, BALL_SPEED_Y * 0.5, 5])  # Add velocity and initial size

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle) or ball.colliderect(obstacle):
            BALL_SPEED_X *= -1

        screen.fill(BLACK)
        draw_stars(stars)
        pygame.draw.rect(screen, left_paddle_color, left_paddle)
        pygame.draw.rect(screen, right_paddle_color, right_paddle)
        pygame.draw.ellipse(screen, ball_color, ball)
        # Draw the rocket obstacle every 3 points
        if (left_score + right_score) % 3 == 0 and (left_score + right_score) != 0:
            if rocket_image:
                screen.blit(rocket_image, obstacle)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        font = pygame.font.Font(None, 74)
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (WIDTH // 4, 10))
        screen.blit(right_text, (WIDTH * 3 // 4, 10))

        # Update and draw particles
        for particle in particles:
            particle[0] += particle[2]  # Move particle horizontally
            particle[1] += particle[3]  # Move particle vertically
            particle[4] -= 0.1  # Decrease particle size
            pygame.draw.circle(screen, WHITE, (int(particle[0]), int(particle[1])), int(particle[4]))
        particles = [p for p in particles if p[4] > 0]  # Remove particles that are too small

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
