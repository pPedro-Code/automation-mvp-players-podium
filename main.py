from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import os
import shutil


class Player:
    def __init__(self, team, name, background, back_void=False):
        self.back_void = back_void
        self.name = name
        self.image_player = Image.open(self.read_file(name, "player"))
        self.background = Image.open(self.read_file(background, "background"))
        self.team = Image.open(self.read_file(team, "teams"))

    @staticmethod
    def read_file(name_file, path_file):
        all_files = os.listdir(path_file)
        for file in all_files:
            name, extend = os.path.splitext(file)
            if name == name_file:
                return f"{path_file}/{name}{extend}"

    # Formatando o tamanho das imagens
    def processing_image(self):
        size_player = self.image_player.size
        x = 576 / size_player[0]
        size_player = (int(size_player[0] * x), int(size_player[1] * x))
        player = self.image_player.resize(size_player)

        # Tirando o plano de fundo da imagem
        if not self.back_void:
            os.remove("image_png\\player.png")
            player = remove(player)
            player.save("player.png")
            shutil.move("player.png", "image_png")
            player = Image.open("image_png\\player.png")

        #
        mvp_player = self.background
        mvp_player.paste(self.team, (0, 0), self.team)
        mvp_player.paste(player, (258, 108), player)

        font = ImageFont.truetype("fonts\\open_sans\\static\\OpenSans_Condensed-Bold.ttf", 150)
        draw = ImageDraw.Draw(mvp_player)
        draw.text((257, 790), text=self.name, font=font)
        mvp_player.save("final_image/dor.jpg")


jogador = Player("bahia", "GOKU", "background", back_void=False)
jogador.processing_image()
