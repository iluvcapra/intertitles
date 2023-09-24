from ffmpeg import vfilters, vtools, avfilters, input, input_source

from collections import namedtuple
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

    def parse_pointsize(rest):
        yield "-pointsize"
        yield rest[0]

    def parse_safe_area(rest):
        state['safe_area'] = (int(rest[0]), int(rest[1]))

    def parse_frame_size(rest):
        state['frame_size'] = (int(rest[0]), int(rest[1]))
        state['safe_area'] = state['frame_size']

    lines = markup.split("\n")
    for line in lines:
        p = shlex.split(line, comments=True, posix=True)
        if len(p) == 0:
            continue

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
        elif p[0] == ".pointsize":
            yield from parse_pointsize(p[1:])
        elif p[0] == ".safe_area":
            parse_safe_area(p[1:])
        elif p[0] == ".frame_size":
            parse_frame_size(p[1:])
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
    # plate = ""
    #in0 = input(plate).video 

    markup_example = """
.bg none
.fill white 
.font /System/Library/Fonts/Supplemental/Futura.ttc
.frame_size 1920 1080
.safe_area 1720 880
.gv West
.pointsize 56
TITLE / Artist / Company
.vs 200
.pointsize 36
This is some information on TITLE.
"""


    dims = {
        "size": "1920x1080",    
        "rate": 30,    
        "duration": 5.000
    }

    command = ["convert"] + list(parse_markup(markup_example)) + ["output_gen.tiff"]
    subprocess.run(command)

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
