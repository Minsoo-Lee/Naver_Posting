import random

class Colors:
    def __init__(self):
        self.color_map = {
            "text": [
                "white",
                "black",
                "white",
                "black",
                "lime",
                "white",
                "white",
                "white",
                "dimgray",
                "yellow"
            ],
            "bg": [
                "black",
                "white",
                "midnightblue",
                "yellow",
                "dimgray",
                "darkgreen",
                "orangered",
                "indigo",
                "whitesmoke",
                "navy"
            ]
        }

    def get_colors(self):
        index = random.randint(0, 9)
        return self.color_map["bg"][index], self.color_map["text"][index]
