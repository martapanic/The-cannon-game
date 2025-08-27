from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import cannon_constants as const

class GameInterface(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for the game interface
        self.layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # UI Elements: Labels for displaying score and shots left
        self.score_label = Label(text="Score: 0", size_hint=(1, 0.1))
        self.shots_label = Label(text="Shots Left: 10", size_hint=(1, 0.1))

        # Background setup: An image that fills the entire screen
        self.background = Image(source="", size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)  # Add background to the widget

        # Buttons for gameplay interactions
        self.start_button = Button(text="Start Game", size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_game)  # Bind start button to function

        self.help_button = Button(text="Help", size_hint=(1, 0.1))
        self.help_button.bind(on_press=self.show_help)  # Bind help button to function

        self.hall_of_fame_button = Button(text="Hall of Fame", size_hint=(1, 0.1))
        self.hall_of_fame_button.bind(on_press=self.show_hall_of_fame)  # Bind hall of fame button to function

        # Adding UI elements to the main layout
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.shots_label)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.help_button)
        self.layout.add_widget(self.hall_of_fame_button)

        # Add the layout to the main widget
        self.add_widget(self.layout)

        # Adding a solid color background behind the game elements
        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)  # Set background to dark grey
            self.bg = Rectangle(pos=self.pos, size=self.size)  # Create a background rectangle

    def update_background(self, source):
        """
        Update the background image of the game interface.
        """
        self.background.source = source

    def update_score(self, score):
        """
        Update the displayed score in the UI.
        """
        self.score_label.text = f"Score: {score}"

    def update_shots(self, shots_left):
        """
        Update the displayed shots left in the UI.
        """
        self.shots_label.text = f"Shots Left: {shots_left}"

    def start_game(self, instance):
        """
        Placeholder function for handling game start logic.
        """
        print("Start Game pressed")

    def show_help(self, instance):
        """
        Placeholder function for displaying help information.
        """
        print("Help button pressed")

    def show_hall_of_fame(self, instance):
        """
        Placeholder function for displaying the hall of fame.
        """
        print("Hall of Fame button pressed")


