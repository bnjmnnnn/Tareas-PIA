import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carga del archivo
df = pd.read_csv("dataset_features_biovid.csv")

print("=== VALIDACIÓN DE GROUND TRUTH Y CLASES ===")
# 2. Distribución y balance de clases de dolor
conteo = df['class_id'].value_counts()
porcentaje = df['class_id'].value_counts(normalize=True) * 100
for idx in sorted(conteo.index):
    print(f"Clase {idx}: {conteo[idx]} muestras ({porcentaje[idx]:.2f}%)")

# 3. Promedio de temperatura real del hardware por cada clase de dolor
print("\nTemperaturas promedio registradas por Clase de Dolor:")
print(df.groupby('class_id')[['max_temp', 'mean_temp']].mean())

# 4. Gráfico de Validación (Boxplot de Temperatura vs Clase de Dolor)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='class_id', y='max_temp', palette='coolwarm')
plt.title('Validación de Ground Truth: Temperatura vs Clase de Dolor')
plt.xlabel('Clase de Dolor (Class ID)')
plt.ylabel('Temperatura Máxima Registrada por el Estimulador (°C)')
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig('validacion_temperatura_clase.png')
plt.show()