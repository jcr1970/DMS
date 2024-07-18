import streamlit as st
import os
import matplotlib.pyplot as plt

# Function to generate a fake user engagement score
def get_user_engagement_score():
    # Get the absolute path of the score file in the src/ui directory
    score_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'score.txt')
    
    if os.path.exists(score_file_path):
        try:
            with open(score_file_path, 'r') as score_file:
                score = float(score_file.read())
                st.write(f"Score read from file: {score}")
                return score
        except Exception as e:
            st.error(f"Failed to read score from {score_file_path}: {e}")
            return None
    else:
        st.error(f"Score file not found: {score_file_path}")
        return None

# Function to explain how the score is calculated
def explain_engagement_score():
    st.write("""
    ### How the score is calculated
    The user engagement score is calculated based on several criteria related to the driver's gaze:
    
    - **Road Focus**: Time spent focusing on the road is considered positive.
    - **Mirror Check**: Time spent checking mirrors is considered positive if within a threshold.
    - **Dashboard Check**: Time spent checking the dashboard is considered positive if within a threshold.
    - **Off Road Gaze**: Time spent looking away from the road is considered negative.
    - **Prolonged Check**: Prolonged checks are considered negative if exceeding a threshold.
    - **Closed Eyes**: Time spent with eyes closed is always negative.
    
    Each gaze direction is scored, and the overall engagement score is calculated as a percentage.
    """)

# Function to generate pie chart
def generate_pie_chart():
    labels = ['Road', 'Rearview Mirror', 'Left Mirror', 'Right Mirror', 'Dashboard']
    sizes = [70, 10, 7, 7, 6]  # realistic percentages
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    explode = (0.1, 0, 0, 0, 0)  # explode the 1st slice (Road)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

st.title("Driver Monitoring Report")

# Get the engagement score from the file
score = get_user_engagement_score()
if score is not None:
    st.header("User Engagement Score")
    st.write(f"**Score:** {score}")

    # Toggle button for explanation
    if st.button("How the score is calculated"):
        if 'show_explanation' not in st.session_state:
            st.session_state['show_explanation'] = True
        else:
            st.session_state['show_explanation'] = not st.session_state['show_explanation']

    # Show or hide the explanation based on the state
    if 'show_explanation' in st.session_state and st.session_state['show_explanation']:
        explain_engagement_score()
else:
    st.write("Score not available.")

# Display the heatmap
heatmap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heatmap.png')
if os.path.exists(heatmap_path):
    st.image(heatmap_path, caption='Driver Gaze Heatmap', use_column_width=True)
else:
    st.write("Heatmap not available.")

# Display the pie chart
st.header("Gaze Distribution")
generate_pie_chart()
