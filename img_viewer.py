# pyrefly: ignore [missing-import]
import FreeSimpleGUI as sg
import os
import os.path
from PIL import Image, ImageOps
from processing_list import *

#Area open folder and select image
file_list_column=[
    [
        sg.Text("Open Image Folder"),
    ],
    [
        sg.In(size=(20,1),enable_events=True,key="ImgFolder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Choose an image from list"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(18,10), key="ImgList"
        )
    ],
]

#Area viewer image input
image_viewer_column=[
    [sg.Text("Image Input")],
    [sg.Text(size=(40,1),key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

#Area image info dan Tombol list of processing
list_processing=[
    [
        sg.Text("Image Information"),
    ],
    [
        sg.Text(size=(20,1),key="ImgSize")  
    ],
    [
        sg.Text(size=(20,1),key="ImgColorDepth"),
    ],
    [
        sg.Text("List of Processing"),
    ],
    [
        sg.Button("Image Negative", size=(20,1),key="ImgNegative"),
    ],
    [
        sg.Button("Rotate CW", size=(9,1), key="ImgRotateCW"),
        sg.Button("Rotate CCW", size=(9,1), key="ImgRotateCCW"),
    ],
    [
        sg.Button("Flip H", size=(9,1), key="ImgFlipH"),
        sg.Button("Flip V", size=(9,1), key="ImgFlipV"),
    ],
    [
        sg.Text("Brightness:"),
        sg.Slider(range=(-255, 255), default_value=0, orientation='h', size=(16, 15), enable_events=True, key="-BRIGHT_SLIDER-")
    ],
    [
        sg.Text("Power Law:"),
        sg.Slider(range=(0.1, 5.0), default_value=1.0, resolution=0.1, orientation='h', size=(16, 15), enable_events=True, key="-GAMMA_SLIDER-")
    ],
    [
        sg.Button("Log Transform", size=(20,1), key="ImgLog"),
    ],
    [
        sg.Text("Blending"),
    ],
    [
        sg.In(size=(15,1), enable_events=True, key="ImgBlend2Path"),
        sg.FileBrowse("Browse", file_types=(("Image Files", "*.png *.jpg *.jpeg *.gif"),)),
    ],
    [
        sg.Text("Alpha:"),
        sg.Slider(range=(0.0, 1.0), default_value=0.5, resolution=0.01, orientation='h', size=(15, 15), key="-BLEND_SLIDER-"),
    ],
    [
        sg.Button("Blend Images", size=(20,1), key="ImgBlend"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Resampling"),
    ],
    [
        sg.Text("W:", size=(3,1)), sg.Input(default_text="300", size=(6,1), key="ResampleW"),
        sg.Text("H:", size=(3,1)), sg.Input(default_text="300", size=(6,1), key="ResampleH"),
    ],
    [
        sg.Button("Resample", size=(20,1), key="ImgResample"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Scaling"),
    ],
    [
        sg.Text("Factor:"),
        sg.Slider(range=(0.1, 4.0), default_value=1.0, resolution=0.1,
                  orientation='h', size=(16, 15), enable_events=True,
                  key="-SCALE_SLIDER-")
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Filtering"),
    ],
    [
        sg.Text("Kernel:"),
        sg.Combo([3, 5, 7], default_value=3, size=(4,1), key="FilterKernel"),
    ],
    [
        sg.Button("Median Filter", size=(20,1), key="ImgMedian"),
    ],
    [
        sg.Button("Mean Filter",   size=(20,1), key="ImgMean"),
    ],
    [
        sg.Button("Gaussian Filter", size=(20,1), key="ImgGaussian"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Edge Detection"),
    ],
    [
        sg.Button("Sobel Filter", size=(20,1), key="ImgSobel"),
    ],
    [
        sg.Button("Prewitt Filter", size=(20,1), key="ImgPrewitt"),
    ],
    [
        sg.Button("Robert Cross", size=(20,1), key="ImgRobert"),
    ],
    [
        sg.Text("Compass:"),
        sg.Combo(["N","NE","E","SE","S","SW","W","NW","ALL"], default_value="ALL", size=(5,1), key="CompassDir"),
    ],
    [
        sg.Button("Compass Filter", size=(20,1), key="ImgCompass"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Button("Reset", size=(20,1), key="ImgReset"),
    ],
]

#Area viewer image output
image_viewer_column2=[
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40,1),key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

#Group full layout
layout=[
    [
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(image_viewer_column),
        sg.VSeparator(),
        sg.Column(list_processing),
        sg.VSeparator(),
        sg.Column(image_viewer_column2),
    ]
]

window = sg.Window("Mini Image Editor",layout)

#Run the event loop
out_files = ["out_a.png", "out_b.png"]
out_idx = 0

def save_output(img, window):
    global out_idx
    out_idx = 1 - out_idx
    path = out_files[out_idx]
    img.save(path)
    window["ImgOutputViewer"].update(filename=path)

while True:
    event, values =window.read()
    
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
#List files in the folder
    if event =="ImgFolder":
        folder =values["ImgFolder"]
        
        try:
            #Get list of files
            file_list=os.listdir(folder)
        except:
            file_list=[]
            
        fnames=[
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower(). endswith((".png",".gif"))
        ]

        window["ImgList"].update(fnames)
    elif event == "ImgList": #A file chosen from listbox
        try:
            filename = os.path.join(
                values["ImgFolder"],values["ImgList"][0]
            )
            window["FilepathImgInput"].update(filename)
            window["ImgInputViewer"].update(filename=filename)
            window["ImgProcessingType"].update(filename)
            window["ImgOutputViewer"].update(filename=filename)
            img_input=Image.open(filename)
            #img_input.show
            
            #Size
            img_width, img_height=img_input.size
            window["ImgSize"].update("Image Size :"+str(img_width)+"x"+str(img_height))
            
            #Color Depth
            mode_to_coldepth={"1":1,"L":8,"P":8,"RGB":24,"RGBA":32,"CMYK":32, "YCbCr":24,"LAB":24,"HSV":24,"I":32,"F":32}
            coldepth=mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update("Color Depth :"+str(coldepth))
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
            window["ImgProcessingType"].update(f"Resampling -> {new_w}x{new_h} px")
            img_output = ImgResample(img_input, coldepth, new_w, new_h)
            save_output(img_output, window)
        except Exception as e:
            print(e)

    elif event == "-SCALE_SLIDER-":
        try:
            factor = float(values["-SCALE_SLIDER-"])  # faktor zoom
            window["ImgProcessingType"].update(f"Scaling x{factor:.1f}")
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
            window["ImgProcessingType"].update(f"Median Filter {k}x{k}")
            img_output = ImgMedianFilter(img_input, coldepth, k)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgMean":
        try:
            k = int(values["FilterKernel"])
            window["ImgProcessingType"].update(f"Mean Filter {k}x{k}")
            img_output = ImgMeanFilter(img_input, coldepth, k)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgGaussian":
        try:
            k = int(values["FilterKernel"])
            window["ImgProcessingType"].update(f"Gaussian Filter {k}x{k}")
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
            window["ImgProcessingType"].update("Robert Cross Filter")
            img_output = ImgRobertCrossFilter(img_input, coldepth)
            save_output(img_output, window)
        except:
            pass

    elif event == "ImgCompass":
        try:
            d = values["CompassDir"]
            window["ImgProcessingType"].update(f"Compass Filter ({d})")
            img_output = ImgCompassFilter(img_input, coldepth, d)
            save_output(img_output, window)
        except:
            pass
        
window.close()