"""
Word Recognition Annotation Tool
Multi-user annotation portal for word image labeling with admin dashboard.
"""

import streamlit as st
from utils.storage import AnnotationStorage

# Page configuration
st.set_page_config(
    page_title="Word Recognition Annotation Tool",
    page_icon="📝",
    layout="wide"
)

# Initialize storage
if 'storage' not in st.session_state:
    st.session_state.storage = AnnotationStorage()


def login_page():
    """Display login/registration page."""
    st.title("📝 Word Recognition Annotation Tool")
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    ### Welcome to the Word Recognition Annotation Tool!
    
    This tool helps you annotate word images with their correct labels. 
    
    **Features:**
    - ⚡ Fast annotation with keyboard shortcuts
    - 📊 Progress tracking and statistics
    - 👥 Multi-user support with role-based access
    - 💾 Export annotations in CSV or JSON format
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        # Username input
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="username_input"
        )
        
        # Role selection
        role = st.selectbox(
            "Role",
            options=["annotator", "admin"],
            help="Select 'annotator' to label images, or 'admin' to view all annotations"
        )
        
        # Existing users list
        storage = st.session_state.storage
        users = storage.load_users()
        
        if users:
            st.markdown("#### Quick Login - Existing Users")
            existing_usernames = [u['username'] for u in users]
            
            # Display users as buttons
            cols = st.columns(3)
            for idx, user in enumerate(users):
                with cols[idx % 3]:
                    if st.button(
                        f"👤 {user['username']} ({user['role']})",
                        key=f"user_{user['username']}",
                        use_container_width=True
                    ):
                        st.session_state.current_user = user['username']
                        st.session_state.current_role = user['role']
                        st.rerun()
        
        st.markdown("---")
        
        # Login button
        if st.button("🚀 Login / Register", type="primary", use_container_width=True):
            if username.strip():
                # Register or login user
                is_new = storage.register_user(username.strip(), role)
                st.session_state.current_user = username.strip()
                st.session_state.current_role = role
                
                if is_new:
                    st.success(f"✅ Welcome {username}! Account created successfully.")
                else:
                    st.success(f"✅ Welcome back {username}!")
                
                st.rerun()
            else:
                st.error("⚠️ Please enter a username")


def main():
    """Main application entry point."""
    
    # Check if user is logged in
    if 'current_user' not in st.session_state:
        login_page()
        return
    
    # User is logged in - show appropriate page based on role
    username = st.session_state.current_user
    role = st.session_state.current_role
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.title("📝 Annotation Tool")
        st.markdown(f"**User:** {username}")
        st.markdown(f"**Role:** {role}")
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            del st.session_state.current_user
            del st.session_state.current_role
            st.rerun()
    
    # Route to appropriate page
    if role == "admin":
        # Import and show admin page
        from pages.admin import show_admin_page
        show_admin_page()
    else:
        # Import and show annotation page
        from pages.annotate import show_annotation_page
        show_annotation_page()


if __name__ == "__main__":
    main()
