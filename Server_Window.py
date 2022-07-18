import tkinter as tk


root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=4, rowspan=4)

instructions = tk.Label(root, text="Add players names", font="Courier")
instructions.grid(column=0, row=0)

# player_one_label = tk.Label(root, text="Player 1: ", font="Courier")
# instructions.grid(column=0, row=1)
# player_two_label = tk.Label(root, text="Add players names", font="Courier")
# instructions.grid(column=0, row=2)

player_one_entry = tk.Entry(fg="black", bg="white", width=50)
player_one_entry.grid(columnspan=1, column=2, row=1)

player_two_entry = tk.Entry(fg="black", bg="white", width=50)
player_two_entry.grid(columnspan=1, column=2, row=2)


def finish_adding_players():
    print("finished adding names")
    player_one_name = player_one_entry.get()
    player_two_name = player_two_entry.get()


button_text = tk.StringVar()
button = tk.Button(root, textvariable=button_text, command=lambda: finish_adding_players(), font="Courier", bg="#0000FF"
                   , fg="white", height=2, width=15)
button_text.set("Done")
button.grid(column=3, row=3)




root.mainloop()
