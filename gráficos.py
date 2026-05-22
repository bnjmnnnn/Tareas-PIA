import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

df = pd.read_csv("dataset_features_biovid.csv")
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
total_muestras = len(df)

# --- Datos para los gráficos ---
sensores = {
    'ecg_bpm':             'ECG\n(BPM)',
    'gsr_max_amplitude':   'GSR\n(Amplitud)',
    'emg_corrugator_auc':  'EMG\nCorrug. AUC',
    'emg_zygomaticus_auc': 'EMG\nZigom. AUC',
    'emg_corrugator_std':  'EMG\nCorrug. Std',
    'emg_zygomaticus_std': 'EMG\nZigom. Std',
    'max_temp':            'Temp.\nMáxima',   # ← AGREGADO
    'mean_temp':           'Temp.\nMedia',    # ← AGREGADO
}
labels  = list(sensores.values())
cols    = list(sensores.keys())
ceros   = [(df[c] == 0).sum() for c in cols]
pct     = [z / total_muestras * 100 for z in ceros]
limpios = [100 - p for p in pct]

# ── GRÁFICO 1: Barras horizontales — conteo de artefactos ──────────────
fig1, ax1 = plt.subplots(figsize=(11, 6))
bar_colors = ['#e74c3c' if z > 0 else '#2ecc71' for z in ceros]
ax1.barh(range(len(labels)), ceros, color=bar_colors, edgecolor='white', height=0.55)

for i, (z, p) in enumerate(zip(ceros, pct)):
    offset = max(ceros) * 0.015
    if z > 0:
        ax1.text(z + offset, i, f"{z} muestras  ({p:.2f}%)", va='center', fontsize=10, color='#222222')
    else:
        ax1.text(offset, i, "✓ Sin artefactos", va='center', fontsize=10, color='#2ecc71', fontweight='bold')

ax1.set_yticks(range(len(labels)))
ax1.set_yticklabels(labels, fontsize=11)
ax1.set_xlabel("N° de muestras con valor cero (artefacto)", fontsize=11)
ax1.set_title("Auditoría de Artefactos por Sensor\nDataset BioVid — Ceros biológicamente imposibles", fontsize=13, fontweight='bold', pad=14)
ax1.set_xlim(0, max(ceros) * 1.35)
ax1.spines[['top', 'right']].set_visible(False)
patch_r = mpatches.Patch(color='#e74c3c', label='Con artefactos')
patch_g = mpatches.Patch(color='#2ecc71', label='Sin artefactos')
ax1.legend(handles=[patch_r, patch_g], loc='lower right', fontsize=10)
plt.tight_layout()
plt.savefig("grafico1_artefactos_por_sensor.png", dpi=150)
plt.show()

# ── GRÁFICO 2: Stacked bar — % limpio vs artefacto ─────────────────────
fig2, ax2 = plt.subplots(figsize=(12, 6))
x = np.arange(len(labels))

ax2.bar(x, limpios, width=0.55, label='Datos limpios',  color='#27ae60', edgecolor='white')
ax2.bar(x, pct,     width=0.55, label='Artefactos (0)', color='#e74c3c', edgecolor='white', bottom=limpios)

for i, (p, l) in enumerate(zip(pct, limpios)):
    if p >= 2:
        # Segmento rojo grande → etiqueta negra centrada dentro
        ax2.text(i, l + p / 2, f"{p:.1f}%", ha='center', va='center',
                 fontsize=9.5, color='#1a1a1a', fontweight='bold')   # ← NEGRO
    elif p > 0:
        # Segmento rojo pequeño → etiqueta roja encima de la barra
        ax2.text(i, 101.5, f"{p:.2f}%", ha='center', va='bottom',
                 fontsize=9, color='#e74c3c', fontweight='bold')      # ← ROJO ARRIBA
    # % limpio dentro de barra verde → amarillo para contraste
    ax2.text(i, l / 2, f"{l:.1f}%", ha='center', va='center',
             fontsize=9, color='#f9e547', fontweight='bold')          # ← AMARILLO

ax2.set_xticks(x)
ax2.set_xticklabels(labels, fontsize=10)
ax2.set_ylabel("Porcentaje de muestras (%)", fontsize=11)
ax2.set_ylim(0, 112)
ax2.set_title("Integridad de Datos por Sensor (%)\nDataset BioVid — Proporción limpio vs ruido", fontsize=13, fontweight='bold', pad=14)
ax2.legend(loc='upper right', fontsize=10)
ax2.spines[['top', 'right']].set_visible(False)
plt.tight_layout()
plt.savefig("grafico2_integridad_porcentaje.png", dpi=150)
plt.show()
