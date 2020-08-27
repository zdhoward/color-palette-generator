from flask import Flask
app = Flask(__name__)

from colormath.color_objects import sRGBColor, HSVColor, HSLColor
from colormath.color_conversions import convert_color

# colormath seems bad

@app.route("/")
def index():
    palette = generate_palette()
    table = "<table><tr>"
    for color in palette:
        table += f"<td style='background-color: {color};'>{color}</td>"
    table += "</tr></table>"
    return table

def generate_palette():
    ###### USE HSV? HSL?
    ## https://python-colormath.readthedocs.io/en/latest/
    ## https://www.youtube.com/watch?v=u5AnzLg1HxY
    ## SELECT BASE COLOR
    base_color = sRGBColor(0.0, 0.75, 0.0)
    palette = [base_color.get_rgb_hex()]
    ## remove some brightness and saturation for 3 more colors, shift hue slightly down
    for i in range(1,4):
        #new_color = convert_color(base_color, HSVColor)
        #new_color.hsv_h += min(0.1 * i, 1.0)
        #new_color.hsv_s += min(0.1 * i, 1.0)
        new_color = convert_color(base_color, HSLColor)
        new_color.hsl_h += min(0.1 * i, 1.0)
        new_color.hsl_s += min(0.05 * i, 1.0)
        new_color.hsl_l += min(0.05 * i, 1.0)

        new_rgb = convert_color(new_color, sRGBColor)
        new_hex = new_rgb.get_rgb_hex().replace("-", "")
        if len(new_hex) == 8:
            print (new_hex)
            new_hex = "#" + new_hex[2:]
            #new_hex = new_hex[:7]
        palette.insert(0, new_hex)#.replace("-", ""))#.replace("#1", "#"))
    ## add some brightness and saturation for 3 more colors, shift hue slightly up
    for i in range(1,4):
        #new_color = convert_color(base_color, HSVColor)
        #new_color.hsv_h -= min(0.1 * i, 1.0)
        #new_color.hsv_s -= min(0.1 * i, 1.0)
        new_color = convert_color(base_color, HSLColor)
        new_color.hsl_h -= max(0.1 * i, -1.0)
        new_color.hsl_s -= max(0.05 * i, -1.0)
        new_color.hsl_l -= max(0.05 * i, -1.0)

        new_rgb = convert_color(new_color, sRGBColor)
        palette.append(new_rgb.get_rgb_hex().replace("-", ""))#.replace("#1", "#"))

    ## add dimension by then  copying what we have and removing saturation while adding brightness and shifting hue slightly up
    ## add dimension by then  copying what we have and adding saturation while removing brightness and shifting hue slightly down

    print (palette)
    return palette

    ## allow for slight randomization so you can regen colour pallete
    ## allow tweaking of base hue

def proof_of_concept():
    rgb_color = sRGBColor(1.0,0.0,0.0)
    print (f"OLD: {rgb_color.get_rgb_hex()}")

    hsv_color = convert_color(rgb_color, HSVColor)
    hsv_color.hsv_h += 0.1
    hsv_color.hsv_s += 0.1
    
    new_rgb_color = convert_color(hsv_color, sRGBColor)
    
    print (f"NEW: {new_rgb_color.get_rgb_hex()}")

if __name__ == "__main__":
    app.run()
