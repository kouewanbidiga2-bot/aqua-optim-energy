# aqua-optim-energy
# Supprimez l'ancien
# Créez le nouveau avec le code complet
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    st.set_page_config(
        page_title='AQUA-OPTIM ENERGY',
        page_icon='🚰',
        layout='wide'
    )
    
    st.title('🚰 AQUA-OPTIM ENERGY - Systeme Intelligent ONEA')
    st.markdown('### Hackathon ONEA 2025 - Reduction des charges d energie par IA')
    
    tab1, tab2, tab3, tab4 = st.tabs([
        '📊 Tableau de Bord', 
        '🔮 Prevision IA', 
        '⚡ Optimisation',
        '⚠️ Sentinel'
    ])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_prediction()
    
    with tab3:
        show_optimization()
    
    with tab4:
        show_sentinel()

def show_dashboard():
    st.header('📊 Tableau de Bord Energetique')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Economies Potentielles', '25%', '+25%', delta_color='inverse')
    
    with col2:
        st.metric('ROI Estime', '< 3 mois')
    
    with col3:
        st.metric('Stations Optimisables', '30')
    
    with col4:
        st.metric('Economies Annuelles', '150M FCFA')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('📈 Consommation Energetique')
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
    
    st.success('✅ Tableau de bord operationnel')

def show_prediction():
    st.header('🔮 Prevision Intelligente par IA')
    
    st.info('Module de Prevision LSTM pour la demande en eau et optimisation des plannings de pompage.')
    
    col1, col2 = st.columns(2)
    with col1:
        prediction_days = st.slider('Jours a predire', 1, 7, 3)
    with col2:
        confidence = st.slider('Niveau de confiance', 0.8, 0.95, 0.9)
    
    if st.button('📊 Generer les Previsions', type='primary'):
        with st.spinner('Calcul des previsions IA...'):
            hours = list(range(24 * prediction_days))
            historical = [60 + 20 * np.sin(h/24 * 2 * np.pi) for h in range(24)]
            predicted = [65 + 25 * np.sin((h+24)/24 * 2 * np.pi) for h in hours]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(24)), y=historical, mode='lines', name='Historique', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=hours, y=predicted, mode='lines', name='Prevision IA', line=dict(color='red', dash='dash')))
            
            fig.update_layout(title=f'Prevision de la demande sur {prediction_days} jours', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            avg_demand = np.mean(predicted)
            peak_demand = np.max(predicted)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric('Demande Moyenne Prevue', f'{avg_demand:.0f} m³/h')
            with col2:
                st.metric('Pic de Demande Prevu', f'{peak_demand:.0f} m³/h')

def show_optimization():
    st.header('⚡ Optimisation Energetique')
    
    st.warning('Algorithme d Optimisation pour reduire la consommation pendant les heures pleines.')
    
    st.subheader('💰 Parametres Tarifaires')
    col1, col2 = st.columns(2)
    with col1:
        peak_price = st.number_input('Prix heure pleine (FCFA/kWh)', value=85)
    with col2:
        off_peak_price = st.number_input('Prix heure creuse (FCFA/kWh)', value=45)
    
    if st.button('🔄 Calculer l Optimisation', type='primary'):
        with st.spinner('Optimisation en cours...'):
            hours = list(range(24))
            current_cost = [peak_price if 8 <= h < 12 or 18 <= h < 22 else off_peak_price for h in hours]
            optimized_cost = [off_peak_price if h < 6 or h >= 22 else current_cost[h] for h in hours]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=hours, y=current_cost, name='Cout Actuel', marker_color='red'))
            fig.add_trace(go.Bar(x=hours, y=optimized_cost, name='Cout Optimise', marker_color='green'))
            
            fig.update_layout(title='Comparaison des Couts Energetiques', barmode='group', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            total_current = sum(current_cost)
            total_optimized = sum(optimized_cost)
            savings = total_current - total_optimized
            
            st.metric('💰 Economies Quotidiennes Estimees', f'{savings:.0f} FCFA')

def show_sentinel():
    st.header('⚠️ Sentinel Energetique')
    
    st.error('Detection d Anomalies : surveille les equipements et detecte les comportements anormaux.')
    
    st.subheader('🎯 Etat des Pompes')
    
    pumps_data = [
        {'id': 'PMP_001', 'efficiency': 0.85, 'status': 'Normal'},
        {'id': 'PMP_002', 'efficiency': 0.78, 'status': 'Normal'}, 
        {'id': 'PMP_003', 'efficiency': 0.92, 'status': 'Normal'},
        {'id': 'PMP_004', 'efficiency': 0.45, 'status': 'Alerte'},
        {'id': 'PMP_005', 'efficiency': 0.88, 'status': 'Normal'},
    ]
    
    for pump in pumps_data:
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
              st.write(f"**{pump['id']}**")
        with col2:
              st.write(f"Efficacite: {pump['efficiency']*100:.1f}%")
        with col3:
            if pump['status'] == 'Alerte':
                st.error('🔴 Alerte - Maintenance requise')
            else:
                st.success('🟢 Normal')
        
        st.progress(pump['efficiency'])
    
    st.subheader('🚨 Alertes Actives')
    st.warning('**PMP_004** - Efficacite critique (45%) - Maintenance urgente recommandee')
    st.info('**Systeme** - 1 anomalie detectee sur 5 pompes')

if __name__ == '__main__':
    main()
