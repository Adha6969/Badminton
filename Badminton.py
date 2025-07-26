from pygame import *
from random import randint

# Load image files
img_back = "court.jpg"
img_player = "racket.png"
img_player2 = "racket2.png"
img_kok = "kok.png"


# Window setup
win_width = 700
win_height = 500
display.set_caption("Badminton")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Font setup
font.init()
font_score = font.SysFont("Arial", 36)
font_end = font.SysFont("Arial", 60)

# Score tracking
score_left = 0
score_right = 0
max_score = 5

# Sprite classes
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_L(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

class Player2(GameSprite):
    def update_R(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.dx = 5
        self.dy = 5

        self.image_normal = self.image
        self.image_flipped = transform.flip(self.image, True, False)
        self.flipped = False
        self.first_hit = False  # For avoiding flip on first hit

    def update(self):
        global score_left, score_right, finish

        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off top/bottom
        if self.rect.y <= 0 or self.rect.y >= win_height - self.rect.height:
            self.dy *= -1

        # Scoring conditions
        if self.rect.x <= 0:
            score_right += 1
            self.reset_ball()
            if score_right >= max_score:
                finish = True

        elif self.rect.x >= win_width - self.rect.width:
            score_left += 1
            self.reset_ball()
            if score_left >= max_score:
                finish = True

        # Collision with rackets
        if self.rect.colliderect(racket.rect) and self.dx < 0:
            self.dx *= -1
            if self.first_hit:
                self.toggle_flip()
            else:
                self.first_hit = True
            self.rect.left = racket.rect.right

        elif self.rect.colliderect(racket2.rect) and self.dx > 0:
            self.dx *= -1
            if self.first_hit:
                self.toggle_flip()
            else:
                self.first_hit = True
            self.rect.right = racket2.rect.left

    def toggle_flip(self):
        self.flipped = not self.flipped
        self.image = self.image_flipped if self.flipped else self.image_normal

    def reset_ball(self):
        self.rect.x = win_width // 2
        self.rect.y = win_height // 2
        self.dx *= -1
        self.first_hit = False
        self.toggle_flip()

# Game objects
kok = Ball(img_kok, 335, 235, 40, 40, 5)
racket = Player(img_player, 30, 200, 100, 140, 5)
racket2 = Player2(img_player2, 570, 200, 100, 140, 5)

# Game loop
finish = False
run = True
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    window.blit(background, (0, 0))

    if not finish:
        # Game logic
        kok.update()
        racket.update_L()
        racket2.update_R()

        # Drawing
        kok.reset()
        racket.reset()
        racket2.reset()

        # Score display
        score_text = font_score.render(f"{score_left} : {score_right}", True, (255, 255, 255))
        window.blit(score_text, (win_width // 2 - score_text.get_width() // 2, 20))
    else:
        # Win/lose message
        if score_left >= max_score:
            result_text = font_end.render("PLAYER 1 WINS!", True, (0, 255, 0))
        else:
            result_text = font_end.render("PLAYER 2 WINS!", True, (0, 255, 0))
        window.blit(result_text, (win_width // 2 - result_text.get_width() // 2,
                                  win_height // 2 - result_text.get_height() // 2))

    display.update()
    clock.tick(60)
