import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt
import pandas as pd

def run_soil_footprint_app():
    # Data for Soil Footprint of Different Foods (kg soil per kg food)
    soil_footprint_data = {
        'Food Item': ['Rice', 'Potatoes', 'Beer', 'Wine', 'Olive oil', 'Sunflower oil', 'Oranges', 'Peaches', 'Rye bread', 'Wheat bread'],
        'Soil Footprint (kg soil/kg food)': [1.20, 0.38, 0.6, 0.8, 5.00, 2.50, 0.83, 0.75, 1.5, 1.67],
        'Consumption (grams per day)': [120, 300, 500, 200, 20, 20, 200, 150, 50, 70]
    }

    # Convert data to DataFrame
    soil_footprint_df = pd.DataFrame(soil_footprint_data)

    # Dropdown options
    dropdown_options = {
        'Rice or Potatoes': ('Rice', 'Potatoes'),
        'Beer or Wine': ('Beer', 'Wine'),
        'Olive oil or Sunflower oil': ('Olive oil', 'Sunflower oil'),
        'Oranges or Peaches': ('Oranges', 'Peaches'),
        'Rye bread or Wheat bread': ('Rye bread', 'Wheat bread')
    }

    # Create dropdown widgets
    dropdowns = {key: widgets.Dropdown(options=options, description=key, style={'description_width': 'initial'}) for key, options in dropdown_options.items()}

    output = widgets.Output()

    def calculate_total_soil_footprint(choices):
        total_loss_per_year, min_loss_per_year = 0, 0
        footprint_by_item, loss_by_item_per_year = {}, {}

        for choice, options in choices.items():
            selected_food_data = soil_footprint_df[soil_footprint_df['Food Item'] == choice].iloc[0]
            footprint_per_kg = selected_food_data['Soil Footprint (kg soil/kg food)']
            daily_consumption_grams = selected_food_data['Consumption (grams per day)']
            annual_consumption_kg = (daily_consumption_grams / 1000) * 365
            total_loss_per_year += footprint_per_kg * annual_consumption_kg
            footprint_by_item[choice] = footprint_per_kg
            loss_by_item_per_year[choice] = footprint_per_kg * annual_consumption_kg
            min_loss_per_year += min(
                [soil_footprint_df.loc[soil_footprint_df['Food Item'] == opt, 'Soil Footprint (kg soil/kg food)'].values[0] *
                 (soil_footprint_df.loc[soil_footprint_df['Food Item'] == opt, 'Consumption (grams per day)'].values[0] / 1000 * 365)
                 for opt in options]
            )
        
        return total_loss_per_year, min_loss_per_year, footprint_by_item, loss_by_item_per_year

    def recommend_food_to_reduce_loss(selected_choices):
        non_selected_items = soil_footprint_df[~soil_footprint_df['Food Item'].isin(selected_choices.keys())]
        min_loss_item, min_loss_value = None, float('inf')
        
        for _, row in non_selected_items.iterrows():
            total_loss = row['Soil Footprint (kg soil/kg food)'] * (row['Consumption (grams per day)'] / 1000) * 365
            if total_loss < min_loss_value:
                min_loss_value, min_loss_item = total_loss, row['Food Item']
        
        return min_loss_item, min_loss_value

    def plot_soil_footprint(choices, total_loss_per_year, min_loss_per_year, footprint_by_item, loss_by_item_per_year):
        food_items = list(choices.keys())
        soil_footprints = [footprint_by_item[food] for food in food_items]
        weighted_losses = [loss_by_item_per_year[food] for food in food_items]

        plt.figure(figsize=(10, 5))
        plt.bar(food_items, soil_footprints, color='skyblue')
        plt.title('Soil Footprint of Selected Food Items (kg soil per kg food)')
        plt.ylabel('Soil Footprint (kg soil/kg food)')
        plt.xticks(rotation=45)
        plt.show()

        plt.figure(figsize=(6, 4))
        plt.bar(['Selected Total', 'Minimum Possible'], [total_loss_per_year, min_loss_per_year], color=['skyblue', 'lightgreen'])
        plt.title('Total Soil Loss vs Minimum Possible (kg soil per year)')
        plt.ylabel('Total Soil Loss (kg soil/year)')
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.bar(food_items, weighted_losses, color='orange')
        plt.title('Weighted Soil Loss of Selected Food Items (kg soil per year)')
        plt.ylabel('Soil Loss (kg soil/year)')
        plt.xticks(rotation=45)
        plt.show()

    def update_total_soil_footprint(change):
        selected_choices = {dropdown.value: options for key, options in dropdown_options.items() for dropdown in dropdowns.values() if dropdown.value in options}
        total_loss_per_year, min_loss_per_year, footprint_by_item, loss_by_item_per_year = calculate_total_soil_footprint(selected_choices)
        recommended_food, reduction = recommend_food_to_reduce_loss(selected_choices)

        with output:
            clear_output()
            print("You have selected the following food items:")
            for key in selected_choices.keys():
                print(f"{key}")
            print(f"\nTotal Soil Loss (kg soil/year): {total_loss_per_year:.4f}")
            print(f"Minimum Possible Soil Loss (kg soil/year): {min_loss_per_year:.4f}")
            print(f"By choosing the more sustainable options, you could reduce your soil loss by {total_loss_per_year - min_loss_per_year:.4f} kg/year.")
            print(f"\nRecommendation: If you switch to {recommended_food}, you could reduce your soil loss by an additional {reduction:.4f} kg/year.")
            plot_soil_footprint(selected_choices, total_loss_per_year, min_loss_per_year, footprint_by_item, loss_by_item_per_year)

    for dropdown in dropdowns.values():
        dropdown.observe(update_total_soil_footprint, names='value')

    display(*dropdowns.values(), output)
    update_total_soil_footprint(None)
    

# Soil footprint data for ingredients (kg soil per kg food)
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

# Meal data: ingredients and their quantities in grams
comidas_data = {
    'Comida': ['Vaso de vino', 'Tortilla de patatas (con cebolla)', 'Tortilla de patatas (sin cebolla)', 
               'Tostada con aceite', 
               'Ración de fruta (naranja)', 'Ración de fruta (melocotón)', 'Ración de fruta (cereza)'],
    'Ingredientes': [
        {'Uva': 200},  # Vino: 200g de uvas
        {'Patata': 200, 'Cebolla': 50, 'Aceite': 30},  # Tortilla con cebolla
        {'Patata': 250, 'Aceite': 30},  # Tortilla sin cebolla
        {'Trigo': 70, 'Aceite': 15},  # Tostada con aceite
        {'Naranja': 150},  # Ración de fruta (naranja)
        {'Melocotón': 150},  # Ración de fruta (melocotón)
        {'Cereza': 150}  # Ración de fruta (cereza)
    ]
}

# Soil footprint data for ingredients (kg soil per kg food)
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

# Meal data: ingredients and their quantities in grams
comidas_data = {
    'Comida': ['Vaso de vino', 'Tortilla de patatas (con cebolla)', 'Tortilla de patatas (sin cebolla)', 
               'Tostada con aceite', 
               'Ración de fruta (naranja)', 'Ración de fruta (melocotón)', 'Ración de fruta (cereza)'],
    'Ingredientes': [
        {'Uva': 200},  # Vino: 200g de uvas
        {'Patata': 200, 'Cebolla': 50, 'Aceite': 30},  # Tortilla con cebolla
        {'Patata': 250, 'Aceite': 30},  # Tortilla sin cebolla
        {'Trigo': 70, 'Aceite': 15},  # Tostada con aceite
        {'Naranja': 150},  # Ración de fruta (naranja)
        {'Melocotón': 150},  # Ración de fruta (melocotón)
        {'Cereza': 150}  # Ración de fruta (cereza)
    ]
}

# Function to calculate soil footprint of a meal
def calcular_huella_suelo_comida(ingredientes):
    huella_total = 0
    for ingrediente, cantidad in ingredientes.items():
        cantidad_kg = cantidad / 1000  # Convert grams to kg
        huella_suelo = huella_suelo_ingredientes[ingrediente] * cantidad_kg
        huella_total += huella_suelo
    return huella_total

# Function to calculate the total weight of a meal
def calcular_peso_total_comida(ingredientes):
    return sum(ingredientes.values())

# Function to update and display the graphs
def actualizar_graficas(comida_seleccionada):
    index = comidas_data['Comida'].index(comida_seleccionada)
    ingredientes_seleccionados = comidas_data['Ingredientes'][index]

    huella_suelo_comida = calcular_huella_suelo_comida(ingredientes_seleccionados)
    peso_total_comida = calcular_peso_total_comida(ingredientes_seleccionados)

    print(f"\nHas seleccionado: {comida_seleccionada}")
    print(f"Huella de suelo de esta comida: {huella_suelo_comida:.4f} kg de suelo consumido")
    print(f"Peso total de la comida: {peso_total_comida} gramos")

    # Bar chart: Soil footprint per ingredient
    ingredientes = list(ingredientes_seleccionados.keys())
    huellas_por_ingrediente = [huella_suelo_ingredientes[ingrediente] * (cantidad / 1000) for ingrediente, cantidad in ingredientes_seleccionados.items()]
    
    plt.figure(figsize=(10, 6))
    plt.bar(ingredientes, huellas_por_ingrediente, color='lightgreen')
    plt.title(f'Huella de Suelo por Ingrediente para {comida_seleccionada}')
    plt.xlabel('Ingrediente')
    plt.ylabel('Huella de Suelo (kg suelo)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Calculate weight and soil footprint percentage distributions
    porcentajes_peso = [(cantidad / peso_total_comida) * 100 for cantidad in ingredientes_seleccionados.values()]
    huella_total = sum(huellas_por_ingrediente)
    porcentajes_huella = [(huella / huella_total) * 100 for huella in huellas_por_ingrediente]

    # Pie charts: Ingredient weight distribution vs. soil footprint distribution
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    axs[0].pie(porcentajes_peso, labels=ingredientes, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    axs[0].set_title(f'Distribución del Peso de Ingredientes\n en {comida_seleccionada}')

    axs[1].pie(porcentajes_huella, labels=ingredientes, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    axs[1].set_title(f'Distribución de la Huella de Suelo\n en {comida_seleccionada}')

    axs[0].axis('equal')
    axs[1].axis('equal')

    plt.show()

# Function to create and display the interactive widget
def mostrar_selector_comida():
    menu_desplegable = widgets.Dropdown(
        options=comidas_data['Comida'],
        description='Comida:',
        disabled=False
    )
    widgets.interact(actualizar_graficas, comida_seleccionada=menu_desplegable)
