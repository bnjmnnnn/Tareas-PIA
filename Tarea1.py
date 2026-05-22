import pandas as pd

# 1. Carga del archivo
df = pd.read_csv("dataset_features_biovid.csv")

print("=== REPORTE DE INTEGRIDAD - DATASET AUTONÓMICO ===")
print(f"1. Total de registros en bruto (Filas, Columnas): {df.shape}")

# 2. Conteo de nulos reales (NaN)
print("\n2. Valores nulos (NaN) detectados por columna:")
print(df.isnull().sum())

# 3. Detección de Artefactos (Ceros lógicos donde no debería haber un cero biológico)
total_muestras = len(df)

# Cálculos de ceros biológicamente imposibles
zeros_ecg = (df['ecg_bpm'] == 0).sum()
zeros_max_temp = (df['max_temp'] == 0).sum()
zeros_mean_temp = (df['mean_temp'] == 0).sum()
# GSR (Falta de respuesta galvánica, sensor desconectado o mal contacto)
zeros_gsr = (df['gsr_max_amplitude'] == 0).sum()
# EMG Corrugator (Falta de actividad muscular)
zeros_emg_corrugator = (df['emg_corrugator_auc'] == 0).sum()
# EMG Medias (Falta de tono muscular basal)
zeros_emg_trap_mean = (df['emg_trapezius_mean'] == 0).sum()
zeros_emg_corr_mean = (df['emg_corrugator_mean'] == 0).sum()
zeros_emg_zygo_mean = (df['emg_zygomaticus_mean'] == 0).sum()

# EMG Desviaciones Estándar (Señal congelada o línea recta plana)
zeros_emg_trap_std = (df['emg_trapezius_std'] == 0).sum()
zeros_emg_corr_std = (df['emg_corrugator_std'] == 0).sum()
zeros_emg_zygo_std = (df['emg_zygomaticus_std'] == 0).sum()
zeros_emg_zygo_s = (df["emg_zygomaticus_auc"] == 0).sum()

print("\n3. Auditoría de Artefactos (Fallas de sensor controladas):")
print(f"⚠️ ECG con ruido (0 BPM): {zeros_ecg} muestras ({zeros_ecg / total_muestras * 100:.2f}%)")
print(f"⚠️ Temperatura Máxima errónea (0 °C): {zeros_max_temp} muestras ({zeros_max_temp / total_muestras * 100:.2f}%)")
print(f"⚠️ Temperatura Media errónea (0 °C): {zeros_mean_temp} muestras ({zeros_mean_temp / total_muestras * 100:.2f}%)")

print("\n   [Fallas de tono muscular basal - Medias en 0]")
print(f"   ⚠️ EMG Trapecio Media 0: {zeros_emg_trap_mean} muestras ({zeros_emg_trap_mean / total_muestras * 100:.2f}%)")
print(f"   ⚠️ EMG Corrugador Media 0: {zeros_emg_corr_mean} muestras ({zeros_emg_corr_mean / total_muestras * 100:.2f}%)")
print(f"   ⚠️ EMG Cigomático Media 0: {zeros_emg_zygo_mean} muestras ({zeros_emg_zygo_mean / total_muestras * 100:.2f}%)")

print("\n   [Fallas de sensor o desconexión - Ceros en señales fisiológicas]")
print(f"⚠️ GSR con ruido (0 µS): {zeros_gsr} muestras ({zeros_gsr / total_muestras * 100:.2f}%)")
print(f"⚠️ EMG con ruido (0 Tensión Corrugador): {zeros_emg_corrugator} muestras ({zeros_emg_corrugator / total_muestras * 100:.2f}%)")

print("\n   [Señales EMG congeladas - Desviación Estándar en 0]")
print(f"   ⚠️ EMG Trapecio Std 0: {zeros_emg_trap_std} muestras ({zeros_emg_trap_std / total_muestras * 100:.2f}%)")
print(f"   ⚠️ EMG Corrugador Std 0: {zeros_emg_corr_std} muestras ({zeros_emg_corr_std / total_muestras * 100:.2f}%)")
print(f"   ⚠️ EMG Cigomático Std 0: {zeros_emg_zygo_std} muestras ({zeros_emg_zygo_std / total_muestras * 100:.2f}%)")
print(f"   ⚠️ EMG Cigomático AUC 0: {zeros_emg_zygo_s} muestras ({zeros_emg_zygo_s / total_muestras * 100:.2f}%)")