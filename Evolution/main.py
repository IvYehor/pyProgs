from tkinter import *
import math, random

root = Tk()
root.title("Test")

class Bot:
    def __init__(self, start_x, start_y, start_rot, start_commands, start_herbivore_level):
        self.pos = [start_x, start_y]
        self.rot = start_rot
        self.health = 100
        self.herbivore_level = start_herbivore_level
        self.commands = start_commands
        self.pointer = 0
        self.is_alife = True
        field[self.pos[1]][self.pos[0]] = 4
    def description(self):
        print("******************")
        print("* Pos: ", self.pos)
        print("* Rot: ", self.rot)
        print("* Commands: ", self.commands)
        print("* Pointer: ", self.pointer)
        print("* Health: ", self.health)
        print("* Alife: ", self.is_alife)
        print("******************")
        print()
    def draw(self):
        if self.is_alife:
            canv.create_rectangle(self.pos[0]*w, self.pos[1]*h, (self.pos[0]+1)*w, (self.pos[1]+1)*h, fill="blue", width = 0)
            if self.rot == 0:
                canv.create_line(self.pos[0]*w, self.pos[1]*h, (self.pos[0]+1)*w, self.pos[1]*h, fill='lightblue', width=3)
            elif self.rot == 1:
                canv.create_line((self.pos[0]+1)*w, self.pos[1]*h, (self.pos[0]+1)*w, (self.pos[1]+1)*h, fill='lightblue', width=3)
            elif self.rot == 2:
                canv.create_line(self.pos[0]*w, (self.pos[1]+1)*h, (self.pos[0]+1)*w, (self.pos[1]+1)*h, fill='lightblue', width=3)
            elif self.rot == 3:
                canv.create_line(self.pos[0]*w, self.pos[1]*h, self.pos[0]*w, (self.pos[1]+1)*h, fill='lightblue', width=3)
    def update(self):
        if self.health <= 0 and self.is_alife:
            self.is_alife = False
            field[self.pos[1]][self.pos[0]] = 3
            return
        if not self.is_alife:
            return
        havedone = False
        while not havedone:
            #print("Command ", self.pointer, ": ", self.commands[self.pointer], "   ", self.pos)
            if self.commands[self.pointer] == 0:  # Move forward
                newpos = [self.pos[0], self.pos[1]]
                if self.rot == 0:  # Up
                    newpos[1] -= 1
                    if newpos[1] < 0:
                        newpos[1] = s - 1
                elif self.rot == 1:  # Right
                    newpos[0] += 1
                    if newpos[0] >= s:
                        newpos[0] = 0
                elif self.rot == 2:  # Down
                    newpos[1] += 1
                    if newpos[1] >= s:
                        newpos[1] = 0
                else:  # Left
                    newpos[0] -= 1
                    if newpos[0] < 0:
                        newpos[0] = s - 1
                if field[newpos[1]][newpos[0]] == 0:
                    field[self.pos[1]][self.pos[0]] = 0
                    field[newpos[1]][newpos[0]] = 4
                    self.pos = [newpos[0], newpos[1]]
                    self.pointer += 1
                else:
                    self.pointer += field[newpos[1]][newpos[0]] + 1
                havedone = True
            elif self.commands[self.pointer] == 1:  # Rotate clockwise
                self.rot += 1
                if self.rot > 3:
                    self.rot = 0
                self.pointer += 1
                havedone = True
            elif self.commands[self.pointer] == 2:  # Rotate counterclockwise
                self.rot -= 1
                if self.rot < 0:
                    self.rot = 3
                self.pointer += 1
                havedone = True
            elif self.commands[self.pointer] == 3:  # Look forward
                if self.rot == 0:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] - 1) + 1
                elif self.rot == 1:
                    self.pointer += look_at_pos(self.pos[0] + 1, self.pos[1]) + 1
                elif self.rot == 2:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] + 1) + 1
                elif self.rot == 3:
                    self.pointer += look_at_pos(self.pos[0] - 1, self.pos[1]) + 1
            elif self.commands[self.pointer] == 4:  # Look right
                if self.rot == 3:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] - 1) + 1
                elif self.rot == 0:
                    self.pointer += look_at_pos(self.pos[0] + 1, self.pos[1]) + 1
                elif self.rot == 1:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] + 1) + 1
                elif self.rot == 2:
                    self.pointer += look_at_pos(self.pos[0] - 1, self.pos[1]) + 1
            elif self.commands[self.pointer] == 5:  # Look backward
                if self.rot == 2:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] - 1) + 1
                elif self.rot == 3:
                    self.pointer += look_at_pos(self.pos[0] + 1, self.pos[1]) + 1
                elif self.rot == 0:
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] + 1) + 1
                elif self.rot == 1:
                    self.pointer += look_at_pos(self.pos[0] - 1, self.pos[1]) + 1
            elif self.commands[self.pointer] == 6:  # Look left
                if self.rot == 1:  # Up
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] - 1) + 1
                elif self.rot == 2:  # Right
                    self.pointer += look_at_pos(self.pos[0] + 1, self.pos[1]) + 1
                elif self.rot == 3:  # Down
                    self.pointer += look_at_pos(self.pos[0], self.pos[1] + 1) + 1
                elif self.rot == 0:  # Left
                    self.pointer += look_at_pos(self.pos[0] - 1, self.pos[1]) + 1
            elif self.commands[self.pointer] == 7:  # Eat food
                # pointer + 1 if food
                # pointer + 2 if wall, space
                # pointer + 3 if poison
                # pointer + 4 if bot
                if self.rot == 0:  # Up
                    if look_at_pos(self.pos[0], self.pos[1] - 1) == 2:
                        self.health += math.floor((self.herbivore_level + 100) * 0.1 / 2)
                        field[self.pos[1] - 1][self.pos[0]] = 0
                        self.pointer += 1
                        self.herbivore_level += 10
                    elif look_at_pos(self.pos[0], self.pos[1] - 1) == 3:
                        self.health -= 20
                        field[self.pos[1] - 1][self.pos[0]] = 0
                        self.pointer += 3
                    elif look_at_pos(self.pos[0], self.pos[1] - 1) == 4:
                        for i in range(len(bots)):
                            if bots[i].pos == [self.pos[0], self.pos[1] - 1]:
                                self.health +=  math.floor(bots[i].health * (1 - self.herbivore_level/100) * 0.5)
                                bots[i].is_alife = False
                                bots[i].health = 0
                                field[self.pos[1] - 1][self.pos[0]] = 0
                                self.pointer += 4
                                self.herbivore_level -= 10
                    else:
                        self.pointer += 2
                elif self.rot == 1:  # Right
                    if look_at_pos(self.pos[0] + 1, self.pos[1]) == 2:
                        self.health += math.floor((self.herbivore_level + 100) * 0.1 / 2)
                        field[self.pos[1]][self.pos[0] + 1] = 0
                        self.pointer += 1
                        self.herbivore_level += 10
                    elif look_at_pos(self.pos[0] + 1, self.pos[1]) == 3:
                        self.health -= 20
                        field[self.pos[1]][self.pos[0] + 1] = 0
                        self.pointer += 3
                    elif look_at_pos(self.pos[0] + 1, self.pos[1]) == 4:
                        for i in range(len(bots)):
                            if bots[i].pos == [self.pos[0] + 1, self.pos[1]]:
                                self.health +=  math.floor(bots[i].health * (1 - self.herbivore_level/100) * 0.5)
                                bots[i].is_alife = False
                                bots[i].health = 0
                                field[self.pos[1]][self.pos[0] + 1] = 0
                                self.pointer += 4
                                self.herbivore_level -= 10
                    else:
                        self.pointer += 2
                elif self.rot == 2:  # Down
                    if look_at_pos(self.pos[0], self.pos[1] + 1) == 2:
                        self.health += math.floor((self.herbivore_level + 100) * 0.1 / 2)
                        field[self.pos[1] + 1][self.pos[0]] = 0
                        self.pointer += 1
                        self.herbivore_level += 10
                    elif look_at_pos(self.pos[0], self.pos[1] + 1) == 3:
                        self.health -= 20
                        field[self.pos[1] + 1][self.pos[0]] = 0
                        self.pointer += 3
                    elif look_at_pos(self.pos[0], self.pos[1] + 1) == 4:
                        for i in range(len(bots)):
                            if bots[i].pos == [self.pos[0], self.pos[1] + 1]:
                                self.health +=  math.floor(bots[i].health * (1 - self.herbivore_level/100) * 0.5)
                                bots[i].is_alife = False
                                bots[i].health = 0
                                field[self.pos[1] + 1][self.pos[0]] = 0
                                self.pointer += 4
                                self.herbivore_level -= 10
                    else:
                        self.pointer += 2
                elif self.rot == 3:  # Left
                    if look_at_pos(self.pos[0] - 1, self.pos[1]) == 2:
                        self.health += math.floor((self.herbivore_level + 100) * 0.1 / 2)
                        field[self.pos[1]][self.pos[0] - 1] = 0
                        self.pointer += 1
                        self.herbivore_level += 10
                    elif look_at_pos(self.pos[0] - 1, self.pos[1]) == 3:
                        self.health -= 20
                        field[self.pos[1]][self.pos[0] - 1] = 0
                        self.pointer += 3
                    elif look_at_pos(self.pos[0] - 1, self.pos[1]) == 4:
                        for i in range(len(bots)):
                            if bots[i].pos == [self.pos[0] - 1, self.pos[1]]:
                                self.health +=  math.floor(bots[i].health * (1 - self.herbivore_level/100) * 0.5)
                                bots[i].is_alife = False
                                bots[i].health = 0
                                field[self.pos[1]][self.pos[0] - 1] = 0
                                self.pointer += 4
                                self.herbivore_level -= 10
                    else:
                        self.pointer += 2
                havedone = True
            elif self.commands[self.pointer] == 8:  # Poison to food
                # pointer + 1 if poison
                # pointer + 2 if wall, food, space or bot
                if self.rot == 0:  # Up
                    if look_at_pos(self.pos[0], self.pos[1] - 1) == 3:
                        field[self.pos[1] - 1][self.pos[0]] = 2
                        self.pointer += 1
                    else:
                        self.pointer += 2
                elif self.rot == 1:  # Right
                    if look_at_pos(self.pos[0] + 1, self.pos[1]) == 3:
                        field[self.pos[1]][self.pos[0] + 1] = 2
                        self.pointer += 1
                    else:
                        self.pointer += 2
                elif self.rot == 2:  # Down
                    if look_at_pos(self.pos[0], self.pos[1] + 1) == 3:
                        field[self.pos[1] + 1][self.pos[0]] = 2
                        self.pointer += 1
                    else:
                        self.pointer += 2
                elif self.rot == 3:  # Left
                    if look_at_pos(self.pos[0] - 1, self.pos[1]) == 3:
                        field[self.pos[1]][self.pos[0] - 1] = 2
                        self.pointer += 1
                    else:
                        self.pointer += 2
                havedone = True
            else:
                self.pointer += self.commands[self.pointer]
            if self.herbivore_level > 100:
                self.herbivore_level = 100
            elif self.herbivore_level < -100:
                self.herbivore_level = -100
            if self.pointer >= len(self.commands):
                havedone = True
            self.pointer %= len(self.commands)
        if self.health > 100:
            self.health = 100
        self.health -= 1

s = 50
w, h = 10, 10
W, H = s * w, s * h
field = []
bots = []
tick = 0
generation = 0
gen_tick = 0
number_of_bots = 64
min_number_of_bots = 8
multiplier = 8
# 0 - space 1 - wall 2 - food 3 - poison 4 - bot
for i in range(s):
    line = [1]
    for j in range(s - 2):
        if i == 0 or i == s - 1:
            line.append(1)
        else:
            line.append(0)
    line.append(1)
    field.append(line)
tick = 0

def start():
    global bots
    bots = []
    for i in range(number_of_bots):
        x, y = random.randint(1, s - 2), random.randint(1, s - 2)
        for j in range(len(bots)):
            if bots[j].pos[0] != x or bots[j].pos[1] != y:
                break
            else:
                x, y = random.randint(1, s - 2), random.randint(1, s - 2)
        rot = random.randint(0, 3)
        commands = []
        for j in range(64):
            commands.append(random.randint(0, 63))
        print(x, ", ", y, "  ", commands)
        bots.append(Bot(x, y, rot, commands, random.randint(-100, 10)))
    #field[3][2] = 2
    #bots = [Bot(3, 3, 0, [7, 1, 2], 0)]
    #bots[0].commands = [3, 12, 1, 8, 8, 21, 17, 7, 4, 1, 11, 3, 30, 12, 7, 12, 1, 22, 23, 10, 45, 36, 6, 8, 0, 3, 49, 23, 61, 56, 10, 1, 10, 10, 55, 24, 4, 5, 37, 5, 11, 20, 40, 10, 58, 5, 1, 24, 0, 9, 32, 11, 20, 0, 40, 16, 22, 46, 54, 3, 0, 63, 7, 40]
    #bots[1].commands = [3, 12, 1, 8, 8, 21, 17, 7, 4, 1, 11, 3, 30, 12, 7, 12, 1, 22, 23, 10, 45, 36, 6, 8, 0, 3, 49, 23, 61, 56, 10, 1, 10, 10, 55, 24, 4, 5, 37, 5, 11, 20, 40, 10, 58, 5, 1, 24, 0, 9, 32, 11, 20, 0, 40, 16, 22, 46, 54, 3, 0, 63, 7, 40]
    #bots[1].herbivore_level = -100
    #bots[1].commands = [8, 1, 9, 2, 1, 8, 3, 7, 1, 0, 11, 13, 6, 6, 7, 10]
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                r = random.random()
                if r < 0.05:
                    field[i][j] = 2
                elif r < 0.1:
                    field[i][j] = 3
                elif r < 0.15:
                    field[i][j] = 1
    draw()

# 0 - move
# 1 - rotate clockwise
# 2 - rotate c-clockwise
# 3 - look forw.
# 4 - look right
# 5 - look back
# 6 - look left
# 7 - eat
# 8 - poison to food
#6, 9, 10, 1, 10, 1, 8\15 Rotate alg
#0, 15, 10, 11, 1, 11, 7, 9 Another alg
#1, 9,  10, 8, 10, 7, 15 poison to food
#[3, 12, 1, 8, 8, 21, 17, 7, 4, 1, 11, 3, 30, 12, 7, 12, 1, 22, 23, 10, 45, 36, 6, 8, 0, 3, 49, 23, 61, 56, 10, 1, 10, 10, 55, 24, 4, 5, 37, 5, 11, 20, 40, 10, 58, 5, 1, 24, 0, 9, 32, 11, 20, 0, 40, 16, 22, 46, 54, 3, 0, 63, 7, 40]
#[8, 6, 12, 3, 10, 7, 17, 12, 5, 4, 11, 1, 30, 12, 7, 12, 1, 22, 12, 5, 12, 4, 7, 2, 3, 12, 49, 23, 8, 6, 0, 1, 10, 5, 12, 0, 3, 1, 10, 5, 3, 20, 40, 10, 58, 4, 1, 3, 0, 11, 0, 11, 10, 0, 8, 9, 7, 11, 3, 12, 0, 63, 6, 0]
#[8, 1, 9, 2, 1, 8, 3, 7, 1, 0, 11, 13, 6, 6, 7, 10]
#[1, 8, 9, 0, 1, 8, 3, 7, 1, 0, 11, 13, 6, 6, 7, 10]

canv = Canvas(root, width = W, height = H)
canv.create_rectangle(0, 0, W, H, fill="white", width = 0)
canv.pack(side=LEFT)
healthbar = Label(root, text = "Hello")
healthbar.pack()
hlvbar = Label(root, text = "Hello2")
hlvbar.pack()
def draw():
    canv.delete('all')
    canv.create_rectangle(0, 0, W, H, fill="white", width = 0)
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 1:
                canv.create_rectangle(j * w, i * h, (j + 1) * w, (i + 1) * h, fill="black", width = 0)
            elif field[i][j] == 2:
                canv.create_rectangle(j * w, i * h, (j + 1) * w, (i + 1) * h, fill="red", width = 0)
            elif field[i][j] == 3:
                canv.create_rectangle(j * w, i * h, (j + 1) * w, (i + 1) * h, fill="green", width = 0)
            # elif field[i][j] == 4:
            #      offset = 4
            #      canv.create_rectangle(j * w-offset, i * h-offset, (j + 1) * w+offset, (i + 1) * h+offset, fill="#F0A7BC", width = 0)
    for i in range(len(bots)):
        bots[i].draw()

def look_at_pos(x, y):
    return field[y][x]
def new_gen():
    global bots, field, generation, gen_tick
    print("New gen")
    generation += 1
    gen_tick = 0
    field = []
    for i in range(s):
        line = [1]
        for j in range(s - 2):
            if i == 0 or i == s - 1:
                line.append(1)
            else:
                line.append(0)
        line.append(1)
        field.append(line)
    print()
    print("Bots (", len(bots), ")*************************************************************")
    for i in range(len(bots)):
        bots[i].description()
    new_bots = []
    for i in range(len(bots)):
        if bots[i].is_alife and bots[i].health > 0:
            new_bots.append(bots[i])
    print()
    print("Newbots (", len(new_bots), ")*************************************************************")
    for i in range(len(new_bots)):
        new_bots[i].description()
    new_bots2 = []
    for i in range(multiplier):
        for j in range(len(new_bots)):
            new_bots2.append(Bot(new_bots[j].pos[0], new_bots[j].pos[1], new_bots[j].rot, new_bots[j].commands[:], new_bots[j].herbivore_level))

    for i in range(len(new_bots2)):
        x, y = random.randint(1, s - 2), random.randint(1, s - 2)
        for j in range(len(new_bots2)):
            if new_bots2[j].pos[0] != x or new_bots2[j].pos[1] != y:
                break
            else:
                x, y = random.randint(1, s - 2), random.randint(1, s - 2)
        rot = random.randint(0, 3)
        field[new_bots2[i].pos[1]][new_bots2[i].pos[0]] = 0
        new_bots2[i].pos = [x, y]
        field[new_bots2[i].pos[1]][new_bots2[i].pos[0]] = 4
        new_bots2[i].rot = rot
        mut = random.random()
        if mut < 0.125:# math.floor(i/len(new_bots)) == len(new_bots)
            rand_index = random.randint(0, len(new_bots2[i].commands) - 1)
            new_bots2[i].commands[rand_index] = random.randint(0, 12)
    bots = new_bots2[:]

    print()
    print("Newbots2 (", len(new_bots2), ")*************************************************************")
    for i in range(len(new_bots2)):
        new_bots2[i].description()

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                r = random.random()
                if r < 0.05:
                    field[i][j] = 2
                elif r < 0.1:
                    field[i][j] = 3
                elif r < 0.15:
                    field[i][j] = 1

def update():
    for i in range(len(bots)):
        bots[i].update()
        number_of_alife_bots = 0
        for j in range(len(bots)):
            if bots[j].is_alife and bots[j].health > 0:
                number_of_alife_bots += 1
        if number_of_alife_bots <= min_number_of_bots:
            new_gen()
            return
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                r = random.random()
                if r < 0.00005:
                    field[i][j] = 2
                elif r >= 0.00005 and r < 0.0001:
                    field[i][j] = 3
start()
def main():
    global tick, gen_tick
    update()
    draw()
    tick+=1
    gen_tick+=1
    title = ""
    title2 = ""
    for i in range(len(bots)):
        title += "  " + str(bots[i].health)
        if i % 20 == 0:
            title += "\n"
        title2 += "  " + str(bots[i].herbivore_level)
        if i % 20 == 0:
            title2 += "\n"
    healthbar.configure(text = title)
    hlvbar.configure(text = title2)
    root.title(str(tick) + "  " + str(generation) + ": " + str(gen_tick))# + "     (" + str(pos[0]) + ", " + str(pos[1]) + ") " + str(rot) + "  " + str(health)
    root.after(1, main)

main()
root.mainloop()
