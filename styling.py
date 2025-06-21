# styling.py
import streamlit as st

def apply_custom_css():
    """
    Applies custom CSS to the Streamlit application for a professional look.
    """
    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        /* Import Font Awesome for Icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');


        /* Color Variables for a Brighter, Professional Palette */
        :root {
            --bg-primary: #0D1117; /* Very Dark Grey/Blue (like GitHub dark) */
            --bg-secondary: #161B22; /* Slightly Lighter Dark Grey/Blue (Card/Header) */
            --text-light: #C9D1D9; /* Light Gray Text */
            --text-medium: #8B949E; /* Medium Gray Text */

            --accent-blue-light: #58A6FF; /* Vibrant Blue */
            --accent-blue-dark: #1F6FD8; /* Darker Blue */

            --success-color: #3FB950; /* Green */
            --danger-color: #F85149; /* Red */
            --warning-color: #DD9F1B; /* Orange/Amber */
            --info-color: #79C0FF; /* Lighter Blue */

            --border-color: #30363D; /* Darker Gray for Borders */
            --shadow-light: rgba(0, 0, 0, 0.2);
            --shadow-medium: rgba(0, 0, 0, 0.4);
            --border-radius-lg: 12px;
            --border-radius-md: 8px;
            --border-radius-sm: 4px;
        }

        /* General Body & Typography */
        html, body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: var(--text-light);
            background-color: var(--bg-primary);
        }

        /* Streamlit App Overrides */
        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-light);
        }

        /* Hero Section Styling for a "Bang" Entrance (Optional, if you want a splash screen) */
        /* .hero-section { ... } */

        /* Main Content Container */
        .main .block-container {
            max-width: 1200px;
            padding: 2.5rem 3rem;
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-lg);
            box-shadow: 0 10px 25px var(--shadow-medium);
            margin: 3rem auto;
            border: 1px solid var(--border-color);
        }

        /* Section Headers */
        .stMarkdown h1, .stMarkdown h2 {
            font-size: 2.2rem;
            color: var(--accent-blue-light);
            margin-top: 2.5rem;
            margin-bottom: 1.8rem;
            border-bottom: 2px solid var(--accent-blue-light);
            padding-bottom: 0.8rem;
            font-weight: 700;
            position: relative;
        }
        .stMarkdown h1::after, .stMarkdown h2::after {
            content: '';
            display: block;
            width: 70px;
            height: 5px;
            background: linear-gradient(90deg, var(--accent-blue-light), transparent);
            position: absolute;
            bottom: -2px;
            left: 0;
            border-radius: var(--border-radius-sm);
        }

        .stMarkdown h3 {
            font-size: 1.8rem;
            color: var(--accent-blue-light);
            margin-top: 2rem;
            margin-bottom: 1.2rem;
            border-bottom: 1px dashed var(--border-color);
            padding-bottom: 0.6rem;
            font-weight: 600;
        }
        .stMarkdown h4 {
            font-size: 1.4rem;
            color: var(--accent-blue-dark);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }

        /* Textareas and Input Fields */
        textarea, .stTextInput > div > div > input, .stCodeEditor, .stSelectbox > div > div {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            color: var(--text-light);
            font-size: 1.05rem;
            padding: 12px 18px;
            box-shadow: inset 0 2px 5px var(--shadow-light);
            transition: all 0.3s ease;
        }
        textarea:focus, .stTextInput > div > div > input:focus, .stCodeEditor:focus-within, .stSelectbox > div > div:focus-within {
            border-color: var(--accent-blue-light);
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5), inset 0 2px 5px var(--shadow-light);
            outline: none;
        }
        textarea::placeholder {
            color: var(--text-medium);
            opacity: 0.6;
        }

        /* Buttons */
        .stButton > button {
            padding: 1rem 2rem;
            border: none;
            border-radius: var(--border-radius-md);
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1.8rem;
            box-shadow: 0 8px 15px var(--shadow-medium);
            letter-spacing: 0.03em;
        }
        .stButton > button:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px var(--shadow-medium);
        }
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 4px 8px var(--shadow-light);
        }

        .stButton > button.primary {
            background: linear-gradient(45deg, var(--accent-blue-dark), var(--accent-blue-light));
            color: #ffffff;
            border: 1px solid var(--accent-blue-light);
        }
        .stButton > button.primary:hover {
            background: linear-gradient(45deg, #3182ce, var(--accent-blue-light));
        }

        .stButton > button.secondary {
            background-color: var(--bg-primary);
            color: var(--accent-blue-light);
            border: 2px solid var(--accent-blue-dark);
        }
        .stButton > button.secondary:hover {
            background-color: var(--accent-blue-dark);
            color: #ffffff;
            border-color: var(--accent-blue-dark);
        }
        .stButton > button i {
            margin-right: 0.7rem;
            font-size: 1.2em;
        }

        /* Markdown output styling (for AI explanations) */
        .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
            color: var(--text-light);
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        .stMarkdown ul {
            list-style-type: '👉 ';
            margin-left: 30px;
            padding-left: 10px;
        }
        .stMarkdown ol {
            margin-left: 30px;
            padding-left: 10px;
        }
        .stMarkdown strong {
            color: var(--accent-blue-light);
            font-weight: 700;
        }
        .stMarkdown em {
            color: var(--text-medium);
            font-style: italic;
        }
        .stMarkdown code {
            background-color: #4a5568;
            padding: 0.3em 0.5em;
            border-radius: var(--border-radius-sm);
            font-family: 'Fira Code', 'Cascadia Code', monospace;
            font-size: 0.95em;
            color: #FFD700;
        }
        .stMarkdown pre code {
            background-color: #0d1217;
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1.5em;
            overflow-x: auto;
            margin-bottom: 2rem;
            display: block;
            box-shadow: inset 0 0 10px var(--shadow-light);
            color: #ffffff;
            font-size: 1em;
            line-height: 1.5;
        }

        /* Alerts and Info Boxes */
        .stAlert {
            border-radius: var(--border-radius-md);
            margin-top: 1.5rem;
            padding: 1.2rem 1.8rem;
            font-weight: 600;
            font-size: 1.05rem;
        }
        .stAlert.st-emotion-cache-1fcpknu { /* Success */
            border-left: 8px solid var(--success-color) !important;
            background-color: rgba(76, 175, 80, 0.15) !important;
            color: var(--success-color) !important;
        }
        .stAlert.st-emotion-cache-1wdd6qg { /* Warning */
            border-left: 8px solid var(--warning-color) !important;
            background-color: rgba(251, 191, 36, 0.15) !important;
            color: var(--warning-color) !important;
        }
        .stAlert.st-emotion-cache-1215i5j { /* Error */
            border-left: 8px solid var(--danger-color) !important;
            background-color: rgba(239, 68, 68, 0.15) !important;
            color: var(--danger-color) !important;
        }
        .stInfo { /* Info */
            border-left: 8px solid var(--info-color);
            background-color: rgba(59, 130, 246, 0.15);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            margin-top: 1.5rem;
            color: var(--info-color);
            font-size: 1.1rem;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            background-color: var(--border-color);
            color: var(--text-light);
            font-weight: 600;
            border-radius: var(--border-radius-md);
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease;
            box-shadow: 0 3px 8px var(--shadow-light);
            font-size: 1.1rem;
        }
        .streamlit-expanderHeader:hover {
            background-color: #5b6980;
        }
        .streamlit-expanderContent {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
            padding: 1.8rem;
            box-shadow: inset 0 0 10px var(--shadow-light);
        }

        /* Horizontal rule */
        hr {
            border-top: 1px solid var(--border-color);
            margin: 3.5rem 0;
            opacity: 0.6;
        }

        /* Custom Metric Card (for potential future use, e.g., showing cost KPIs) */
        .custom-metric-card {
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            box-shadow: 0 6px 15px var(--shadow-medium);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 140px;
            border: 1px solid var(--border-color);
            height: 100%;
        }
        .custom-metric-card:hover {
            transform: translateY(-7px);
            box-shadow: 0 10px 25px var(--shadow-medium);
        }

        .custom-metric-value {
            font-size: 3.2em;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.3rem;
            color: var(--accent-blue-light);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }

        .custom-metric-label {
            font-size: 1.1em;
            color: var(--text-medium);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.5rem;
        }
        .custom-metric-label i {
            margin-right: 0.8rem;
            color: var(--accent-blue-dark);
        }

        /* Responsive Design */
        @media (max-width: 1024px) {
            .main .block-container {
                padding: 2rem 2.5rem;
            }
            .stMarkdown h1, .stMarkdown h2 {
                font-size: 1.9rem;
            }
            .stMarkdown h3 {
                font-size: 1.6rem;
            }
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding: 1.5rem;
                margin: 1.5rem auto;
                width: 95%;
            }
            .stButton > button {
                display: block;
                width: 100%;
                margin: 0.8rem 0;
            }
            .stMarkdown h1, .stMarkdown h2 {
                font-size: 1.8rem;
            }
            .stMarkdown h3 {
                font-size: 1.4rem;
            }
            .stMarkdown h4 {
                font-size: 1.1rem;
            }
            textarea, .stTextInput > div > div > input, .stSelectbox > div > div {
                padding: 0.6rem 1rem;
                font-size: 0.95rem;
            }
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.8rem 1rem;
                font-size: 1rem;
            }
            .stMarkdown ul {
                margin-left: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
