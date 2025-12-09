import pandas as pd
import numpy as np


try:
    df_ventas = pd.read_csv('ventas.csv')
    df_clientes = pd.read_csv('Clientes.csv')
except FileNotFoundError:
    print("Error: Asegúrese de que 'ventas.csv' y 'Clientes.csv' existan.")
    exit()


df_ventas['Total'] = pd.to_numeric(df_ventas['Total'], errors='coerce').fillna(0)
df_ventas['PrecioUnitario'] = pd.to_numeric(df_ventas['PrecioUnitario'], errors='coerce').fillna(0)


df_integrado = df_ventas.merge(df_clientes[['Cliente', 'Ciudad', 'Categoria_Cliente']], 
                              on='Cliente', 
                              how='left')


print("--- 1. Agrupación y Cálculo de Métricas ---")


agrupacion_cols = ['Ciudad', 'Categoria_Cliente', 'Cliente', 'Producto']
metricas = {
    'Total': 'sum',
    'PrecioUnitario': 'mean',
    'Producto': 'size'  
}

df_reporte = df_integrado.groupby(agrupacion_cols).agg(
    Suma_Total=('Total', 'sum'),
    Promedio_Precio_Unitario=('PrecioUnitario', 'mean'),
    Cantidad_Compras=('Producto', 'size')
).reset_index()


print("--- 2. Ordenamiento y Exportación ---")


df_reporte.sort_values(by=['Ciudad', 'Suma_Total'], ascending=[True, False], inplace=True)


df_reporte.to_csv('reporte_multinivel.csv', index=False, float_format='%.2f')
print("Archivo 'reporte_multinivel.csv' generado con éxito.")


print("\n--- 3. Indicadores Clave ---")


df_ciudad_total = df_integrado.groupby('Ciudad')['Total'].sum().idxmax()
ciudad_max_total = df_integrado.groupby('Ciudad')['Total'].sum().max()
print(f"Ciudad con mayor volumen total: **{df_ciudad_total}** ({ciudad_max_total:,.2f})")



df_cliente_productos = df_integrado.groupby('Cliente')['Producto'].nunique()
cliente_max_variedad = df_cliente_productos.idxmax()
max_variedad = df_cliente_productos.max()
print(f"Cliente con mayor variedad de productos: **{cliente_max_variedad}** ({max_variedad} productos únicos)")