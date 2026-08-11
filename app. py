import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Zuhri Formalism Engine Suite",
    page_icon="🛡️",
    layout="wide"
)

# --- KONSTANTA ENGINE ZMO ---
KAPPA_0 = 1.0
LAMBDA_Z = 42.5
PI_0 = math.pi

# --- ENGINE HELPER FUNCTIONS ---
def analyze_water_point(pi_eff, grad_h, phase_var):
    is_coherent = phase_var < 0.05
    delta_pi = abs(pi_eff - PI_0)
    if delta_pi <= 1e-6 or grad_h <= 0:
        return is_coherent, 0.0
    ratio = (KAPPA_0 * grad_h) / delta_pi
    if ratio <= 1.0:
        return is_coherent, 0.0
    return is_coherent, abs(LAMBDA_Z * math.log(ratio))

def analyze_gold_point(pi_eff, grad_h, phase_var, porosity_dip):
    is_gold_coherent = phase_var < 0.02
    is_high_density = porosity_dip > 0.6
    delta_pi = abs(pi_eff - PI_0)
    if delta_pi <= 1e-6 or grad_h <= 0:
        return False, 0.0, 0.0
    ratio = (KAPPA_0 * grad_h) / delta_pi
    if ratio <= 1.0:
        return False, 0.0, 0.0
    z_depth = abs(LAMBDA_Z * math.log(ratio))
    gold_purity_score = min(100.0, (porosity_dip / 0.95) * 100)
    return (is_gold_coherent and is_high_density), z_depth, gold_purity_score

# --- HEADER APLIKASI ---
st.title("🛡️ Zuhri Formalism Integrated Engine Suite")
st.caption("Aplikasi Rekayasa Metrik Ruang-Waktu & Pemetaan Sub-Permukaan Jarak Jauh")

# --- TAB NAVIGASI MULTI-APLIKASI ---
tab1, tab2, tab3 = st.tabs([
    "🌊 ZMO Geo-Mapper (Air Murni)", 
    "🥇 VPD Gold Detector (Emas)", 
    "⚙️ Kalkulator Mekanika Vakum"
])

# ==========================================
# TAB 1: EKSPLORASI AIR MURNI (AKUIFER)
# ==========================================
with tab1:
    st.header("🌊 Pemeta Akuifer Air Murni Sub-Permukaan")
    st.markdown("Mengisolasi sinyal koherensi akuifer air murni dari lempung/air asin.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Control Panel")
        mode_water = st.radio("Mode Air", ["Single Point", "Grid Scan (10x10)"], key="m_water")
        
        pi_eff_w = st.number_input("Pi Efektif (π_eff)", value=3.14189, format="%.5f", key="pi_w")
        grad_h_w = st.number_input("Gradien Regangan (∇h_μν)", value=12.4, key="grad_w")
        phase_var_w = st.number_input("Varians Fase (ϕ_z)", value=0.015, format="%.4f", key="var_w")
        
        btn_water = st.button("Jalankan Pemindaian Air", type="primary", key="btn_w")

    with col2:
        if mode_water == "Single Point":
            st.subheader("Hasil Analisis Titik")
            if btn_water:
                coherent, depth = analyze_water_point(pi_eff_w, grad_h_w, phase_var_w)
                if coherent and depth > 0:
                    st.success(f"✅ **AKUIFER AIR MURNI TERKONFIRMASI**\n\nEstimasi Kedalaman Bor: **{depth:.2f} Meter**")
                else:
                    st.error("❌ **INKOHEREN / BUKAN AKUIFER AKTIF**")
        else:
            st.subheader("Heatmap Grid Area (10x10)")
            if btn_water:
                grid_size = 10
                coh_matrix = np.zeros((grid_size, grid_size))
                dep_matrix = np.zeros((grid_size, grid_size))
                target_x, target_y = 6, 4
                
                for x in range(grid_size):
                    for y in range(grid_size):
                        dist = math.sqrt((x - target_x)**2 + (y - target_y)**2)
                        p_eff = PI_0 + (0.0008 / (dist + 1))
                        g_h = 15.0 / (dist + 1)
                        p_var = 0.01 * (dist + 0.5)
                        coh, dep = analyze_water_point(p_eff, g_h, p_var)
                        if coh and dep > 0:
                            coh_matrix[y, x] = max(0, 100 - (dist * 18))
                            dep_matrix[y, x] = dep

                fig, ax = plt.subplots(figsize=(5, 4))
                cax = ax.imshow(coh_matrix, cmap='viridis', origin='lower')
                ax.plot(target_x, target_y, marker='X', color='red', markersize=12, label="Episentrum Bor")
                ax.set_title(f"Episentrum: X={target_x}, Y={target_y} | Z_depth={dep_matrix[target_y, target_x]:.1f}m")
                ax.legend()
                st.pyplot(fig)

# ==========================================
# TAB 2: DETEKTOR URAT EMAS (VPD)
# ==========================================
with tab2:
    st.header("🥇 Sensor Kuantisasi Pori Ruang (Gold VPD)")
    st.markdown("Mendeteksi kompresi pori-pori ruang ZPE akibat rapat massa emas ($19.3 \\text{ g/cm}^3$).")
    
    col1_g, col2_g = st.columns([1, 2])
    
    with col1_g:
        st.subheader("Control Panel Emas")
        mode_gold = st.radio("Mode Emas", ["Single Point", "Grid Scan (10x10)"], key="m_gold")
        
        pi_eff_g = st.number_input("Pi Efektif (π_eff)", value=3.14245, format="%.5f", key="pi_g")
        grad_h_g = st.number_input("Gradien Regangan (∇h_μν)", value=18.5, key="grad_g")
        phase_var_g = st.number_input("Varians Fase (ϕ_z)", value=0.008, format="%.4f", key="var_g")
        porosity_dip_g = st.number_input("Dip Porositas Vakum", value=0.82, format="%.2f", key="dip_g")
        
        btn_gold = st.button("Jalankan Pemindaian Emas", type="primary", key="btn_g")

    with col2_g:
        if mode_gold == "Single Point":
            st.subheader("Hasil Analisis Deposit Emas")
            if btn_gold:
                is_gold, depth_g, purity_g = analyze_gold_point(pi_eff_g, grad_h_g, phase_var_g, porosity_dip_g)
                if is_gold:
                    st.success(f"🥇 **URAT EMAS TERKONFIRMASI!**\n\n"
                               f"* **Kedalaman (Z_depth):** `{depth_g:.2f} Meter`\n"
                               f"* **Kadar/Kepadatan:** `{purity_g:.1f}%`")
                else:
                    st.warning("⚠️ **BUKAN DEPOSIT EMAS** (Batuan biasa / Pasir Besi)")
        else:
            st.subheader("Heatmap Kepadatan Emas (10x10)")
            if btn_gold:
                grid_size = 10
                gold_matrix = np.zeros((grid_size, grid_size))
                dep_g_matrix = np.zeros((grid_size, grid_size))
                target_x_g, target_y_g = 3, 7
                
                for x in range(grid_size):
                    for y in range(grid_size):
                        dist = math.sqrt((x - target_x_g)**2 + (y - target_y_g)**2)
                        p_eff = PI_0 + (0.0012 / (dist + 1))
                        g_h = 22.0 / (dist + 1)
                        p_var = 0.005 * (dist + 0.2)
                        p_dip = max(0.1, 0.9 - (dist * 0.15))
                        is_g, dep, pur = analyze_gold_point(p_eff, g_h, p_var, p_dip)
                        if is_g:
                            gold_matrix[y, x] = pur
                            dep_g_matrix[y, x] = dep

                fig_g, ax_g = plt.subplots(figsize=(5, 4))
                cax_g = ax_g.imshow(gold_matrix, cmap='YlOrRd', origin='lower')
                fig_g.colorbar(cax_g, label="Kadar (%)")
                ax_g.plot(target_x_g, target_y_g, marker='*', color='gold', markersize=14, markeredgecolor='black', label="Episentrum Emas")
                ax_g.set_title(f"Episentrum: X={target_x_g}, Y={target_y_g} | Z_depth={dep_g_matrix[target_y_g, target_x_g]:.1f}m")
                ax_g.legend()
                st.pyplot(fig_g)

# ==========================================
# TAB 3: KALKULATOR MEKANIKA VAKUM
# ==========================================
with tab3:
    st.header("⚙️ Kalkulator Tensor Regangan Vakum")
    st.markdown("Menghitung energi regangan medium $S_{\\text{medium}}$ berdasarkan Tensor Regangan Topologis $\\epsilon_{\\mu\\nu}$.")
    
    st.latex(r"\mathcal{S}_{\text{medium}} = \int_{\mathcal{M}} \kappa_0 \cdot \|\epsilon_{\mu\nu}\|^2 \, d^4x")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        kappa_val = st.number_input("Konstanta Kelenturan (κ_0)", value=1.0)
        epsilon_val = st.number_input("Besar Regangan (||ε_μν||)", value=2.5)
        volume_val = st.number_input("Volume Ruang Modulasi (m³)", value=10.0)
    
    with col_v2:
        if st.button("Hitung Energi Regangan"):
            strain_energy = kappa_val * (epsilon_val ** 2) * volume_val
            st.info(f"⚡ **Total Energi Regangan Medium:** `{strain_energy:.4f} Joule`")
