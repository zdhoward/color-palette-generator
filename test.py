from flask import Flask, request

app = Flask(__name__)

from colour import Color

HUE_VARIANCE = 0.05
SATURATION_VARIANCE = 0.05
LUMINANCE_VARIANCE = 0.05

AMOUNT = 0

HUE_Opts = [0.01, 0.5, 0.75]
SAT_Opts = [0.01, 0.1, 0.2]
LUM_Opts = [0.01, 0.05, 0.1]


def html_form(hex, hue, sat, lum, is_sub=False, amount=0):
    table = "<table class='submit_form' heght=5% width=100%>"
    table += "<tr height=50><form name='settings'>"
    table += f"<td><input type='color' id='hex' name='hex' value='{hex}'></td>"
    table += f"<td><label for='Hue Variation'>Hue Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={hue} id='hue' name='hue'></td>"
    table += f"<td><label for='Saturation Variation'>Saturation Variation:</label><input type='number' step='0.01' min='0.01' max='0.1' value={sat} id='saturation' name='saturation'></td>"
    table += f"<td><label for='Luminance Variation'>Luminance Variation:</label><input type='number' step='0.01' min='0.02' max='0.1' value={lum} id='luminance' name='luminance'></td>"
    if is_sub:
        table += f"<td><label for='Number of Colours'>Number of Colours:</label><input type='number' min='0' max='6' value={amount} id='amount' name='amount'></td>"
    table += "<td><input type='submit' value='Submit'></td>"
    table += "</form></tr>"
    table += "</table>"
    return table


def html_palette(hex_color, hue, saturation, luminance):
    palettes = generate_palette(hex_color, hue, saturation, luminance)
    table = "<table height=95% width=100%>"
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
    subpalettes = generate_subpalettes(palette, amount)
    return ""


def html_include_js():
    return "<script src='static/color-generator.js'></script>"


def html_include_css():
    return "<link rel='stylesheet' href='static/color-generator.css'>"


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

    page += html_palette(hex_color, hue, saturation, luminance)

    ## generate subpalettes
    palette = generate_palette(hex_color, hue, saturation, luminance)
    page = html_subpalettes(palette, amount)
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
