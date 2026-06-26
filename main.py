# ============================================================
# FAST FOOD - LINEAR REGRESSION LOYIHASI
# Maqsad: total_price ni bashorat qilish
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 120
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. DATA YUKLASH
# ============================================================
print("=" * 55)
print("  1-BOSQICH: DATA YUKLASH")
print("=" * 55)

df = pd.read_csv('fast_food_data.csv')
print(f"Dataset shakli: {df.shape[0]} qator, {df.shape[1]} ustun")
print(f"\nUstunn nomlari: {df.columns.tolist()}")
print(f"\nBirinchi 3 qator:\n{df.head(3)}")


# ============================================================
# 2. DATA TOZALASH (Data Cleaning)
# ============================================================
print("\n" + "=" * 55)
print("  2-BOSQICH: DATA TOZALASH")
print("=" * 55)

print(f"Null qiymatlar:\n{df.isnull().sum()}")
print(f"\nDublikat qatorlar: {df.duplicated().sum()}")
print(f"Data turlari:\n{df.dtypes}")

# order_time dan yangi ustunlar chiqarish
df['order_time'] = pd.to_datetime(df['order_time'])
df['month'] = df['order_time'].dt.month
df['day']   = df['order_time'].dt.day

print("\n✅ order_time dan month va day ustunlari yaratildi.")


# ============================================================
# 3. FEATURE ENGINEERING (Encoding)
# ============================================================
print("\n" + "=" * 55)
print("  3-BOSQICH: ENCODING (Kategoriyalarni raqamga)")
print("=" * 55)

le_company = LabelEncoder()
le_product  = LabelEncoder()
le_day      = LabelEncoder()

df['company_enc']  = le_company.fit_transform(df['company_name'])
df['product_enc']  = le_product.fit_transform(df['product_name'])
df['day_enc']      = le_day.fit_transform(df['day_of_week'])

print("Label Encoding natijalari:")
print(f"  company_name : {dict(zip(le_company.classes_, le_company.transform(le_company.classes_)))}")
print(f"  product_name : {dict(zip(le_product.classes_, le_product.transform(le_product.classes_)))}")


# ============================================================
# 4. FEATURES va TARGET TANLASH
# ============================================================
print("\n" + "=" * 55)
print("  4-BOSQICH: FEATURES va TARGET")
print("=" * 55)

# X = kiruvchi o'zgaruvchilar (features)
# y = bashorat qilinuvchi o'zgaruvchi (target)

features = ['price', 'quantity', 'customer_count', 'hour',
            'company_enc', 'product_enc', 'day_enc', 'month', 'day']
target   = 'total_price'

X = df[features]
y = df[target]

print(f"Features (X): {features}")
print(f"Target  (y): {target}")
print(f"\nX shakli: {X.shape}")
print(f"y shakli: {y.shape}")


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================
print("\n" + "=" * 55)
print("  5-BOSQICH: TRAIN / TEST BO'LISH")
print("=" * 55)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Train to'plami: {X_train.shape[0]} ta yozuv (80%)")
print(f"Test  to'plami: {X_test.shape[0]} ta yozuv (20%)")


# ============================================================
# 6. SCALING (Normallashtirish)
# ============================================================
print("\n" + "=" * 55)
print("  6-BOSQICH: SCALING (StandardScaler)")
print("=" * 55)

scaler  = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("✅ StandardScaler qo'llanildi:")
print(f"   Har bir feature o'rtacha=0, std=1 ga keltirildi")


# ============================================================
# 7. MODEL QURISH va O'QITISH
# ============================================================
print("\n" + "=" * 55)
print("  7-BOSQICH: LINEAR REGRESSION MODELI")
print("=" * 55)

model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("✅ Model muvaffaqiyatli o'qitildi!")
print(f"\nModel koeffitsientlari (har bir feature ta'siri):")
for fname, coef in zip(features, model.coef_):
    print(f"   {fname:20s}: {coef:+.2f}")
print(f"\nIntercept (b₀): {model.intercept_:.2f}")


# ============================================================
# 8. BASHORAT va NATIJALARNI BAHOLASH (Metrics)
# ============================================================
print("\n" + "=" * 55)
print("  8-BOSQICH: BAHOLASH METRIKALAR")
print("=" * 55)

y_pred = model.predict(X_test_scaled)

mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2   = r2_score(y_test, y_pred)

print(f"  MAE  (O'rtacha absolut xato)  : {mae:,.0f} so'm")
print(f"  RMSE (Kvadrat xato ildizi)    : {rmse:,.0f} so'm")
print(f"  R²   (Aniqlik koeffitsienti)  : {r2:.4f}  ({r2*100:.2f}%)")
print()
if r2 >= 0.9:
    print("  🟢 Ajoyib natija! Model juda yaxshi ishlayapti.")
elif r2 >= 0.7:
    print("  🟡 Yaxshi natija. Model asosiy pattern ni topdi.")
else:
    print("  🔴 Yetarli emas. Yangi features qo'shish kerak.")


# ============================================================
# 9. VIZUALIZATSIYA
# ============================================================
print("\n" + "=" * 55)
print("  9-BOSQICH: GRAFIKLAR CHIZISH")
print("=" * 55)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Fast Food - Linear Regression Tahlil', fontsize=15, fontweight='bold')

# --- Graf 1: Haqiqiy vs Bashorat ---
ax1 = axes[0, 0]
sample = min(300, len(y_test))
ax1.scatter(y_test[:sample], y_pred[:sample], alpha=0.5, color='steelblue', s=20)
mn = min(y_test.min(), y_pred.min())
mx = max(y_test.max(), y_pred.max())
ax1.plot([mn, mx], [mn, mx], 'r--', linewidth=1.5, label='Ideal chiziq')
ax1.set_xlabel("Haqiqiy narx")
ax1.set_ylabel("Bashorat qilingan narx")
ax1.set_title("Haqiqiy vs Bashorat")
ax1.legend()

# --- Graf 2: Xato taqsimoti ---
ax2 = axes[0, 1]
residuals = y_test.values - y_pred
ax2.hist(residuals, bins=50, color='salmon', edgecolor='white')
ax2.axvline(0, color='red', linestyle='--')
ax2.set_xlabel("Xato (Residual)")
ax2.set_ylabel("Soni")
ax2.set_title("Xatolar taqsimoti")

# --- Graf 3: Feature muhimligi ---
ax3 = axes[1, 0]
coef_abs = np.abs(model.coef_)
sorted_idx = np.argsort(coef_abs)
colors = ['#2ecc71' if c > 0 else '#e74c3c' for c in model.coef_[sorted_idx]]
ax3.barh([features[i] for i in sorted_idx], coef_abs[sorted_idx], color=colors)
ax3.set_xlabel("Koeffitsient (mutlaq qiymat)")
ax3.set_title("Feature ta'siri (Feature Importance)")

# --- Graf 4: Kompaniya bo'yicha o'rtacha total_price ---
ax4 = axes[1, 1]
comp_avg = df.groupby('company_name')['total_price'].mean().sort_values(ascending=False)
bars = ax4.bar(comp_avg.index, comp_avg.values,
               color=['#3498db','#e67e22','#2ecc71','#9b59b6','#e74c3c'])
ax4.set_ylabel("O'rtacha total narx (so'm)")
ax4.set_title("Kompaniya bo'yicha o'rtacha narx")
ax4.tick_params(axis='x', rotation=20)
for bar, val in zip(bars, comp_avg.values):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
             f"{val:,.0f}", ha='center', fontsize=8)

plt.tight_layout()
plt.savefig('linear_regression_results.png', bbox_inches='tight')
print("✅ Graf saqlandi: linear_regression_results.png")


# ============================================================
# 10. YANGI BUYURTMA BASHORATLASH
# ============================================================
print("\n" + "=" * 55)
print("  10-BOSQICH: YANGI BUYURTMA BASHORATLASH")
print("=" * 55)

# Misol: KFC da 2 ta Burger, kechki 7 da, 1 ta mijoz
new_order = pd.DataFrame([{
    'price'        : 30000,
    'quantity'     : 2,
    'customer_count': 1,
    'hour'         : 19,
    'company_enc'  : le_company.transform(['KFC'])[0],
    'product_enc'  : le_product.transform(['Burger'])[0],
    'day_enc'      : le_day.transform(['Friday'])[0],
    'month'        : 3,
    'day'          : 15
}])

new_scaled = scaler.transform(new_order[features])
pred_price = model.predict(new_scaled)[0]

print(f"  Buyurtma: KFC, 2x Burger, Juma, soat 19:00")
print(f"  Bashorat qilingan narx: {pred_price:,.0f} so'm")
print(f"  (Haqiqiy narx odatda: {30000*2:,} so'm)")

print("\n" + "=" * 55)
print("  LOYIHA MUVAFFAQIYATLI YAKUNLANDI! ✅")
print("=" * 55)