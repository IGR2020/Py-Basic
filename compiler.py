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

            if "." in line[i+1]:
                file.write(indent+
                f"window.blit(assets['{line[i+1]}'], ({line[-2]}, {line[-1]}))\n"
            )
                
            else:

                if " ".join(line[i+1:-3]) in vars_defined:
                    file.write(indent+
                    f"EPT.blit_text(window, {" ".join(line[i+1:-3])}, pos=({line[-2]}, {line[-1]}), colour=text_colour)\n"
                )

                else:
                    file.write(indent+
                        f"EPT.blit_text(window, '{" ".join(line[i+1:-3])}', pos=({line[-2]}, {line[-1]}), colour=text_colour)\n"
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

            file.write(indent+" ".join(line) + "\n")

            if "=" in line:
                vars_defined.append(word)

            skip_counter = len(line)

    skip_counter = 0
