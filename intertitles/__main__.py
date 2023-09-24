from ffmpeg import vfilters, vtools, avfilters, input, input_source

from collections import namedtuple

TextFlow = namedtuple("TextFlow", ["alignment", "text" ])

def main():
    # plate = ""
    #in0 = input(plate).video 

    dims = {
        "size": "1920x1080",    
        "rate": 30,    
        "duration": 5.000
    }

    import subprocess

# Output TIFF file name
    output_file = "output.tiff"

# Path to the TrueType font file (.ttf)
    font_file = "/System/Library/Fonts/Supplemental/Futura.ttc"
# Font size
    font_size = 36

    frame_size = "1920x1080"
    safe_size = "1720x880"

# Text color
    text_color = "white"

    command = [
        "convert",
        "-background", "none", 
        "(",
        "1.png",
        "2.png",
        "3.png",
        "+append",
        "-scale", "1720x400",
        "-extent", "1720x400",
        ")",
        "(",
        "-size","1720x",
        "-fill", text_color,
        "-font", font_file,
        "-pointsize", str(font_size),
        f"caption:TEST TITLE / Jamie Hardt\nSecond Line\nThird\nFourth",
        ")",
        "-append",
        "-gravity", "West",
        "-extent", safe_size,
        "-gravity", "North",
        "-extent", frame_size,
        output_file
    ]

# Run the ImageMagick command
    subprocess.run(command)

    print(f"TIFF image with transparent background created: {output_file}")


    in0 = input_source("color", color="black", **dims)
    text_in1 = input(output_file)
   
    title_filter = in0.overlay(text_in1)

    # in1_scaled = vfilters.scale(in1v, width=800, height=-1)
    # comp = title_filter.overlay(in1_scaled, x="10", y="main_h - overlay_h - 10")
    # comp = avfilters.concat(title_filter, in1v, in0)
    comp = title_filter
    comp.output("output.mov", codec="prores", v_profile="0").run()
