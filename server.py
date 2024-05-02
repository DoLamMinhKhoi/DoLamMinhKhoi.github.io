from flask import Flask, request, url_for, render_template, flash 
from random import randint
from numpy import arcsin

import math
import os
from PIL import Image, ImageDraw
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'mabimat'

element_radius = {
    "H": 0.53, "He": 0.31, "Li": 1.67, "Be": 1.12, "B": 0.87, "C": 0.67, "N": 0.56, "O": 0.48, "F": 0.42,
    "Na": 1.90, "Mg": 1.45, "Al": 1.18, "Si": 1.11, "P": 0.98, "S": 0.88, "Cl": 0.79,
    "K": 2.43, "Ca": 1.94, "Sc": 1.84, "Ti": 1.76, "V": 1.71, "Cr": 1.66, "Mn": 1.61, "Fe": 1.56,
    "Co": 1.52, "Ni": 1.49, "Cu": 1.45, "Zn": 1.42, "Ga": 1.36, "Ge": 1.25, "As": 1.14, "Se": 1.03, "Br": 0.94,
    "Rb": 2.65, "Sr": 2.19, "Y": 2.12, "Zr": 2.06, "Nb": 1.98, "Mo": 1.90, "Tc": 1.83, "Ru": 1.78, "Rh": 1.73,
    "Pd": 1.69, "Ag": 1.65, "Cd": 1.61, "In": 1.56, "Sn": 1.45, "Sb": 1.33, "Te": 1.23, "I": 1.15,
    "Cs": 2.98, "Ba": 2.53, "La": 1.95, "Ce": 1.85, "Pr": 2.47, "Nd": 2.06, "Pm": 2.05, "Sm": 2.38,
    "Eu": 2.31, "Gd": 2.33, "Tb": 2.25, "Dy": 2.28, "Ho": 2.26, "Er": 2.26, "Tm": 2.22, "Yb": 2.22, "Lu": 2.17,
    "Hf": 2.08, "Ta": 2.00, "W": 1.93, "Re": 1.88, "Os": 1.85, "Ir": 1.80, "Pt": 1.77, "Au": 1.74, "Hg": 1.71,
    "Tl": 1.56, "Pb": 1.54, "Bi": 1.43, "Po": 1.35, "At": 1.27, "Fr": None, "Ra": None, "Ac": 1.95,
    "Th": 1.80, "Pa": 1.80, "U": 1.75, "Np": 1.75, "Pu": 1.75, "Am": 1.75, "Cm": None
}

element_list = [
    "H", "Li", "Be", "B", "C", "N", "O", "F", "Na", "Mg", "Al",
    "Si", "P", "S", "Cl", "K", "Ar", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe",
    "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",
    "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb",
    "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu",
    "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re",
    "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr",
    "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm"
]

element_periods = {
    "H": 1, "He": 1,
    "Li": 2, "Be": 2, "B": 2, "C": 2, "N": 2, "O": 2, "F": 2, "Ne": 2,
    "Na": 3, "Mg": 3, "Al": 3, "Si": 3, "P": 3, "S": 3, "Cl": 3, "Ar": 3,
    "K": 4, "Ca": 4, "Sc": 4, "Ti": 4, "V": 4, "Cr": 4, "Mn": 4, "Fe": 4, "Co": 4, "Ni": 4, "Cu": 4, "Zn": 4,
    "Ga": 4, "Ge": 4, "As": 4, "Se": 4, "Br": 4, "Kr": 4,
    "Rb": 5, "Sr": 5, "Y": 5, "Zr": 5, "Nb": 5, "Mo": 5, "Tc": 5, "Ru": 5,
    "Rh": 5, "Pd": 5, "Ag": 5, "Cd": 5, "In": 5, "Sn": 5, "Sb": 5, "Te": 5, "I": 5, "Xe": 5,
    "Cs": 6, "Ba": 6, "La": 6, "Hf": 6, "Ta": 6, "W": 6, "Re": 6, "Os": 6, "Ir": 6, "Pt": 6,
    "Au": 6, "Hg": 6, "Tl": 6, "Pb": 6, "Bi": 6, "Po": 6, "At": 6, "Rn": 6,
    "Fr": 7, "Ra": 7, "Ac": 7, "Th": 7, "Pa": 7, "U": 7, "Np": 7, "Pu": 7, "Am": 7, "Cm": 7
}


element_valence_electrons = {
    "H": 1, "He": 2, "Li": 1, "Be": 2, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8,
    "Na": 1, "Mg": 2, "Al": 3, "Si": 4, "P": 5, "S": 6, "Cl": 7, "K": 1, "Ar": 8, "Ca": 2,
    "Sc": 2, "Ti": 2, "V": 2, "Cr": 1, "Mn": 2, "Fe": 2, "Co": 2, "Ni": 2, "Cu": 1, "Zn": 2,
    "Ga": 3, "Ge": 4, "As": 5, "Se": 6, "Br": 7, "Kr": 8, "Rb": 1, "Sr": 2, "Y": 2, "Zr": 2,
    "Nb": 1, "Mo": 1, "Tc": 2, "Ru": 1, "Rh": 1, "Pd": 0, "Ag": 1, "Cd": 2, "In": 3, "Sn": 4,
    "Sb": 5, "Te": 6, "I": 7, "Xe": 8, "Cs": 1, "Ba": 2, "La": 3, "Ce": 4, "Pr": 4, "Nd": 4,
    "Pm": 4, "Sm": 4, "Eu": 4, "Gd": 4, "Tb": 4, "Dy": 4, "Ho": 4, "Er": 4, "Tm": 4, "Yb": 4,
    "Lu": 3, "Hf": 4, "Ta": 5, "W": 6, "Re": 7, "Os": 8, "Ir": 9, "Pt": 10, "Au": 1, "Hg": 2,
    "Tl": 3, "Pb": 4, "Bi": 5, "Po": 6, "At": 7, "Rn": 8, "Fr": 1, "Ra": 2, "Ac": 3, "Th": 4,
    "Pa": 5, "U": 6, "Np": 7, "Pu": 8, "Am": 9, "Cm": 10,
}

element_ElectroNegativity = {'H': 2.2, 'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 
              'F': 3.98, 'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.9, 'P': 2.19, 'S': 2.58, 
              'Cl': 3.16, 'K': 0.82, 'Ca': 1, 'Sc': 1.36, 'Ti': 1.54, 'V': 1.63, 'Cr': 1.66, 
              'Mn': 1.55, 'Fe': 1.83, 'Co': 1.88, 'Ni': 1.91, 'Cu': 1.9, 'Zn': 1.65, 'Ga': 1.81, 'Ge': 2.01, 
              'As': 2.18, 'Se': 2.55, 'Br': 2.96, 'Kr': 3, 'Rb': 0.82, 'Sr': 0.95, 'Y': 1.22, 'Zr': 1.33, 
              'Nb': 1.6, 'Mo': 2.16, 'Tc': 1.9, 'Ru': 2.2, 'Rh': 2.28, 'Pd': 2.2, 'Ag': 1.93, 'Cd': 1.69, 
              'In': 1.78, 'Sn': 1.96, 'Sb': 2.05, 'Te': 2.1, 'I': 2.66, 'Xe': 2.6, 'Cs': 0.79, 'Ba': 0.89, 
              'La': 1.1, 'Ce': 1.12, 'Pr': 1.13, 'Nd': 1.14, 'Pm': 1.13, 'Sm': 1.17, 'Eu': 1.2, 
              'Gd': 1.2, 'Tb': 1.22, 'Dy': 1.23, 'Ho': 1.24, 'Er': 1.24, 'Tm': 1.25, 'Yb': 1.1, 'Lu': 1.27, 
              'Hf': 1.3, 'Ta': 1.5, 'W': 2.36, 'Re': 1.9, 'Os': 2.2, 'Ir': 2.2, 'Pt': 2.28, 'Au': 2.54, 
              'Hg': 2, 'Tl': 1.62, 'Pb': 2.33, 'Bi': 2.02, 'Po': 2, 'At': 2.2, 'Fr': 0.7,
              'Ra': 0.89, 'Ac': 1.1, 'Th': 1.3, 'Pa': 1.5, 'U': 1.38, 'Np': 1.36, 'Pu': 1.28, 'Am': 1.3, 
              'Cm': 1.3, 'Bk': 1.3, 'Cf': 1.3, 'Es': 1.3, 'Fm': 1.3, 'Md': 1.3, 'No': 1.3
}

noble_gas_list = ["He", "Ne", "Ar", "Kr", "Xe", "Rn"]

# app.config['UPLOAD_FOLDER'] = 'C:/Users/Admin/Downloads/ElementBonding (3)/static/images'
app.config['UPLOAD_FOLDER'] = 'D:\Minh Khôi\SIU\THI\CUỐI HK6\HÓA\ElementBonding (4)\ElementBonding (3)\static\images'

@app.route('/', methods=['GET', 'POST'])
def home():
    first_element_radius = None
    second_element_radius = None
    first_imageE_data = None
    second_imageE_data = None
    first_element_electronegativity = None
    second_element_electronegativity = None
    electronegativity_difference = None
    bond_type = 'Chưa tính toán'
    bond_color = '#888888'  # Màu sắc mặc định
    text_color = '#000000'
    border_radius = '5px'
    border_thickness = '3px'
    
    if request.method == 'POST':
        # Lấy thông tin số electron lớp ngoài cùng từ từ điển
        first_element = request.form.get('fElement').capitalize()
        second_element = request.form.get('sElement').capitalize()

        if first_element in element_list and second_element in element_list:
            try:
                first_element_radius = element_radius.get(first_element)
                second_element_radius = element_radius.get(second_element)
                first_element_electronegativity = element_ElectroNegativity.get(first_element)
                second_element_electronegativity = element_ElectroNegativity.get(second_element)

                if first_element_electronegativity is not None and second_element_electronegativity is not None:
                    electronegativity_difference = abs(first_element_electronegativity - second_element_electronegativity)
                    if electronegativity_difference >= 1.7:
                        bond_type = 'Liên kết ion'
                        bond_color = '#FFBF00'  # Example: Red for ionic
                        text_color = '#8B0000'  # White text color
                    elif electronegativity_difference > 0.4:
                        bond_type = 'Liên kết cộng hoá trị phân cực'
                        bond_color = '#b87333'  # Example: Yellow for polar covalent
                        text_color = '#000080'  # Black text color
                    else:
                        bond_type = 'Liên kết cộng hoá trị không phân cực'
                        bond_color = '#40E0D0'  # Example: Green for nonpolar covalent
                        text_color = '#008000'  # Black text color

                first_imageE_data = draw_first_element_electrons(first_element, first_element_radius, element_valence_electrons.get(first_element, 0), app.config['UPLOAD_FOLDER'], bond_type)
                second_imageE_data = draw_second_element_electrons(second_element, second_element_radius, element_valence_electrons.get(second_element, 0), app.config['UPLOAD_FOLDER'], bond_type)
    
            except FileNotFoundError:
                flash(f'Không tìm thấy hình ảnh cho nguyên tố "{first_element} {second_element}"', 'error')
                first_imageE_data = None
                second_imageE_data = None
    
    # Render the template with the image URLs (will be None if invalid or empty)
    return render_template('index.html', 
                           first_element_radius=first_element_radius,
                           second_element_radius=second_element_radius,
                           first_imageE_data=first_imageE_data,
                           second_imageE_data=second_imageE_data,
                           electronegativity_difference=electronegativity_difference,
                           bond_type=bond_type,
                           bond_color=bond_color,
                           text_color=text_color,
                           border_radius=border_radius, 
                           border_thickness=border_thickness)

def get_element_color(element_symbol, upload_folder):
    image_path = os.path.join(upload_folder, f'{element_symbol}3.png')  # Đường dẫn đến file ảnh nguyên tố
    with Image.open(image_path) as img:
        width, height = img.size
        center = (width // 2, height // 2)
        return img.getpixel(center)

def draw_first_element_electrons(element_symbol, radius, valence_electrons, upload_folder, bond_type, border_size=200):
    if bond_type == 'Liên kết ion':
        element_color = None
        image_suffix = '1.png' 
        element_image_path = os.path.join(upload_folder, f'{element_symbol}{image_suffix}')
        return none_draw(math.pi / 2, radius, element_image_path, valence_electrons, element_color, border_size=border_size)
    else:
        element_color = get_element_color(element_symbol, upload_folder)
        image_suffix = '2.png'
        element_image_path = os.path.join(upload_folder, f'{element_symbol}{image_suffix}')
        return draw_electrons_on_image(math.pi / 2, radius, element_image_path, valence_electrons, element_color, border_size=border_size)

def draw_second_element_electrons(element_symbol, radius, valence_electrons, upload_folder, bond_type, border_size=200):
    if bond_type == 'Liên kết ion':
        element_color = None
        image_suffix = '1.png'  
        element_image_path = os.path.join(upload_folder, f'{element_symbol}{image_suffix}')
        return none_draw(math.pi / 2, radius, element_image_path, valence_electrons, element_color, border_size=border_size)
    else:
        element_color = get_element_color(element_symbol, upload_folder)
        image_suffix = '2.png' 
        element_image_path = os.path.join(upload_folder, f'{element_symbol}{image_suffix}')
        return draw_electrons_on_image(-math.pi / 2, radius, element_image_path, valence_electrons, element_color, border_size=border_size)
    
def none_draw(start_angle, element_radius, element_image_path, valence_electrons, electron_color, border_size=500):
    with Image.open(element_image_path) as img:
        valency = min(8 - valence_electrons, valence_electrons)
        width, height = img.size
        new_width = width + 2 * border_size
        new_height = height + 2 * border_size

        new_img = Image.new('RGB', (new_width, new_height), 'white')
        new_img.paste(img, (border_size, border_size))

        draw = ImageDraw.Draw(new_img)
        center = (new_width // 2, new_height // 2)
        radius = min(width, height) // 2 * 1.5  
        
        buffered = BytesIO()
        new_img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"


def draw_electrons_on_image(start_angle, element_radius, element_image_path, valence_electrons, electron_color, num_orbitals=1, border_size=500):
    with Image.open(element_image_path) as img:
        valency = min(8 - valence_electrons, valence_electrons)
        width, height = img.size
        new_width = width + 2 * border_size
        new_height = height + 2 * border_size

        new_img = Image.new('RGB', (new_width, new_height), 'white')
        new_img.paste(img, (border_size, border_size))

        draw = ImageDraw.Draw(new_img)
        center = (new_width // 2, new_height // 2)
        radius = min(width, height) // 2 * 1.5
        
        center_x, center_y = new_width // 2, new_height // 2
        spacing = 20  # Khoảng cách giữa các quỹ đạo
        
        for i in range(num_orbitals):
            orbit_radius = min(width, height) // 2 + border_size // 2 - i * spacing
            draw.ellipse((center_x - orbit_radius, center_y - orbit_radius,
                          center_x + orbit_radius, center_y + orbit_radius),
                         outline="black", width=3, fill=None)
        
        i = 0
        pairs = (valence_electrons - valency) // 2 + 1
        electron_angle = 10 * math.pi / 180
        while valence_electrons > valency:
            # draw first electron in pair
            angle = 2 * math.pi * i / pairs - electron_angle + start_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')

            # draw second electron in pair
            angle = 2 * math.pi * i / pairs + electron_angle + start_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')
            i += 1
            valence_electrons -= 2

        if valency == 1:
            angle = start_angle - math.pi / 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')
        elif valency == 2:
            electron_angle = arcsin(22 / (150 * element_radius))
            # draw first electron in pair
            angle = start_angle - math.pi / 2 - electron_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')

            # draw second electron in pair
            angle = start_angle - math.pi / 2 + electron_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')
        else:
            angle = start_angle - math.pi / 2
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')

            electron_angle = arcsin(45 / (150 * element_radius))
            # draw first electron in pair
            angle = start_angle - math.pi / 2 - electron_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')

            # draw second electron in pair
            angle = start_angle - math.pi / 2 + electron_angle
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            draw.ellipse((x - (35 / element_radius), y - (35 / element_radius), x + (35 / element_radius), y + (35 / element_radius)), fill=electron_color, outline='black')

        # for i in range(valence_electrons):
        #     angle = 2 * math.pi * i / valence_electrons
        #     x = center[0] + radius * math.cos(angle)
        #     y = center[1] + radius * math.sin(angle)
        #     draw.ellipse((x - 50, y - 50, x + 50, y + 50), fill=electron_color, outline='black')

        buffered = BytesIO()
        new_img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"


if __name__ == '__main__':
    app.run(debug=True)
