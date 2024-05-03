# usefull functions
def is_int(string: str) -> bool:
    if len(string) == 1:
        return string.isdigit()
    if string[0] == "-":
        return string[1:].isdigit()
    return string.isdigit()

def is_float(string: str) -> bool:
    string = string.replace(".", "", 1)
    if len(string) == 1:
        return string.isdigit()
    if string[0] == "-":
        return string[1:].isdigit()
    return string.isdigit()

# extracting data
with open("target file.txt", "r") as file:
    code = file.read().splitlines()
    file.close()

# extracting indent map
indent_map = [""]
for line in code:
    for char in line:
        if char == " ":
            indent_map[-1] += char
        else:
            break
    indent_map.append("")

# seperating words
temp = []
for line in code:
    temp.append(line.split())
code = temp
del temp

# opening output file and preparing
file = open("output.py", "w")
file.write(
    "import pygame as pg\nimport EPT\n\nassets={}\n\nwindow_width, window_height = 900, 500\nwindow=pg.display.set_mode((window_width, window_height))\nbackground = (255, 255, 255)\n\nclock = pg.time.Clock()\nfps=60\nrun = True\n\ntext_colour=(0, 0, 0)\n\n"
)
file.close()
file = open("output.py", "a")

vars_defined = []
skip_counter = 0

for line, indent in zip(code, indent_map):

    for i, word in enumerate(line):

        if skip_counter > 0:
            skip_counter -= 1
            continue

        elif word == "load":

            if len(line) > 2 and line[-3] == "size":
                file.write(indent+
                    f"assets.update(EPT.load_assets('{line[i+1]}', ({line[-2]}, {line[-1]})))\n"
                )

            else:
                file.write(indent+f"assets.update(EPT.load_assets('{line[i+1]}'))\n")

            skip_counter = len(line)

        elif word == "show":

            at_index = line.index("at")

            if "." in line[i+1]:
                file.write(indent+
                f"window.blit(assets['{line[i+1]}'], ({line[at_index+1]}, {line[at_index+2]}))\n"
            )
                
            else:

                try:
                    colour_index = line.index("colour")
                    colour = (int(line[colour_index+1]), int(line[colour_index+2]), int(line[colour_index+3]))
                
                except ValueError:
                    colour = 'text_colour'

                file.write(indent+
                    f"EPT.blit_text(window, '{" ".join(line[i+1:-3])}', pos=({line[at_index+1]}, {line[at_index+2]}), colour={colour})\n"
                )

            skip_counter = len(line)

        elif " ".join(line[:2]) == "text colour":

            file.write(indent + f"text_colour {" ".join(line[2:])}\n")
            skip_counter = len(line)

        elif " ".join(line[:2]) == "window name":

            if " ".join(line[3:]) in vars_defined:
                file.write(indent + f"pg.display.set_caption({" ".join(line[3:])})\n")

            else:
                file.write(indent + f"pg.display.set_caption('{" ".join(line[3:])}')\n")
            skip_counter = len(line)


        elif word in ("while", "for", "if", "def"):
            file.write(indent+f"{word} {" ".join(line[1:])}:\n")

            if " ".join(line) == "while run":

                file.write(f"{indent}    clock.tick(fps)\n{indent}    for event in pg.event.get():\n{indent}        if event.type == pg.QUIT:\n{indent}            run = False\n")
            
            skip_counter = len(line)

        elif word == "end":
            file.write("pg.quit()\nquit()\n")
            skip_counter = len(line)

        elif word == "refresh":
            file.write(f"{indent}pg.display.update()\n{indent}window.fill(background)\n")

        else:

            if "=" in line:

                vars_defined.append(word)

            file.write(indent+ " ".join(line) + "\n")

            skip_counter = len(line)

    skip_counter = 0

file.close()

import output
quit()
