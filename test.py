from flask import Flask, request
from random import randrange, shuffle

app = Flask(__name__)

from colour import Color

AMOUNT = 0

HUE_Opts = {"LOW": 0.025, "MEDIUM": 0.05, "HIGH": 0.075}
SAT_Opts = {"LOW": 0.01, "MEDIUM": 0.1, "HIGH": 0.2}
LUM_Opts = {"LOW": 0.01, "MEDIUM": 0.05, "HIGH":0.1}

HUE_VARIANCE = HUE_Opts["MEDIUM"]
SATURATION_VARIANCE = SAT_Opts["MEDIUM"]
LUMINANCE_VARIANCE = LUM_Opts["MEDIUM"]

def html_form(hex, hue, sat, lum, is_sub=False, amount=0):
    table = "<table class='submit_form' heght=5% width=100%>"
    table += "<tr height=50><form name='settings'>"
    table += f"<td id='color_picker_cell' ><input id='color_picker' type='color' id='hex' name='hex' value='{hex}'></div></td>"
    
    #table += f"<td><label for='Hue Variation'>Hue Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={hue} id='hue' name='hue'></td>"
    table += "<td><label for='hue'>Hue Variation</label><select id='hue' class='select-style' name='hue'>"
    for key in HUE_Opts.keys():
        selected = ""
        if HUE_Opts[key] == hue:
            selected = "selected"
        table += f"<option value='{HUE_Opts[key]}' {selected}>{key}</option>"
    table += "</select></td>"
    
    #table += f"<td><label for='Saturation Variation'>Saturation Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={sat} id='saturation' name='saturation'></td>"
    table += "<td><label for='saturation'>Saturation Var.</label><select id='saturation' class='select-style' name='saturation'>"
    for key in SAT_Opts.keys():
        selected = ""
        if SAT_Opts[key] == sat:
            selected = "selected"
        table += f"<option value='{SAT_Opts[key]}' {selected}>{key}</option>"
    table += "</select></td>"

    #table += f"<td><label for='Luminance Variation'>Luminance Variation:</label><input type='number' step='0.01' min='0.02' max='0.1' value={lum} id='luminance' name='luminance'></td>"
    table += "<td><label for='luminance'>Luminance Var.</label><select id='luminance' class='select-style' name='luminance'>"
    for key in LUM_Opts.keys():
        selected = ""
        if LUM_Opts[key] == lum:
            selected = "selected"
        table += f"<option value='{LUM_Opts[key]}' {selected}>{key}</option>"
    table += "</select></td>"
    
    if is_sub:
        table += f"<td><label for='Number of Palettes'>Number of Palettes:</label><input type='number' min='0' max='6' value={amount} id='amount' name='amount'></td>"
    table += "<td><input class='submit_button' type='submit' value='Submit'></td>"
    table += "</form></tr>"
    table += "</table>"
    return table


def html_palette(hex_color, hue, saturation, luminance):
    palettes = generate_palette(hex_color, hue, saturation, luminance)
    table = "<table height=90% width=100%>"
    id_counter = 1
    for palette in palettes:
        table += "<tr>"
        for color in palette:
            table += f"<td id={id_counter} class='hex-color' onClick='copycell({id_counter});'; align='center' height=33.33% width=14.25% style='background-color: {color};'>{color}</td>"
            id_counter += 1
        table += "</tr>"
    table += "</table>"
    return table


def html_subpalettes(palette, amount):
    page = ""
    subpalettes = generate_subpalettes(palette, amount)
    page += "<table>"
    id_counter = 1
    for subpalette in subpalettes:
        page += "<tr>"
        for color in subpalette:
            page += f"<td id={id_counter} class='hex-color' onClick='copycell({id_counter});'; align='center' height=33.33% width=14.25% style='background-color: {color};'>{color}</td>"
        page += "</tr>"
    page += "</table>"
    return page


def html_include_js():
    return "<script src='/static/color-generator.js'></script>"


def html_include_css():
    return "<link rel='stylesheet' href='/static/color-generator.css'>"


@app.route("/")
def palette_index():
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

    page = html_include_js()
    page += html_include_css()

    page += "<body>"

    page += html_palette(hex_color, hue, saturation, luminance)

    page += html_form(hex_color, hue, saturation, luminance)
    page += "</body>"
    return page


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

    page = html_include_js()
    page += html_include_css()

    page += "<body>"

    # page += html_palette(hex_color, hue, saturation, luminance)

    ## generate subpalettes
    palette = generate_palette(hex_color, hue, saturation, luminance)
    page += html_subpalettes(palette, amount)
    page += html_form(hex_color, hue, saturation, luminance, True, amount)
    page += "</body>"

    return page


def rotate_hue(_hue, _diff):
    hue = _hue + _diff
    while hue > 1.0:
        hue -= 1.0
    while hue < 0.0:
        hue += 1.0
    return hue


def generate_subpalettes(palette, amount):
    subpalettes = []
    for i in range(amount):
        subpalette = []
        num_of_colors = 4  # randrange(3, 6, 1)
        colors = list(range(7))
        shuffle(colors)
        for j in range(num_of_colors):
            subpalette.append(palette[randrange(0, 3)][colors[j]])
        subpalettes.append(subpalette)

    return subpalettes


def generate_palette(_color, _hue_variance, _saturation_variance, _luminance_variance):
    base_color = Color(_color)
    palette = [base_color.hex_l]

    print(f"{_hue_variance} * 3 = {_hue_variance * 3}")

    print(base_color.rgb)
    print(base_color.hsl)

    print(
        f"BASE: H={base_color.hue} S={base_color.saturation} L={base_color.luminance}"
    )

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, -(_hue_variance * i))
        new_color.saturation = max(
            0.0, base_color.saturation - (_saturation_variance * i)
        )
        new_color.luminance = max(0.0, base_color.luminance - (_luminance_variance * i))
        palette.append(new_color.hex_l)

    for i in range(1, 4):
        new_color = Color(base_color)
        new_color.hue = rotate_hue(base_color.hue, (_hue_variance * i))
        new_color.saturation = min(
            1.0, base_color.saturation + (_saturation_variance * i)
        )
        new_color.luminance = min(1.0, base_color.luminance + (_luminance_variance * i))
        print(new_color.rgb)
        print(new_color.hsl)
        palette.insert(0, new_color.hex_l)

    print(palette)

    lighter_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, -_hue_variance / 2)
        new_color.saturation = max(
            0.0, base_color.saturation - (_saturation_variance * i)
        )
        new_color.luminance = min(1.0, base_color.luminance + (_luminance_variance * i))
        lighter_palette.append(new_color.hex_l)

    darker_palette = []
    for color in palette:
        new_color = Color(color)
        new_color.hue = rotate_hue(new_color.hue, _hue_variance / 2)
        new_color.saturation = min(
            1.0, base_color.saturation + (_saturation_variance * i)
        )
        new_color.luminance = max(0.0, base_color.luminance - (_luminance_variance * i))
        darker_palette.append(new_color.hex_l)

    palettes = [lighter_palette, palette, darker_palette]

    return palettes


if __name__ == "__main__":
    app.run(debug=True)
