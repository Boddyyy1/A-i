import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

image_path = "assets"

def create_domino_set():
    return [(i, j) for i in range(7) for j in range(i, 7)]

def distribute_tiles(domino_set):
    random.shuffle(domino_set)
    player1 = domino_set[:7]
    player2 = domino_set[7:14]
    remaining = domino_set[14:]
    return player1, player2, remaining

class DominoGame:
    def __init__(self, root):  # تغيير هنا
        self.root = root
        self.root.title("Domino Game")
        self.root.geometry("1000x600")
        self.root.config(bg="#2c3e50")

        self.domino_set = create_domino_set()
        self.player1_tiles, self.player2_tiles, self.remaining_tiles = distribute_tiles(self.domino_set)
        self.table_tiles = []
        self.current_player = 1

        self.domino_images = self.load_domino_images()

        self.board_frame = tk.Frame(root, bg="#27ae60", width=800, height=300, relief=tk.SUNKEN, bd=5)
        self.board_frame.pack(pady=20, expand=True, fill=tk.BOTH)

        self.player_label = tk.Label(root, text="Your Tiles:", font=("Arial", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.player_label.pack()

        self.tiles_frame = tk.Frame(root, bg="#34495e")
        self.tiles_frame.pack(pady=10)

        self.info_frame = tk.Frame(root, bg="#2c3e50")
        self.info_frame.pack(pady=10)

        self.remaining_label = tk.Label(self.info_frame, text="Remaining Tiles: 0", font=("Arial", 14), bg="#2c3e50", fg="#ecf0f1")
        self.remaining_label.grid(row=0, column=0, padx=10)

        self.draw_button = tk.Button(self.info_frame, text="Draw Tile", font=("Arial", 12, "bold"), bg="#e67e22", fg="white", command=self.draw_tile)
        self.draw_button.grid(row=0, column=1, padx=10)

        self.end_turn_button = tk.Button(self.info_frame, text="End Turn", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", command=self.end_turn)
        self.end_turn_button.grid(row=0, column=2, padx=10)

        self.turn_label = tk.Label(root, text="Player 1's Turn", font=("Arial", 14, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.turn_label.pack()

        self.update_ui()

    def load_domino_images(self):
        images = {}
        for i in range(7):
            for j in range(i, 7):
                path = f"{image_path}/{i}-{j}.png"
                if not os.path.exists(path):
                    print(f"Image not found: {path}")
                    continue
                image = Image.open(path)
                image = image.resize((60, 120), Image.Resampling.LANCZOS)
                images[(i, j)] = ImageTk.PhotoImage(image)
        return images

    def update_ui(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for tile in self.table_tiles:
            tile_image = self.domino_images[tile]
            label = tk.Label(self.board_frame, image=tile_image, bg="#27ae60")
            label.pack(side=tk.LEFT, padx=5)

        for widget in self.tiles_frame.winfo_children():
            widget.destroy()

        if self.current_player == 1:
            player_tiles = self.player1_tiles
        else:
            player_tiles = self.player2_tiles

        for idx, tile in enumerate(player_tiles):
            tile_image = self.domino_images[tile]
            btn = tk.Button(self.tiles_frame, image=tile_image, bg="#34495e", command=lambda i=idx: self.play_tile(i))
            btn.pack(side=tk.LEFT, padx=5)

        self.remaining_label.config(text=f"Remaining Tiles: {len(self.remaining_tiles)}")
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def is_valid_play(self, tile):
        return not self.table_tiles or tile[0] == self.table_tiles[-1][1] or tile[1] == self.table_tiles[0][0]

    def play_tile(self, idx):
        if self.current_player == 1:
            tile = self.player1_tiles[idx]
        else:
            tile = self.player2_tiles[idx]

        if self.is_valid_play(tile):
            if self.current_player == 1:
                self.player1_tiles.pop(idx)
            else:
                self.player2_tiles.pop(idx)

            if not self.table_tiles or tile[0] == self.table_tiles[-1][1]:
                self.table_tiles.append(tile)
            else:
                self.table_tiles.insert(0, tile)

            self.check_win()
        else:
            messagebox.showerror("Invalid Move", "You can only play a tile that matches the board!")

        self.update_ui()

    def draw_tile(self):
        if self.remaining_tiles:
            tile = self.remaining_tiles.pop(0)
            if self.current_player == 1:
                self.player1_tiles.append(tile)
            else:
                self.player2_tiles.append(tile)
            self.update_ui()
        else:
            messagebox.showinfo("No Tiles Left", "No tiles left to draw!")

    def end_turn(self):
        self.current_player = 1 if self.current_player == 2 else 2
        self.update_ui()
        messagebox.showinfo("Next Turn", f"Player {self.current_player}, it's your turn!")

    def check_win(self):
        if not self.player1_tiles:
            messagebox.showinfo("Game Over", "Player 1 wins!")
            self.root.destroy()
        elif not self.player2_tiles:
            messagebox.showinfo("Game Over", "Player 2 wins!")
            self.root.destroy()
        else:
            self.check_game_over()

    def check_game_over(self):
        if not self.remaining_tiles and not any(self.is_valid_play(tile) for tile in self.player1_tiles + self.player2_tiles):
            messagebox.showinfo("Game Over", "No valid moves left. Game ends in a draw!")
            self.root.destroy()

if __name__ == "__main__":  # تغيير هنا
    root = tk.Tk()
    game = DominoGame(root)
    root.mainloop()
