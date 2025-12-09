import pandas as pd
import numpy as np


TOTAL_FINAL_GLOBAL = 0.0
ventas_por_producto = {}
max_chunk_sales = -1.0
best_chunk_index = -1
chunk_index = 0

print("--- 1. Procesamiento Distribuido (Chunks de 1000) ---")


try:
    for chunk in pd.read_csv('ventas.csv', chunksize=1000):
       
        for col in ['Cantidad', 'PrecioUnitario', 'Total']:
            chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0) 
       
        chunk['Subtotal'] = chunk['Cantidad'] * chunk['PrecioUnitario']

       
        conditions = [
            chunk['Total'] < 5000,
            (chunk['Total'] >= 5000) & (chunk['Total'] <= 20000),
            chunk['Total'] > 20000
        ]
        rates = [0.10, 0.15, 0.18]
        chunk['Tasa_Impuesto'] = np.select(conditions, rates)

        
        chunk['Impuesto_Monto'] = chunk['Total'] * chunk['Tasa_Impuesto']
        chunk['Total_Final'] = chunk['Total'] + chunk['Impuesto_Monto']

       
        chunk_total_final = chunk['Total_Final'].sum()
        TOTAL_FINAL_GLOBAL += chunk_total_final

        
        ventas_chunk = chunk.groupby('Producto')['Total_Final'].sum()
        for producto, venta in ventas_chunk.items():
            ventas_por_producto[producto] = ventas_por_producto.get(producto, 0.0) + venta

        
        if chunk_total_final > max_chunk_sales:
            max_chunk_sales = chunk_total_final
            best_chunk_index = chunk_index
        
        chunk_index += 1

except FileNotFoundError:
    print("Error: No se pudo encontrar 'ventas.csv'.")
    exit()


print("\n--- 2. Informe Final de Procesamiento ---")


print(f"Total Final Global acumulado: **{TOTAL_FINAL_GLOBAL:,.2f}**")


if ventas_por_producto:
    top_5 = pd.Series(ventas_por_producto).sort_values(ascending=False).head(5)
    print("\nTop 5 Productos más vendidos (por Total Final):")
    print(top_5.to_markdown(numalign="left", stralign="left", floatfmt=",.2f"))
else:
    print("\nNo se pudo calcular el Top 5 de productos (datos vacíos).")


print(f"\nChunk con mayor contribución en ventas (Índice): **{best_chunk_index}**")
print(f"Ventas de este chunk: **{max_chunk_sales:,.2f}**")