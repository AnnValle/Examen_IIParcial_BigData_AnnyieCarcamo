import pandas as pd
import numpy as np
import re
from pathlib import Path


def limpiar_nombre(nombre):
    """Limpia el nombre para ser usado en rutas de carpetas y archivos."""
    
    cleaned = re.sub(r'[^\w\s\-\.]', '', str(nombre)).strip()
    
    cleaned = re.sub(r'[\s\.\-]+', '_', cleaned)
    return cleaned


OUTPUT_DIR = Path('salidas')
OUTPUT_DIR.mkdir(exist_ok=True)
global_summary_list = []

try:
    df = pd.read_csv('ventas.csv')
except FileNotFoundError:
    print("Error: No se encontró 'ventas.csv'.")
    exit()


for col in ['Total', 'PrecioUnitario']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)


print("--- Exportación Segmentada por Producto ---")


for product_name, group in df.groupby('Producto'):
    cleaned_name = limpiar_nombre(product_name)
    

    product_folder = OUTPUT_DIR / f'Producto={cleaned_name}'
    product_folder.mkdir(exist_ok=True)
    

    total_ventas = group['Total'].sum()
    cantidad_registros = len(group)
    precio_unitario_promedio = group['PrecioUnitario'].mean()


    global_summary_list.append({
        'Producto': product_name,
        'Total_Ventas': total_ventas,
        'Cantidad_Registros': cantidad_registros,
        'Precio_Unitario_Promedio': precio_unitario_promedio
    })


    group.to_csv(product_folder / 'archivo.csv', index=False, float_format='%.2f')
    

    with open(product_folder / 'resumen.txt', 'w', encoding='utf-8') as f:
        f.write(f"Producto: {product_name}\n")
        f.write(f"Total de ventas del producto: {total_ventas:,.2f}\n")
        f.write(f"Cantidad de registros: {cantidad_registros}\n")
        f.write(f"Precio Unitario promedio: {precio_unitario_promedio:,.2f}\n")
    
    print(f"Exportado: {product_folder.name} con {cantidad_registros} registros.")


print("\n--- Generación de Resumen Global ---")
df_resumen_global = pd.DataFrame(global_summary_list)


df_resumen_global.to_csv('resumen_global_productos.csv', index=False, float_format='%.2f')
print("Archivo 'resumen_global_productos.csv' creado con el resumen de métricas por producto.")
print("\n¡Proceso de exportación avanzada finalizado!")