ANIME_CHAR_SET = {
    "sonar_soft":  ["    .    ", "    o    ", "   (O)   ", "  (( ))  ", " ((( ))) ", "(((   )))", "((     ))", "(       )", "         "],
    "sonar_solid": ["    .    ", "    ▫    ", "   [□]   ", "  [[ ]]  ", " [[[ ]]] ", "[[[   ]]]", "[[     ]]", "[       ]", "         " ],
    "dots":  ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
}


class Anime:
    def __init__(self, char_set="dots"):
        self.char_set = char_set
        self.char_index = 0
        self.current_char = ANIME_CHAR_SET[char_set][0]

    def update(self):
        anim_chars = ANIME_CHAR_SET[self.char_set]
        self.current_char = anim_chars[self.char_index]
        self.char_index = (self.char_index + 1) % len(anim_chars)
        return self.current_char

    def get_current_char(self):
        return self.current_char
