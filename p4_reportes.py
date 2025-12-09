import pandas as pd
import numpy as np


print("--- 1. Lectura e Integración ---")
try:
    
    df_ventas = pd.read_csv('ventas.csv')
    df_clientes = pd.read_csv('Clientes.csv')
    
   
    df_ventas['Total'] = pd.to_numeric(df_ventas['Total'], errors='coerce').fillna(0)
    df_ventas['PrecioUnitario'] = pd.to_numeric(df_ventas['PrecioUnitario'], errors='coerce').fillna(0)
    
   
    df_integrado = df_ventas.merge(
        df_clientes[['Cliente', 'Ciudad', 'Categoria_Cliente']].dropna(subset=['Cliente']), 
        on='Cliente', 
        how='left'
    )
   
    df_integrado[['Ciudad', 'Categoria_Cliente']] = df_integrado[['Ciudad', 'Categoria_Cliente']].fillna('Desconocido')
    
except FileNotFoundError:
    print("Error: Asegúrese de que 'ventas.csv' y 'Clientes.csv' existan.")
    exit()


print("--- 2. Agrupación y Métricas ---")

agrupacion_cols = ['Ciudad', 'Categoria_Cliente', 'Cliente', 'Producto']


df_reporte = df_integrado.groupby(agrupacion_cols).agg(
    Suma_Total=('Total', 'sum'),
    Promedio_Precio_Unitario=('PrecioUnitario', 'mean'),
    Cantidad_Compras=('Producto', 'size') 
).reset_index()


print("--- 3. Reporte y Exportación ---")


df_reporte.sort_values(by=['Ciudad', 'Suma_Total'], ascending=[True, False], inplace=True)


df_reporte.to_csv('reporte_multinivel.csv', index=False, float_format='%.2f')
print(" Archivo 'reporte_multinivel.csv' generado con éxito.")


print("\n--- 4. Indicadores Clave ---")


ciudad_max_total = df_integrado.groupby('Ciudad')['Total'].sum().sort_values(ascending=False).index[0]
total_ciudad = df_integrado.groupby('Ciudad')['Total'].sum().max()
print(f" Ciudad con mayor volumen total: **{ciudad_max_total}** ({total_ciudad:,.2f})")

cliente_max_variedad = df_integrado.groupby('Cliente')['Producto'].nunique().sort_values(ascending=False).index[0]
max_variedad = df_integrado.groupby('Cliente')['Producto'].nunique().max()
print(f" Cliente con mayor variedad de productos: **{cliente_max_variedad}** ({max_variedad} productos únicos)")
