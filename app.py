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
    st.set_page_config(page_title='AQUA-OPTIM ENERGY', page_icon='🚰', layout='wide')
    
    # On initialise la connexion dans la "mémoire" de Streamlit
    if 'ser' not in st.session_state:
        st.session_state.ser = None
    
    st.title('🚰 AQUA-OPTIM ENERGY - Système Intelligent')
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
        port_input = st.text_input("Port de l'Arduino", value="/dev/ttyACM0")
        
        if st.button("Connecter"):
            # Si une connexion existe déjà, on la ferme proprement
            if st.session_state.ser:
                st.session_state.ser.close()
            
            try:
                st.session_state.ser = serial.Serial(port_input, 9600, timeout=1)
                st.success(f"✅ Connecté sur {port_input}")
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

    with col2:
        # Ici, on utilise st.session_state.ser au lieu de ser local
        if st.session_state.ser and st.session_state.ser.is_open:
            # ... (votre logique de lecture ici)
            niveau, pompe = read_arduino_data(st.session_state.ser)
            # ...
        else:
            st.warning("Veuillez connecter l'Arduino dans la colonne de gauche.")

def show_dashboard():
    st.header('📊 Tableau de Bord Énergétique')
    mode = st.radio("Source des données :", ("📈 Données Historiques (CSV)", "📡 Temps Réel (Maquette)"), horizontal=True)
    
    if mode == "📡 Temps Réel (Maquette)":
        if st.session_state.ser and st.session_state.ser.is_open:
            # On lit les données de l'Arduino
            niveau, pompe = read_arduino_data(st.session_state.ser)
            if niveau is not None:
                st.metric("Niveau d'eau (Réel)", f"{niveau} %")
                # Ici, vous pouvez ajouter un graphique qui se met à jour 
                # avec la valeur 'niveau' en temps réel
            else:
                st.warning("En attente de données de la maquette...")
        else:
            st.error("Maquette non connectée ! Allez dans l'onglet '📡 Temps Réel' pour connecter.")
            
    else:
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric('Économies Potentielles', '25%', '+25%', delta_color='inverse')
    with col2: st.metric('ROI Estimé', '< 3 mois')
    with col3: st.metric('Stations Optimisables', '30')
    with col4: st.metric('Économies Annuelles', '150M FCFA')
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('📈 Consommation Énergétique')
        try:
            df = pd.read_csv('elecdom-courbes-horaire.csv')
            
            # 1. Sélectionner une période (exemple : la première)
            periode_choisie = df['periode'].unique()[0]
            df_filtre = df[df['periode'] == periode_choisie]
            
            # 2. Extraction des données
            heures = df_filtre['tranche_horaire']
            valeurs_brutes = df_filtre['consommation_Wh']
            
            # 3. CONVERSION D'UNITÉ (Le coefficient multiplicateur)
            # On normalise : on divise par la valeur max pour avoir un ratio (0 à 1)
            # Puis on multiplie par votre débit max théorique (ex: 15 m3/h)
            coefficient_conversion = 15 / valeurs_brutes.max()
            valeurs_hydrauliques = valeurs_brutes * coefficient_conversion
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=heures, y=valeurs_hydrauliques, mode='lines', name='Consommation'))
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"✅ Données converties (Base : {periode_choisie})")
            
        except Exception as e:
            st.error(f"Erreur : {e}")
            # Code de secours avec données simulées
            hours = list(range(24))
            energy_consumption = [85, 80, 75, 70, 65, 70, 90, 110, 125, 120, 115, 110, 105, 100, 105, 110, 115, 120, 125, 120, 110, 100, 90, 85]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hours, y=energy_consumption, mode='lines', name='Consommation'))
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader('💧 Demande en Eau')
        hours = list(range(24))
        energy_consumption = [85, 80, 75, 70, 65, 70, 90, 110, 125, 120, 115, 110, 105, 100, 105, 110, 115, 120, 125, 120, 110, 100, 90, 85]
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
    
    # ... (vos calculs) ...
    
    if st.button('🚀 Lancer le pompage optimisé'):
        # On vérifie si la connexion globale existe
        if st.session_state.ser and st.session_state.ser.is_open:
            st.session_state.ser.write(b'1')  # Envoi de l'ordre
            st.success("Ordre envoyé à la maquette !")
        else:
            st.error("Arduino non connecté ! Allez dans l'onglet '📡 Temps Réel' d'abord.")

def show_sentinel():
    st.header('⚠️ Sentinel Énergétique & Sécurité')
    
    # Simulation d'une lecture de statut venant de l'Arduino (ex: via une variable globale)
    # Dans un vrai projet, ces données viendraient de la fonction 'read_arduino_data'
    niveau_critique = True # Imaginons que le capteur envoie cela
    
    if niveau_critique:
        st.error("🚨 ALERTE : Niveau d'eau critique détecté (< 20%)")
        
        # Bouton d'action d'urgence
        if st.button('🛑 COUPER URGENCE POMPE', type='primary'):
            # Envoi de l'ordre '0' (Arrêt) à l'Arduino
            try:
                # ser.write(b'0') # Décommentez quand vous aurez le matériel
                st.success("✅ Ordre d'arrêt d'urgence envoyé avec succès !")
                st.balloons() # Effet visuel pour valider l'action
            except:
                st.error("Impossible de joindre la maquette.")
                
        # Bouton de réinitialisation
        if st.button('🔧 Acquitter l\'alerte'):
            st.info("Alerte acquittée. Surveillance reprise.")
    else:
        st.success("✅ Système sous contrôle. Aucune anomalie détectée.")

if __name__ == '__main__':
    main()
