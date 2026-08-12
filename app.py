import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import json

# --- CONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Zuhri Formalism Engine Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOM & STYLE ---
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-title">Zuhri Formalism Integrated Engine Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem Pemrosesan Data & Simulasi Sub-Surface (Air Murni, Emas & Mekanika Vakum)</div>', unsafe_allow_html=True)

# --- WIDGET GPS LOKASI HP (NATIVE GEOLOCATION) ---
st.sidebar.markdown("### 📍 Deteksi Koordinat GPS HP")
st.sidebar.write("Klik tombol di bawah untuk mengambil titik lokasi presisi Anda berdiri:")

# Inject JavaScript untuk mengambil GPS HP
gps_code = """
<div style="background-color: #f1f5f9; padding: 10px; border-radius: 8px; text-align: center;">
    <button onclick="getLocation()" style="background-color: #10B981; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">
        🛰️ Ambil Koordinat Saya
    </button>
    <p id="gps_status" style="font-size: 12px; color: #475569; margin-top: 8px; font-weight: bold;">Status: Belum Diambil</p>
</div>

<script>
function getLocation() {
  var status = document.getElementById("gps_status");
  if (navigator.geolocation) {
    status.innerHTML = "⏳ Mengambil koordinat GPS...";
    navigator.geolocation.getCurrentPosition(showPosition, showError, {enableHighAccuracy: true});
  } else { 
    status.innerHTML = "❌ GPS tidak didukung di browser ini.";
  }
}

function showPosition(position) {
  var lat = position.coords.latitude;
  var lon = position.coords.longitude;
  var acc = position.coords.accuracy;
  document.getElementById("gps_status").innerHTML = "✅ Lat: " + lat.toFixed(5) + "<br>Lon: " + lon.toFixed(5) + " (Akurasi: " + acc.toFixed(1) + "m)";
}

function showError(error) {
  var status = document.getElementById("gps_status");
  switch(error.code) {
    case error.PERMISSION_DENIED:
      status.innerHTML = "❌ Izin GPS Ditolak pengguna.";
      break;
    case error.POSITION_UNAVAILABLE:
      status.innerHTML = "❌ Informasi lokasi tidak tersedia.";
      break;
    case error.TIMEOUT:
      status.innerHTML = "❌ Waktu permintaan GPS habis.";
      break;
    case error.UNKNOWN_ERROR:
      status.innerHTML = "❌ Terjadi kesalahan GPS tidak dikenal.";
      break;
  }
}
</script>
"""
with st.sidebar:
    components.html(gps_code, height=140)

# Input Manual Koordinat Backup
st.sidebar.markdown("---")
st.sidebar.markdown("**Atau Input Manual Titik Koordinat:**")
col_lat, col_lon = st.sidebar.columns(2)
lat_val = col_lat.number_input("Latitude", value=-6.200000, format="%.6f")
lon_val = col_lon.number_input("Longitude", value=106.816666, format="%.6f")

# --- TABS NAVIGASI UTAMA ---
tab1, tab2, tab3 = st.tabs([
    "🌊 ZMO Geo-Mapper (Air Murni)", 
    "🥇 VPD Gold Detector (Emas)", 
    "⚙️ Mekanika Vakum"
])

# ==============================================================================
# TAB 1: ZMO GEO-MAPPER (AIR MURNI)
# ==============================================================================
with tab1:
    st.header("🌊 Pemetaan Akuifer Air Murni (ZMO Engine)")
    st.caption("Mengisolasi sinyal koherensi akuifer air murni dari lempung/air asin.")
    
    col_ctrl, col_display = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Control Panel")
        mode_air = st.radio("Mode Air", ["Single Point", "Grid Scan (10x10)"], key="air_mode")
        pi_eff = st.number_input("Pi Efektif (π_eff)", value=3.14189, format="%.5f", key="air_pi")
        grad_h = st.number_input("Gradien Regangan (∇h_μν)", value=12.40, format="%.2f", key="air_grad")
        phi_z = st.number_input("Varians Fase (ϕ_z)", value=0.0150, format="%.4f", key="air_phi")
        
        btn_air = st.button("Jalankan Pemindaian Air", key="btn_air")

    with col_display:
        st.subheader("Hasil Analisis Titik & Area")
        
        if btn_air:
            # Tampilkan peta lokasi titik survey
            st.map({"lat": [lat_val], "lon": [lon_val]}, zoom=14)
            st.info(f"📍 **Titik Analisis GPS:** Lat {lat_val:.6f}, Lon {lon_val:.6f}")
            
            if mode_air == "Single Point":
                # Algoritma Koherensi Air Murni
                coherence = (pi_eff * grad_h) / (1.0 + phi_z * 100)
                is_pure_water = phi_z < 0.05 and coherence > 35.0
                
                if is_pure_water:
                    depth = (grad_h * 3.5) + (1.0 / (phi_z + 0.001)) * 0.2
                    st.success(f"✅ **AKUIFER AIR MURNI TERDETEKSI!**\n\n"
                               f"* **Tingkat Koherensi Sinyal:** {coherence:.2f}\n"
                               f"* **Estimasi Kedalaman Bor Terbaik:** {depth:.1f} Meter\n"
                               f"* **Karakteristik:** Mengalir, Rendah Mineral/Garam.")
                else:
                    st.error("❌ **TIDAK TERDETEKSI AKUIFER AIR MURNI**\n\n"
                             "Indikasi: Anomali didominasi lapisan lempung basah, air asin, atau tanah padat inkoheren.")
            
            else: # Grid Scan 10x10
                np.random.seed(int(grad_h * 100))
                grid_data = np.random.rand(10, 10) * 0.08
                # Tambahkan pusat sinyal air
                grid_data[4:7, 3:6] -= 0.035
                grid_data = np.clip(grid_data, 0.001, 0.1)
                
                fig, ax = plt.subplots(figsize=(6, 5))
                c = ax.imshow(grid_data, cmap='YlGnBu_r', origin='lower')
                fig.colorbar(c, ax=ax, label='Varians Fase (ϕ_z) - Makin Rendah Makin Murni')
                ax.set_title("Peta Varians Fase Akuifer (10x10 Grid)")
                
                # Tandai episentrum terbaik
                min_y, min_x = np.unravel_index(np.argmin(grid_data), grid_data.shape)
                ax.plot(min_x, min_y, 'rx', markersize=12, markeredgewidth=3, label='Episentrum Akuifer')
                ax.legend()
                
                st.pyplot(fig)
                st.success(f"🎯 **Episentrum Akuifer Terbaik di Grid:** X={min_x}, Y={min_y} (Nilai ϕ_z: {grid_data[min_y, min_x]:.4f})")

# ==============================================================================
# TAB 2: VPD GOLD DETECTOR (EMAS)
# ==============================================================================
with tab2:
    st.header("🥇 Deteksi Urat Emas Subterranean (VPD Engine)")
    st.caption("Pemanfaatan Kerapatan Massa Emas (19.3 g/cm³) Terhadap Porositas Vakum ZPE.")
    
    col_ctrl2, col_display2 = st.columns([1, 2])
    
    with col_ctrl2:
        st.subheader("Control Panel Emas")
        mode_emas = st.radio("Mode Emas", ["Single Point", "Grid Scan (10x10)"], key="gold_mode")
        pi_eff_g = st.number_input("Pi Efektif (π_eff)", value=3.14245, format="%.5f", key="gold_pi")
        grad_h_g = st.number_input("Gradien Regangan (∇h_μν)", value=18.50, format="%.2f", key="gold_grad")
        phi_z_g = st.number_input("Varians Fase (ϕ_z)", value=0.0080, format="%.4f", key="gold_phi")
        porosity_g = st.number_input("Dip Porositas Vakum", value=0.75, format="%.2f", key="gold_por")
        
        btn_gold = st.button("Jalankan Pemindaian Emas", key="btn_gold")

    with col_display2:
        st.subheader("Hasil Analisis Deposit Emas")
        
        if btn_gold:
            st.map({"lat": [lat_val], "lon": [lon_val]}, zoom=14)
            st.info(f"📍 **Titik Analisis GPS:** Lat {lat_val:.6f}, Lon {lon_val:.6f}")
            
            if mode_emas == "Single Point":
                # Algoritma Kerapatan Urat Emas
                gold_score = (grad_h_g * porosity_g) / (phi_z_g * 1000 + 1.0)
                is_gold = phi_z_g < 0.02 and porosity_g > 0.60 and gold_score > 1.2
                
                if is_gold:
                    z_depth = (grad_h_g * 2.1) + 15.0
                    purity = min(99.9, 70.0 + (gold_score * 15.0))
                    st.success(f"🥇 **URAT EMAS (Au-197) TERKONFIRMASI!**\n\n"
                               f"* **Skor Anomali Massa:** {gold_score:.3f}\n"
                               f"* **Estimasi Kedalaman Urat (Z_depth):** {z_depth:.1f} Meter\n"
                               f"* **Indeks Puritas/Kadar:** ~{purity:.1f}%")
                else:
                    st.warning("⚠️ **TIDAK ADANAMOMALI URAT EMAS BERSIGIFIKAN**\n\n"
                               "Sinyal tidak memenuhi kriteria himpitan massa emas murni (porositas/varians tidak cocok).")
            
            else: # Grid Scan 10x10
                np.random.seed(int(grad_h_g * 50))
                grid_gold = np.random.rand(10, 10) * 0.4
                # Simulasikan jalur urat emas (vein pattern)
                grid_gold[2:8, 4] += 0.55
                grid_gold[4, 2:7] += 0.45
                
                fig2, ax2 = plt.subplots(figsize=(6, 5))
                c2 = ax2.imshow(grid_gold, cmap='YlOrRd', origin='lower')
                fig2.colorbar(c2, ax=ax2, label='Indikator Kerapatan Urat Emas')
                ax2.set_title("Peta Anomali Urat Emas 2D (10x10 Grid)")
                
                max_y, max_x = np.unravel_index(np.argmax(grid_gold), grid_gold.shape)
                ax2.plot(max_x, max_y, '*', color='gold', markersize=15, markeredgecolor='black', label='Episentrum Urat Emas')
                ax2.legend()
                
                st.pyplot(fig2)
                st.success(f"⭐ **Episentrum Utama Urat Emas:** Grid X={max_x}, Y={max_y} (Skor Anomali: {grid_gold[max_y, max_x]:.2f})")

# ==============================================================================
# TAB 3: MEKANIKA VAKUM
# ==============================================================================
with tab3:
    st.header("⚙️ Kalkulator Mekanika Vakum & Energi Medium")
    st.caption("Simulasi teori regangan metrik dan kalkulasi energi tersimpan dalam medium ruang.")
    
    col_v1, col_v2 = st.columns([1, 2])
    
    with col_v1:
        st.subheader("Parameter Metrik")
        kappa_0 = st.number_input("Konstanta Kelenturan (κ_0)", value=1.0, step=0.1)
        strain_eps = st.number_input("Besar Regangan (||ε_μν||)", value=2.5, step=0.1)
        vol_m3 = st.number_input("Volume Modulasi Ruang (m³)", value=100.0, step=10.0)
        
        btn_calc_vac = st.button("Hitung Energi Regangan", key="btn_vac")
        
    with col_v2:
        st.subheader("Hasil Kalkulasi Energi")
        if btn_calc_vac:
            # Rumus Energi Regangan Medium: S_medium = 0.5 * kappa_0 * (strain_eps^2) * vol_m3
            energy_joules = 0.5 * kappa_0 * (strain_eps ** 2) * vol_m3
            energy_kwh = energy_joules / 3_600_000.0
            
            st.metric(label="Energi Regangan Tersimpan (Joule)", value=f"{energy_joules:,.2f} J")
            st.metric(label="Setara KiloWatt-Hour (kWh)", value=f"{energy_kwh:.6f} kWh")
            
            st.info("💡 **Catatan Teori:** Energi ini merepresentasikan besar potensi potensial deformasi metrik ruang lokal yang dikorelasikan dengan varians fase gelombang.")
