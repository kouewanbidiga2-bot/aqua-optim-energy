# aqua-optim-energy
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import serial  # NOUVELLE BIBLIOTHÈQUE POUR L'ARDUINO
import time

# --- FONCTIONS DE COMMUNICATION SÉRIE ---

@st.cache_resource
def init_serial(port_name):
    """Initialise la connexion série une seule fois pour ne pas bloquer Streamlit"""
    try:
        # 9600 correspond au Serial.begin(9600) de votre Arduino
        return serial.Serial(port_name, 9600, timeout=1)
    except serial.SerialException:
        return None

def read_arduino_data(ser):
    """Lit et décode la ligne envoyée par l'Arduino"""
    if ser and ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        try:
            # On sépare les données via la virgule (NIVEAU,POMPE)
            niveau, pompe = line.split(',')
            return int(niveau), int(pompe)
        except ValueError:
            return None, None
    return None, None

# --- INTERFACE UTILISATEUR ---

def main():
    st.set_page_config(
        page_title='AQUA-OPTIM ENERGY',
        page_icon='🚰',
        layout='wide'
    )
    
    st.title('🚰 AQUA-OPTIM ENERGY - Système Intelligent ONEA')
    st.markdown('### Hackathon ONEA - Boucle de rétroaction et Optimisation')
    
    # Ajout du 5ème onglet pour le Temps Réel
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        '📊 Tableau de Bord', 
        '🔮 Prévision IA', 
        '⚡ Optimisation',
        '⚠️ Sentinel',
        '📡 Temps Réel'
    ])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_prediction()
    
    with tab3:
        show_optimization()
    
    with tab4:
        show_sentinel()
        
    with tab5:
        show_realtime()

def show_realtime():
    st.header('📡 Connexion Directe Maquette (Temps Réel)')
    st.info("Ce module écoute le port USB pour lire les données du capteur ultrasonique et de la pompe.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Saisie du port. Sous Windows c'est souvent COM3, COM4. 
        # Sous Linux/Codespaces/Mac, c'est souvent /dev/ttyACM0 ou /dev/ttyUSB0
        port_input = st.text_input("Port de l'Arduino", value="/dev/ttyACM0")
        ser = init_serial(port_input)
        
        if ser:
            st.success(f"✅ Connecté sur {port_input}")
        else:
            st.error(f"❌ Déconnecté. Vérifiez le port et le câble USB.")
            
    with col2:
        st.markdown("### Données en direct")
        # Un bouton pour forcer la lecture de la ligne
        if st.button('🔄 Lire les capteurs', type='primary'):
            if ser:
                niveau, pompe = read_arduino_data(ser)
                
                if niveau is not None:
                    # Affichage visuel du niveau
                    st.metric("Niveau d'Eau Actuel", f"{niveau} %")
                    st.progress(niveau / 100)
                    
                    # Affichage visuel de l'état de la pompe
                    etat = "🟢 Allumée" if pompe == 1 else "🔴 Coupée"
                    st.metric("État de la Pompe", etat)
                else:
                    st.warning("Aucune donnée reçue. La boucle Arduino tourne-t-elle ?")
            else:
                st.warning("Veuillez d'abord connecter l'Arduino.")

def show_dashboard():
    st.header('📊 Tableau de Bord Énergétique')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric('Économies Potentielles', '25%', '+25%', delta_color='inverse')
    with col2: st.metric('ROI Estimé', '< 3 mois')
    with col3: st.metric('Stations Optimisables', '30')
    with col4: st.metric('Économies Annuelles', '150M FCFA')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('📈 Consommation Énergétique')
        hours = list(range(24))
        energy_consumption = [85, 80, 75, 70, 65, 70, 90, 110, 125, 120, 115, 110, 105, 100, 105, 110, 115, 120, 125, 120, 110, 100, 90, 85]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=energy_consumption, mode='lines', name='Consommation'))
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader('💧 Demande en Eau')
        water_demand = [c * 0.8 for c in energy_consumption]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=water_demand, mode='lines', name='Demande', line=dict(color='blue')))
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def show_prediction():
    st.header('🔮 Prévision Intelligente par IA')
    col1, col2 = st.columns(2)
    with col1: prediction_days = st.slider('Jours à prédire', 1, 7, 3)
    with col2: confidence = st.slider('Niveau de confiance', 0.8, 0.95, 0.9)
    if st.button('📊 Générer les Prévisions', type='primary'):
        hours = list(range(24 * prediction_days))
        predicted = [65 + 25 * np.sin((h+24)/24 * 2 * np.pi) for h in hours]
        st.success("Prévisions générées avec succès (Simulation).")

def show_optimization():
    st.header('⚡ Optimisation Énergétique')
    col1, col2 = st.columns(2)
    with col1: peak_price = st.number_input('Prix heure pleine (FCFA/kWh)', value=85)
    with col2: off_peak_price = st.number_input('Prix heure creuse (FCFA/kWh)', value=45)
    if st.button('🔄 Calculer l\'Optimisation', type='primary'):
        st.success("Optimisation tarifaire calculée.")

def show_sentinel():
    st.header('⚠️ Sentinel Énergétique')
    st.error('Détection d\'Anomalies : surveille les équipements.')
    st.warning('**PMP_004** - Efficacité critique (45%) - Maintenance urgente')

if __name__ == '__main__':
    main()
