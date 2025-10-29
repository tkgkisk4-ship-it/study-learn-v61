
# Wrapper so platforms that expect app.py can run the Streamlit app.
import os
os.system("streamlit run streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0")
