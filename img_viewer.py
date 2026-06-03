# pyrefly: ignore [missing-import]
import FreeSimpleGUI as sg
import os
import os.path
from PIL import Image, ImageOps
from processing_list import *

sg.set_options(font=('Segoe UI', 10))

def section_header(text):
    return sg.Text(text, font=('Segoe UI Semibold', 10), pad=(0,6))

def section_sep():
    return sg.HSeparator(pad=(0,4))

def panel_btn(text, key, size=(22,1)):
    return sg.Button(text, size=size, key=key, font=('Segoe UI', 9), pad=(0,2))

left_panel = [
    [sg.Text("EXPLORER", font=('Segoe UI Semibold', 9), pad=(0,4))],
    [sg.In(size=(22,1), enable_events=True, key="ImgFolder", pad=(0,2)),
     sg.FolderBrowse("...", size=(3,1))],
    [sg.Listbox(values=[], enable_events=True, size=(26,20), key="ImgList", pad=(0,4))],
    [section_sep()],
    [sg.Text("", size=(20,1), key="ImgSize", font=('Segoe UI', 9))],
    [sg.Text("", size=(20,1), key="ImgColorDepth", font=('Segoe UI', 9))],
]

canvas_area = [
    [sg.Column(
        [[sg.Text("INPUT", font=('Segoe UI Semibold', 9))],
         [sg.Text("", size=(50,1), key="FilepathImgInput", font=('Segoe UI', 8))],
         [sg.Image(key="ImgInputViewer")]],
        pad=(4,4), expand_x=True, expand_y=True, element_justification='center'
    ),
    sg.Column(
        [[sg.Text("OUTPUT", font=('Segoe UI Semibold', 9))],
         [sg.Text("", size=(50,1), key="ImgProcessingType", font=('Segoe UI', 8))],
         [sg.Image(key="ImgOutputViewer")]],
        pad=(4,4), expand_x=True, expand_y=True, element_justification='center'
    )],
]

right_tools = [
    [section_header("ADJUSTMENTS")],
    [panel_btn("Image Negative", "ImgNegative")],
    [sg.Text("Brightness", font=('Segoe UI', 9))],
    [sg.Slider(range=(-255,255), default_value=0, orientation='h', size=(18,14),
               enable_events=True, key="-BRIGHT_SLIDER-", pad=(0,0))],
    [sg.Text("Power Law (Gamma)", font=('Segoe UI', 9))],
    [sg.Slider(range=(0.1,5.0), default_value=1.0, resolution=0.1, orientation='h', size=(18,14),
               enable_events=True, key="-GAMMA_SLIDER-", pad=(0,0))],
    [panel_btn("Log Transform", "ImgLog")],
    [section_sep()],
    [section_header("TRANSFORM")],
    [panel_btn("Rotate CW", "ImgRotateCW", (10,1)), panel_btn("Rotate CCW", "ImgRotateCCW", (10,1))],
    [panel_btn("Flip H", "ImgFlipH", (10,1)), panel_btn("Flip V", "ImgFlipV", (10,1))],
    [sg.Text("Scale Factor", font=('Segoe UI', 9))],
    [sg.Slider(range=(0.1,4.0), default_value=1.0, resolution=0.1, orientation='h', size=(18,14),
               enable_events=True, key="-SCALE_SLIDER-", pad=(0,0))],
    [sg.Text("Resample", font=('Segoe UI', 9)),
     sg.Text("W:"), sg.Input("300", size=(5,1), key="ResampleW"),
     sg.Text("H:"), sg.Input("300", size=(5,1), key="ResampleH")],
    [panel_btn("Resample", "ImgResample")],
    [section_sep()],
    [section_header("BLENDING")],
    [sg.In(size=(17,1), enable_events=True, key="ImgBlend2Path", pad=(0,2)),
     sg.FileBrowse("...", size=(3,1),
                   file_types=(("Image Files", "*.png *.jpg *.jpeg *.gif"),))],
    [sg.Text("Alpha", font=('Segoe UI', 9))],
    [sg.Slider(range=(0.0,1.0), default_value=0.5, resolution=0.01, orientation='h', size=(18,14),
               key="-BLEND_SLIDER-", pad=(0,0))],
    [panel_btn("Blend Images", "ImgBlend")],
    [section_sep()],
    [section_header("FILTERING")],
    [sg.Text("Kernel:", font=('Segoe UI', 9)), sg.Combo([3,5,7], default_value=3, size=(4,1), key="FilterKernel")],
    [panel_btn("Median Filter", "ImgMedian")],
    [panel_btn("Mean Filter", "ImgMean")],
    [panel_btn("Gaussian Filter", "ImgGaussian")],
    [section_sep()],
    [section_header("EDGE DETECTION")],
    [panel_btn("Sobel", "ImgSobel", (10,1)), panel_btn("Prewitt", "ImgPrewitt", (10,1))],
    [panel_btn("Robert Cross", "ImgRobert")],
    [sg.Text("Compass:", font=('Segoe UI', 9)),
     sg.Combo(["N","NE","E","SE","S","SW","W","NW","ALL"], default_value="ALL", size=(5,1), key="CompassDir")],
    [panel_btn("Compass Filter", "ImgCompass")],
    [section_sep()],
    [panel_btn("Reset", "ImgReset")],
]

layout = [
    [
        sg.Column(left_panel, vertical_alignment='top', pad=(0,0), expand_y=True, size=(220, None)),
        sg.VSeparator(),
        sg.Column(canvas_area, expand_x=True, expand_y=True, pad=(0,0), element_justification='center'),
        sg.VSeparator(),
        sg.Column(right_tools, vertical_alignment='top', pad=(0,0), expand_y=True,
                  scrollable=True, vertical_scroll_only=True, size=(240, None)),
    ]
]

window = sg.Window("Mini Image Editor", layout, resizable=True, finalize=True, margins=(0,0), size=(1280,720))

out_files = ["out_a.png", "out_b.png"]
out_idx = 0

def save_output(img, window):
    global out_idx
    out_idx = 1 - out_idx
    path = out_files[out_idx]
    img.save(path)
    window["ImgOutputViewer"].update(filename=path)

while True:
    event, values = window.read()

    if event in ("Exit", sg.WIN_CLOSED):
        break

    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg", ".jpeg", ".bmp"))
        ]
        window["ImgList"].update(fnames)

    elif event == "ImgList":
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(values["ImgList"][0])
            window["ImgInputViewer"].update(filename=filename)
            window["ImgProcessingType"].update("Original")
            window["ImgOutputViewer"].update(filename=filename)
            img_input = Image.open(filename)
            img_width, img_height = img_input.size
            window["ImgSize"].update(f"Size: {img_width} x {img_height} px")
            mode_to_coldepth = {"1":1,"L":8,"P":8,"RGB":24,"RGBA":32,"CMYK":32,"YCbCr":24,"LAB":24,"HSV":24,"I":32,"F":32}
            coldepth = mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update(f"Depth: {coldepth}-bit")
        except:
            pass

    elif event == "ImgRotateCW":
        try:
            window["ImgProcessingType"].update("Rotate CW")
            img_output = ImgRotate(img_input, coldepth, "C")
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgRotateCCW":
        try:
            window["ImgProcessingType"].update("Rotate CCW")
            img_output = ImgRotate(img_input, coldepth, "CC")
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgFlipH":
        try:
            window["ImgProcessingType"].update("Flip Horizontal")
            img_output = ImgFlip(img_input, coldepth, "H")
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgFlipV":
        try:
            window["ImgProcessingType"].update("Flip Vertical")
            img_output = ImgFlip(img_input, coldepth, "V")
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgReset":
        try:
            window["-BRIGHT_SLIDER-"].update(value=0)
            window["-GAMMA_SLIDER-"].update(value=1.0)
            window["-SCALE_SLIDER-"].update(value=1.0)
            window["ResampleW"].update(value="300")
            window["ResampleH"].update(value="300")
            window["ImgProcessingType"].update("Reset")
            window["ImgOutputViewer"].update(filename=filename)
        except:
            pass

    elif event == "ImgResample":
        try:
            new_w = int(values["ResampleW"])
            new_h = int(values["ResampleH"])
            window["ImgProcessingType"].update(f"Resample {new_w}x{new_h}")
            img_output = ImgResample(img_input, coldepth, new_w, new_h)
            save_output(img_output, window)
        except Exception as e:
            print(e)

    elif event == "-SCALE_SLIDER-":
        try:
            factor = float(values["-SCALE_SLIDER-"])
            window["ImgProcessingType"].update(f"Scale x{factor:.1f}")
            img_output = ImgScaling(img_input, coldepth, factor)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgNegative":
        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output = ImgNegative(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "-BRIGHT_SLIDER-":
        try:
            val = int(values["-BRIGHT_SLIDER-"])
            window["ImgProcessingType"].update("Brightness")
            img_output = ImgBrightness(img_input, coldepth, val)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgLog":
        try:
            window["ImgProcessingType"].update("Log Transform")
            img_output = ImgLogTransform(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "-GAMMA_SLIDER-":
        try:
            val = float(values["-GAMMA_SLIDER-"])
            window["ImgProcessingType"].update("Power Law")
            img_output = ImgPowerLaw(img_input, coldepth, val)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgBlend":
        try:
            blend2_path = values["ImgBlend2Path"]
            alpha = float(values["-BLEND_SLIDER-"])
            img2 = Image.open(blend2_path)
            window["ImgProcessingType"].update("Blending")
            img_output = ImgBlending(img_input, img2, coldepth, alpha)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgMedian":
        try:
            k = int(values["FilterKernel"])
            window["ImgProcessingType"].update(f"Median {k}x{k}")
            img_output = ImgMedianFilter(img_input, coldepth, k)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgMean":
        try:
            k = int(values["FilterKernel"])
            window["ImgProcessingType"].update(f"Mean {k}x{k}")
            img_output = ImgMeanFilter(img_input, coldepth, k)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgGaussian":
        try:
            k = int(values["FilterKernel"])
            window["ImgProcessingType"].update(f"Gaussian {k}x{k}")
            img_output = ImgGaussianFilter(img_input, coldepth, k)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgSobel":
        try:
            window["ImgProcessingType"].update("Sobel Filter")
            img_output = ImgSobelFilter(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgPrewitt":
        try:
            window["ImgProcessingType"].update("Prewitt Filter")
            img_output = ImgPrewittFilter(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgRobert":
        try:
            window["ImgProcessingType"].update("Robert Cross")
            img_output = ImgRobertCrossFilter(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgCompass":
        try:
            d = values["CompassDir"]
            window["ImgProcessingType"].update(f"Compass ({d})")
            img_output = ImgCompassFilter(img_input, coldepth, d)
            save_output(img_output, window)
        except:
            pass

window.close()