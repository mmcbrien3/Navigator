import random, pygame
import Bank, Obstruction

water_line = pygame.image.load("Images/water_line.bmp")
bank = pygame.image.load("Images/bank.bmp")
bank_width = 4
class PathGenerator(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.water_positions = []
        self.left_banks = []
        self.right_banks = []
        self.obstructions = []
        self.score_at_last_obstruction = 0
        self.max_shift = 5

        for i in range(height):
            self.water_positions.append(width/4)
            self.left_banks.append(Bank.Bank(width/4 - bank_width, height - i - 1))
            self.right_banks.append(Bank.Bank(width/4 + width/2, height - i - 1))

    def get_next_water_position(self):
        self.water_positions.pop(0)

        last_pos = self.water_positions[-1]
        next_pos = random.randint(-5, 5) + last_pos
        while next_pos < 0 or next_pos > self.width / 2:
            next_pos = random.randint(-5, 5) + last_pos
        self.water_positions.append(next_pos)
        self.update_banks()

    def update_banks(self):
        self.left_banks.pop(0)
        self.right_banks.pop(0)
        self.left_banks.append(
            Bank.Bank(self.water_positions[len(self.water_positions) - 1] - bank_width, -1)
        )
        self.right_banks.append(
            Bank.Bank(self.water_positions[len(self.water_positions) - 1] + self.width/2, -1)
        )

        for i in range(len(self.left_banks) - 1):
            self.left_banks[i].rect.y += 1
            self.right_banks[i].rect.y += 1

    def get_next_obstruction(self):
        x = self.water_positions[-1] + random.randint(0, int(self.width/2 - 64))
        self.obstructions.append(Obstruction.Obstruction(x, 0))

    def update_obstructions(self, score):
        for o in self.obstructions:
            o.rect.y += 1

        if len(self.obstructions) > 0 and self.obstructions[0].rect.y > self.height:
            self.obstructions.pop(0)

        if score - self.score_at_last_obstruction > 100:
            self.get_next_obstruction()
            self.score_at_last_obstruction = score

