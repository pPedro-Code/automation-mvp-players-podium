from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import os
import shutil


class Player:
    def __init__(self, team, name, back_void=False):
        self.team = team
        self.name = name
        self.back_void = back_void
        image_format = "png" if back_void else "jpg"
        self.image_player = Image.open(f"player\\{self.name}.{image_format}")

    def processing_image(self):
        player = ''
        size_player = self.image_player.size
        if size_player[0] != 576:
            x = 576 / size_player[0]
            size_player = (int(size_player[0] * x), int(size_player[1] * x))
            player = self.image_player.resize(size_player)

        if not self.back_void:
            os.remove("image_png\\player.png")
            player = remove(player)
            player.save("player.png")
            shutil.move("player.png", "image_png")
            player = Image.open("image_png\\player.png")

        background = Image.open("background\\background_br.jpg").copy()
        team = Image.open(f"teams\\{self.team}.png")
        mvp_player = background
        mvp_player.paste(team, (0, 0), team)
        mvp_player.paste(player, (258, 108), player)

        font = ImageFont.truetype("fonts\\open_sans\\static\\OpenSans_Condensed-Bold.ttf", 150)
        draw = ImageDraw.Draw(mvp_player)
        draw.text((257, 790), text=self.name, font=font)
        mvp_player.save("dor.jpg")


jogador = Player("bahia", "GOKU", back_void=False)
jogador.processing_image()
