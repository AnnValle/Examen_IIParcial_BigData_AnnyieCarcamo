import pandas as pd
import numpy as np


try:
    df = pd.read_csv('ventas.csv')
except FileNotFoundError:
    print("Error: No se encontró 'ventas.csv'.")
    exit()


for col in ['Cantidad', 'PrecioUnitario', 'Total']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(df[col].mean(), inplace=True)


df['Subtotal_Calculado'] = df['Cantidad'] * df['PrecioUnitario']


df['Diferencia'] = np.abs(df['Subtotal_Calculado'] - df['Total'])
max_abs = np.maximum(df['Total'].abs(), df['Subtotal_Calculado'].abs())


df['Error_Relativo'] = np.where(max_abs != 0, (df['Diferencia'] / max_abs) * 100, 0.0)


UMBRAL = 5.0
df_inconsistencias = df[df['Error_Relativo'] > UMBRAL].copy()


cols_export = [
    'Fecha', 'Cliente', 'Producto', 'Cantidad', 'PrecioUnitario', 
    'Subtotal_Calculado', 'Total', 'Diferencia', 'Error_Relativo'
]
df_inconsistencias[cols_export].to_csv('inconsistencias.csv', index=False, float_format='%.4f')


total_inconsistentes = len(df_inconsistencias)

print("--- REPORTE DE INCONSISTENCIAS DE VENTA ---")
print(f"Total de registros inconsistentes (> {UMBRAL}%): **{total_inconsistentes}**")

if total_inconsistentes > 0:
    promedio_error = df_inconsistencias['Error_Relativo'].mean()
    producto_mas_inconsistente = df_inconsistencias['Producto'].mode().iloc[0]
    
    print(f"Promedio del Error Relativo: **{promedio_error:.2f}%**")
    print(f"Producto con más inconsistencias: **{producto_mas_inconsistente}**")
else:
    print("No se detectaron inconsistencias que superen el umbral.")