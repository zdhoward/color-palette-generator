from flask import Flask, request
app = Flask(__name__)

from colormath.color_objects import sRGBColor, HSVColor, HSLColor
from colormath.color_conversions import convert_color

from colour import Color

# colormath seems bad

HUE_VARIANCE = 0.05
SATURATION_VARIANCE = 0.05
LUMINANCE_VARIANCE = 0.05

AMOUNT = 0

@app.route("/")
def palette_index():
    table = "<script type='text/javascript'>"
    table += "function copycell(id){var text = document.getElementById(id).innerHTML; navigator.clipboard.writeText(text);}"
    #table += 'var cells = table.getElementsByTagName("td"); for (var i = 0; i < cells.length; i++) {    cells[i].onclick = function(){tes();};}'
    table += "</script>"
    table += "<table height=100% width=100%>"
    if request.args.get("hex"):
        hex_color = request.args.get("hex")
    else:
        hex_color = "#ff0000"
    if request.args.get("hue"):
        hue = float(request.args.get("hue"))
    else:
        hue = HUE_VARIANCE
    if request.args.get("saturation"):
        saturation = float(request.args.get("saturation"))
    else:
        saturation = SATURATION_VARIANCE
    if request.args.get("luminance"):
        luminance = float(request.args.get("luminance"))
    else:
        luminance = LUMINANCE_VARIANCE


    palettes = generate_palette(hex_color, hue, saturation, luminance)
    id_counter = 1
    for palette in palettes:
        table += "<tr>"
        for color in palette:
            table += f"<td id={id_counter} class='hex-color' onClick='copycell({id_counter});'; align='center' height=33.33% width=14.25% style='background-color: {color};'>{color}</td>"
            id_counter += 1
        table += "</tr>"
        
    table += "<tr height=50><form name='settings'>"
    table += f"<td><input type='color' id='hex' name='hex' value='{hex_color}'></td>"
    table += f"<td><label for='Hue Variation'>Hue Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={hue} id='hue' name='hue'></td>"
    table += f"<td><label for='Saturation Variation'>Saturation Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={saturation} id='saturation' name='saturation'></td>"
    table += f"<td><label for='Luminance Variation'>Luminance Variation:</label><input type='number' step='0.01' min='0.02' max='0.1' value={luminance} id='luminance' name='luminance'></td>"
    table += "<td><input type='submit' value='Submit'></td>"
    table += "</form></tr>"
    table += "</table>"
    return table

@app.route("/sub/")
def subpalette_index():
    if request.args.get("hex"):
        hex_color = request.args.get("hex")
    else:
        hex_color = "#ff0000"
    if request.args.get("hue"):
        hue = float(request.args.get("hue"))
    else:
        hue = HUE_VARIANCE
    if request.args.get("saturation"):
        saturation = float(request.args.get("saturation"))
    else:
        saturation = SATURATION_VARIANCE
    if request.args.get("luminance"):
        luminance = float(request.args.get("luminance"))
    else:
        luminance = LUMINANCE_VARIANCE
    if request.args.get("amount"):
        amount = int(request.args.get("amount"))
    else:
        amount = AMOUNT

    palettes = generate_palette(hex_color, hue, saturation, luminance)
    id_counter = 1

    ## generate subpalettes

    table = "<table height=100% width=100%>"
    table += "<tr height=50><form name='settings'>"
    table += f"<td><input type='color' id='hex' name='hex' value='{hex_color}'></td>"
    table += f"<td><label for='Hue Variation'>Hue Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={hue} id='hue' name='hue'></td>"
    table += f"<td><label for='Saturation Variation'>Saturation Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={saturation} id='saturation' name='saturation'></td>"
    table += f"<td><label for='Luminance Variation'>Luminance Variation:</label><input type='number' step='0.01' min='0.02' max='0.1' value={luminance} id='luminance' name='luminance'></td>"
    table += f"<td><label for='Number of Colours'>Number of Colours:</label><input type='number' min='0' max='6' value={amount} id='amount' name='amount'></td>"
    table += "<td><input type='submit' value='Submit'></td>"
    table += "</form></tr>"
    table += "</table>"
    return table

def rotate_hue(_hue, _diff):
    hue = _hue + _diff
    while hue > 1.0:
        hue -= 1.0
    while hue < 0.0:
        hue += 1.0
    return hue

def generate_palette(_color, _hue_variance, _saturation_variance, _luminance_variance):
    base_color = Color(_color)
    palette = [base_color.hex_l]

    print (f"{_hue_variance} * 3 = {_hue_variance * 3}")

    print(base_color.rgb)
    print(base_color.hsl)

    print (f"BASE: H={base_color.hue} S={base_color.saturation} L={base_color.luminance}")

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, -(_hue_variance * i))
        new_color.saturation = max(0.0, base_color.saturation - (_saturation_variance * i))
        new_color.luminance = max(0.0, base_color.luminance - (_luminance_variance * i))
        palette.append(new_color.hex_l)

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, (_hue_variance * i))
        new_color.saturation = min(1.0,base_color.saturation + (_saturation_variance * i))
        new_color.luminance = min(1.0,base_color.luminance + (_luminance_variance * i))
        print(new_color.rgb)
        print(new_color.hsl)
        palette.insert(0,new_color.hex_l)

    print (palette)

    lighter_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, -(_hue_variance / 3))
        new_color.saturation = max(0.0, base_color.saturation - (_saturation_variance * i))
        new_color.luminance = min(1.0,base_color.luminance + (_luminance_variance * i))
        lighter_palette.append(new_color.hex_l)

    darker_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, (_hue_variance / 3))
        new_color.saturation = min(1.0, base_color.saturation + (_saturation_variance * i))
        new_color.luminance = max(0.0,base_color.luminance - (_luminance_variance * i))
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
