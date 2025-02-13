import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
import matplotlib.patches as mpatches
import pandas as pd

# Soil footprint data (kg soil per kg food)
huella_suelo_ingredientes = {
    'Uva': 0.90,
    'Patata': 0.15,
    'Cebolla': 0.10,
    'Aceite': 3.50,
    'Trigo': 1.75,
    'Naranja': 0.20,
    'Melocotón': 0.25,
    'Cereza': 1.75,
    'Maiz': 0.25,
    'Pimiento': 0.25
}

# Function to calculate and plot soil consumption
def calcular_huella_suelo():
    # Data: Average annual consumption per person in Spain (kg) and soil footprint (kg soil/kg food)
    data = {
        'Cultivo': ['Vid (Uva de mesa + Vino)', 'Patata', 'Cebolla', 'Olivo (Aceituna + Aceite)', 'Trigo (Harina + Pan)', 
                    'Naranja', 'Melocotón', 'Cereza', 'Maíz', 'Pimiento'],
        'Consumo anual (kg/persona)': [10/0.75 + 2.1, 26, 8, 7 + 2.5, 30.4, 17, 3, 0.2, 2, 5.7],  # Example data
        'Huella de suelo (kg suelo/kg alimento)': [0.90, 0.15, 0.1, 3.50, 1.75, 0.2, 0.25, 1.75, 0.25, 0.25]  # Example data
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Calculate total soil consumption per year per person
    df['Kilos de suelo consumidos (kg/persona/año)'] = df['Consumo anual (kg/persona)'] * df['Huella de suelo (kg suelo/kg alimento)']
    total_suelo_consumido = df['Kilos de suelo consumidos (kg/persona/año)'].sum()

    # Display results
    print(f"Kilos de suelo consumidos al año por persona en total: {total_suelo_consumido:.2f} kg")
    print(df[['Cultivo', 'Kilos de suelo consumidos (kg/persona/año)']])

    # Bar chart: Soil consumption per crop
    plt.figure(figsize=(10, 6))
    plt.bar(df['Cultivo'], df['Kilos de suelo consumidos (kg/persona/año)'], color='skyblue')
    plt.title('Kilos de Suelo Consumidos al Año por Persona y por Cultivo')
    plt.xlabel('Cultivo')
    plt.ylabel('Kilos de Suelo (kg/persona/año)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Pie chart: Distribution of total soil consumption
    plt.figure(figsize=(10, 10))
    plt.pie(df['Kilos de suelo consumidos (kg/persona/año)'], labels=df['Cultivo'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Distribución del Consumo de Suelo por Cultivo (%)')
    plt.axis('equal')
    plt.show()

# Soil footprint data (kg of soil lost per kg of crop)
SOIL_FOOTPRINT = {
    'Grape': 0.90,
    'Potato': 0.15,
    'Onion': 0.10,
    'Olive': 3.50,
    'Wheat': 1.75,
    'Orange': 0.20,
    'Peach': 0.25,
    'Cherry': 1.75,
    'Corn': 0.25,
    'Pepper': 0.25
}

# Annual consumption per person in Spain (kg/person)
ANNUAL_CONSUMPTION = {
    'Grape': 10/0.75 + 2.1,
    'Potato': 26,
    'Onion': 8,
    'Olive': 7 + 2.5,
    'Wheat': 30.4,
    'Orange': 17,
    'Peach': 3,
    'Cherry': 0.2,
    'Corn': 2,
    'Pepper': 5.7
}

# Categorization of crops
FRUITS = ["Orange", "Peach", "Grape", "Cherry", "Olive"]
VEGETABLES = ["Potato", "Pepper", "Onion"]
CEREALS = ["Wheat", "Corn"]

# Assign colors based on categories
COLORS = {
    "Fruits": 'orange',
    "Vegetables": 'green',
    "Cereals": 'blue'
}

# Assign colors to each crop
CROP_COLORS = {
    crop: COLORS['Fruits'] if crop in FRUITS 
    else COLORS['Vegetables'] if crop in VEGETABLES 
    else COLORS['Cereals']
    for crop in SOIL_FOOTPRINT.keys()
}

def calculate_soil_loss():
    """
    Calculate the total kg of soil lost per person annually for each crop.
    """
    return {crop: SOIL_FOOTPRINT[crop] * ANNUAL_CONSUMPTION[crop] for crop in SOIL_FOOTPRINT.keys()}

def sort_by_category(data):
    """
    Sorts the data according to predefined categories: Fruits, Vegetables, and Cereals.
    """
    sorted_categories = FRUITS + VEGETABLES + CEREALS
    return {crop: data[crop] for crop in sorted_categories}

def sort_descending(data):
    """
    Sorts the data in descending order based on soil footprint values.
    """
    return dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

def plot_soil_footprint(data_type="soil footprint", sorting="descending"):
    """
    Plots a bar chart showing either the soil footprint per crop or the total soil lost per person annually.
    
    Parameters:
        data_type (str): "soil footprint" or "total soil lost"
        sorting (str): "descending" or "by category"
    """
    plt.figure(figsize=(10, 6))

    if data_type == "total soil lost":
        data = calculate_soil_loss()
    else:
        data = SOIL_FOOTPRINT

    if sorting == "by category":
        data = sort_by_category(data)
    else:
        data = sort_descending(data)

    colors = [CROP_COLORS[crop] for crop in data.keys()]
    
    plt.bar(data.keys(), data.values(), color=colors)
    plt.xlabel('Crop')
    plt.ylabel('Kg of Soil Lost per Kg of Crop' if data_type == "soil footprint" 
               else 'Kg of Soil Lost per Person Annually')
    plt.title(f'{data_type.capitalize()} ({sorting.capitalize()})')
    plt.xticks(rotation=45)

    # Add legend
    fruit_patch = mpatches.Patch(color=COLORS['Fruits'], label='Fruits')
    vegetable_patch = mpatches.Patch(color=COLORS['Vegetables'], label='Vegetables')
    cereal_patch = mpatches.Patch(color=COLORS['Cereals'], label='Cereals')
    plt.legend(handles=[fruit_patch, vegetable_patch, cereal_patch], title="Category")

    plt.show()

def interactive_soil_footprint():
    """
    Creates an interactive visualization where users can select the type of data and sorting method.
    """
    data_selector = widgets.Dropdown(
        options=['soil footprint', 'total soil lost'],
        value='soil footprint',
        description='Data:',
    )

    sorting_selector = widgets.Dropdown(
        options=['descending', 'by category'],
        value='descending',
        description='Sorting:',
    )

    output = widgets.Output()

    def update_plot(change=None):
        with output:
            output.clear_output(wait=True)
            plot_soil_footprint(data_selector.value, sorting_selector.value)

    data_selector.observe(update_plot, names='value')
    sorting_selector.observe(update_plot, names='value')

    display(data_selector, sorting_selector, output)

    with output:
        plot_soil_footprint(data_selector.value, sorting_selector.value)
