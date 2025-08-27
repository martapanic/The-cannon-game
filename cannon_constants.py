# ----------------------------------
# Constants Module for Cannon Game
# ----------------------------------

# Projectile sizes (in pixels)
BULLET_RADIUS = 10
BOMB_RADIUS = 15
LASER_DIST = 5

# Game screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Frame rate (frames per second)
FPS = 20

# Mass properties of projectiles
BULLET_MASS = SCREEN_WIDTH / 2  # Bullet mass is half the screen width
BOMB_MASS = SCREEN_WIDTH / 3  # Bomb mass is one-third of the screen width

# Maximum velocity for different projectiles
BULLET_MAX_VEL = BULLET_MASS  # Bullet velocity is determined by its mass
BOMB_MAX_VEL = BOMB_MASS  # Bomb velocity is determined by its mass
LASER_VEL = SCREEN_WIDTH / 1.5

# Damage radius and impact range for projectiles
BULLET_RADIUS = SCREEN_WIDTH / 100  # Bullet's effective radius
BOMB_RADIUS = SCREEN_WIDTH / 50  # Bomb's effective radius
LASER_DIST = SCREEN_WIDTH / 100  # Laser's effective distance

# Drill effect and impulse properties
BOMB_DRILL = SCREEN_WIDTH / 50  # Bomb drill distance
LASER_IMPULSE = SCREEN_WIDTH / 30  # Laser impulse effect
