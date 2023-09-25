from ffmpeg import vfilters, vtools, avfilters, input, input_source

import shlex

import subprocess

def parse_markup(markup: str):
    state = dict()
    state['safe_area'] = (0,0)
    state['frame_size'] = (0,0)

    def parse_gv(rest):
        gravity = rest[0]
        yield "-gravity"
        yield gravity

    def parse_vs(rest):
        yield "("
        yield "-size"
        yield f"{state['safe_area'][0]}x{int(rest[0])}"
        yield "canvas:none"
        yield ")"

    def parse_line(rest):
        yield "("
        yield "-size"
        yield f"{state['safe_area'][0]}x"
        yield f"caption:{shlex.join(rest)}"
        yield ")"
    
    def parse_bg(rest):
        yield "-background"
        yield rest[0]

    def parse_fill(rest):
        yield "-fill"
        yield rest[0]

    def parse_font(rest):
        yield "-font"
        yield rest[0]

    def parse_textsize(rest):
        yield "-textsize"
        yield rest[0]

    def parse_safe_area(rest):
        state['safe_area'] = (int(rest[0]), int(rest[1]))

    def parse_frame_size(rest):
        state['frame_size'] = (int(rest[0]), int(rest[1]))
        state['safe_area'] = state['frame_size']
    
    def parse_img(rest):
        yield "("
        yield from iter(rest)
        if len(rest) > 0:
            yield "+append"
        yield "-resize" 
        yield f"{state['safe_area'][0]}x{state['safe_area'][1]}>"
        yield "-extent"
        yield f"{state['safe_area'][0]}x"
        yield ")"

    lines = markup.split("\n")
    for line in lines:
        p = shlex.split(line, comments=True, posix=True)
        if len(p) == 0:
            continue

        if p[0][0:1] == ".":
            if p[0] == ".gv":
                yield from parse_gv(p[1:])
            elif p[0] == ".vs":
                yield from parse_vs(p[1:])
            elif p[0] == ".bg":
                yield from parse_bg(p[1:])
            elif p[0] == ".fill":
                yield from parse_fill(p[1:])
            elif p[0] == ".font":
                yield from parse_font(p[1:])
            elif p[0] == ".textsize":
                yield from parse_textsize(p[1:])
            elif p[0] == ".safe_area":
                parse_safe_area(p[1:])
            elif p[0] == ".frame_size":
                parse_frame_size(p[1:])
            elif p[0] == ".img":
                yield from parse_img(p[1:])
            else:
                raise RuntimeError()
        else:
            yield from parse_line(p)

    yield "-append"
    yield "-extent"
    yield f"{state['safe_area'][0]}x{state['safe_area'][1]}"
    yield "-gravity"
    yield "Center"
    yield "-extent"
    yield f"{state['frame_size'][0]}x{state['frame_size'][1]}"


def main():
    markup_example = """
.bg none
.fill white 
.font /System/Library/Fonts/Supplemental/Futura.ttc
.frame_size 1920 1080
.safe_area 1620 780
.gv Center
.img JH.tiff JH.tiff 
.gv West
.textsize 56
TITLE / Artist / Company
.vs 120
.gv West
.textsize 36
This is some information on TITLE.
# .gv East
# Some right-aligned text.
"""

    command = ["convert"] + list(parse_markup(markup_example)) + ["output_gen.tiff"]
    subprocess.run(command)

   # dims = {
   #     "size": "1920x1080",    
   #     "rate": 30,    
   #     "duration": 5.000
   # }

   #  output_file = "output.tiff"
   #  tiff_text_frame(output=output_file, 
   #                  font_file="/System/Library/Fonts/Supplemental/Futura.ttc",
   #                  font_size=36,
   #                  text_color="white",
   #                  frame_size=(1920,1080),
   #                  safe_size=(1720,880))
   #
   #  in0 = input_source("color", color="black", **dims)
   #  text_in1 = input(output_file)
   # 
   #  title_filter = in0.overlay(text_in1)
   #
   #  comp = title_filter
   #  comp.output("output.mov", codec="prores", v_profile="0").run()
