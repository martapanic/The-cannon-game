# -------------------------------------------------------------------------------
# main.py
# Final Exam Project – A.Y. 2023/24
# Università degli Studi di Pavia
#
#  The game is a 2D side-view artillery game in which the player controls a cannon to fire projectiles at a target.
# The project includes multiple projectile types (bullet, bombshell, laser) and obstacles
# (rock, mirror, perpetio, wormhole, etc.). Below, we add detailed comments to explain
# how each part of the code works.
# -------------------------------------------------------------------------------

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Rectangle
import random
import math
from kivy.uix.scrollview import ScrollView
import cannon_constants as const
import math
from kivy.uix.widget import Widget
from kivy.uix.image import Image
import cannon_constants as const
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
import math
import random
import cannon_constants as const
from kivy.graphics import Color, Ellipse

import math
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Rectangle

# ---------------------------
# Projectile Class Definition
# ---------------------------
class Projectile(Widget):
    def __init__(self, projectile_type, start_position, **kwargs):
        super().__init__(**kwargs)
        # Initialize the projectile type and starting position based on game logic.
        self.projectile_type = projectile_type
        self.position = list(start_position)  # Convert position to a mutable list.
        self.velocity = [0, 0]  # Initial velocity (will be set on launch).
        self.active = True  # Flag to determine if the projectile is still in play.
        self.just_teleported = False  # Flag to manage wormhole teleport cooldown.
        self.teleport_cooldown = 0.5  # Cooldown time before teleporting again.

        # Store the launch time for tracking projectile motion over time.
        self.launch_time = None

        # Assign properties based on projectile type.
        if self.projectile_type == "bullet":
            # Bullet follows a parabolic trajectory under gravity.
            self.radius = const.BULLET_RADIUS
            self.image_source = "images/small_images/bullet_widget.png"
        elif self.projectile_type == "bombshell":
            # Bombshell follows similar physics to bullets but may have different damage.
            self.radius = const.BOMB_RADIUS
            self.image_source = "images/small_images/bombshell_widget.png"
        elif self.projectile_type == "laser":
            # Laser moves in a straight line without gravity influence.
            self.radius = const.LASER_DIST
            self.image_source = "images/small_images/laser_widget.png"

        # Create and display the image representing the projectile.
        self.image_widget = Image(
            source=self.image_source,
            size=(80, 80),  # Fixed size for the visual representation.
            pos=(self.position[0] - self.radius, self.position[1] - self.radius)
        )
        self.add_widget(self.image_widget)
    
    @staticmethod
    def distance_between(pos1, pos2):
        """
        Calculate the Euclidean distance between two points.
        This is used for collision detection.
        """
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def launch(self, angle, power):
        """
        Launch the projectile by calculating its initial velocity.
        The velocity depends on the projectile type and is based on the launch angle and power.
        
        - Bullets and bombshells follow parabolic motion, so their velocity components are computed
          using a multiplier of 5.
        - Lasers move in a straight line, so they have a higher velocity multiplier (15).
        """
        self.launch_time = Clock.get_boottime()  # Record the time of launch.
        radian_angle = math.radians(angle)  # Convert angle to radians for trigonometric calculations.

        if self.projectile_type in ["bullet", "bombshell"]:
            # Compute horizontal (x) and vertical (y) velocity components.
            self.velocity = [
                power * math.cos(radian_angle) * 5,  # Horizontal velocity.
                power * math.sin(radian_angle) * 5   # Initial vertical velocity.
            ]
        elif self.projectile_type == "laser":
            # Lasers move in a straight line, thus use a higher velocity.
            self.velocity = [
                power * math.cos(radian_angle) * 15,
                power * math.sin(radian_angle) * 15
            ]
        print(f"{self.projectile_type.capitalize()} launched with velocity: {self.velocity}")

    def update(self, dt):
        """
        Update the projectile's position each frame based on physics rules.
        
        - Bullets and bombshells experience gravity, so they follow a parabolic trajectory.
        - Lasers move in a straight line without gravity influence.
        - Projectiles that move off the screen are deactivated.
        """
        if not self.active:
            return

        # Handle teleport cooldown if the projectile recently passed through a wormhole.
        if self.just_teleported:
            self.teleport_cooldown -= dt
            if self.teleport_cooldown <= 0:
                self.just_teleported = False

        # Apply motion physics based on projectile type.
        if self.projectile_type in ["bullet", "bombshell"]:
            time_elapsed = Clock.get_boottime() - self.launch_time
            # Horizontal movement (constant velocity)
            self.position[0] += self.velocity[0] * dt
            # Vertical movement (affected by gravity: y = v0*t - 0.5*g*t^2)
            self.position[1] += self.velocity[1] * dt - (0.5 * 9.8 * (time_elapsed ** 2))
        elif self.projectile_type == "laser":
            # Straight-line motion without gravity.
            self.position[0] += self.velocity[0] * dt
            self.position[1] += self.velocity[1] * dt

        # Check if projectile moves off-screen; if so, deactivate it.
        if (self.position[0] > const.SCREEN_WIDTH or
                self.position[0] < 0 or
                self.position[1] > const.SCREEN_HEIGHT or
                self.position[1] < 0):
            self.deactivate()

        # Update the position of the visual representation.
        if self.active and hasattr(self, 'image_widget'):
            self.image_widget.pos = (
                self.position[0] - self.radius,
                self.position[1] - self.radius
            )

    def deactivate(self):
        """
        Deactivate the projectile when it goes off-screen or collides.
        This stops further movement and removes its image widget from the game.
        """
        self.active = False
        if hasattr(self, 'image_widget') and self.image_widget.parent:
            self.image_widget.parent.remove_widget(self.image_widget)

    def is_active(self):
        """Check if the projectile is still active (has not been removed)."""
        return self.active

    def get_position(self):
        """Return the current position of the projectile."""
        return self.position

    def get_radius(self):
        """Return the radius, which is used for collision detection."""
        return self.radius

    def reflect(self):
        """
        Reflect the projectile when it collides with a mirror-like object.
        This is done by inverting its velocity components, causing it to travel in the opposite direction.
        """
        self.velocity[0] = -self.velocity[0]  # Reverse horizontal velocity.
        self.velocity[1] = -self.velocity[1]  # Reverse vertical velocity.
        print(f"{self.projectile_type.capitalize()} reflected! New velocity: {self.velocity}")

# ---------------------------
# Obstacle Class Definition
# ---------------------------
class Obstacle(Widget):
    def __init__(self, obstacle_type, game, image=None, **kwargs):
        super().__init__(**kwargs)
        # Initialize obstacle type and set a default collision radius.
        self.obstacle_type = obstacle_type
        self.radius = 60  # Standard radius for all obstacles.
        self.game = game  # Reference to the game instance.
        
        # Set a random initial position within the game field, ensuring obstacles are placed correctly.
        self.position = [
            random.randint(const.SCREEN_WIDTH // 2, const.SCREEN_WIDTH - self.radius * 2),
            random.randint(150, const.SCREEN_HEIGHT // 2)
        ]

        # Assign random velocities to enable smooth movement across the screen.
        self.vx = random.uniform(-5, 5)  # Random horizontal speed.
        self.vy = random.uniform(-5, 5)  # Random vertical speed.
        print(f"Obstacle initialized with velocity: vx={self.vx}, vy={self.vy}")

        # If the obstacle is a wormhole ('perpetio') and no image is provided, assign a default image.
        if self.obstacle_type == "perpetio" and not image:
            image = "images/small_images/perpetio.jpg"

        # Rocks are destructible, so they have health.
        self.health = 3 if self.obstacle_type == "rock" else None

        # Create a visual representation of the obstacle using an image widget.
        self.image_widget = Image(
            source=image,
            size=(self.radius * 2, self.radius * 2),  # Set image size to match the obstacle's radius.
            pos=(self.position[0] - self.radius, self.position[1] - self.radius)
        )
        self.add_widget(self.image_widget)

    def update(self, dt):
        """
        Update the obstacle's position each frame.
        - Moves based on its velocity.
        - Bounces back when it hits screen boundaries.
        """
        self.position[0] += self.vx * dt
        self.position[1] += self.vy * dt

        # Reverse horizontal velocity if it reaches screen edges.
        if self.position[0] - self.radius <= 0 or self.position[0] + self.radius >= Window.width:
            self.vx = -self.vx

        # Reverse vertical velocity if it reaches screen edges.
        if self.position[1] - self.radius <= 0 or self.position[1] + self.radius >= Window.height:
            self.vy = -self.vy

        # Update the position of the image widget to match the obstacle's movement.
        self.image_widget.pos = (self.position[0] - self.radius, self.position[1] - self.radius)

    def collides_with(self, projectile):
        """
        Check if the obstacle collides with a given projectile.
        Uses Euclidean distance to determine if their radii overlap.
        """
        proj_x, proj_y = projectile.get_position()
        distance = math.sqrt((proj_x - self.position[0]) ** 2 + (proj_y - self.position[1]) ** 2)
        return distance < self.radius + projectile.get_radius()

    def on_hit(self, projectile):
        """
        Handle collision effects when a projectile strikes an obstacle.
        - If the obstacle is a rock, reduce health.
        - If health reaches zero, remove the obstacle from the game.
        - Returns True if the obstacle is destroyed.
        """
        if self.obstacle_type == "rock":
            self.health -= 1
            if self.health <= 0:
                if self in self.game.obstacles:
                    self.game.obstacles.remove(self)  # Remove from game list.
                if hasattr(self, 'image_widget'):
                    self.game.layout.remove_widget(self.image_widget)  # Remove visual representation.
                self.game.layout.remove_widget(self)  # Remove the obstacle itself.
                return True  # Indicate destruction.
        return False

    def get_exit_position(self, paired_wormhole):
        """
        If the obstacle is a wormhole, return the exit position from the paired wormhole.
        """
        if self.obstacle_type == "wormhole" and paired_wormhole:
            return [paired_wormhole.position[0], paired_wormhole.position[1]]

    def reflect_projectile(self, projectile):
        """
        Handle projectile reflection when it collides with a mirror obstacle.
        - Bullets and bombshells disappear upon collision.
        - Lasers reflect, inverting their dominant velocity component.
        """
        if self.obstacle_type == "mirror":
            if projectile.projectile_type in ["bullet", "bombshell"]:
                if hasattr(projectile, 'image_widget') and projectile.image_widget.parent:
                    self.parent.remove_widget(projectile.image_widget)
                if projectile in self.parent.projectiles:
                    self.parent.projectiles.remove(projectile)
                projectile.active = False  # Mark projectile as inactive.
                print(f"{projectile.projectile_type.capitalize()} disappeared upon hitting the mirror!")
            elif projectile.projectile_type == "laser":
                # Reflect horizontally if moving mostly in x-direction, otherwise reflect vertically.
                if abs(projectile.velocity[0]) > abs(projectile.velocity[1]):
                    projectile.velocity[0] = -projectile.velocity[0]  # Reverse horizontal velocity.
                else:
                    projectile.velocity[1] = -projectile.velocity[1]  # Reverse vertical velocity.
                print(f"Laser reflected by the mirror! New velocity: {projectile.velocity}")

# ---------------------------
# Cannon Class Definition
# ---------------------------
class Cannon(Widget):
    def __init__(self, position, angle=30, **kwargs):
        super().__init__(**kwargs)
        # Initialize the cannon's base position and firing angle.
        self.position = position  # (x, y) coordinates of the cannon base.
        self.angle = angle  # Initial angle in degrees.
        self.barrel_length = 60  # Length of the cannon barrel used for calculations.

        # Draw the cannon image on the canvas with rotation applied.
        with self.canvas:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.position)  # Rotation centered on the base.
            self.image = Rectangle(
                source="images/small_images/cannon_widget.png",
                size=(230, 188),  # Fixed image dimensions.
                pos=(self.position[0] - 50, self.position[1] - 25)  # Offset to align image properly.
            )
            PopMatrix()

    def rotate(self, direction):
        """
        Adjust the cannon's angle based on user input.
        - 'up' increases the angle.
        - 'down' decreases it.
        - Maximum angle is 360 degrees, minimum is -90 degrees.
        """
        if direction == "up":
            self.angle = min(self.angle + 5, 360)  # Prevent exceeding 360 degrees.
        elif direction == "down":
            self.angle = max(self.angle - 5, -90)  # Prevent going below -90 degrees.

        # Update the rotation transformation to reflect the new angle.
        self.rotation.angle = self.angle
        self.canvas.ask_update()  # Request a redraw of the canvas.
        print(f"Cannon rotated to angle: {self.angle}")

    def get_angle(self):
        """
        Retrieve the current firing angle of the cannon.
        """
        return self.angle

    def get_tip_position(self):
        """
        Compute the tip position of the cannon barrel.
        This is used as the starting location for launched projectiles.
        """
        radian_angle = math.radians(self.angle)  # Convert angle to radians for calculations.
        tip_x = self.position[0] + math.cos(radian_angle) * (self.barrel_length + 10)
        tip_y = self.position[1] + math.sin(radian_angle) * (self.barrel_length + 10)
        return [tip_x, tip_y]  # Return the computed tip coordinates.


# ---------------------------
# CannonGame Class Definition
# ---------------------------
class CannonGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize game state variables.
        self.state = "enter_nickname"
        self.nickname = ""
        self.score = 0
        self.shots_left = 10
        self.projectiles = []
        self.obstacles = []
        self.selected_projectile = "bullet"
        self.level = 1
        self.angle = 45
        self.velocity = 50
        self.cannon = None  # The cannon will be initialized during gameplay.
        self.file_path = "hall_of_fame.txt"

        # Schedule the update loop (running at 120 FPS for smooth animations).
        Clock.schedule_interval(self.update, 1 / 120)

        # Define background images for different levels.
        self.level_backgrounds = {
            1: "images/cannon_america.jpg",
            2: "images/cannon_africa.jpg",
            3: "images/level3.jpg",
            4: "images/level4.jpg",
            5: "images/level5.jpg",
        }

        # Set the initial background (choice screen background).
        with self.canvas.before:
            self.background = Rectangle(
                source="images/choice_background.png",
                pos=self.pos, size=self.size
            )

        # Bind the background size and position to the main widget's size/pos.
        self.bind(size=self.update_background, pos=self.update_background)

        # Create a FloatLayout for UI elements (allows absolute positioning).
        self.layout = FloatLayout(size=self.size)
        self.bind(size=self.on_layout_resize)
        self.add_widget(self.layout)

        # Create the nickname input field and start button for initial game setup.
        self.nickname_input = TextInput(
            hint_text="Enter your nickname",
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            multiline=False
        )
        self.start_button = Button(
            background_normal="images/buttons/immagine_continue.jpg",
            size_hint=(None, None),
            size=(200, 90),
            pos_hint={"center_x": 0.5, "center_y": 0.2}
        )
        self.start_button.bind(on_press=self.go_to_start_screen)

        # Add these initial widgets to the layout.
        self.layout.add_widget(self.nickname_input)
        self.layout.add_widget(self.start_button)

        print("Initialized nickname input and start button.")

    def on_layout_resize(self, *args):
        # Ensure the layout always matches the size of the game widget.
        self.layout.size = self.size

    def update_background(self, *args):
        # Update the background rectangle's position and size.
        self.background.pos = self.pos
        self.background.size = self.size

    def go_to_start_screen(self, instance):
        """
        Transition from nickname input to the start screen.
        Resets the cannon if it exists and updates the background image.
        """
        self.nickname = self.nickname_input.text
        self.state = "start"
        if self.cannon:
            self.remove_widget(self.cannon)
            self.cannon = None  # Reset cannon.
        print("Switching to start screen.")

        self.background.source = "images/homescreen_background.jpg"
        self.layout.clear_widgets()

        # Create and bind the start, Hall of Fame, and help buttons.
        self.start_button = Button(
            background_normal="images/buttons/play_button.png",
            size_hint=(None, None),
            size=(200, 72),
            pos_hint={"center_x": 0.2, "center_y": 0.1}
        )
        self.start_button.bind(on_press=self.go_to_projectile_screen)

        self.hall_of_fame_button = Button(
            background_normal="images/buttons/immagine_hof copia 2.jpeg",
            size_hint=(None, None),
            size=(134, 116),
            pos_hint={"center_x": 0.9, "center_y": 0.9}
        )
        self.hall_of_fame_button.bind(on_press=self.show_hall_of_fame)

        self.help_button = Button(
            background_normal="images/buttons/help_button.jpeg",
            size_hint=(None, None),
            size=(134, 116),
            pos_hint={"center_x": 0.9, "center_y": 0.6}
        )
        self.help_button.bind(on_press=self.show_help_screen)

        self.layout.add_widget(self.hall_of_fame_button)
        self.layout.add_widget(self.help_button)
        self.layout.add_widget(self.start_button)

    def go_to_projectile_screen(self, instance):
        """
        Transition to the projectile selection screen.
        The player chooses which type of projectile to use.
        """
        self.state = "choose_projectile"
        self.layout.clear_widgets()
        self.background.source = "images/trajectory_choice.jpg"

        # Create buttons for each projectile type.
        self.bullet_button = Button(
            background_normal="images/buttons/bullet_button.jpeg",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.2, "center_y": 0.4}
        )
        self.bullet_button.bind(on_press=lambda x: self.select_projectile("bullet"))

        self.bombshell_button = Button(
            background_normal="images/buttons/bombshell_button.jpeg",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.5, "center_y": 0.4}
        )
        self.bombshell_button.bind(on_press=lambda x: self.select_projectile("bombshell"))

        self.laser_button = Button(
            background_normal="images/buttons/laser_button.jpeg",
            size_hint=(None, None),
            size=(150, 150),
            pos_hint={"center_x": 0.8, "center_y": 0.4}
        )
        self.laser_button.bind(on_press=lambda x: self.select_projectile("laser"))

        self.layout.add_widget(self.bullet_button)
        self.layout.add_widget(self.bombshell_button)
        self.layout.add_widget(self.laser_button)
        print("Projectile selection screen initialized with bullet, bombshell, and laser options.")


    def show_hall_of_fame(self, instance):
        """
        Displays the Hall of Fame in a scrollable popup.
        Ensures the latest scores appear at the top.
        """
        try:
            with open("hall_of_fame.txt", "r") as f:
                hof_data = f.readlines()  # Read all lines
        except FileNotFoundError:
            hof_data = ["No Hall of Fame data found."]

            # Strip whitespace and remove empty lines
        hof_data = [line.strip() for line in hof_data if line.strip()]

        # Convert list to a single string with line breaks (reverse order for display)
        hof_text = "\n".join(hof_data[::-1])  # This reverses the list

        # Create a TextInput (Read-only) with scrolling enabled
        text_display = TextInput(
            text=hof_text,
            readonly=True,  # Prevents editing
            multiline=True,  # Allows multiple lines
            size_hint=(1, None),  # Fix width but allow dynamic height
            height=1000,  # Set the height for scrolling
            background_color=(0, 0, 0, 0),  # Transparent background
            foreground_color=(1, 1, 1, 1),  # White text
            font_size='20sp',
            cursor_blink=False  # No need for a blinking cursor
        )

        # Wrap the TextInput in a ScrollView to enable proper scrolling
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(text_display)

        # Create and open the popup
        popup = Popup(
            title="Hall of Fame",
            content=scroll_view,
            size_hint=(0.8, 0.8)
        )
        popup.open()

    
    def save_to_hall_of_fame(self):
        """
        Saves the player's nickname, score, and level to the Hall of Fame file.
        Ensures the score is saved only once per game session.
        The latest entry appears at the top of the file.
        """
        # Prevent saving multiple times in the same session
        if hasattr(self, "saved_to_hall_of_fame") and self.saved_to_hall_of_fame:
            return  # Do nothing if already saved

        # Prepare the new entry
        new_entry = f"Nickname: {self.nickname}, Score: {self.score}, Level: {self.level}\n"

        # Read existing records (if the file exists)
        try:
            with open("hall_of_fame.txt", "r") as f:
                old_records = f.readlines()
        except FileNotFoundError:
            old_records = []

        # Insert the new entry at the top and rewrite the file
        with open("hall_of_fame.txt", "w") as f:
            f.write(new_entry)
            f.writelines(old_records)

        # Mark the score as saved to prevent duplicates
        self.saved_to_hall_of_fame = True

    def show_help_screen(self, instance):
        """
        Display a help popup with an image.
        If the help image cannot be loaded, show an error message.
        """
        help_image_path = "images/help.jpg"
        if Image(source=help_image_path).texture:
            popup_content = Image(source=help_image_path, allow_stretch=True, keep_ratio=True)
        else:
            print(f"Help image not found: {help_image_path}")
            popup_content = Label(text="Help image is missing. Please contact support.")

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(popup_content)
        popup = Popup(
            title="Help",
            content=layout,
            size_hint=(0.8, 0.8)
        )
        popup.open()

    def select_projectile(self, projectile_type):
        """
        Save the selected projectile type and transition to gameplay.
        """
        self.selected_projectile = projectile_type
        print(f"Projectile selected: {projectile_type}")
        self.layout.clear_widgets()
        self.initialize_gameplay()

    def show_final_screen(self):
        """
        Display the final congratulations screen after all levels are completed.
        Provides an option to restart the game.
        """
        print("Displaying Final Congratulations Screen")
        self.state = "final_screen"
        self.layout.clear_widgets()
        with self.canvas.before:
            self.background.source = "images/final_image.jpg"
            self.background.pos = self.pos
            self.background.size = self.size
        restart_button = Button(
            text="Restart Game",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        restart_button.bind(on_press=self.go_to_start_screen)
        self.layout.add_widget(restart_button)

    def next_level(self, instance=None):
        """
        Proceed to the next level.
        If the current level is the last one, show the final screen.
        """
        total_levels = len(self.level_backgrounds)
        if self.level >= total_levels:
            print("All levels completed! Showing final screen.")
            self.show_final_screen()
        else:
            self.level += 1
            self.shots_left = 10
            self.initialize_gameplay()

    def initialize_gameplay(self, instance=None):
        """
        Initialize gameplay elements for the current level.
        Sets the background, initializes the cannon and obstacles, and prepares UI elements.
        """
        print(f"Starting level {self.level}!")
        self.state = f"level_{self.level}"
        if hasattr(self, 'background'):
            self.background.source = self.level_backgrounds.get(self.level, "")
        else:
            with self.canvas.before:
                self.background = Rectangle(
                    source=self.level_backgrounds.get(self.level, ""),
                    pos=self.pos,
                    size=self.size
                )
            self.bind(size=self.update_background, pos=self.update_background)
        self.layout.clear_widgets()
        if not self.cannon:
            self.cannon = Cannon(position=[100, 100], angle=25)
            self.add_widget(self.cannon)
            print(f"Cannon initialized at position: {self.cannon.position}")
        self.cannon.position = [100, 100]
        self.cannon.angle = 25
        self.initialize_obstacles()
        self.score_text = f"Score: {self.score}   Shots Left: {self.shots_left}"
        self.score_label = Label(
            text=self.score_text,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"x": 0.01, "top": 0.98},
            halign="left",
            valign="middle",
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.score_label)
        self.pause_button = Button(
            text="Pause",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={"center_x": 0.9, "center_y": 0.9}
        )
        self.pause_button.bind(on_press=self.toggle_pause)
        self.layout.add_widget(self.pause_button)
        Clock.schedule_interval(self.update, 1 / 120)

    def toggle_pause(self, instance):
        """
        Toggle the game pause state.
        When paused, display options for changing the projectile type, resuming, or resetting.
        """
        if hasattr(self, 'paused') and self.paused:
            self.paused = False
            Clock.schedule_interval(self.update, 1 / 120)
            self.layout.clear_widgets()
            self.initialize_gameplay()
            print(f"Game resumed. Shots left: {self.shots_left}")
        else:
            self.paused = True
            Clock.unschedule(self.update)
            self.layout.clear_widgets()
            button_width, button_height = 150, 100
            self.bullet_button = Button(
                text="Bullet", size_hint=(None, None), size=(button_width, button_height),
                pos_hint={"center_x": 0.2, "center_y": 0.5}
            )
            self.bullet_button.bind(on_press=lambda x: self.change_projectile("bullet"))
            self.bombshell_button = Button(
                text="Bombshell", size_hint=(None, None), size=(button_width, button_height),
                pos_hint={"center_x": 0.5, "center_y": 0.5}
            )
            self.bombshell_button.bind(on_press=lambda x: self.change_projectile("bombshell"))
            self.laser_button = Button(
                text="Laser", size_hint=(None, None), size=(button_width, button_height),
                pos_hint={"center_x": 0.8, "center_y": 0.5}
            )
            self.laser_button.bind(on_press=lambda x: self.change_projectile("laser"))
            self.resume_button = Button(
                text="Resume", size_hint=(None, None), size=(100, 50),
                pos_hint={"center_x": 0.5, "center_y": 0.2}
            )
            self.resume_button.bind(on_press=self.toggle_pause)
            self.reset_button = Button(
                text="Reset", size_hint=(None, None), size=(100, 50),
                pos_hint={"center_x": 0.5, "center_y": 0.3}
            )
            self.reset_button.bind(on_press=self.go_to_start_screen)
            self.layout.add_widget(self.bullet_button)
            self.layout.add_widget(self.bombshell_button)
            self.layout.add_widget(self.laser_button)
            self.layout.add_widget(self.resume_button)
            self.layout.add_widget(self.reset_button)
            print(f"Game paused. Shots left: {self.shots_left}")

    def change_projectile(self, new_projectile):
        """
        Change the projectile type without affecting the current shot count.
        After the change, resume the game.
        """
        self.selected_projectile = new_projectile
        print(f"Projectile changed to {new_projectile}. Shots left: {self.shots_left}")
        self.toggle_pause(None)

    def initialize_obstacles(self):
        """
        Generate obstacles on the game field.
        Fixed total count is used with:
         - A fixed number of wormholes (in pairs),
         - A random count of mirrors and perpetios,
         - The remainder being rocks.
        Positions are randomized with screen padding.
        """
        self.obstacles = []
        total_obstacles = 10  # Fixed total obstacles.
        num_wormholes = 2
        num_mirrors = random.randint(0, 2)
        num_perpetio = random.randint(0, total_obstacles // 5)
        num_rocks = total_obstacles - (num_wormholes + num_mirrors + num_perpetio)
        screen_padding = 50

        def get_random_position():
            return [
                random.randint(screen_padding, const.SCREEN_WIDTH - screen_padding),
                random.randint(screen_padding, const.SCREEN_HEIGHT - screen_padding)
            ]

        # Add wormhole pairs.
        for _ in range(num_wormholes // 2):
            wormhole1 = Obstacle("wormhole", self, image="images/small_images/immagine_wormhole.png", pos=get_random_position())
            wormhole2 = Obstacle("wormhole", self, image="images/small_images/immagine_wormhole.png", pos=get_random_position())
            self.obstacles.extend([wormhole1, wormhole2])

        # Add mirror obstacles.
        for _ in range(num_mirrors):
            self.obstacles.append(Obstacle("mirror", self, image="images/small_images/immaginespecchio.jpg", pos=get_random_position()))

        # Add perpetio obstacles.
        for _ in range(num_perpetio):
            self.obstacles.append(Obstacle("perpetio", self, image="images/small_images/perpetio.png", pos=get_random_position()))

        # Add rock obstacles.
        for _ in range(num_rocks):
            self.obstacles.append(Obstacle("rock", self, image="images/small_images/immagineroccia.png", pos=get_random_position()))

        for obstacle in self.obstacles:
            self.layout.add_widget(obstacle)
        print(f"Obstacles initialized: {num_rocks} rocks, {num_wormholes} wormholes, {num_mirrors} mirrors, {num_perpetio} perpetios.")

    def update_score_text(self):
        # Update the score label text.
        self.score_text = f"Score: {self.score}   Shots Left: {self.shots_left}"

    def update(self, dt):
        """
        Main update loop.
        Updates obstacles and projectiles, checks for collisions, and updates score display.
        Also verifies if the game is over due to no shots remaining.
        """
        if not self.state.startswith("level_"):
            return

        for obstacle in self.obstacles:
            obstacle.update(dt)
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if not projectile.is_active():
                self.projectiles.remove(projectile)
        self.handle_collisions()

        if self.shots_left <= 0:
            print("Game over: No shots left")
            self.game_over()
            
        self.update_score_text()
        self.score_label.text = self.score_text

    def handle_collisions(self):
        """
        Check for collisions between projectiles and obstacles.
        Handles special cases:
         - Wormholes: Teleport projectiles.
         - Mirrors: Reflect or remove projectiles.
         - Perpetios: Remove projectiles.
         - Rocks: Reduce health, update score, and clear level if all rocks are destroyed.
        """
        for obstacle in self.obstacles[:]:
            for projectile in self.projectiles[:]:
                if obstacle.collides_with(projectile):
                    if obstacle.obstacle_type == "wormhole" and not projectile.just_teleported:
                        paired_wormhole = next(
                            (o for o in self.obstacles if o.obstacle_type == "wormhole" and o != obstacle), None
                        )
                        if paired_wormhole:
                            print(f"Paired wormhole found: {paired_wormhole}")
                            min_distance = obstacle.radius + paired_wormhole.radius + 50
                            while Projectile.distance_between(obstacle.position, paired_wormhole.position) < min_distance:
                                paired_wormhole.position = [
                                    random.randint(const.SCREEN_WIDTH // 2, const.SCREEN_WIDTH - paired_wormhole.radius * 2),
                                    random.randint(150, const.SCREEN_HEIGHT // 2)
                                ]
                            offset = paired_wormhole.radius + 10
                            exit_position = [
                                paired_wormhole.position[0] + offset,
                                paired_wormhole.position[1] + offset
                            ]
                            projectile.position = exit_position
                            projectile.image_widget.pos = (
                                exit_position[0] - projectile.radius,
                                exit_position[1] - projectile.radius
                            )
                            projectile.just_teleported = True
                            projectile.teleport_cooldown = 0.5
                            print(f"Exit position calculated: {exit_position}")
                    elif obstacle.obstacle_type == "mirror":
                        if projectile.projectile_type == "laser":
                            obstacle.reflect_projectile(projectile)
                        else:
                            print(f"{projectile.projectile_type} destroyed on mirror impact.")
                            if projectile in self.projectiles:
                                projectile.remove_widget(projectile.image_widget)
                    elif obstacle.obstacle_type == "perpetio":
                        print(f"{projectile.projectile_type} destroyed upon hitting perpetio.")
                        if projectile in self.projectiles :
                            projectile.remove_widget(projectile.image_widget)
                    elif obstacle.on_hit(projectile):
                        if obstacle.obstacle_type == "rock":
                            self.score += 10
                            if obstacle in self.obstacles:
                                self.obstacles.remove(obstacle)
                                obstacle.remove_widget(obstacle.image_widget)
                            if not any(o.obstacle_type == "rock" for o in self.obstacles):
                                print("Congratulations! All rocks destroyed.")
                                self.congratulations_screen()
                        if hasattr(obstacle, 'image_widget'):
                            obstacle.remove_widget(obstacle.image_widget)
                        if hasattr(projectile, 'image_widget'):
                            projectile.remove_widget(projectile.image_widget)
                        if obstacle in self.obstacles:
                            self.obstacles.remove(obstacle)
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)

    def shutdown(self):
        # Shut down the game by stopping the Kivy application.
        print("Shutting down game.")
        App.get_running_app().stop()

    def game_over(self):
        """
        Trigger game over:
         - Save player's data.
         - Show a popup with options to restart or shutdown.
         - Auto shutdown after a delay.
        """
        print("Game Over! You ran out of shots.")
        self.save_to_hall_of_fame()
        popup_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_content.add_widget(Label(text="GAME OVER! Choose an option."))
        popup = Popup(
            title="Game Over",
            content=popup_content,
            size_hint=(0.6, 0.4)
        )
        restart_button = Button(text="Restart", size_hint=(None, None), size=(200, 50))
        restart_button.bind(on_press=lambda instance: self.restart_game(popup))
        shutdown_button = Button(text="Shutdown", size_hint=(None, None), size=(200, 50))
        shutdown_button.bind(on_press=lambda instance: self.shutdown())
        popup_content.add_widget(restart_button)
        popup_content.add_widget(shutdown_button)
        popup.open()
        Clock.schedule_once(lambda dt: self.shutdown(), 3)

    def restart_game(self, popup):
        # Dismiss the popup and restart the game by returning to the start screen.
        popup.dismiss()
        print("Restarting game...")
        self.go_to_start_screen(None)

    def win_game(self):
        """
        (Optional) Handle level win.
        This function is not actively used since we call congratulations_screen.
        """
        print(f"Level {self.level} completed!")
        self.state = "win"
        self.layout.clear_widgets()
        self.continue_button = Button(
            text="Next Level",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.3}
        )
        self.layout.add_widget(self.continue_button)

    def congratulations_screen(self):
        """
        Show a congratulatory popup upon clearing a level.
        Provides an option to proceed to the next level.
        """
        print("Displaying Congratulations Screen")
        self.state = "congratulations"
        popup_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        popup_content.add_widget(Label(text="Congratulations! Click next to continue."))
        next_button = Button(text="Next", size_hint=(None, None), size=(200, 50))
        popup_content.add_widget(next_button)
        popup = Popup(
            title="Level Complete",
            content=popup_content,
            size_hint=(0.6, 0.4)
        )
        next_button.bind(on_press=lambda instance: self.next_level(popup))
        popup.open()

    def lose_game(self):
        """
        Alternate game over handler.
        Saves game data and then triggers the game over sequence.
        """
        print("Game Over!")
        self.state = "lose"
        try:
            with open("hall_of_fame.txt", "a") as f:
                f.write(f"{self.nickname}, Level: {self.level}\n")
        except IOError:
            print("Failed to save to Hall of Fame.")
        self.game_over()

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        """
        Handle keyboard events:
         - Spacebar: shoot a projectile.
         - Left/Right arrows: rotate the cannon.
         - Up/Down arrows: adjust the muzzle velocity.
        """
        print(f"Key pressed: {key}")
        if self.state.startswith("level_"):
            if key == 32:  # Spacebar to shoot.
                print("Shooting projectile")
                self.shoot_projectile()
            elif key == 276:  # Left arrow: rotate down.
                print("Rotating cannon down")
                self.cannon.rotate("down")
            elif key == 275:  # Right arrow: rotate up.
                print("Rotating cannon up")
                self.cannon.rotate("up")
            elif key == 273:  # Up arrow: increase velocity.
                self.velocity = min(self.velocity + 10, 100)
                print(f"Velocity increased to {self.velocity}")
            elif key == 274:  # Down arrow: decrease velocity.
                self.velocity = max(self.velocity - 10, 10)
                print(f"Velocity decreased to {self.velocity}")

    def shoot_projectile(self):
        """
        Launch a projectile from the cannon if there are shots remaining.
        Decrease the shot counter and add the projectile to the game.
        """
        if self.shots_left <= 0:
            print("No shots left! Game over.")
            self.game_over()
            return

        tip_position = self.cannon.get_tip_position()
        print(f"Launching projectile from {tip_position}")
        projectile = Projectile(
            projectile_type=self.selected_projectile,
            start_position=tip_position
        )
        projectile.launch(
            angle=self.cannon.get_angle(),
            power=self.velocity
        )
        self.projectiles.append(projectile)
        self.add_widget(projectile)
        self.shots_left -= 1
        print(f"Shots left: {self.shots_left}")
        if self.shots_left == 0:
            print("No shots remaining!")

# ---------------------------
# ScoreDisplay Class
# ---------------------------
class ScoreDisplay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configure layout for displaying the score.
        self.orientation = 'horizontal'  # Aligns elements in a row.
        self.size_hint = (None, None)  # Prevents automatic resizing.
        self.size = (200, 50)  # Sets the dimensions.
        self.pos_hint = {"x": 0, "y": 0.9}  # Positions near the top left.
        self.padding = [10, 5, 10, 5]  # Adds internal spacing.

        # Draws a semi-transparent black background.
        with self.canvas.before:
            Color(0, 0, 0, 0.5)  # RGBA values: Black with 50% transparency.
            self.bg = Rectangle(size=self.size, pos=self.pos)  # Background rectangle.

        # Create a label to display score and shots left.
        self.label = Label(
            text=f"Score: 0   Shots Left: 10",
            color=(1, 1, 1, 1),  # White text color.
        )
        self.add_widget(self.label)  # Add label to layout.

    def update_text(self, score, shots_left):
        """
        Update the score display with new values.
        - Updates the label text.
        - Ensures background size and position stay consistent.
        """
        self.label.text = f"Score: {score}   Shots Left: {shots_left}"
        self.bg.size = self.size
        self.bg.pos = self.pos

# ---------------------------
# CannonApp Class
# ---------------------------
class CannonApp(App):
    def build(self):
        """
        Initializes the game application and sets up the main game screen.
        - Creates an instance of CannonGame.
        - Sets the game screen size based on constants.
        - Binds keyboard inputs to game actions.
        """
        game = CannonGame()
        game.size = (const.SCREEN_WIDTH, const.SCREEN_HEIGHT)  # Set screen dimensions.
        from kivy.core.window import Window  # Import Window for keyboard binding.
        Window.bind(on_key_down=game.on_key_down)  # Bind keyboard events to the game.
        return game

if __name__ == "__main__":
    print("Starting Cannon Game...")
    CannonApp().run()  # Start the Kivy app.

