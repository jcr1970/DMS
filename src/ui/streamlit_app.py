# src/ui/streamlit_app.py

import streamlit as st
import json
import os
import numpy as np
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

# Function to load report data from JSON file
def load_report_data():
    report_file_path = 'src/data/report_data.json'
    if os.path.exists(report_file_path):
        try:
            with open(report_file_path, 'r') as report_file:
                report_data = json.load(report_file)
                return report_data
        except Exception as e:
            st.error(f"Failed to read report data from {report_file_path}: {e}")
            return None
    else:
        st.error(f"Report data file not found: {report_file_path}")
        return None

# Function to plot circular progress
def plot_circular_progress(score):
    fig = go.Figure(go.Pie(
        values=[score, 100-score],
        hole=0.7,
        textinfo='none',
        marker=dict(colors=['#00cc96', '#e6e6e6']),
    ))
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(text=f'{score:.2f}%', x=0.5, y=0.5, font_size=40, showarrow=False)]
    )
    st.plotly_chart(fig)

# Function to plot engagement percentage bar chart
def plot_engagement_percentage(engagement_percentage):
    df = pd.DataFrame(list(engagement_percentage.items()), columns=['Stimuli', 'Percentage'])
    fig = px.bar(df, x='Stimuli', y='Percentage', color='Percentage', 
                 color_continuous_scale='Blues', title='Engagement Percentage by Stimuli',
                 labels={'Percentage':'Engagement Percentage (%)'})
    st.plotly_chart(fig)

# Function to plot total engagement time bar chart
def plot_engagement_time(total_engagement_time):
    df = pd.DataFrame(list(total_engagement_time.items()), columns=['Stimuli', 'Time'])
    fig = px.bar(df, y='Stimuli', x='Time', orientation='h', color='Time', 
                 color_continuous_scale='Greens', title='Total Engagement Time by Stimuli',
                 labels={'Time':'Time (seconds)'})
    st.plotly_chart(fig)

# Function to plot heatmap
def plot_heatmap(gaze_points):
    screen_size = (2560, 1440)
    
    all_points = []
    for region, points in gaze_points.items():
        all_points.extend(points)
    
    all_points = np.array(all_points)
    filtered_intersections = [p for p in all_points if 0 <= p[0] <= screen_size[0] and 0 <= p[1] <= screen_size[1]]
    heatmap, xedges, yedges = np.histogram2d(
        [p[0] for p in filtered_intersections],
        [p[1] for p in filtered_intersections],
        bins=(screen_size[0]//10, screen_size[1]//10)
    )
    
    heatmap = gaussian_filter(heatmap, sigma=8)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    cax = ax.imshow(heatmap.T, extent=[0, screen_size[0], 0, screen_size[1]], origin='lower', cmap='jet')
    fig.colorbar(cax, ax=ax, label='Gaze Intensity')
    ax.set_xlabel('Horizontal Position (pixels)')
    ax.set_ylabel('Vertical Position (pixels)')
    
    # Add labels for regions
    ax.text(1280, 720, 'Road', color='white', fontsize=12, ha='center')
    ax.text(1280, 1300, 'Rearview Mirror', color='white', fontsize=12, ha='center')
    ax.text(1280, 100, 'Dashboard', color='white', fontsize=12, ha='center')
    ax.text(400, 720, 'Left Mirror', color='white', fontsize=12, ha='center')
    ax.text(2160, 720, 'Right Mirror', color='white', fontsize=12, ha='center')
    
    plt.title('Driver Gaze Heatmap')
    st.pyplot(fig)

# Load report data
report_data = load_report_data()

if report_data:
    st.title("Driver Monitoring Report")

    # Display engagement score
    st.header("User Engagement Score")
    plot_circular_progress(report_data['engagement_score'])

    # Display total tracking time
    st.write(f"**Total Tracking Time:** {report_data['total_time']:.2f} seconds")

    # Display most and least engaged stimuli
    st.write(f"**Most Engaged Stimulus:** {report_data['most_engaged_stimulus']} ({report_data['engagement_percentage'][report_data['most_engaged_stimulus']]:.2f}%)")
    st.write(f"**Least Engaged Stimulus:** {report_data['least_engaged_stimulus']} ({report_data['engagement_percentage'][report_data['least_engaged_stimulus']]:.2f}%)")

    # Plot engagement percentage bar chart
    st.header("Engagement Percentage by Stimuli")
    plot_engagement_percentage(report_data['engagement_percentage'])

    # Plot total engagement time bar chart
    st.header("Total Engagement Time by Stimuli")
    plot_engagement_time(report_data['total_engagement_time'])

    # Plot heatmap
    # st.header("Engagement Heatmap")
    # plot_heatmap(report_data['gaze_points'])
