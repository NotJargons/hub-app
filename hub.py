import streamlit as st
import pandas as pd
import time
import io
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Excel to SQL Generator", 
    page_icon="🔄", 
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
    }
    .creator-info {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .success-msg {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-msg {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .preview-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .code-preview {
        background-color: #f4f4f4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 400px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🔄 Excel to SQL Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="creator-info">Created by Emmanuel Imafidon</div>', unsafe_allow_html=True)

# File upload
st.subheader("📄 Upload Excel File")
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

# Excel File Preview Section
if uploaded_file:
    st.markdown("---")
    st.subheader("📋 Excel File Preview")
    
    try:
        # Read Excel file with all columns as strings (to preserve leading zeros)
        df = pd.read_excel(uploaded_file, dtype=str)
        
        with st.expander("🔍 View Excel File Structure", expanded=False):
            st.markdown('<div class="preview-section">', unsafe_allow_html=True)
            st.write(f"**File shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            st.write("**Columns:** " + ", ".join(df.columns.tolist()))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
            
            if len(df) > 10:
                st.info(f"Showing first 10 rows of {len(df)} total records")
        
        # Required columns check
        required_cols = ['EMAIL_ADDRESS', 'SURNAME', 'FIRST_NAME', 'BRANCH', 'PHONE', 'COUNTRY', 'EMPLOYEE_ID']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
        else:
            st.success("✅ All required columns found!")
            
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")

# Generate SQL button
if uploaded_file:
    
    if st.button("🚀 Generate SQL Script", type="primary", use_container_width=True):
        
        # Start timing
        start_time = time.time()
        
        with st.spinner('Generating SQL script...'):
            
            try:
                # Read Excel file
                df = pd.read_excel(uploaded_file, dtype=str)
                
                # SQL Template
                template = """INSERT INTO CSSERVICE.UBACS_APPUSERS
   (EMAIL_ADDRESS, SURNAME, FIRST_NAME, MIDDLE_NAME, BRANCH,
    ROLE, CREATION_DATE, PASSWORD, ACTIVE, CHANGE_PWD_ON_LOGON,
    LAST_LOGON_DATE, DELETED, CHECKED, FLOOR, SERVICE_GROUP_ID,
    PHONE, COUNTRY, EMPLOYEE_ID, STATE)
VALUES
   ('{EMAIL_ADDRESS}', '{SURNAME}', '{FIRST_NAME}', 'NA', '{BRANCH}',
    1, sysdate, 'MEFX6Mg1W0', 1, 0,
    sysdate, 0, 0, NULL, -1,
    '{PHONE}', '{COUNTRY}', '{EMPLOYEE_ID}', NULL);"""
                
                # Generate SQL statements
                sql_statements = []
                for _, row in df.iterrows():
                    sql_statements.append(template.format(**row))
                
                # Join all statements
                full_sql = "\n\n".join(sql_statements)
                
                # End timing
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Store results
                st.session_state.sql_content = full_sql
                st.session_state.execution_time = execution_time
                st.session_state.record_count = len(df)
                st.session_state.file_name = uploaded_file.name
                
                # Success message
                st.markdown(f'<div class="success-msg">✅ SQL script generated in {execution_time:.3f} seconds!</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f'<div class="error-msg">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
                st.session_state.sql_content = ""

# Show results if they exist
if 'sql_content' in st.session_state and st.session_state.sql_content:
    
    st.markdown("---")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("📊 Records Processed", st.session_state.record_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("📝 SQL Statements", st.session_state.record_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("⏱️ Processing Time", f"{st.session_state.execution_time:.3f}s")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Preview section
    st.subheader("🔍 SQL Script Preview")
    
    # Show first few statements
    preview_lines = st.session_state.sql_content.split('\n')[:50]  # First 50 lines
    preview_text = '\n'.join(preview_lines)
    
    if len(preview_lines) < len(st.session_state.sql_content.split('\n')):
        preview_text += "\n\n... (truncated for preview)"
    
    st.markdown('<div class="code-preview">', unsafe_allow_html=True)
    st.code(preview_text, language='sql')
    st.markdown('</div>', unsafe_allow_html=True)
    
    if len(st.session_state.sql_content.split('\n')) > 50:
        total_lines = len(st.session_state.sql_content.split('\n'))
        st.info(f"Showing first 50 lines. Complete script has {total_lines} lines.")
    
    # Download section
    st.subheader("📥 Download SQL Script")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download as .sql file
        sql_filename = Path(st.session_state.file_name).stem + ".sql"
        
        st.download_button(
            label="📄 Download SQL File (.sql)",
            data=st.session_state.sql_content,
            file_name=f"{sql_filename}",
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        # Download as .txt file
        txt_filename = Path(st.session_state.file_name).stem + "_sql_script.txt"
        
        st.download_button(
            label="📄 Download as Text File (.txt)",
            data=st.session_state.sql_content,
            file_name=f"{txt_filename}",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.info("📋 Upload an Excel file and click 'Generate SQL Script' to start processing.")

# Required columns info
st.markdown("---")
st.subheader("📋 Required Excel Columns")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Required Columns:**
    - EMAIL_ADDRESS
    - SURNAME  
    - FIRST_NAME
    - BRANCH
    """)

with col2:
    st.markdown("""
    **Additional Required:**
    - PHONE
    - COUNTRY
    - EMPLOYEE_ID
    """)

st.info("💡 **Tip:** Make sure your Excel file contains all required columns with the exact names shown above.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 0.8rem; margin-top: 2rem;">
    Excel to SQL Generator v1.0 | Emmanuel Imafidon © 2024
    </div>
    """, 
    unsafe_allow_html=True
)
