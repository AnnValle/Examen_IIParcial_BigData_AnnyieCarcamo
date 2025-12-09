import pandas as pd
import numpy as np


df_ventas = pd.read_csv('ventas.csv')
df_clientes = pd.read_csv('Clientes.csv')
df_productos = pd.read_csv('productos.csv')
filas_iniciales = len(df_ventas)


clientes_validos = set(df_clientes['Cliente'].unique())
productos_validos = set(df_productos['Producto'].unique())


df_ventas = df_ventas[df_ventas['Producto'].isin(productos_validos)].copy()
df_ventas = df_ventas[df_ventas['Cliente'].isin(clientes_validos)].copy()
filas_después_filtrado = len(df_ventas)
filas_rechazadas = filas_iniciales - filas_después_filtrado


columnas_numericas = ['Cantidad', 'PrecioUnitario', 'Total']
invalidos_total = 0

for col in columnas_numericas:
    
    df_ventas[col] = pd.to_numeric(df_ventas[col], errors='coerce')
    
    
    invalidos_total += df_ventas[col].isnull().sum()
    
    
    df_ventas[col].fillna(df_ventas[col].mean(), inplace=True)


df_final = (
    df_ventas
    .merge(df_clientes, on='Cliente', how='left')
    .merge(df_productos, on='Producto', how='left')
)


print("--- PROBLEMA 1: INFORME DE INTEGRACIÓN DE DATOS ---")
print(f"Filas iniciales en ventas.csv: {filas_iniciales}")
print(f"Filas rechazadas (Cliente/Producto inválido): {filas_rechazadas}")
print(f"Valores de datos corregidos (NaN -> Media): {invalidos_total}")
print(f"Filas finales en el DataFrame integrado: {len(df_final)}\n")

print("Primeras 10 filas del DataFrame final:")
print(df_final.head(10).to_markdown(index=False, numalign="left", stralign="left"))