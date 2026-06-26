# ============================================================
#  FAST FOOD DATASET — TO'LIQ EDA VIZUALIZATSIYA
#  EDA standartlari: taqsimot, markaziy tendensiya, outlier
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'figure.facecolor' : '#0f1117',
    'axes.facecolor'   : '#1a1d2e',
    'axes.edgecolor'   : '#2d3154',
    'axes.labelcolor'  : '#c8cde8',
    'axes.titlecolor'  : '#e8ecff',
    'axes.titlesize'   : 11,
    'axes.labelsize'   : 9,
    'xtick.color'      : '#8890b5',
    'ytick.color'      : '#8890b5',
    'xtick.labelsize'  : 8,
    'ytick.labelsize'  : 8,
    'text.color'       : '#c8cde8',
    'grid.color'       : '#2d3154',
    'grid.linewidth'   : 0.6,
    'grid.alpha'       : 0.8,
})

BLUE    = '#4f8ef7'
PURPLE  = '#9b6dff'
TEAL    = '#2ecfb1'
ORANGE  = '#f5a623'
PINK    = '#f76fa0'
RED     = '#ff5f5f'
GREEN   = '#4fd97f'
PALETTE = [BLUE, PURPLE, TEAL, ORANGE, PINK]

# ── DATA ──────────────────────────────────────────────────
df = pd.read_csv('fast_food_data.csv')
df['order_time'] = pd.to_datetime(df['order_time'])
NUM_COLS = ['price', 'quantity', 'total_price', 'customer_count', 'hour']

def iqr_bounds(series):
    Q1, Q3 = series.quantile(0.25), series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - 1.5*IQR, Q3 + 1.5*IQR, Q1, Q3, IQR

# ══════════════════════════════════════════════════════════
#  SHEET 1 — MARKAZIY TENDENSIYA + TAQSIMOT
# ══════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(20, 24))
fig1.patch.set_facecolor('#0f1117')
fig1.suptitle(
    '🍔  FAST FOOD EDA — MARKAZIY TENDENSIYA & TAQSIMOT',
    fontsize=16, fontweight='bold', color='#e8ecff', y=0.98
)

gs1 = gridspec.GridSpec(4, 2, figure=fig1, hspace=0.50, wspace=0.35,
                        left=0.07, right=0.97, top=0.95, bottom=0.04)

# ── 1. Umumiy statistika jadvali ──
ax_tbl = fig1.add_subplot(gs1[0, :])
ax_tbl.set_facecolor('#0f1117')
ax_tbl.axis('off')

desc = df[NUM_COLS].describe().T.round(2)
desc['skewness'] = df[NUM_COLS].skew().round(3)
desc['kurtosis'] = df[NUM_COLS].kurt().round(3)
desc.columns = [c.upper() for c in desc.columns]
desc.index   = [c.replace('_', ' ').upper() for c in desc.index]

col_labels = list(desc.columns)
row_labels  = list(desc.index)
cell_data   = desc.values.tolist()

tbl = ax_tbl.table(
    cellText  = [[f'{v:.2f}' if isinstance(v, float) else str(v) for v in row] for row in cell_data],
    rowLabels  = row_labels,
    colLabels  = col_labels,
    cellLoc    = 'center',
    loc        = 'center',
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
for (r, c), cell in tbl.get_celld().items():
    if r == 0 or c == -1:
        cell.set_facecolor('#2a3060')
        cell.set_text_props(color='#e8ecff', fontweight='bold')
    else:
        cell.set_facecolor('#1a1d2e' if r % 2 == 0 else '#20243a')
        cell.set_text_props(color='#c8cde8')
    cell.set_edgecolor('#2d3154')
    cell.set_linewidth(0.5)
ax_tbl.set_title('📊  Umumiy Statistika Jadvali  (Markaziy Tendensiya + Shakl Ko\'rsatkichlari)',
                 color='#e8ecff', fontsize=12, pad=10)

# ── 2-6. Har bir numerik ustun uchun Histogram + KDE ──
hist_positions = [(1,0),(1,1),(2,0),(2,1),(3,0)]
colors_h = [BLUE, PURPLE, TEAL, ORANGE, PINK]

for i, (col, pos, clr) in enumerate(zip(NUM_COLS, hist_positions, colors_h)):
    ax = fig1.add_subplot(gs1[pos[0], pos[1]])
    data = df[col]
    mean_v, med_v, mode_v = data.mean(), data.median(), float(data.mode()[0])
    _, p_norm = stats.shapiro(data.sample(min(500, len(data)), random_state=42))

    n, bins, patches = ax.hist(data, bins=40, color=clr, alpha=0.55,
                               edgecolor='none', density=True)

    # KDE
    kde_x = np.linspace(data.min(), data.max(), 300)
    kde   = stats.gaussian_kde(data)
    ax.plot(kde_x, kde(kde_x), color=clr, linewidth=2.2)

    # Normal qiyosiy egri chiziq
    mu, sigma = data.mean(), data.std()
    norm_y = stats.norm.pdf(kde_x, mu, sigma)
    ax.plot(kde_x, norm_y, color='#ffffff', linewidth=1.2,
            linestyle='--', alpha=0.45, label='Normal')

    # Markaziy tendensiya chiziqlari
    ax.axvline(mean_v,  color=GREEN,  linewidth=1.8, linestyle='-',  label=f'Mean   {mean_v:,.0f}')
    ax.axvline(med_v,   color=ORANGE, linewidth=1.8, linestyle='--', label=f'Median {med_v:,.0f}')
    ax.axvline(mode_v,  color=RED,    linewidth=1.8, linestyle=':',  label=f'Mode   {mode_v:,.0f}')

    skw = data.skew()
    skw_txt = ('Musbat (o\'ng)' if skw > 0.5 else
               'Manfiy (chap)' if skw < -0.5 else 'Simmetrik')
    norm_txt = 'Normal ✓' if p_norm > 0.05 else 'Normal ✗'
    ax.set_title(f'{col.replace("_"," ").upper()}', fontsize=10, fontweight='bold')
    ax.set_xlabel(col, labelpad=4)
    ax.set_ylabel('Zichlik', labelpad=4)
    ax.legend(fontsize=7, loc='upper right',
              framealpha=0.2, labelcolor='white')
    ax.text(0.02, 0.97,
            f'Skewness: {skw:.3f} ({skw_txt})\nKurtosis: {data.kurt():.3f}\n{norm_txt}',
            transform=ax.transAxes, fontsize=7.5, verticalalignment='top',
            color='#adb5d8',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#12152a',
                      edgecolor='#2d3154', alpha=0.85))
    ax.grid(True, axis='y')

# ── 7. Pearson korrelyatsiya issiqligi xaritasi ──
ax_corr = fig1.add_subplot(gs1[3, 1])
corr = df[NUM_COLS].corr()
im = ax_corr.imshow(corr.values, cmap='RdYlGn', vmin=-1, vmax=1, aspect='auto')
ax_corr.set_xticks(range(len(NUM_COLS)))
ax_corr.set_yticks(range(len(NUM_COLS)))
labels_short = [c.replace('_','\n') for c in NUM_COLS]
ax_corr.set_xticklabels(labels_short, fontsize=7.5)
ax_corr.set_yticklabels(labels_short, fontsize=7.5)
for r in range(len(NUM_COLS)):
    for c in range(len(NUM_COLS)):
        val = corr.values[r, c]
        ax_corr.text(c, r, f'{val:.2f}',
                     ha='center', va='center', fontsize=8,
                     color='#0a0a0a' if abs(val) > 0.5 else '#e8ecff',
                     fontweight='bold')
plt.colorbar(im, ax=ax_corr, fraction=0.046, pad=0.04)
ax_corr.set_title('Pearson Korrelyatsiya Matritsasi', fontweight='bold')

plt.savefig('eda_sheet1_distribution.png', dpi=130,
            bbox_inches='tight', facecolor='#0f1117')
print("✅  Sheet 1 saqlandi: eda_sheet1_distribution.png")
plt.close(fig1)


# ══════════════════════════════════════════════════════════
#  SHEET 2 — OUTLIER TAHLILI
# ══════════════════════════════════════════════════════════
fig2 = plt.figure(figsize=(20, 22))
fig2.patch.set_facecolor('#0f1117')
fig2.suptitle(
    '🔍  FAST FOOD EDA — OUTLIER (CHEKLOVDAN TASHQARI QIYMATLAR) TAHLILI',
    fontsize=15, fontweight='bold', color='#e8ecff', y=0.99
)
gs2 = gridspec.GridSpec(4, 2, figure=fig2, hspace=0.52, wspace=0.35,
                        left=0.07, right=0.97, top=0.95, bottom=0.04)

# ── Outlier jadval xulosa ──
ax_ot = fig2.add_subplot(gs2[0, :])
ax_ot.axis('off')
rows_ot = []
for col in NUM_COLS:
    lo, up, Q1, Q3, IQR = iqr_bounds(df[col])
    n_out = ((df[col] < lo) | (df[col] > up)).sum()
    rows_ot.append([
        col.replace('_', ' ').upper(),
        f'{Q1:,.1f}', f'{Q3:,.1f}', f'{IQR:,.1f}',
        f'{lo:,.1f}', f'{up:,.1f}',
        str(n_out), f'{n_out/len(df)*100:.2f}%',
        '🚨 BOR' if n_out > 0 else '✅ YO\'Q'
    ])
col_ot = ['USTUN','Q1','Q3','IQR','QUYI CHEGARA','YUQORI CHEGARA',
          'OUTLIER SONI','%','HOLAT']
tbl2 = ax_ot.table(cellText=rows_ot, colLabels=col_ot,
                   cellLoc='center', loc='center')
tbl2.auto_set_font_size(False)
tbl2.set_fontsize(9)
for (r,c), cell in tbl2.get_celld().items():
    if r == 0:
        cell.set_facecolor('#2a3060')
        cell.set_text_props(color='#e8ecff', fontweight='bold')
    elif c == 8 and r > 0:
        v = rows_ot[r-1][8]
        cell.set_facecolor('#3a1520' if '🚨' in v else '#0f2a1a')
        cell.set_text_props(color=RED if '🚨' in v else GREEN, fontweight='bold')
    else:
        cell.set_facecolor('#1a1d2e' if r % 2 == 0 else '#20243a')
        cell.set_text_props(color='#c8cde8')
    cell.set_edgecolor('#2d3154')
ax_ot.set_title('IQR Metodi — Outlier Aniqlash Jadvali  '
                '(Chegara: Q1−1.5×IQR  ···  Q3+1.5×IQR)',
                color='#e8ecff', fontsize=11, pad=10)

# ── Box-plot va Strip-plot kombinatsiyasi ──
box_pos = [(1,0),(1,1),(2,0),(2,1),(3,0)]
for col, pos, clr in zip(NUM_COLS, box_pos, colors_h):
    ax = fig2.add_subplot(gs2[pos[0], pos[1]])
    lo, up, Q1, Q3, IQR = iqr_bounds(df[col])
    normal  = df[col][(df[col] >= lo) & (df[col] <= up)]
    outlier = df[col][(df[col] < lo)  | (df[col] > up)]

    # Box-plot
    bp = ax.boxplot(df[col].values, vert=False, patch_artist=True,
                    widths=0.35,
                    boxprops      = dict(facecolor=clr, alpha=0.35, linewidth=1.5, edgecolor=clr),
                    whiskerprops  = dict(color=clr, linewidth=1.5, linestyle='--'),
                    capprops      = dict(color=clr, linewidth=2),
                    medianprops   = dict(color=GREEN, linewidth=2.5),
                    flierprops    = dict(marker='D', color=RED, markersize=5, alpha=0.7))

    # Normal nuqtalar (jitter)
    jitter = np.random.uniform(-0.12, 0.12, size=len(normal))
    ax.scatter(normal.values, 1 + jitter,
               color=clr, alpha=0.18, s=8, zorder=2)

    # Outlier nuqtalar
    if len(outlier) > 0:
        jitter_o = np.random.uniform(-0.12, 0.12, size=len(outlier))
        ax.scatter(outlier.values, 1 + jitter_o,
                   color=RED, alpha=0.85, s=28, marker='D', zorder=5,
                   label=f'Outlier ({len(outlier)})')

    # IQR chegaralar chiziqlari
    ax.axvline(lo,  color=ORANGE, linewidth=1.2, linestyle=':', alpha=0.7)
    ax.axvline(up,  color=ORANGE, linewidth=1.2, linestyle=':', alpha=0.7)
    ax.axvspan(lo, up, alpha=0.06, color=GREEN)

    ax.set_title(f'{col.replace("_"," ").upper()} — Box-plot + Strip-plot',
                 fontweight='bold')
    ax.set_xlabel(col)
    ax.set_yticks([])
    ax.grid(True, axis='x')

    stat_txt = (f'Outlier: {len(outlier)} ta ({len(outlier)/len(df)*100:.2f}%)\n'
                f'Q1={Q1:,.0f}  Q3={Q3:,.0f}\n'
                f'IQR={IQR:,.0f}\n'
                f'[{lo:,.0f} — {up:,.0f}]')
    ax.text(1.01, 0.5, stat_txt, transform=ax.transAxes,
            fontsize=7.5, va='center', color='#adb5d8',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#12152a',
                      edgecolor='#2d3154', alpha=0.9))
    if len(outlier) > 0:
        ax.legend(fontsize=8, framealpha=0.2, labelcolor=RED)

# ── Z-score ümumiy taqqoslash ──
ax_z = fig2.add_subplot(gs2[3, 1])
z_counts = {}
for col in NUM_COLS:
    z = np.abs(stats.zscore(df[col]))
    z_counts[col.replace('_','\n')] = (z > 3).sum()
bars = ax_z.bar(list(z_counts.keys()), list(z_counts.values()),
                color=[BLUE,PURPLE,TEAL,ORANGE,PINK], edgecolor='none',
                width=0.55)
for bar, val in zip(bars, z_counts.values()):
    ax_z.text(bar.get_x() + bar.get_width()/2,
              bar.get_height() + 0.5,
              str(val), ha='center', color='white', fontsize=9, fontweight='bold')
ax_z.set_title('Z-Score > 3  (Ekstremal Outlierlar)', fontweight='bold')
ax_z.set_ylabel('Outlier soni')
ax_z.grid(True, axis='y')
ax_z.set_facecolor('#1a1d2e')

plt.savefig('eda_sheet2_outliers.png', dpi=130,
            bbox_inches='tight', facecolor='#0f1117')
print("✅  Sheet 2 saqlandi: eda_sheet2_outliers.png")
plt.close(fig2)


# ══════════════════════════════════════════════════════════
#  SHEET 3 — KATEGORIK + BUSINESS TAHLIL
# ══════════════════════════════════════════════════════════
fig3 = plt.figure(figsize=(20, 22))
fig3.patch.set_facecolor('#0f1117')
fig3.suptitle(
    '📈  FAST FOOD EDA — KATEGORIK TAHLIL & BIZNES KO\'RSATKICHLARI',
    fontsize=15, fontweight='bold', color='#e8ecff', y=0.99
)
gs3 = gridspec.GridSpec(3, 3, figure=fig3, hspace=0.50, wspace=0.38,
                        left=0.07, right=0.97, top=0.95, bottom=0.04)

DAY_ORDER = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

# ── 1. Kompaniya buyurtmalar soni (horizontal bar) ──
ax1 = fig3.add_subplot(gs3[0, 0])
comp = df['company_name'].value_counts()
bars = ax1.barh(comp.index, comp.values, color=PALETTE, edgecolor='none', height=0.6)
for bar, val in zip(bars, comp.values):
    ax1.text(bar.get_width()+15, bar.get_y()+bar.get_height()/2,
             f'{val:,}', va='center', fontsize=8.5, color='white')
ax1.set_title("Kompaniya Bo'yicha\nBuyurtmalar Soni", fontweight='bold')
ax1.set_xlabel('Buyurtma soni')
ax1.grid(True, axis='x')
ax1.invert_yaxis()

# ── 2. Mahsulot taqsimoti (Donut) ──
ax2 = fig3.add_subplot(gs3[0, 1])
prod = df['product_name'].value_counts()
wedges, texts, autotexts = ax2.pie(
    prod.values, labels=prod.index, autopct='%1.1f%%',
    colors=PALETTE + [GREEN], startangle=140,
    pctdistance=0.78, wedgeprops=dict(width=0.55, edgecolor='#0f1117', linewidth=2)
)
for at in autotexts:
    at.set_fontsize(8); at.set_color('white'); at.set_fontweight('bold')
for t in texts:
    t.set_fontsize(8.5); t.set_color('#c8cde8')
ax2.set_title("Mahsulot Taqsimoti\n(Donut Chart)", fontweight='bold')

# ── 3. Kunlar bo'yicha buyurtmalar ──
ax3 = fig3.add_subplot(gs3[0, 2])
day_cnt = df['day_of_week'].value_counts().reindex(DAY_ORDER)
clr_day = [RED if d in ['Saturday','Sunday'] else BLUE for d in DAY_ORDER]
bars3 = ax3.bar(DAY_ORDER, day_cnt.values, color=clr_day, edgecolor='none', width=0.6)
for bar, val in zip(bars3, day_cnt.values):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10,
             str(val), ha='center', fontsize=8, color='white')
ax3.set_title("Kun Bo'yicha\nBuyurtmalar", fontweight='bold')
ax3.set_xticklabels(DAY_ORDER, rotation=35, ha='right', fontsize=8)
ax3.grid(True, axis='y')
ax3.text(0.98, 0.97, '🔴 Dam olish kunlari', transform=ax3.transAxes,
         ha='right', va='top', fontsize=7.5, color=RED)

# ── 4. Soatlik savdo zichligi (KDE + histogram) ──
ax4 = fig3.add_subplot(gs3[1, :2])
for comp_name, clr in zip(df['company_name'].unique(), PALETTE):
    d = df[df['company_name']==comp_name]['hour']
    kde = stats.gaussian_kde(d, bw_method=0.4)
    x = np.linspace(0, 23, 300)
    ax4.plot(x, kde(x), label=comp_name, linewidth=2.2, color=clr)
    ax4.fill_between(x, kde(x), alpha=0.08, color=clr)
ax4.set_title("Soatlik Savdo Zichligi — Kompaniyalar Qiyosi  (KDE)", fontweight='bold')
ax4.set_xlabel('Soat')
ax4.set_ylabel('Zichlik')
ax4.set_xticks(range(0,24))
ax4.grid(True, axis='both')
ax4.legend(fontsize=8, framealpha=0.2, ncol=5)

# ── 5. Kompaniya × total_price violin ──
ax5 = fig3.add_subplot(gs3[1, 2])
comp_names = df['company_name'].unique()
positions  = range(len(comp_names))
vp = ax5.violinplot(
    [df[df['company_name']==c]['total_price'].values for c in comp_names],
    positions=list(positions), showmedians=True, showextrema=True
)
for i, (body, clr) in enumerate(zip(vp['bodies'], PALETTE)):
    body.set_facecolor(clr); body.set_alpha(0.5)
vp['cmedians'].set_color(GREEN); vp['cmedians'].set_linewidth(2)
vp['cmaxes'].set_color('#ffffff60'); vp['cmins'].set_color('#ffffff60')
ax5.set_xticks(list(positions))
ax5.set_xticklabels([c.replace(' ','\n') for c in comp_names], fontsize=7.5)
ax5.set_title("Kompaniya × Total Narx\n(Violin Plot)", fontweight='bold')
ax5.set_ylabel("Total Price (so'm)")
ax5.grid(True, axis='y')

# ── 6. Mahsulot × o'rtacha narx (grouped bar) ──
ax6 = fig3.add_subplot(gs3[2, :2])
pivot = df.groupby(['product_name','company_name'])['total_price'].mean().unstack()
x = np.arange(len(pivot.index))
w = 0.16
for i, (comp_name, clr) in enumerate(zip(pivot.columns, PALETTE)):
    offset = (i - len(pivot.columns)/2) * w + w/2
    ax6.bar(x + offset, pivot[comp_name], width=w, label=comp_name,
            color=clr, edgecolor='none')
ax6.set_xticks(x)
ax6.set_xticklabels(pivot.index, fontsize=9)
ax6.set_title("Mahsulot × Kompaniya — O'rtacha Total Narq\n(Grouped Bar)", fontweight='bold')
ax6.set_ylabel("O'rtacha narx (so'm)")
ax6.legend(fontsize=8, framealpha=0.2, ncol=5)
ax6.grid(True, axis='y')

# ── 7. Scatter: quantity vs total_price (outlier highlight) ──
ax7 = fig3.add_subplot(gs3[2, 2])
lo_tp, up_tp, *_ = iqr_bounds(df['total_price'])
normal  = df[(df['total_price'] >= lo_tp) & (df['total_price'] <= up_tp)]
outlier = df[(df['total_price'] < lo_tp)  | (df['total_price'] > up_tp)]
ax7.scatter(normal['quantity'],  normal['total_price'],
            color=BLUE,  alpha=0.25, s=12, label=f'Normal ({len(normal)})')
ax7.scatter(outlier['quantity'], outlier['total_price'],
            color=RED,   alpha=0.9,  s=45, marker='D',
            label=f'Outlier ({len(outlier)})', zorder=5)
ax7.axhline(up_tp, color=ORANGE, linewidth=1.5, linestyle='--',
            label=f'Yuqori chegara ({up_tp:,.0f})')
ax7.set_title("Quantity vs Total Price\n(Outlier Highlight)", fontweight='bold')
ax7.set_xlabel('Quantity')
ax7.set_ylabel("Total Price")
ax7.legend(fontsize=7.5, framealpha=0.2)
ax7.grid(True)

plt.savefig('eda_sheet3_categorical.png', dpi=130,
            bbox_inches='tight', facecolor='#0f1117')
print("✅  Sheet 3 saqlandi: eda_sheet3_categorical.png")
plt.close(fig3)

print("\n🎉  Barcha 3 ta EDA grafik muvaffaqiyatli yaratildi!")