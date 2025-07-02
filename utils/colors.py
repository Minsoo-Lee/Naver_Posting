import random

class Colors:
    def __init__(self):
        self.color_map = {
            "text": [
                "white", "black", "red", "blue", "yellow", "green", "magenta", "cyan", "orange", "lime",
                "gold", "aqua", "pink", "chartreuse", "deeppink", "lightblue", "plum", "coral", "salmon", "orchid",
                "indigo", "hotpink", "greenyellow", "tomato", "wheat", "seagreen", "lightcoral", "turquoise", "navy",
                "crimson",
                "khaki", "violet", "skyblue", "forestgreen", "darkorange", "cadetblue", "rosybrown", "darkturquoise",
                "steelblue", "slateblue",
                "palegreen", "springgreen", "lemonchiffon", "lightseagreen", "dodgerblue", "darkseagreen", "lightskyblue",
                "sienna", "mediumorchid", "peru",
                "mediumseagreen", "lavender", "moccasin", "honeydew", "antiquewhite", "thistle", "aliceblue", "burlywood",
                "azure", "bisque",
                "blanchedalmond", "cornsilk", "gainsboro", "ghostwhite", "ivory", "linen", "mintcream", "oldlace",
                "seashell", "snow",
                "whitesmoke", "beige", "darkkhaki", "darkgoldenrod", "firebrick", "darkred", "darkblue", "darkgreen",
                "darkmagenta", "darkslateblue",
                "mediumblue", "mediumvioletred", "saddlebrown", "mediumslateblue", "mediumspringgreen", "mediumturquoise",
                "midnightblue", "navajowhite", "olivedrab", "palevioletred",
                "peachpuff", "powderblue", "rebeccapurple", "slategray", "tan", "teal", "yellowgreen", "lightsteelblue",
                "darkcyan", "darkslategray"
            ],
            "bg": [
                "black", "white", "navy", "ivory", "midnightblue", "whitesmoke", "darkgreen", "lightyellow", "darkblue",
                "aliceblue",
                "maroon", "honeydew", "darkslategray", "beige", "purple", "oldlace", "saddlebrown", "azure", "brown",
                "mintcream",
                "blueviolet", "wheat", "indianred", "seashell", "chocolate", "floralwhite", "darkolivegreen", "cornsilk",
                "firebrick", "linen",
                "lightcoral", "lavenderblush", "orangered", "papayawhip", "teal", "lemonchiffon", "indigo",
                "blanchedalmond", "navy", "bisque",
                "dimgray", "moccasin", "gray", "burlywood", "olive", "wheat", "lightgray", "tan", "slategray",
                "antiquewhite",
                "darkcyan", "gainsboro", "black", "linen", "darkslategray", "oldlace", "gray", "snow", "maroon",
                "mintcream",
                "blue", "white", "orange", "ivory", "brown", "beige", "navy", "ghostwhite", "gold", "floralwhite",
                "purple", "seashell", "olive", "azure", "teal", "cornsilk", "red", "papayawhip", "darkgreen",
                "lemonchiffon",
                "crimson", "blanchedalmond", "lime", "burlywood", "maroon", "wheat", "darkred", "tan", "black",
                "antiquewhite",
                "forestgreen", "gainsboro", "chocolate", "linen", "slateblue", "oldlace", "cyan", "snow", "deeppink",
                "mintcream"
            ]
            # "text": [
            #     "white",
            #     "black",
            #     "white",
            #     "black",
            #     "lime",
            #     "white",
            #     "white",
            #     "white",
            #     "dimgray",
            #     "yellow"
            # ],
            # "bg": [
            #     "black",
            #     "white",
            #     "midnightblue",
            #     "yellow",
            #     "dimgray",
            #     "darkgreen",
            #     "orangered",
            #     "indigo",
            #     "whitesmoke",
            #     "navy"
            # ]
        }

    def get_random_colors(self):
        index = random.randint(0, 100)
        return self.color_map["bg"][index], self.color_map["text"][index]

    def get_color(self, index):
        return self.color_map["bg"][index], self.color_map["text"][index]
