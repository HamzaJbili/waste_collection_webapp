# map_tools.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from data_handler import save_settings

def show_map_tab(settings):
    st.markdown("### 🗘️ Collection Circuit Map")
    st.write("Draw or view collection zones. Circuits are stored in your settings.")

    m = folium.Map(location=[36.8, 10.1], zoom_start=11)
    draw = Draw(export=True)
    draw.add_to(m)

    for name, geojson in settings.get("zones", {}).items():
        gj = folium.GeoJson(geojson, name=name)
        gj.add_to(m)

    map_data = st_folium(m, width=700, height=500)

    if st.button("📂 Save Map Zones"):
        if map_data and 'all_drawings' in map_data:
            new_zones = {f"Zone_{i+1}": shape for i, shape in enumerate(map_data['all_drawings'])}
            settings["zones"] = new_zones
            save_settings(settings)
            st.success("Zones saved successfully.")
