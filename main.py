from rembg import remove
import os
import shutil
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont


class Player:
    def __init__(self, team, player, background, name, position_player, gray_shade, back_void):
        self.back_void = back_void
        self.name = name.strip()
        self.image_player = Image.open(f"player/{player}")
        self.background = Image.open(f"background/{background}")
        self.gray_shade = gray_shade
        self.team = Image.open(f"teams/{team}")
        self.position_player = position_player

    def resize_image(self, image_resized, x):
        height_bk = self.background.height
        size_image_resized = image_resized.size
        x = (height_bk / x) / size_image_resized[1]
        size_image_resized = (int(size_image_resized[0] * x), int(size_image_resized[1] * x))
        return image_resized.resize(size_image_resized)

    # Formatando o tamanho das imagens
    def processing_image(self):
        player = self.resize_image(self.image_player, 2)
        self.team = self.resize_image(self.team, 3)

        # Tirando o plano de fundo da imagem
        if not self.back_void:
            os.remove("image_png\\player.png")
            player = remove(player)
            player.save("player.png")
            shutil.move("player.png", "image_png")
            player = Image.open("image_png\\player.png")

        player = fit_size(player)
        self.team = fit_size(self.team)

        # Colocando o player
        width_bk, height_bk = self.background.size
        height_bk = int((height_bk - player.height) / 2)
        width_bk = int((width_bk - player.width) / 2)
        mvp_player = self.background.copy()
        mvp_player.paste(self.team, (0, 0), self.team,)
        if not self.back_void:
            mvp_player.paste(player, (width_bk, height_bk), player)
        else:
            mvp_player.paste(player, (width_bk, height_bk))

        # Colocando o nome
        font1 = ImageFont.truetype("fonts\\open_sans\\static\\OpenSans_Condensed-Bold.ttf", 150)
        font2 = ImageFont.truetype("fonts\\open_sans\\static\\OpenSans_Condensed-Bold.ttf", 75)
        draw = ImageDraw.Draw(mvp_player)
        text_width = draw.textlength(self.name, font=font1)
        text_height = height_bk + player.height
        draw.text(
            (int((mvp_player.width - text_width) / 2),
             text_height),
            text=str(self.name),
            font=font1,
            fill="black"
        )
        draw.text(
            (int((mvp_player.width - text_width) / 2),
             text_height + 20),
            text=str(self.position_player),
            font=font2,
            fill="black"
        )
        if self.gray_shade:
            mvp_player = mvp_player.convert("L")
        mvp_player.save(f"final_image/{self.name} ({len(os.listdir("final_image")) + 1}).jpg")


def fit_size(image_png):
    image_png = image_png.convert("RGBA")
    bbox = image_png.getbbox()
    return image_png.crop(bbox)


# Interface
def list_file(path_file):
    all_files = os.listdir(path_file)
    return all_files


def submmit_choices():
    jogador = Player(
        team=teams_dpd.get(),
        player=players_dpd.get(),
        background=background_dpd.get(),
        back_void=bool(back_void_value.get()),
        name=name_box.get(),
        gray_shade=bool(gray_value.get()),
        position_player=position_box
    )
    jogador.processing_image()


# Inicializa a janela principal
windows = Tk()
teams_list = list_file("teams")
teams_label = Label(windows, text="Selecione o time")
teams_label.grid(column=0, row=0, padx=10)
teams_dpd = ttk.Combobox(windows, values=teams_list)
teams_dpd.grid(column=0, row=1, padx=10)

players_list = list_file("player")
players_label = Label(windows, text="Selecione o jogador")
players_label.grid(column=2, row=0, padx=10)
players_dpd = ttk.Combobox(windows, values=players_list)
players_dpd.grid(column=2, row=1, padx=10)

background_list = list_file("background")
background_label = Label(windows, text="Selecione o fundo")
background_label.grid(column=1, row=0, padx=10)
background_dpd = ttk.Combobox(windows, values=background_list)
background_dpd.grid(column=1, row=1, padx=10)

back_void_value = IntVar()
back_void_choice = ttk.Checkbutton(windows, text="Deseja manter o fundo do jogador?", variable=back_void_value)
back_void_choice.grid(column=2, row=2, padx=10)

gray_value = IntVar()
shades_gray = ttk.Checkbutton(windows, text="Deseja colocar tudo em tons de cinza?", variable=gray_value)
shades_gray.grid(column=0, row=5, padx=10)

name_box_label = Label(windows, text="Insira o nome do Jogador")
name_box_label.grid(column=0, row=3)
name_box = Entry(width=25)
name_box.grid(column=0, row=4)

position_box_label = Label(windows, text="Insira a posição do Jogador")
position_box_label.grid(column=1, row=3)
position_box = Entry(width=25)
position_box.grid(column=1, row=4)

generet_buttom = Button(windows, text="Gerar Imagem", command=submmit_choices)
generet_buttom.grid(column=2, row=5, padx=10, pady=10)
windows.mainloop()
