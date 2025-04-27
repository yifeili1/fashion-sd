"""
FashionSD - A Streamlit-based frontend for the Fashion Design Service
"""
import streamlit as st
import requests
import json
from datetime import datetime
import os
import time
from pathlib import Path

# Constants
API_BASE_URL = "http://localhost:5000"
STATIC_DIR = os.path.join(os.path.dirname(__file__), "service", "static", "images")

# Page configuration
st.set_page_config(
    page_title="FashionSD",
    page_icon="👗",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 50% !important;
        min-width: 160px !important;
        max-width: 220px !important;
        margin: 0.5rem 0 !important;
        display: block !important;
        text-align: left !important;
        padding-left: 1rem !important;
    }
    .stDownloadButton > button {
        width: 50% !important;
        min-width: 160px !important;
        max-width: 220px !important;
        margin: 0.5rem 0 !important;
        display: block !important;
        text-align: left !important;
        padding-left: 1rem !important;
    }
    .sidebar .sidebar-content {
        width: 200px !important;
    }
    .sidebar .sidebar-title {
        font-size: 32px !important;
        margin-bottom: 1.5rem !important;
        font-weight: bold !important;
    }
    .sidebar .stRadio > div {
        font-size: 22px !important;
        padding: 0.5rem 0 !important;
    }
    .image-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
    }
    .image-card {
        width: 300px;
        margin: 1rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .image-card:hover {
        transform: scale(1.02);
    }
    .metadata {
        font-family: Arial, sans-serif;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_image_path(file_path):
    """Convert API file path to actual file path"""
    if not file_path:
        return None
    path = os.path.join(STATIC_DIR, os.path.basename(file_path))
    return path if os.path.isfile(path) else None

def get_all_designs():
    """Fetch all designs from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/designs")
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        st.error(f"Error fetching designs: {e}")
        return []

def create_design(prompt):
    """Create a new design using the API"""
    if not prompt.strip():
        return None, "Prompt cannot be empty!"
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/designs",
            json={
                "prompt": prompt,
                "negative_prompt": "ugly, blurry, low quality",
                "width": 512,
                "height": 1024  # Updated default height
            }
        )
        if response.status_code == 201:
            return response.json(), None
        return None, f"Error creating design: {response.text}"
    except Exception as e:
        return None, f"Error creating design: {str(e)}"

def get_design(design_id):
    """Fetch a specific design from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/designs/{design_id}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching design: {e}")
        return None

def delete_design(design_id):
    """Delete a design using the API"""
    try:
        response = requests.delete(f"{API_BASE_URL}/designs/{design_id}")
        return response.status_code == 204
    except Exception as e:
        st.error(f"Error deleting design: {e}")
        return False

def format_prompt(prompt):
    """Format prompt into a list of words/phrases"""
    return [p.strip() for p in prompt.split(",")]

def format_timestamp(timestamp):
    """Format timestamp to human-readable format"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return timestamp

def show_gallery():
    """Show the gallery page"""
    st.title("FashionSD Gallery")
    
    designs = get_all_designs()
    if not designs:
        st.info("No designs found. Create your first design!")
        return
    
    # Create a grid of images
    cols = st.columns(3)
    for i, design in enumerate(designs):
        image_path = get_image_path(design['file_path'])
        if image_path:
            with cols[i % 3]:
                # Create a container for the image and button
                with st.container():
                    # Display the image without caption
                    st.image(
                        image_path,
                        use_container_width=True
                    )
                    
                    # Add a view details button
                    if st.button("View Details", key=f"view_{design['id']}"):
                        st.session_state.current_design = design
                        st.session_state.current_page = "show"
                        st.rerun()

def show_create():
    """Show the create page"""
    st.title("Create New Design")
    
    # Get the pre-filled prompt from session state
    initial_prompt = st.session_state.get("create_prompt", "")
    
    with st.form("create_design_form"):
        prompt = st.text_area(
            "Enter your prompt (comma-separated words/phrases)",
            value=initial_prompt,  # Pre-fill the prompt
            placeholder="e.g., modern dress, floral pattern, elegant",
            height=100
        )
        
        submitted = st.form_submit_button("Generate Design")
        
        if submitted:
            if not prompt.strip():
                st.error("Prompt cannot be empty!")
            else:
                with st.spinner("Generating design..."):
                    design, error = create_design(prompt)
                    if error:
                        st.error(error)
                    else:
                        st.session_state.current_design = design
                        st.session_state.current_page = "show"
                        st.success("Design created successfully!")
                        st.rerun()

def show_design():
    """Show the design details page"""
    if "current_design" not in st.session_state:
        st.session_state.current_page = "Gallery"
        return
    
    design = st.session_state.current_design
    image_path = get_image_path(design['file_path'])
    
    if not image_path:
        st.error("Image not found")
        return
    
    st.title("Design Details")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Prompt section
        st.markdown("#### Prompt")
        for word in format_prompt(design["prompt"]):
            st.markdown(f"- {word}")
        
        # Resolution
        st.markdown(f"#### Resolution")
        st.markdown(f"{design['width']} x {design['height']}")
        
        # Creation time
        st.markdown(f"#### Created")
        st.markdown(format_timestamp(design['created_at']))
        
        # Actions section
        st.markdown("### Actions")
        
        # Unified button width and alignment
        with st.container():
            with open(image_path, "rb") as f:
                st.download_button(
                    "Download Image",
                    f,
                    file_name=os.path.basename(image_path),
                    mime="image/png"
                )
            
            if st.button("New Design with Same Prompt"):
                st.session_state.create_prompt = design["prompt"]
                st.session_state.current_page = "Create"
                st.rerun()
            
            if st.button("Delete Design"):
                if st.warning("Are you sure you want to delete this design?"):
                    if delete_design(design["id"]):
                        st.success("Design deleted successfully!")
                        st.session_state.current_design = None
                        st.session_state.current_page = "Gallery"
                        st.rerun()
                    else:
                        st.error("Failed to delete design")
            
            if st.button("Back to Gallery"):
                st.session_state.current_page = "Gallery"
                st.rerun()
    
    with col2:
        st.image(image_path, use_container_width=True)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Gallery"
if "create_prompt" not in st.session_state:
    st.session_state.create_prompt = ""
if "current_design" not in st.session_state:
    st.session_state.current_design = None

# Navigation sidebar with improved styling
st.sidebar.title("FashionSD")
navigation_options = ["Gallery", "Create", "About"]

# Use radio button value directly for navigation, only use session state for 'show' page
if st.session_state.get("current_page", "Gallery") != "show":
    selected_page = st.sidebar.radio(
        "Menu",
        navigation_options,
        index=navigation_options.index(st.session_state.get("current_page", "Gallery")),
        key="navigation_radio"
    )
    if selected_page == "Gallery":
        show_gallery()
    elif selected_page == "Create":
        show_create()
    elif selected_page == "About":
        st.title("About FashionSD")
        st.markdown("""
        FashionSD is a fashion design system built on top of Stable Diffusion.
        
        This application allows you to:
        - Browse existing fashion designs
        - Create new designs using text prompts
        - View and manage your designs
        
        Created with ❤️ using Streamlit
        """)
else:
    show_design() 