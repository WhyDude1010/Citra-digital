from PIL import Image, ImageOps
import math

def ImgNegative(img_input,coldepth):
    if coldepth !=24:
        img_input=img_input.convert('RGB')
        
    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()

    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r,g,b = img_input.getpixel((i,j))
            pixels[i,j] = (255-r,255-g,255-b)
        
    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output=img_output.convert("RGB")
    
    return img_output

def ImgRotate(img_input, coldepth, direction):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (height, width))
    pixels = img_output.load()

    for i in range(height):
        for j in range(width):
            if direction == "C":  # Clockwise
                r, g, b = img_input.getpixel((j, height - 1 - i))
            else:  # Counter Clockwise
                r, g, b = img_input.getpixel((width - 1 - j, i))
            
            pixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgFlip(img_input, coldepth, direction):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    if direction == "H":
        img_output = img_input.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        img_output = img_input.transpose(Image.FLIP_TOP_BOTTOM)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgBrightness(img_input, coldepth, value):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))

            r = max(0, min(255, r + value))
            g = max(0, min(255, g + value))
            b = max(0, min(255, b + value))

            pixels[i, j] = (r, g, b)  

    return img_output

def ImgBlending(img1, img2, coldepth, alpha):
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    w1, h1 = img1.size
    w2, h2 = img2.size
    
    out_width = max(w1, w2)
    out_height = max(h1, h2)

    img_output = Image.new('RGB', (out_width, out_height))
    pixels = img_output.load()

    for i in range(out_width):
        for j in range(out_height):
            in1 = (i < w1 and j < h1)
            in2 = (i < w2 and j < h2)

            if in1 and in2:
                r1, g1, b1 = img1.getpixel((i, j))
                r2, g2, b2 = img2.getpixel((i, j))
                r = int(alpha * r1 + (1 - alpha) * r2)
                g = int(alpha * g1 + (1 - alpha) * g2)
                b = int(alpha * b1 + (1 - alpha) * b2)
            elif in1:
                r, g, b = img1.getpixel((i, j))
            elif in2:
                r, g, b = img2.getpixel((i, j))
            else:
                r, g, b = 0, 0, 0

            pixels[i, j] = (r, g, b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgLogTransform(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()

    c = 255 / math.log(1 + 255)

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))

            r = int(c * math.log(1 + r))
            g = int(c * math.log(1 + g))
            b = int(c * math.log(1 + b))

            pixels[i, j] = (r, g, b)

    return img_output

def ImgPowerLaw(img_input, coldepth, gamma):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', img_input.size)
    pixels = img_output.load()

    c = 255 / (255 ** gamma)

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))

            r = int(c * (r ** gamma))
            g = int(c * (g ** gamma))
            b = int(c * (b ** gamma))

            pixels[i, j] = (r, g, b)

    return img_output

def ImgResample(img_input, coldepth, new_width, new_height):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    old_width, old_height = img_input.size
    img_output = Image.new('RGB', (new_width, new_height))
    pixels = img_output.load()

    for i in range(new_width):
        for j in range(new_height):
            src_x = int(i * old_width / new_width)
            src_y = int(j * old_height / new_height)
            pixels[i, j] = img_input.getpixel((src_x, src_y))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output



def ImgScaling(img_input, coldepth, scale_factor):

    if coldepth != 24:
        img_input = img_input.convert("RGB")

    old_width, old_height = img_input.size

    new_width = int(old_width * scale_factor)
    new_height = int(old_height * scale_factor)

    img_output = Image.new("RGB", (new_width, new_height))

    for x in range(new_width):
        for y in range(new_height):

            src_x = int(x / scale_factor)
            src_y = int(y / scale_factor)

            pixel = img_input.getpixel((src_x, src_y))

            img_output.putpixel((x, y), pixel)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgMedianFilter(img_input, coldepth, kernel_size):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    half = kernel_size // 2
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            r_list, g_list, b_list = [], [], []
            for ki in range(-half, half + 1):
                for kj in range(-half, half + 1):
                    ni = min(max(i + ki, 0), width - 1)
                    nj = min(max(j + kj, 0), height - 1)
                    r, g, b = img_input.getpixel((ni, nj))
                    r_list.append(r)
                    g_list.append(g)
                    b_list.append(b)
            r_list.sort()
            g_list.sort()
            b_list.sort()
            mid = len(r_list) // 2
            pixels[i, j] = (r_list[mid], g_list[mid], b_list[mid])

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgMeanFilter(img_input, coldepth, kernel_size):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    half = kernel_size // 2
    total = kernel_size * kernel_size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            r_sum, g_sum, b_sum = 0, 0, 0
            for ki in range(-half, half + 1):
                for kj in range(-half, half + 1):
                    ni = min(max(i + ki, 0), width - 1)
                    nj = min(max(j + kj, 0), height - 1)
                    r, g, b = img_input.getpixel((ni, nj))
                    r_sum += r
                    g_sum += g
                    b_sum += b
            pixels[i, j] = (r_sum // total, g_sum // total, b_sum // total)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgGaussianFilter(img_input, coldepth, kernel_size):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    half = kernel_size // 2
    sigma = kernel_size / 6.0

    kernel = []
    k_sum = 0
    for ki in range(-half, half + 1):
        row = []
        for kj in range(-half, half + 1):
            val = math.exp(-(ki * ki + kj * kj) / (2 * sigma * sigma))
            row.append(val)
            k_sum += val
        kernel.append(row)

    for ki in range(kernel_size):
        for kj in range(kernel_size):
            kernel[ki][kj] /= k_sum

    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            r_val, g_val, b_val = 0.0, 0.0, 0.0
            for ki in range(-half, half + 1):
                for kj in range(-half, half + 1):
                    ni = min(max(i + ki, 0), width - 1)
                    nj = min(max(j + kj, 0), height - 1)
                    w = kernel[ki + half][kj + half]
                    r, g, b = img_input.getpixel((ni, nj))
                    r_val += r * w
                    g_val += g * w
                    b_val += b * w
            pixels[i, j] = (int(r_val), int(g_val), int(b_val))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def _apply_3x3(img_input, kx, ky):
    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            rx, gx, bx = 0, 0, 0
            ry, gy, by = 0, 0, 0
            for ki in range(-1, 2):
                for kj in range(-1, 2):
                    ni = min(max(i + ki, 0), width - 1)
                    nj = min(max(j + kj, 0), height - 1)
                    r, g, b = img_input.getpixel((ni, nj))
                    wx = kx[ki + 1][kj + 1]
                    wy = ky[ki + 1][kj + 1]
                    rx += r * wx; gx += g * wx; bx += b * wx
                    ry += r * wy; gy += g * wy; by += b * wy
            rm = min(255, int(math.sqrt(rx*rx + ry*ry)))
            gm = min(255, int(math.sqrt(gx*gx + gy*gy)))
            bm = min(255, int(math.sqrt(bx*bx + by*by)))
            pixels[i, j] = (rm, gm, bm)

    return img_output

def ImgSobelFilter(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    kx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    ky = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    img_output = _apply_3x3(img_input, kx, ky)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgPrewittFilter(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    kx = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    ky = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]

    img_output = _apply_3x3(img_input, kx, ky)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgRobertCrossFilter(img_input, coldepth):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            ni = min(i + 1, width - 1)
            nj = min(j + 1, height - 1)
            r00, g00, b00 = img_input.getpixel((i, j))
            r11, g11, b11 = img_input.getpixel((ni, nj))
            r10, g10, b10 = img_input.getpixel((ni, j))
            r01, g01, b01 = img_input.getpixel((i, nj))
            gx_r = r00 - r11; gy_r = r10 - r01
            gx_g = g00 - g11; gy_g = g10 - g01
            gx_b = b00 - b11; gy_b = b10 - b01
            rm = min(255, int(math.sqrt(gx_r*gx_r + gy_r*gy_r)))
            gm = min(255, int(math.sqrt(gx_g*gx_g + gy_g*gy_g)))
            bm = min(255, int(math.sqrt(gx_b*gx_b + gy_b*gy_b)))
            pixels[i, j] = (rm, gm, bm)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgCompassFilter(img_input, coldepth, direction):
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    compass_kernels = {
        "N":  [[ 1,  1,  1], [ 0,  0,  0], [-1, -1, -1]],
        "NE": [[ 0,  1,  1], [-1,  0,  1], [-1, -1,  0]],
        "E":  [[-1,  0,  1], [-1,  0,  1], [-1,  0,  1]],
        "SE": [[-1, -1,  0], [-1,  0,  1], [ 0,  1,  1]],
        "S":  [[-1, -1, -1], [ 0,  0,  0], [ 1,  1,  1]],
        "SW": [[ 0, -1, -1], [ 1,  0, -1], [ 1,  1,  0]],
        "W":  [[ 1,  0, -1], [ 1,  0, -1], [ 1,  0, -1]],
        "NW": [[ 1,  1,  0], [ 1,  0, -1], [ 0, -1, -1]],
    }

    if direction == "ALL":
        kernels = list(compass_kernels.values())
    else:
        kernels = [compass_kernels[direction]]

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()

    for i in range(width):
        for j in range(height):
            max_r, max_g, max_b = 0, 0, 0
            for kern in kernels:
                sr, sg, sb = 0, 0, 0
                for ki in range(-1, 2):
                    for kj in range(-1, 2):
                        ni = min(max(i + ki, 0), width - 1)
                        nj = min(max(j + kj, 0), height - 1)
                        r, g, b = img_input.getpixel((ni, nj))
                        w = kern[ki + 1][kj + 1]
                        sr += r * w; sg += g * w; sb += b * w
                max_r = max(max_r, abs(sr))
                max_g = max(max_g, abs(sg))
                max_b = max(max_b, abs(sb))
            pixels[i, j] = (min(255, max_r), min(255, max_g), min(255, max_b))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output