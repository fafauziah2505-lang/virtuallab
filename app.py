import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, minimize

st.set_page_config(layout="wide", page_title="Virtual Lab Fungsi Polinomial")

# --- Fungsi Inti Matematika ---

def fungsi_polinomial(x, koefisien):
    """Menghitung nilai fungsi polinomial P(x).
    koefisien[0] adalah koefisien x^n, koefisien[-1] adalah konstanta."""
    y = 0
    n = len(koefisien) - 1
    for i, a in enumerate(koefisien):
        y += a * (x**(n - i))
    return y

def turunan_polinomial(koefisien):
    """Menghghitung koefisien turunan pertama (untuk mencari titik kritis)."""
    n = len(koefisien) - 1
    koefisien_turunan = []
    for i in range(n):
        derajat = n - i
        koefisien_turunan.append(koefisien[i] * derajat)
    return koefisien_turunan

# --- Antarmuka Streamlit (UI) ---

st.title("➗ Virtual Lab: Eksplorasi Fungsi Polinomial")
st.markdown("Ubah koefisien fungsi $P(x)$ dan amati perubahan pada Domain, Range, dan Titik Kritisnya.")

# --- Input Koefisien (Sidebar) ---

st.sidebar.header("📥 Koefisien Fungsi Polinomial")
st.sidebar.markdown("Bentuk Umum: $P(x) = a_n x^n + ... + a_1 x + a_0$")

# Derajat tertinggi
derajat = st.sidebar.select_slider(
    "Pilih Derajat Tertinggi ($n$)",
    options=[2, 3, 4, 5],
    value=3 # Default ke fungsi kubik
)

# Input koefisien berdasarkan derajat yang dipilih
koefisien = []
for i in range(derajat, -1, -1):
    a = st.sidebar.number_input(
        f"Koefisien $a_{i}$ (untuk $x^{i}$)",
        value=1 if i == derajat else (0 if i > 0 else 0), # Default a_n=1, a_0=0
        step=0.1,
        key=f"a{i}"
    )
    koefisien.append(a)

# Pastikan koefisien tertinggi tidak nol untuk mempertahankan derajat
if koefisien[0] == 0 and derajat > 0:
    st.sidebar.warning(f"Koefisien $a_{derajat}$ tidak boleh nol. Menggunakan 1 sebagai ganti.")
    koefisien[0] = 1

# --- Visualisasi dan Analisis (Main Content) ---

# Tampilkan Fungsi yang Diinput
polinomial_str = ""
for i in range(derajat + 1):
    a = koefisien[i]
    if a != 0:
        power = derajat - i
        term = f"{abs(a):.1f}"
        if power > 1:
            term += f"x^{power}"
        elif power == 1:
            term += "x"
        
        if i == 0: # Term pertama
            polinomial_str += (f"{term}" if a > 0 else f"-{term}")
        else:
            sign = " + " if a > 0 else " - "
            polinomial_str += f"{sign}{term}"
        
# Bersihkan kasus jika koefisien[0] adalah 1 atau -1
polinomial_str = polinomial_str.replace("1.0x", "x").replace("1.0x^", "x^")
polinomial_str = polinomial_str.replace("0.0", "").strip()
if polinomial_str.startswith("-"):
    polinomial_str = polinomial_str.replace("-", "-", 1)
st.markdown(f"**Fungsi Saat Ini: $P(x) = {polinomial_str}$**")


col_grafik, col_analisis = st.columns([2, 1])

# --- 1. GRAFIK FUNGSI ---
with col_grafik:
    st.subheader("Visualisasi Grafik Fungsi")

    # Batas Plot X
    x_min_plot = st.slider("Batas X (Plot Min)", -10.0, 0.0, -5.0, step=0.5)
    x_max_plot = st.slider("Batas X (Plot Max)", 0.0, 10.0, 5.0, step=0.5)
    
    # Generate data
    X = np.linspace(x_min_plot, x_max_plot, 500)
    Y = np.array([fungsi_polinomial(x, koefisien) for x in X])
    
    # Buat Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(X, Y, label=f"$P(x)$", color='blue')
    
    # Atur Sumbu dan Grid
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.5)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlabel("x (Domain)")
    ax.set_ylabel("y (Range)")
    ax.set_title(f"Grafik Fungsi Polinomial Derajat {derajat}")
    ax.legend()
    
    # Batas Sumbu Y otomatis agar grafik terlihat jelas
    y_min_plot = Y.min() - (Y.max() - Y.min()) * 0.1
    y_max_plot = Y.max() + (Y.max() - Y.min()) * 0.1
    ax.set_ylim([y_min_plot, y_max_plot])
    
    st.pyplot(fig)


# --- 2. ANALISIS DOMAIN, RANGE, DAN TITIK KRITIS ---
with col_analisis:
    st.subheader("Hasil Analisis")

    # --- Domain ---
    st.markdown("#### 1. Domain")
    st.success("Domain ($\mathbf{D_P}$): $\\mathbf{x \\in \\mathbb{R}}$")
    st.markdown("Untuk semua fungsi polinomial, domainnya adalah **semua bilangan real** ($\mathbb{R}$) karena tidak ada pembatasan nilai $x$ yang menyebabkan fungsi tidak terdefinisi.")
    
    # --- Range ---
    st.markdown("#### 2. Range")
    if derajat % 2 == 1:
        # Fungsi berderajat ganjil (Kubik, Quintik, dll.)
        st.info("Range ($\mathbf{R_P}$): $\\mathbf{y \\in \\mathbb{R}}$")
        st.markdown("Karena derajat tertinggi **ganjil**, grafik akan membentang dari $-\\infty$ hingga $+\\infty$ (atau sebaliknya). Range-nya adalah **semua bilangan real** ($\mathbb{R}$).")
    else:
        # Fungsi berderajat genap (Kuadratik, Quartik, dll.)
        st.warning("Range ($\mathbf{R_P}$): Terbatas")
        
        # Mencari nilai minimum/maksimum global (yang menentukan range)
        a_n = koefisien[0]
        
        # Mencari titik kritis untuk estimasi batas Range
        turunan_koef = turunan_polinomial(koefisien)
        
        try:
            # Menggunakan minimisasi numerik
            if a_n > 0: # U terbuka ke atas (punya minimum global)
                # Mencari minimum
                result = minimize(lambda x: fungsi_polinomial(x, koefisien), x0=0)
                y_min = result.fun
                st.markdown(f"Karena $a_{derajat} > 0$, grafik terbuka ke atas. Range: $\\mathbf{{y \\geq {y_min:.2f}}}$")
            else: # U terbuka ke bawah (punya maksimum global)
                # Mencari maksimum (minimisasi dari -P(x))
                result = minimize(lambda x: -fungsi_polinomial(x, koefisien), x0=0)
                y_max = -result.fun
                st.markdown(f"Karena $a_{derajat} < 0$, grafik terbuka ke bawah. Range: $\\mathbf{{y \\leq {y_max:.2f}}}$")
        except Exception:
            st.error("Gagal menghitung Range secara numerik.")
            
    # --- Titik Kritis ---
    st.markdown("#### 3. Titik Kritis (Minimum/Maksimum Lokal)")
    if derajat < 2:
        st.info("Tidak ada titik kritis (derajat $\\leq 1$). Ini adalah garis lurus.")
    else:
        try:
            turunan_ko = turunan_polinomial(koefisien)
            
            # Mencari akar dari turunan pertama P'(x) = 0
            # Fungsi polinomial yang di-turunkan
            def P_prime(x):
                 return fungsi_polinomial(x, turunan_ko)

            # Mencari semua akar (titik kritis x-nya)
            # Solusi praktis, hanya mencari min dan max dalam range plot
            # Untuk aplikasi yang lebih kokoh, perlu algoritma pencarian akar yang lebih kompleks (mis. np.roots)
            
            # Mencari nilai ekstrem dalam range plot
            x_ekstrem_min_plot = minimize_scalar(lambda x: fungsi_polinomial(x, koefisien), bounds=(x_min_plot, x_max_plot), method='bounded').x
            y_ekstrem_min_plot = fungsi_polinomial(x_ekstrem_min_plot, koefisien)
            
            x_ekstrem_max_plot = minimize_scalar(lambda x: -fungsi_polinomial(x, koefisien), bounds=(x_min_plot, x_max_plot), method='bounded').x
            y_ekstrem_max_plot = fungsi_polinomial(x_ekstrem_max_plot, koefisien)
            
            titik_kritis_x = []
            
            # Saring agar hanya menampilkan titik kritis yang berbeda
            if x_ekstrem_min_plot not in titik_kritis_x and x_ekstrem_min_plot > x_min_plot + 0.01 and x_ekstrem_min_plot < x_max_plot - 0.01:
                 titik_kritis_x.append(x_ekstrem_min_plot)
            if x_ekstrem_max_plot not in titik_kritis_x and x_ekstrem_max_plot > x_min_plot + 0.01 and x_ekstrem_max_plot < x_max_plot - 0.01:
                 titik_kritis_x.append(x_ekstrem_max_plot)
                 
            # Hilangkan duplikat jika min dan max ada di ujung batas
            titik_kritis_x = list(set(np.round(titik_kritis_x, 2)))
            
            st.markdown(f"Fungsi dapat memiliki hingga **{derajat - 1}** titik kritis.")
            
            if len(titik_kritis_x) > 0:
                for x_crit in titik_kritis_x:
                    y_crit = fungsi_polinomial(x_crit, koefisien)
                    
                    # Tambahkan tanda titik kritis ke grafik
                    with col_grafik:
                        ax.plot(x_crit, y_crit, 'o', color='red', markersize=8, label='Titik Kritis')
                        ax.text(x_crit + 0.1, y_crit, f"({x_crit:.2f}, {y_crit:.2f})", color='red')
                    
                    st.markdown(f" - **$({x_crit:.2f}, {y_crit:.2f})$**")
                
                # Update grafik dengan titik kritis baru
                st.pyplot(fig)
            else:
                 st.markdown("Tidak ada titik kritis yang terdeteksi dalam rentang plot.")
                 
        except Exception as e:
            st.error(f"Gagal mencari titik kritis: {e}")
