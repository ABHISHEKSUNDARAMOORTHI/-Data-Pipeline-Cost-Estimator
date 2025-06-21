
# 💸 Data Pipeline Cost Estimator

## 🧠 Overview

The **Data Pipeline Cost Estimator** is a Streamlit-based AI-powered web application that helps data engineers, architects, and analysts estimate the monthly cloud costs of running data pipelines across major cloud providers—**AWS**, **GCP**, and **Azure**.

Whether you're managing a complex ETL architecture or just planning your cloud infrastructure, this tool provides:

- Cost breakdowns of your pipeline components
- Intelligent suggestions for optimizing spending
- Scenario comparisons for informed decision-making

Built with usability, aesthetics, and performance in mind, it features custom CSS and session state management for a seamless user experience.

---

## ✨ Features

### 📥 User Input

- Select a cloud provider (AWS, GCP, or Azure)
- Define pipeline components such as:
  - Storage (S3, BigQuery, Blob)
  - Compute (EMR, Dataflow, Databricks, etc.)
  - Orchestration (Airflow, Step Functions)
  - Data Movement (Kafka, Pub/Sub, Kinesis)

### ⚙️ AI-Powered Estimation

- Uses Google Gemini AI to:
  - Analyze selected components
  - Estimate monthly costs
  - Suggest cheaper or more efficient alternatives
  - Compare alternative architecture costs

### 📊 Cost Breakdown Output

- Human-readable Markdown cost summaries
- Detailed list of components and estimated monthly cost
- Total monthly cost estimate
- Suggestions to reduce cost or switch cloud services
- Optional side-by-side cost comparison (Scenario A vs. B)

### 🎨 Responsive & Polished UI

- Custom dark-themed CSS
- Smooth layout and interactivity
- Scrollable sections, aesthetic buttons, and professional typography

---

## 🚀 Technologies Used

- **Python** 🐍 — core logic and app structure
- **Streamlit** ⚡ — interactive web app
- **Google Generative AI (Gemini)** 🧠 — AI cost estimation
- **pandas** 🐼 — for structured data management
- **streamlit.session_state** — to persist user inputs and results
- **Custom CSS** 🎨 — for branding and UI enhancements

---

## 🛠️ Setup Instructions

### ✅ Prerequisites

- Python 3.8+
- pip package manager
- Google Gemini API Key

---

### 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <your_repo_url>
   cd data-pipeline-cost-estimator
````

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your Google Gemini API Key**:

   * Create a `.env` file in the root directory:

     ```
     GEMINI_API_KEY="your_actual_key_here"
     ```

---

## ▶️ Running the App

From the project root directory:

```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your browser.

---

## 📂 Project Structure

```
.
├── main.py                    # Main app logic and UI orchestration
├── features.py               # Handles input, AI calls, output rendering
├── ai_logic.py               # Communicates with Gemini API
├── styling.py                # Applies custom Streamlit CSS styles
├── requirements.txt          # Python dependencies
├── .env                      # Environment file with GEMINI_API_KEY
```

---

## 📌 Sample Use Case

> You're migrating a pipeline from AWS to GCP and want to compare compute + storage + orchestration costs. Select AWS in panel A, configure the pipeline, and estimate cost. Then switch to GCP in panel B and do the same. View suggestions from AI and compare monthly savings.

---

## 🙌 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -m 'Add feature xyz'`)
4. Push to the branch (`git push origin feature/xyz`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 🌐 Author

Developed by **Abhishek Sundaramoorthi**
