from flask import Flask
app = Flask(__name__)

from colormath.color_objects import sRGBColor, HSVColor, HSLColor
from colormath.color_conversions import convert_color

from colour import Color

# colormath seems bad

HUE_VARIANCE = 0.05
SATURATION_VARIANCE = 0.05
LUMINANCE_VARIANCE = 0.05

@app.route("/")
def index():
    palettes = generate_palette()
    table = "<table height=100% width=100%>"
    for palette in palettes:
        table += "<tr>"
        for color in palette:
            table += f"<td align='center' height=33.33% width=14.25% style='background-color: {color};'>{color}</td>"
        table += "</tr>"
    table += "</table>"
    return table

def rotate_hue(_hue, _diff):
    hue = _hue + _diff
    while hue > 1.0:
        hue -= 1.0
    while hue < 0.0:
        hue += 1.0
    return hue

def generate_palette():
    base_color = Color("blue")
    palette = [base_color.hex_l]

    print (f"{HUE_VARIANCE} * 3 = {HUE_VARIANCE * 3}")

    print(base_color.rgb)
    print(base_color.hsl)

    print (f"BASE: H={base_color.hue} S={base_color.saturation} L={base_color.luminance}")

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, -(HUE_VARIANCE * i))
        new_color.saturation = max(0.0, base_color.saturation - (SATURATION_VARIANCE * i))
        new_color.luminance = max(0.0, base_color.luminance - (LUMINANCE_VARIANCE * i))
        palette.append(new_color.hex_l)

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, (HUE_VARIANCE * i))
        new_color.saturation = min(1.0,base_color.saturation + (SATURATION_VARIANCE * i))
        new_color.luminance = min(1.0,base_color.luminance + (LUMINANCE_VARIANCE * i))
        print(new_color.rgb)
        print(new_color.hsl)
        palette.insert(0,new_color.hex_l)

    print (palette)

    lighter_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, -(HUE_VARIANCE / 3))
        new_color.saturation = max(0.0, base_color.saturation - (SATURATION_VARIANCE * i))
        new_color.luminance = min(1.0,base_color.luminance + (LUMINANCE_VARIANCE * i))
        lighter_palette.append(new_color.hex_l)

    darker_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, (HUE_VARIANCE / 3))
        new_color.saturation = min(1.0, base_color.saturation + (SATURATION_VARIANCE * i))
        new_color.luminance = max(0.0,base_color.luminance - (LUMINANCE_VARIANCE * i))
        darker_palette.append(new_color.hex_l)

    palettes = [lighter_palette, palette, darker_palette]


    return palettes

def generate_palette_old():
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
    app.run(debug=True)
