# features.py
import streamlit as st
import json
import re # For cleaning user input from comments
from ai_logic import ask_gemini_structured # Import the function for structured AI calls

def render_input_section():
    """
    Renders the input section for the Data Pipeline Cost Estimator,
    allowing users to define their pipeline components and select a cloud provider.
    Returns the collected inputs.
    """
    st.markdown("<h2>☁️ Define Your Data Pipeline</h2>", unsafe_allow_html=True)
    st.markdown("Specify the cloud provider, and then add individual components (services, data volumes, frequency) of your data pipeline.")

    # --- Cloud Provider Selection ---
    st.markdown("<h3><i class='fas fa-cloud'></i> Cloud Platform</h3>", unsafe_allow_html=True)
    cloud_provider_options = ["AWS", "GCP", "Azure"]
    cloud_provider = st.radio(
        "Select your target cloud platform:",
        options=cloud_provider_options,
        index=0, # Default to AWS
        key="cloud_provider_radio"
    )
    st.session_state.cloud_provider = cloud_provider # Store in session state

    st.markdown("---")

    # --- Pipeline Components Input (Dynamic) ---
    st.markdown("<h3><i class='fas fa-cogs'></i> Pipeline Components</h3>", unsafe_allow_html=True)
    st.markdown("Add details for each service used in your pipeline. Click 'Add New Component' to add more rows.")
    
    # Initialize pipeline components in session state if not present
    if 'pipeline_components' not in st.session_state:
        st.session_state.pipeline_components = [
            {"service": "AWS Glue", "operation": "DPU-hours", "quantity": 10, "unit": "GB processed", "frequency": "each run", "num_runs_per_month": 3},
            {"service": "AWS Redshift", "operation": "data loaded", "quantity": 500, "unit": "GB", "frequency": "monthly"},
            {"service": "AWS Lambda", "operation": "invocations", "quantity": 10000, "unit": "count", "frequency": "monthly"}
        ]
    
    # Add/Remove component buttons
    add_col, remove_col = st.columns([0.2, 0.8])
    with add_col:
        if st.button("➕ Add New Component", key="add_component_btn", use_container_width=True):
            st.session_state.pipeline_components.append({
                "service": "", "operation": "", "quantity": 0, "unit": "", "frequency": "monthly", "num_runs_per_month": 1
            })
    with remove_col:
        if st.session_state.pipeline_components and st.button("🗑️ Remove Last Component", key="remove_component_btn"):
            st.session_state.pipeline_components.pop()

    st.markdown("<br>", unsafe_allow_html=True) # Spacer

    # Render input fields for each component dynamically
    for i, component in enumerate(st.session_state.pipeline_components):
        with st.expander(f"Component #{i+1} Details", expanded=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                component['service'] = st.text_input(
                    "Service Name (e.g., Glue, BigQuery, Data Factory):",
                    value=component.get("service", ""),
                    key=f"service_{i}"
                )
            with col2:
                component['operation'] = st.text_input(
                    "Operation/Metric (e.g., DPU-hours, data loaded, invocations):",
                    value=component.get("operation", ""),
                    key=f"operation_{i}"
                )
            with col3:
                component['frequency'] = st.selectbox(
                    "Billing Frequency:",
                    options=["monthly", "daily", "each run"],
                    index=["monthly", "daily", "each run"].index(component.get("frequency", "monthly")),
                    key=f"frequency_{i}"
                )
            
            col_qty, col_unit, col_runs = st.columns([1, 1, 1])
            with col_qty:
                component['quantity'] = st.number_input(
                    "Quantity/Volume:",
                    value=float(component.get("quantity", 0)),
                    min_value=0.0,
                    format="%f",
                    key=f"quantity_{i}"
                )
            with col_unit:
                component['unit'] = st.text_input(
                    "Unit (e.g., TB, GB, count):",
                    value=component.get("unit", ""),
                    key=f"unit_{i}"
                )
            with col_runs:
                if component['frequency'] == "each run":
                    component['num_runs_per_month'] = st.number_input(
                        "Number of runs per month:",
                        value=int(component.get("num_runs_per_month", 1)),
                        min_value=1,
                        step=1,
                        key=f"num_runs_{i}"
                    )
                else:
                    # Ensure num_runs_per_month is not used if frequency is not 'each run'
                    if 'num_runs_per_month' in component:
                        del component['num_runs_per_month']
    
    st.session_state.pipeline_components = st.session_state.pipeline_components # Update session state

    return cloud_provider, st.session_state.pipeline_components

def generate_cost_estimate_report(cloud_provider: str, pipeline_components: list):
    """
    Constructs a prompt for the AI and calls it to get a structured cost estimate.
    Updates session state with the AI's response.
    """
    if not pipeline_components:
        st.error("Please add at least one pipeline component to estimate costs.")
        return

    # Filter out empty components
    valid_components = [
        c for c in pipeline_components
        if c.get("service") and c.get("quantity") is not None and c.get("unit")
    ]
    if not valid_components:
        st.warning("No valid pipeline components provided. Please fill out service, quantity, and unit for each component.")
        return


    detailed_pipeline_description = []
    for comp in valid_components:
        desc = f"- {comp['quantity']}{comp['unit']} on {comp['service']} for {comp['operation']}"
        if comp.get('frequency') == 'each run' and comp.get('num_runs_per_month'):
            desc += f" (running {comp['num_runs_per_month']} times per month)"
        elif comp.get('frequency'):
            desc += f" ({comp['frequency']})"
        detailed_pipeline_description.append(desc)

    prompt = f"""
    You are an expert cloud cost estimator. I will provide details of a data pipeline, and you need to estimate its monthly operational cost on {cloud_provider}.
    Provide a breakdown by service and a total monthly cost. If certain costs are negligible or hard to estimate precisely without more context, state them as such.
    Normalize all costs to a monthly basis. Use typical on-demand pricing for {cloud_provider} in a standard region (e.g., us-east-1 for AWS, us-central1 for GCP, East US for Azure), assuming no significant discounts or reserved instances unless specified.

    Here is the data pipeline configuration:
    {chr(10).join(detailed_pipeline_description)}

    Return the cost breakdown and total in a structured JSON format.
    Include a 'notes' field for any assumptions made or considerations.

    JSON Output Schema:
    {{
        "total_monthly_cost": {{ "type": "number", "description": "Total estimated monthly cost in USD." }},
        "breakdown": {{
            "type": "array",
            "items": {{
                "type": "object",
                "properties": {{
                    "component": {{ "type": "string", "description": "Cloud service component (e.g., AWS Glue, Redshift, Lambda)." }},
                    "cost": {{ "type": "number", "description": "Estimated monthly cost for this component in USD." }}
                }},
                "required": ["component", "cost"]
            }}
        }},
        "notes": {{ "type": "string", "description": "Any additional notes or assumptions made by the AI." }}
    }}

    Ensure your response is *only* the JSON object.
    """

    # Define the response schema explicitly for ask_gemini_structured
    response_schema = {
        "type": "object",
        "properties": {
            "total_monthly_cost": {"type": "number"},
            "breakdown": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "component": {"type": "string"},
                        "cost": {"type": "number"}
                    },
                    "required": ["component", "cost"]
                }
            },
            "notes": {"type": "string"}
        },
        "required": ["total_monthly_cost", "breakdown"]
    }

    with st.spinner("Asking Gemini to estimate costs... This may take a moment. ⏳"):
        cost_estimate_response = ask_gemini_structured(prompt, response_schema)

        if cost_estimate_response and not cost_estimate_response.get("error"):
            st.session_state.cost_breakdown = cost_estimate_response # Store in session state
            st.success("Cost estimate generated! �")
            st.toast("Cost estimate ready!")
        else:
            st.error(f"Failed to get cost estimate: {cost_estimate_response.get('error', 'Unknown AI error')}. Please try again.")
            st.session_state.cost_breakdown = None # Clear on error

def render_cost_output():
    """
    Renders the AI-generated cost breakdown.
    """
    st.markdown("<h2>💰 Estimated Monthly Cost</h2>", unsafe_allow_html=True)
    if st.session_state.get('cost_breakdown'):
        cost_data = st.session_state.cost_breakdown

        st.markdown(f"""
        <div style="
            background-color: #2d3748; /* bg-secondary */
            border: 2px solid #63b3ed; /* accent-blue-light */
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        ">
            <p style="font-size: 1.5em; color: #a0aec0; margin-bottom: 0.5em;">Total Estimated Monthly Cost:</p>
            <h1 style="font-size: 4em; color: #3FB950; margin-top: 0;">${cost_data['total_monthly_cost']:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h3>Breakdown by Component:</h3>", unsafe_allow_html=True)
        # Using columns for a nicer display of breakdown
        cols_per_row = 2
        columns = st.columns(cols_per_row)
        for i, item in enumerate(cost_data['breakdown']):
            with columns[i % cols_per_row]:
                st.markdown(f"""
                <div style="
                    background-color: #1a202c; /* bg-primary */
                    border: 1px solid #4a5568; /* border-color */
                    border-radius: 8px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                ">
                    <h4>{item['component']}</h4>
                    <p style="font-size: 1.5em; color: #FBBF24; font-weight: 600;">${item['cost']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        if cost_data.get('notes'):
            st.markdown("---")
            st.markdown("<h3>📝 Notes & Assumptions:</h3>", unsafe_allow_html=True)
            st.info(cost_data['notes'])
    else:
        st.info("No cost estimate generated yet. Define your pipeline above and click 'Estimate Monthly Cost'.")

def render_suggestions_and_comparison():
    """
    Renders the sections for cheaper service alternatives and scenario comparison.
    These features will use AI for suggestions.
    """
    st.markdown("---")
    st.markdown("<h2>💡 Cost Optimization & Comparison</h2>", unsafe_allow_html=True)

    # --- Suggest Cheaper Service Alternatives ---
    st.markdown("<h3><i class='fas fa-lightbulb'></i> Suggest Cheaper Alternatives</h3>", unsafe_allow_html=True)
    st.markdown("Get AI-powered recommendations for alternative services that could reduce your pipeline costs.")
    
    if st.button("✨ Get Alternatives", key="get_alternatives_btn", use_container_width=True):
        if st.session_state.get('cost_breakdown') and st.session_state.get('pipeline_components'):
            current_pipeline_desc = []
            for comp in st.session_state.pipeline_components:
                if comp.get("service"):
                    desc = f"- {comp['quantity']}{comp['unit']} on {comp['service']} for {comp['operation']}"
                    if comp.get('frequency') == 'each run' and comp.get('num_runs_per_month'):
                        desc += f" (running {comp['num_runs_per_month']} times per month)"
                    elif comp.get('frequency'):
                        desc += f" ({comp['frequency']})"
                    current_pipeline_desc.append(desc)

            alternatives_prompt = f"""
            You are a cloud cost optimization expert. Based on the following data pipeline components running on {st.session_state.cloud_provider}, suggest cheaper service alternatives where applicable.
            For each suggestion, briefly explain the alternative, its typical use case, and potential trade-offs (e.g., performance, managed service level).
            Prioritize alternatives within the same cloud provider if possible, but also mention cross-cloud conceptual alternatives if highly beneficial.

            Current Pipeline Components:
            {chr(10).join(current_pipeline_desc)}

            Format your response using Markdown with clear headings and bullet points for each suggested alternative.
            """
            with st.spinner("Asking Gemini for cheaper alternatives... 🤑"):
                alternatives_response = ask_gemini_structured(
                    alternatives_prompt,
                    {
                        "type": "object",
                        "properties": {
                            "suggestions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "original_service": {"type": "string"},
                                        "alternative_service": {"type": "string"},
                                        "explanation": {"type": "string"}
                                    },
                                    "required": ["original_service", "alternative_service", "explanation"]
                                }
                            },
                            "notes": {"type": "string"}
                        },
                        "required": ["suggestions"]
                    }
                )
                if alternatives_response and not alternatives_response.get("error"):
                    st.session_state.alternatives_suggestions = alternatives_response
                    st.success("Alternative suggestions generated! ✅")
                else:
                    st.error(f"Failed to get alternatives: {alternatives_response.get('error', 'Unknown AI error')}")
                    st.session_state.alternatives_suggestions = None
        else:
            st.warning("Please estimate the pipeline cost first to get alternative suggestions.")

    if st.session_state.get('alternatives_suggestions'):
        with st.expander("📖 AI-Suggested Alternatives", expanded=True):
            for suggestion in st.session_state['alternatives_suggestions'].get('suggestions', []):
                st.markdown(f"**From `{suggestion['original_service']}` to `{suggestion['alternative_service']}`**")
                st.write(suggestion['explanation'])
                st.markdown("---")
            if st.session_state['alternatives_suggestions'].get('notes'):
                st.info(st.session_state['alternatives_suggestions']['notes'])
            st.caption("Powered by Gemini. Always verify pricing and suitability for your specific use case.")

    st.markdown("---")

    # --- Allow Scenario Comparison (Option A vs Option B) ---
    st.markdown("<h3><i class='fas fa-balance-scale'></i> Scenario Comparison (Option A vs. Option B)</h3>", unsafe_allow_html=True)
    st.markdown("Compare two different pipeline configurations side-by-side to see which is more cost-effective.")

    # Implement input for Scenario B (Scenario A is the main input already)
    st.info("The first scenario (Option A) uses the pipeline defined in the 'Define Your Data Pipeline' section above.")
    st.markdown("<h4>Define Option B Pipeline Components:</h4>", unsafe_allow_html=True)
    
    if 'pipeline_components_b' not in st.session_state:
        st.session_state.pipeline_components_b = []

    # Add/Remove component buttons for Scenario B
    add_b_col, remove_b_col = st.columns([0.2, 0.8])
    with add_b_col:
        if st.button("➕ Add Component (Option B)", key="add_component_b_btn", use_container_width=True):
            st.session_state.pipeline_components_b.append({
                "service": "", "operation": "", "quantity": 0, "unit": "", "frequency": "monthly", "num_runs_per_month": 1
            })
    with remove_b_col:
        if st.session_state.pipeline_components_b and st.button("🗑️ Remove Last (Option B)", key="remove_component_b_btn"):
            st.session_state.pipeline_components_b.pop()

    for i, component in enumerate(st.session_state.pipeline_components_b):
        with st.expander(f"Option B Component #{i+1} Details", expanded=False): # Start collapsed for Option B
            col1_b, col2_b, col3_b = st.columns([2, 1, 1])
            with col1_b:
                component['service'] = st.text_input(
                    "Service Name (B):",
                    value=component.get("service", ""),
                    key=f"service_b_{i}"
                )
            with col2_b:
                component['operation'] = st.text_input(
                    "Operation/Metric (B):",
                    value=component.get("operation", ""),
                    key=f"operation_b_{i}"
                )
            with col3_b:
                component['frequency'] = st.selectbox(
                    "Billing Frequency (B):",
                    options=["monthly", "daily", "each run"],
                    index=["monthly", "daily", "each run"].index(component.get("frequency", "monthly")),
                    key=f"frequency_b_{i}"
                )
            
            col_qty_b, col_unit_b, col_runs_b = st.columns([1, 1, 1])
            with col_qty_b:
                component['quantity'] = st.number_input(
                    "Quantity/Volume (B):",
                    value=float(component.get("quantity", 0)),
                    min_value=0.0,
                    format="%f",
                    key=f"quantity_b_{i}"
                )
            with col_unit_b:
                component['unit'] = st.text_input(
                    "Unit (B):",
                    value=component.get("unit", ""),
                    key=f"unit_b_{i}"
                )
            with col_runs_b:
                if component['frequency'] == "each run":
                    component['num_runs_per_month'] = st.number_input(
                        "Number of runs per month (B):",
                        value=int(component.get("num_runs_per_month", 1)),
                        min_value=1,
                        step=1,
                        key=f"num_runs_b_{i}"
                    )
                else:
                    if 'num_runs_per_month' in component:
                        del component['num_runs_per_month']
    
    st.session_state.pipeline_components_b = st.session_state.pipeline_components_b # Update session state

    if st.button("⚖️ Compare Scenarios", key="compare_scenarios_btn", type="primary", use_container_width=True):
        if not st.session_state.get('pipeline_components') or not st.session_state.pipeline_components[0].get("service"):
            st.warning("Please define Option A pipeline components first in the 'Define Your Data Pipeline' section.")
            return
        if not st.session_state.get('pipeline_components_b') or not st.session_state.pipeline_components_b[0].get("service"):
            st.warning("Please define Option B pipeline components.")
            return

        # Estimate cost for Option A (using existing logic)
        st.session_state.comparison_cost_a = None
        st.session_state.comparison_cost_b = None

        # Re-using the generate_cost_estimate_report logic, but saving to temporary variables
        # To avoid overwriting main cost_breakdown
        
        # --- Estimate for Option A ---
        st.subheader("Estimating Cost for Option A (Your Current Pipeline)")
        option_a_prompt = _generate_cost_prompt(st.session_state.cloud_provider, st.session_state.pipeline_components)
        option_a_response_schema = {
            "type": "object",
            "properties": {
                "total_monthly_cost": {"type": "number"},
                "breakdown": {"type": "array", "items": {"type": "object", "properties": {"component": {"type": "string"}, "cost": {"type": "number"}}, "required": ["component", "cost"]}},
                "notes": {"type": "string"}
            },
            "required": ["total_monthly_cost", "breakdown"]
        }
        with st.spinner("Estimating Option A cost..."):
            cost_a = ask_gemini_structured(option_a_prompt, option_a_response_schema)
            if cost_a and not cost_a.get("error"):
                st.session_state.comparison_cost_a = cost_a
                st.success("Option A cost estimated.")
            else:
                st.error(f"Failed to estimate Option A cost: {cost_a.get('error', 'Unknown error')}")

        # --- Estimate for Option B ---
        st.subheader("Estimating Cost for Option B")
        option_b_prompt = _generate_cost_prompt(st.session_state.cloud_provider, st.session_state.pipeline_components_b)
        option_b_response_schema = {
            "type": "object",
            "properties": {
                "total_monthly_cost": {"type": "number"},
                "breakdown": {"type": "array", "items": {"type": "object", "properties": {"component": {"type": "string"}, "cost": {"type": "number"}}, "required": ["component", "cost"]}},
                "notes": {"type": "string"}
            },
            "required": ["total_monthly_cost", "breakdown"]
        }
        with st.spinner("Estimating Option B cost..."):
            cost_b = ask_gemini_structured(option_b_prompt, option_b_response_schema)
            if cost_b and not cost_b.get("error"):
                st.session_state.comparison_cost_b = cost_b
                st.success("Option B cost estimated.")
            else:
                st.error(f"Failed to estimate Option B cost: {cost_b.get('error', 'Unknown error')}")

    # Display comparison results
    if st.session_state.get('comparison_cost_a') and st.session_state.get('comparison_cost_b'):
        cost_a_total = st.session_state.comparison_cost_a['total_monthly_cost']
        cost_b_total = st.session_state.comparison_cost_b['total_monthly_cost']

        st.markdown("---")
        st.markdown("<h4>Comparison Results:</h4>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"""
            <div style="
                background-color: #1a202c;
                border: 2px solid {st.session_state.cloud_provider};
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            ">
                <p style="font-size: 1.2em; color: #a0aec0;">Option A Total:</p>
                <h3 style="font-size: 2.5em; color: {'#3FB950' if cost_a_total <= cost_b_total else '#F85149'}; margin-top: 0;">${cost_a_total:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Option A Breakdown"):
                for item in st.session_state.comparison_cost_a['breakdown']:
                    st.write(f"- {item['component']}: `${item['cost']:.2f}`")
                if st.session_state.comparison_cost_a.get('notes'):
                    st.caption(f"Notes: {st.session_state.comparison_cost_a['notes']}")

        with col_b:
            st.markdown(f"""
            <div style="
                background-color: #1a202c;
                border: 2px solid {st.session_state.cloud_provider};
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            ">
                <p style="font-size: 1.2em; color: #a0aec0;">Option B Total:</p>
                <h3 style="font-size: 2.5em; color: {'#3FB950' if cost_b_total <= cost_a_total else '#F85149'}; margin-top: 0;">${cost_b_total:.2f}</h3>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Option B Breakdown"):
                for item in st.session_state.comparison_cost_b['breakdown']:
                    st.write(f"- {item['component']}: `${item['cost']:.2f}`")
                if st.session_state.comparison_cost_b.get('notes'):
                    st.caption(f"Notes: {st.session_state.comparison_cost_b['notes']}")
        
        if cost_a_total < cost_b_total:
            st.success("Option A is estimated to be cheaper! 🎉")
        elif cost_b_total < cost_a_total:
            st.success("Option B is estimated to be cheaper! 🎉")
        else:
            st.info("Both options have similar estimated costs.")

def _generate_cost_prompt(cloud_provider: str, pipeline_components: list) -> str:
    """Helper function to generate the prompt for a given set of pipeline components."""
    valid_components = [
        c for c in pipeline_components
        if c.get("service") and c.get("quantity") is not None and c.get("unit")
    ]
    
    detailed_pipeline_description = []
    for comp in valid_components:
        desc = f"- {comp['quantity']}{comp['unit']} on {comp['service']} for {comp['operation']}"
        if comp.get('frequency') == 'each run' and comp.get('num_runs_per_month'):
            desc += f" (running {comp['num_runs_per_month']} times per month)"
        elif comp.get('frequency'):
            desc += f" ({comp['frequency']})"
        detailed_pipeline_description.append(desc)

    return f"""
    You are an expert cloud cost estimator. I will provide details of a data pipeline, and you need to estimate its monthly operational cost on {cloud_provider}.
    Provide a breakdown by service and a total monthly cost. If certain costs are negligible or hard to estimate precisely without more context, state them as such.
    Normalize all costs to a monthly basis. Use typical on-demand pricing for {cloud_provider} in a standard region (e.g., us-east-1 for AWS, us-central1 for GCP, East US for Azure), assuming no significant discounts or reserved instances unless specified.

    Here is the data pipeline configuration:
    {chr(10).join(detailed_pipeline_description)}

    Return the cost breakdown and total in a structured JSON format.
    Include a 'notes' field for any assumptions made or considerations.

    JSON Output Schema:
    {{
        "total_monthly_cost": {{ "type": "number", "description": "Total estimated monthly cost in USD." }},
        "breakdown": {{
            "type": "array",
            "items": {{
                "type": "object",
                "properties": {{
                    "component": {{ "type": "string", "description": "Cloud service component (e.g., AWS Glue, Redshift, Lambda)." }},
                    "cost": {{ "type": "number", "description": "Estimated monthly cost for this component in USD." }}
                }},
                "required": ["component", "cost"]
            }}
        }},
        "notes": {{ "type": "string", "description": "Any additional notes or assumptions made by the AI." }}
    }}

    Ensure your response is *only* the JSON object.
    """


def render_footer():
    """Renders a consistent footer for the application."""
    st.markdown("---")
    st.caption("☁️ Data Pipeline Cost Estimator | Powered by Streamlit & Google Gemini AI")

def render_clear_button():
    """Renders a button to clear all application state and rerun."""
    st.markdown("---")
    st.markdown("<h3>🧹 Reset Application</h3>", unsafe_allow_html=True)
    if st.button("🔄 Clear All Data & Restart", type="secondary", use_container_width=True, key="clear_all_app_data_button"):
        # Clear all relevant session state variables
        for key in list(st.session_state.keys()):
            # Only clear keys related to this application's state
            if key.startswith(('cloud_provider', 'pipeline_components', 'cost_breakdown', 
                               'alternatives_suggestions', 'comparison_cost', 'pipeline_components_b')):
                del st.session_state[key]
        st.info("Application state cleared. Reloading...")
        st.rerun()