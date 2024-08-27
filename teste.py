import customtkinter as ctk
import tkinter as tk


# Função para ocultar e mostrar a Listbox
def toggle_listbox():
    if listbox_frame.winfo_ismapped():
        listbox_frame.grid_forget()  # Oculta o frame que contém a Listbox
    else:
        listbox_frame.grid(row=1, column=0, padx=10, pady=10)  # Mostra o frame que contém a Listbox


def new_listbox():
    name_listbox = tk.Listbox(janela)
    name_listbox.pack()
    for item in ["Item 1", "Item 2", "Item 3"]:
        name_listbox.insert(tk.END, item)
    return name_listbox


# Inicializa a janela principal
janela = ctk.CTk()
janela.geometry("400x400")
teams_list = new_listbox()
toggle_button = ctk.CTkButton(janela, text="Toggle Listbox", command=toggle_listbox)
toggle_button.grid(row=0, column=0, padx=10, pady=10)


# Inicia a aplicação
janela.mainloop()
