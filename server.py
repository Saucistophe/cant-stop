import random
from itertools import permutations
from random import randrange

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, computed_field, Field
import ast

app = FastAPI()

class Move(BaseModel):
    combination: list[int] = Field(default_factory=list)
    player_name: str = Field(default_factory=str)

class Player(BaseModel):
    name: str = Field(default_factory=str)
    markers: dict[int, int] = Field(default_factory=dict)
    hooks: dict[int, int] = Field(default_factory=dict)

def get_chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst) - len(lst) % n, n)]

class Game(BaseModel):
    dice: list[int] = Field(default_factory=lambda: [6, 6, 6, 6])
    allowed_dice_merge: int = 2
    max_markers: int = 3
    current_dice: list[int] = Field(default_factory=list)
    players: list[Player] = Field(default_factory=list)
    rows: dict[int, int] = Field(default_factory=dict)
    current_player_idx: int = None

    @computed_field(return_type=Player)
    @property
    def current_player(self):
        if self.current_player_idx is None or not self.players:
            return ""
        return self.players[self.current_player_idx]

    @computed_field(return_type=list[list[int]])
    @property
    def possible_moves(self):
        candidate_moves = []
        combinations = self.combinations()
        for combination in combinations:
            candidate_move = []
            for v in combination:
                if len(self.current_player.markers) >= self.max_markers and v not in self.current_player.markers.keys():
                    continue
                if any(p.hooks.get(v) == self.rows.get(v) for p in self.players if v in p.hooks):
                    continue

                candidate_move.append(v)

            # zero left => bail out
            if len(candidate_move) == 0:
                continue
            candidate_moves.append(candidate_move)
        return candidate_moves

    def combinations(self):
        all_permutations = list(set(permutations(self.current_dice)))
        all_chunks = [get_chunks(p, self.allowed_dice_merge) for p in all_permutations]

        values = [sorted([sum(v) for v in c]) for c in all_chunks]
        result = []
        for elem in values:
            if elem not in result:
                result.append(elem)
        return sorted(result)

    def load(self):
        with open("sample.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        self.rows = {}
        self.dice = [6, 6, 6, 6]
        self.current_dice = []
        self.players = []

        for line in lines:
            if line.startswith("dice:"):
                self.dice = ast.literal_eval(line.split(":", 1)[1].strip())
            elif line.startswith("current_dice:"):
                self.current_dice = ast.literal_eval(line.split(":", 1)[1].strip())
            elif line.startswith("players:"):
                self.players = [Player(name=n) for n in ast.literal_eval(line.split(":", 1)[1].strip())]
            elif line.startswith("allowed_dice_merge:"):
                self.allowed_dice_merge = int(line.split(":", 1)[1].strip())
            elif line.startswith("max_markers:"):
                self.max_markers = int(line.split(":", 1)[1].strip())

            elif line.startswith("current_player:"):
                # current_player: None or name
                value = line.split(":", 1)[1].strip()
                if value == "None":
                    self.current_player_idx = None
                else:
                    self.current_player_idx = self.players.index(value)

            else:
                # board lines: "2 XXX"
                parts = line.split()
                if len(parts) == 2:
                    row = int(parts[0])
                    xs = parts[1]
                    self.rows[row] = len(xs)

        # If no current player → pick random
        if self.current_player_idx is None:
            self.current_player_idx = random.randint(0, len(self.players) - 1)
        self.roll_dice()

    def roll_dice(self):
        self.current_dice = [randrange(1, d + 1) for d in self.dice]

    def apply_move(self, move: Move):
        if move.player_name != self.current_player:
            raise ValueError(f"It's not {move.player_name}'s turn")
        if sorted(move.combination) not in self.combinations:
            raise ValueError(f"Combination {move.combination} not allowed")



        # Switch turn
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.roll_dice()

game = Game()
game.load()


@app.get("/game")
def get_game():
    return game


@app.post("/move")
def post_move(move: Move):
    try:
        game.apply_move(move)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return game
