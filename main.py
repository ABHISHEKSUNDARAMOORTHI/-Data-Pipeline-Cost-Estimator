# main.py
import streamlit as st
from styling import apply_custom_css
from features import (
    render_input_section,
    generate_cost_estimate_report,
    render_cost_output,
    render_suggestions_and_comparison,
    render_footer,
    render_clear_button
)

def main():
    """
    Main function to run the Streamlit Data Pipeline Cost Estimator application.
    Orchestrates the UI rendering and calls to features and AI logic.
    """
    # 1. Page Configuration
    st.set_page_config(
        page_title="Data Pipeline Cost Estimator",
        page_icon="💸",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 2. Apply Custom CSS for Branding and Aesthetics
    apply_custom_css()

    # 3. Application Header
    st.markdown("<h1 style='text-align: center;'>💸 Data Pipeline Cost Estimator</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: center; font-size: 1.2em; color: #8B949E;'>
        Estimate the monthly operational costs of your cloud data pipelines across AWS, GCP, and Azure.
        Leverage AI to get a breakdown, compare scenarios, and find optimization opportunities.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Initialize session state variables if not already present
    # This helps persist data across reruns of the app
    if 'cloud_provider' not in st.session_state:
        st.session_state.cloud_provider = "AWS"
    if 'pipeline_components' not in st.session_state:
        st.session_state.pipeline_components = []
    if 'cost_breakdown' not in st.session_state:
        st.session_state.cost_breakdown = None
    if 'alternatives_suggestions' not in st.session_state:
        st.session_state.alternatives_suggestions = None
    if 'pipeline_components_b' not in st.session_state:
        st.session_state.pipeline_components_b = []
    if 'comparison_cost_a' not in st.session_state:
        st.session_state.comparison_cost_a = None
    if 'comparison_cost_b' not in st.session_state:
        st.session_state.comparison_cost_b = None


    # 4. Render Input Section
    cloud_provider, pipeline_components = render_input_section()

    # 5. Cost Estimation Trigger Button
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    if st.button("🚀 Estimate Monthly Cost", type="primary", use_container_width=True, key="estimate_cost_btn"):
        generate_cost_estimate_report(cloud_provider, pipeline_components)
    
    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # 6. Render Cost Output (only if estimate is available)
    render_cost_output()

    # 7. Render Suggestions and Comparison
    render_suggestions_and_comparison()

    # 8. Render Clear Button
    render_clear_button()

    # 9. Render Footer
    render_footer()

if __name__ == "__main__":
    main()
