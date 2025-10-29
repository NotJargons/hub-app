import streamlit as st
import pandas as pd
import time
import io
import os
import re
from datetime import datetime
from pathlib import Path
import numpy as np
from io import BytesIO

# Configure page
st.set_page_config(
    page_title="ITCare Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 1rem auto;
        max-width: 280px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .login-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .tool-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .tool-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .tool-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .tool-description {
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .tool-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .category-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        margin: 1.5rem 0 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .download-button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
    }
    
    .admin-badge {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }
    
    .tool-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .tool-container {
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Authentication function
def check_login(username, password):
    """Check user credentials and return role"""
    admin_user = st.secrets["ADMIN_USER"]
    admin_pass = st.secrets["ADMIN_PASS"]
    user_user = st.secrets["USER_USER"]
    user_pass = st.secrets["USER_PASS"]

    if username == admin_user and password == admin_pass:
        return "admin"
    elif username == user_user and password == user_pass:
        return "user"
    return None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None

# Login page
if not st.session_state.authenticated:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<h1 class="login-title">ITCare Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-top: -0.5rem; font-size: 1.1rem;">Streamlined IT Operations</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("**Login**")
        
        with st.form("login_form"):
            username = st.text_input("Username", label_visibility="visible")
            password = st.text_input("Password", type="password", label_visibility="visible")
            login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button:
            role = check_login(username, password)
            if role:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.session_state.username = username
                st.success(f"Welcome {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Main application (authenticated users only)
    
    # Header with user info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="main-header">
            <h1>⚡ ITCare Hub</h1>
            <p>Automating Workflows</p>
            <small>Created by Emmanuel Imafidon 2025</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.user_role == "admin":
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <p>Welcome, {st.session_state.username}</p>
                <span class="admin-badge">ADMIN</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: center; margin-top: 2rem;">
                <p>Welcome, {st.session_state.username}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()

    # Tool selection page with modern design
    st.markdown('<div class="category-header"><h2>🔧 Users Email Creator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🏢</div>
            <div class="tool-title">AD Bulk Creator</div>
            <div class="tool-description">Creates Active Directory users from HR Excel files.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=ad_bulk" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">👤</div>
            <div class="tool-title">Single User Creator</div>
            <div class="tool-description">Create individual user or vendor accounts with manual entry.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=single_user" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="category-header"><h2>📧 Non-Users Email Creator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📧</div>
            <div class="tool-title">Generic Email Creator</div>
            <div class="tool-description">Creates generic email accounts for specific purposes.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=generic_email" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🔧</div>
            <div class="tool-title">Service Email Creator</div>
            <div class="tool-description">Creates service email accounts for applications.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=service_email" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="category-header"><h2>🗄️ Other Tools</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📝</div>
            <div class="tool-title">GRP Script Generator</div>
            <div class="tool-description">Generates SQL INSERT statements for UBACS application users from Excel data.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=grp_script" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📤</div>
            <div class="tool-title">Exit File Converter</div>
            <div class="tool-description">Converts exit portal files to the required template format.</div>
            <div style="text-align: center; margin-top: 1rem;">
                <a href="?tool=exit_file" style="text-decoration: none;">
                    <button style="background: white; color: #764ba2; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; cursor: pointer;">Open Tool</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Get the selected tool from URL parameters
    query_params = st.experimental_get_query_params()
    selected_tool = query_params.get("tool", [""])[0]
    
    # AD Bulk Creator Functions
    def normalize_hr_file(hr_df: pd.DataFrame) -> pd.DataFrame:
        """Normalize HR file column names — handles variations automatically"""
        column_map = {
            "staff id": ["staff id", "employee id", "employee_id", "employment number", "staff_no", "staff number"],
            "first name": ["first name", "firstname", "emp first name", "given name"],
            "surname": ["surname", "last name", "lastname", "family name"],
            "middle name": ["middle name", "middlename", "other name", "othername"],
            "phone number": ["phone number", "phone", "mobile", "number", "contact", "telephone"],
            "role": ["role","title", "job role", "position", "designation", "job title"],
            "sol id": ["sol id", "work address sol id", "branch code", "sol", "location id"],
            "department": ["department", "dept", "unit", "division"]
        }

        df = hr_df.copy()
        df.columns = [c.strip().lower() for c in df.columns]

        rename_map = {}
        for standard, variants in column_map.items():
            for v in variants:
                match = [c for c in df.columns if c == v]
                if match:
                    rename_map[match[0]] = standard.upper()
                    break

        df = df.rename(columns=rename_map)

        expected_cols = ["STAFF ID", "FIRST NAME", "SURNAME", "MIDDLE NAME",
                         "PHONE NUMBER", "ROLE", "SOL ID", "DEPARTMENT"]

        for col in expected_cols:
            if col not in df.columns:
                df[col] = ""

        return df[expected_cols]

    ABBREVIATIONS = {"ATM", "POS", "HR", "IT", "CEO", "MD", "PSG", "ESRM"}

    def normalize_name(name: str, case="title"):
        if not name or str(name).lower() == "nan": return ""
        name = str(name).strip().replace(" ", "-")
        return name.title() if case=="title" else name.lower()

    def proper_case(text: str):
        if not text or str(text).lower()=="nan": return "N/A"
        return " ".join([w.upper() if w.upper() in ABBREVIATIONS else w.capitalize() for w in str(text).split()])

    def clean_sol(sol_val):
        """Clean SOL ID - remove non-digits and pad to 4 digits"""
        try: 
            sol = str(sol_val).split(".")[0].strip()
            # Remove any non-digit characters
            sol = re.sub(r'\D', '', sol)
            # Pad with leading zeros to make it 4 digits
            return sol.zfill(4) if sol.isdigit() else None
        except: 
            return None

    def format_phone(phone):
        phone = str(phone).split(".")[0].strip().replace(" ","").replace("-","")
        formatted = "N/A"
        
        if phone.startswith("0") and len(phone)==11: 
            formatted = "+234-"+phone[1:4]+"-"+phone[4:7]+"-"+phone[7:]
        elif phone.startswith("234") and len(phone)==13: 
            formatted = "+234-"+phone[3:6]+"-"+phone[6:9]+"-"+phone[9:]
        elif phone.startswith("+234") and len(phone)==14: 
            formatted = "+234-"+phone[4:7]+"-"+phone[7:10]+"-"+phone[10:]
        elif phone.isdigit() and len(phone)>5: 
            formatted = "+234-"+phone
        
        # Add single quote prefix to preserve + in Excel
        return f"{formatted}"

    def build_title_department_mapping(existing_df):
        # Find the correct column names for title and department
        title_col = None
        dept_col = None
        
        # Try to find title column
        for col in existing_df.columns:
            if "title" in col.lower() or "role" in col.lower() or "position" in col.lower():
                title_col = col
                break
        
        # Try to find department column
        for col in existing_df.columns:
            if "department" in col.lower() or "dept" in col.lower() or "unit" in col.lower():
                dept_col = col
                break
        
        if title_col is None or dept_col is None:
            st.warning("Could not find title or department columns in existing users file")
            return {}
        
        # Create a count of departments for each title
        title_dept_counts = {}
        for _, row in existing_df.iterrows():
            title = str(row[title_col]).strip().lower()
            dept = str(row[dept_col]).strip()
            
            if title and title != "nan" and dept and dept != "nan":
                # Use proper case for department
                dept = proper_case(dept)
                
                if title not in title_dept_counts:
                    title_dept_counts[title] = {}
                
                if dept not in title_dept_counts[title]:
                    title_dept_counts[title][dept] = 0
                
                title_dept_counts[title][dept] += 1
        
        # Create the mapping by selecting the most frequent department for each title
        mapping = {}
        for title, dept_counts in title_dept_counts.items():
            # Find the department with the highest count
            most_common_dept = max(dept_counts.items(), key=lambda x: x[1])[0]
            mapping[title] = most_common_dept
        
        return mapping

    def clean_department(dept_val, role_val, title_dept_mapping):
        role = proper_case(role_val)
        
        # First check if we have a valid department in the HR file
        dept = proper_case(dept_val)
        if dept != "N/A":
            return dept
        
        # If no valid department, try to map using the title
        role_lower = str(role_val).strip().lower()
        if role_lower in title_dept_mapping:
            return title_dept_mapping[role_lower]
        
        # Special case handling
        if role_lower == "direct sales executive":
            return "Marketing"
        elif role_lower == "relationship officer":
            return "Marketing"
        
        # If no mapping found, use the role as department
        return role if role != "N/A" else ""

    def choose_upn(fname, mname, lname, existing_sam):
        reasons=[]
        # Prefer FIRST.LAST, fallback to MIDDLE.LAST
        if fname:
            f_upn = f"{fname.lower()}.{lname.lower()}"
            if len(f_upn) > 20: reasons.append("Firstname.lastname exceeds 20 chars")
            elif f_upn in existing_sam: reasons.append("Firstname.lastname already exists")
            else: return f_upn, fname, None
        if mname:
            m_upn = f"{mname.lower()}.{lname.lower()}"
            if len(m_upn) > 20: reasons.append("Middlename.lastname exceeds 20 chars")
            elif m_upn in existing_sam: reasons.append("Middlename.lastname already exists")
            else: return m_upn, mname, None
        return None, None, "; ".join(reasons) if reasons else "No valid UPN"

    # Exit File Converter Functions
    def clean_solid(v):
        """Ensure SolID is always text and starts with 0 if it looks numeric."""
        if pd.isna(v) or v == "":
            return ""
        s = str(v).strip()
        s = re.sub(r"\D", "", s)  # keep only digits
        if s and not s.startswith("0"):
            s = "0" + s
        return s

    # Tool-specific content
    if selected_tool == "ad_bulk":
        st.markdown("---")
        st.markdown('<div class="tool-card"><h2>🏢 AD Bulk Creator</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📁 File Upload")
            
            # File uploaders
            hr_file = st.file_uploader("Upload HR File (Excel)", type=['xlsx'], key="hr_file")
            existing_file = st.file_uploader("Upload Existing Users File (Excel)", type=['xlsx'], key="existing_file")
            sol_file = st.file_uploader("Upload SOL Mapping File (Excel)", type=['xlsx'], key="sol_file")
            
            # Preview uploaded files
            if hr_file:
                st.markdown("#### 👀 HR File Preview")
                hr_df = pd.read_excel(hr_file)
                st.dataframe(hr_df.head(), use_container_width=True)
                
            if existing_file:
                st.success("✅ Existing Users file uploaded")
                    
            if sol_file:
                st.success("✅ SOL Mapping file uploaded")
        
        with col2:
            st.markdown("### ⚡ Execution")
            
            # Password option
            password_option = st.radio(
                "Password Option:",
                ["Use Default Password", "Set Custom Password"],
                index=0
            )
            
            if password_option == "Set Custom Password":
                custom_password = st.text_input("Custom Password", type="password")
                password_feedback = st.empty()
                
                def validate_password(pw):
                    if len(pw) < 10:
                        return False, "❌ Password must be at least 10 characters long."
                    if not pw[0].isupper():
                        return False, "❌ First letter must be capital."
                    if not all(c.islower() or c.isdigit() for c in pw[1:]):
                        return False, "❌ Remaining characters must be lowercase letters or numbers."
                    return True, "✅ Password meets all criteria."
                
                if custom_password:
                    valid, msg = validate_password(custom_password)
                    if valid:
                        password_feedback.success(msg)
                    else:
                        password_feedback.error(msg)
            
            if st.button("🚀 Process Files", type="primary", use_container_width=True):
                if hr_file and existing_file and sol_file:
                    # Validate custom password if selected
                    if password_option == "Set Custom Password" and (not custom_password or not validate_password(custom_password)[0]):
                        st.error("Please provide a valid custom password")
                        st.stop()
                    
                    start_time = time.time()
                    
                    with st.spinner("Processing files..."):
                        try:
                            # Load and process files
                            hr = normalize_hr_file(pd.read_excel(hr_file))
                            
                            # Load existing users
                            xls = pd.ExcelFile(existing_file)
                            existing = None
                            for sheet in xls.sheet_names:
                                try:
                                    df_temp = pd.read_excel(existing_file, sheet_name=sheet, skiprows=6, header=0)
                                    if "SAM Account Name" in df_temp.columns and "Employee ID" in df_temp.columns:
                                        existing = df_temp
                                        break
                                except:
                                    continue
                            
                            if existing is None:
                                st.error("Could not find required sheet in existing users file")
                                st.stop()
                            
                            solmap = pd.read_excel(sol_file)
                            
                            existing_sam = set(existing["SAM Account Name"].str.lower().dropna())
                            existing_staff_ids = set(existing["Employee ID"].dropna().astype(str))
                            
                            # Build SOL dictionary with proper key cleaning
                            sol_dict = {}
                            for _, r in solmap.iterrows():
                                # Clean the SOL ID from the mapping file
                                sol_key = clean_sol(r.get("SOL ID", ""))
                                if sol_key:
                                    # Fixed typo: "physicalDevliveryOfficeName" -> "physicalDeliveryOfficeName"
                                    sol_dict[sol_key] = (
                                        str(r.get("physicalDeliveryOfficeName", "N/A")),
                                        str(r.get("streetAddress", "N/A"))
                                    )
                            
                            # Build title-department mapping from existing users
                            title_dept_mapping = build_title_department_mapping(existing)
                            
                            if title_dept_mapping:
                                st.success(f"✅ Built department mapping for {len(title_dept_mapping)} unique job titles")
                                
                                # Show some sample mappings for verification
                                with st.expander("📋 Sample Title-Department Mappings"):
                                    sample_mappings = list(title_dept_mapping.items())[:10]
                                    for title, dept in sample_mappings:
                                        st.write(f"- **{title}**: {dept}")
                            else:
                                st.warning("⚠️ Could not build department mapping from existing users")
                            
                            # Process HR input
                            output, skipped = [], []
                            
                            # Fixed fields
                            FIXED_FIELDS = {
                                "OUName": "CN=Users,DC=ubagroup,DC=com",
                                "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
                                "msExchOmaAdminWirelessEnable": "0",
                                "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
                                "memberOf": "All Staff Nigeria;UBAMicrosoftCloud;NG_Normal",
                                "pwdLastSet": "0"
                            }
                            
                            # Determine password to use
                            final_password = custom_password if password_option == "Set Custom Password" else "Developer2378"
                            
                            for _, row in hr.iterrows():
                                staff_id = str(row["STAFF ID"]).strip().upper()
                                lname = normalize_name(row["SURNAME"], "title")
                                
                                # Skip if SURNAME missing
                                if not lname:
                                    skipped.append({"Staff ID": staff_id, "Reason": "Missing SURNAME"})
                                    continue
                                
                                fname = normalize_name(row["FIRST NAME"], "title")
                                mname = normalize_name(row.get("MIDDLE NAME",""), "title")
                                fname_lc = normalize_name(row["FIRST NAME"], "lower")
                                mname_lc = normalize_name(row.get("MIDDLE NAME",""), "lower")
                                lname_lc = normalize_name(row["SURNAME"], "lower")
                                
                                # Skip if both FIRST NAME and MIDDLE NAME missing
                                if not fname and not mname:
                                    skipped.append({"Staff ID": staff_id, "Reason": "Missing both FIRST NAME and MIDDLE NAME"})
                                    continue
                                
                                role = proper_case(row["ROLE"])
                                department = clean_department(row.get("DEPARTMENT",""), row["ROLE"], title_dept_mapping)
                                sol_id = clean_sol(row["SOL ID"])
                                phone = format_phone(row["PHONE NUMBER"])  # Excel-friendly format
                                
                                if staff_id in existing_staff_ids:
                                    skipped.append({"Staff ID": staff_id, "Reason":"Duplicate Staff ID"})
                                    continue
                                
                                base_upn, given_name, fail_reason = choose_upn(fname_lc, mname_lc, lname_lc, existing_sam)
                                if not base_upn:
                                    skipped.append({"Staff ID": staff_id, "Reason": fail_reason})
                                    continue
                                
                                # Fixed: Proper SOL lookup
                                if sol_id and sol_id in sol_dict:
                                    office, address = sol_dict[sol_id]
                                else:
                                    office, address = "N/A", "N/A"
                                    if sol_id:
                                        skipped.append({"Staff ID": staff_id, "Reason": f"SOL ID {sol_id} not found in mapping"})
                                
                                display_name = f"{given_name.title()} {lname}".strip()
                                
                                output.append({
                                    "givenName": given_name.title(),
                                    "sn": lname,
                                    "userPrincipalName": base_upn,
                                    "displayName": display_name,
                                    "description": staff_id,
                                    "title": role,
                                    "department": department,
                                    "sAMAccountName": base_upn,
                                    "physicalDeliveryOfficeName": office,
                                    "streetAddress": address,
                                    "telephoneNumber": phone,
                                    "name": display_name,
                                    "mail": f"{base_upn}@ubagroup.com",
                                    "company": "United Bank for Africa Plc",
                                    "co": "Nigeria",
                                    "mobile": phone,
                                    "OUName": FIXED_FIELDS["OUName"],
                                    "homeMDB": FIXED_FIELDS["homeMDB"],
                                    "msExchOmaAdminWirelessEnable": FIXED_FIELDS["msExchOmaAdminWirelessEnable"],
                                    "msExchHomeServerName": FIXED_FIELDS["msExchHomeServerName"],
                                    "mailNickName": base_upn,
                                    "memberOf": FIXED_FIELDS["memberOf"],
                                    "employeeID": staff_id,
                                    "password": final_password,
                                    "displayNamePrintable": display_name,
                                    "pwdLastSet": FIXED_FIELDS["pwdLastSet"]
                                })
                                
                                existing_sam.add(base_upn)  # Prevent duplicates
                            
                            end_time = time.time()
                            execution_time = round(end_time - start_time, 2)
                            
                            # Store results in session state
                            st.session_state['ad_output'] = output
                            st.session_state['ad_skipped'] = skipped
                            st.session_state['ad_hr'] = hr
                            st.session_state['ad_execution_time'] = execution_time
                            st.session_state['ad_title_dept_mapping'] = title_dept_mapping
                            
                            st.success(f"✅ Processing completed in {execution_time}s!")
                            
                        except Exception as e:
                            st.error(f"❌ Error processing files: {str(e)}")
                else:
                    st.warning("Please upload all required files")

        # Display results if available
        if 'ad_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Results")
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("✅ Users Generated", len(st.session_state['ad_output']))
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("⚠️ Users Skipped", len(st.session_state['ad_skipped']))
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("⏱️ Processing Time", f"{st.session_state['ad_execution_time']}s")
                st.markdown('</div>', unsafe_allow_html=True)
            with col4:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                success_rate = round(len(st.session_state['ad_output'])/(len(st.session_state['ad_output'])+len(st.session_state['ad_skipped']))*100, 1) if (len(st.session_state['ad_output'])+len(st.session_state['ad_skipped'])) > 0 else 0
                st.metric("📊 Success Rate", f"{success_rate}%")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Output preview
            if st.session_state['ad_output']:
                st.markdown("#### 👥 Created Users Preview")
                output_df = pd.DataFrame(st.session_state['ad_output'])
                st.dataframe(output_df[['givenName', 'sn', 'userPrincipalName', 'employeeID', 'department', 'physicalDeliveryOfficeName']].head(10), use_container_width=True)
            
            # Skipped users
            if st.session_state['ad_skipped']:
                st.markdown("#### ⚠️ Skipped Users")
                skipped_df = pd.DataFrame(st.session_state['ad_skipped'])
                st.dataframe(skipped_df, use_container_width=True)
            
            # Department mapping info
            if 'ad_title_dept_mapping' in st.session_state and st.session_state['ad_title_dept_mapping']:
                st.markdown("#### 📋 Title-Department Mapping Used")
                mapping_df = pd.DataFrame([
                    {"Title": title, "Department": dept} 
                    for title, dept in st.session_state['ad_title_dept_mapping'].items()
                ])
                st.dataframe(mapping_df.head(10), use_container_width=True)
                
                if len(mapping_df) > 10:
                    st.info(f"Showing first 10 of {len(mapping_df)} mappings. All mappings were used during processing.")
            
            # Download section
            st.markdown("### 📥 Download Files")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.session_state['ad_output']:
                    # CSV download with all fields
                    all_fields = [
                        "givenName", "sn", "userPrincipalName", "displayName", "description", 
                        "title", "department", "sAMAccountName", "physicalDeliveryOfficeName", 
                        "streetAddress", "telephoneNumber", "name", "mail", "company", "co", 
                        "mobile", "OUName", "homeMDB", "msExchOmaAdminWirelessEnable", 
                        "msExchHomeServerName", "mailNickName", "memberOf", "employeeID", 
                        "password", "displayNamePrintable", "pwdLastSet"
                    ]
                    csv_buffer = io.StringIO()
                    pd.DataFrame(st.session_state['ad_output'])[all_fields].to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="📁 Download Users CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"ad_bulk_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if st.session_state['ad_skipped']:
                    # Skipped users CSV download
                    skipped_csv_buffer = io.StringIO()
                    pd.DataFrame(st.session_state['ad_skipped']).to_csv(skipped_csv_buffer, index=False)
                    st.download_button(
                        label="⚠️ Download Skipped CSV",
                        data=skipped_csv_buffer.getvalue(),
                        file_name=f"ad_bulk_skipped_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col3:
                if st.session_state['ad_output'] or st.session_state['ad_skipped']:
                    # HTML report with conditional skipped users section
                    html_content = "<html><body>"
                    
                    # Created users section
                    if len(st.session_state['ad_output']) > 1:
                        html_content += "<p><b>Users have been created as:</b></p>"
                        html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
                        html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>Official Mail</th></tr>"
                        for user in st.session_state['ad_output']:
                            email = f"{user['userPrincipalName']}@ubagroup.com"
                            html_content += f"<tr><td>{user['employeeID']}</td><td><a href='mailto:{email}'>{email}</a></td></tr>"
                        html_content += "</table>"
                        html_content += "<p>Please contact ITCARE on 0201-2807200 Ext.18200 for login details.</p><br>"
                    elif len(st.session_state['ad_output']) == 1:
                        html_content += "<p><b>User has been created as:</b></p>"
                        html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
                        html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>Official Mail</th></tr>"
                        for user in st.session_state['ad_output']:
                            email = f"{user['userPrincipalName']}@ubagroup.com"
                            html_content += f"<tr><td>{user['employeeID']}</td><td><a href='mailto:{email}'>{email}</a></td></tr>"
                        html_content += "</table>"
                        html_content += "<p>Please contact ITCARE on 0201-2807200 Ext.18200 for login details.</p><br>"
                    
                    # Skipped users section - only show if there are skipped users
                    if st.session_state['ad_skipped']:
                        if len(st.session_state['ad_skipped']) > 1:
                            html_content += "<p><b>However, the below users were not created due to errors below:</b></p>"
                            html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
                            html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>First Name</th><th>Last Name</th><th>Middle Name</th><th>Reason</th></tr>"
                            for s in st.session_state['ad_skipped']:
                                staff = st.session_state['ad_hr'][st.session_state['ad_hr']["STAFF ID"].str.upper() == s["Staff ID"]]
                                if not staff.empty:
                                    staff = staff.iloc[0]
                                    html_content += f"<tr><td>{s['Staff ID']}</td><td>{staff.get('FIRST NAME','')}</td><td>{staff.get('SURNAME','')}</td><td>{staff.get('MIDDLE NAME','')}</td><td>{s['Reason']}</td></tr>"
                            html_content += "</table>"
                            html_content += "<p>Please review the above errors and revert.</p>"
                        else:
                            html_content += "<p><b>However, the below user was not created due to error below:</b></p>"
                            html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
                            html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>First Name</th><th>Last Name</th><th>Middle Name</th><th>Reason</th></tr>"
                            for s in st.session_state['ad_skipped']:
                                staff = st.session_state['ad_hr'][st.session_state['ad_hr']["STAFF ID"].str.upper() == s["Staff ID"]]
                                if not staff.empty:
                                    staff = staff.iloc[0]
                                    html_content += f"<tr><td>{s['Staff ID']}</td><td>{staff.get('FIRST NAME','')}</td><td>{staff.get('SURNAME','')}</td><td>{staff.get('MIDDLE NAME','')}</td><td>{s['Reason']}</td></tr>"
                            html_content += "</table>"
                            html_content += "<p>Please review the above error and revert.</p>"
                    
                    html_content += "</body></html>"
                    
                    st.download_button(
                        label="📄 Download HTML Report",
                        data=html_content,
                        file_name=f"ad_bulk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
            
            with col4:
                if 'ad_title_dept_mapping' in st.session_state and st.session_state['ad_title_dept_mapping']:
                    # Title-Department mapping CSV download
                    mapping_csv_buffer = io.StringIO()
                    mapping_df = pd.DataFrame([
                        {"Title": title, "Department": dept} 
                        for title, dept in st.session_state['ad_title_dept_mapping'].items()
                    ])
                    mapping_df.to_csv(mapping_csv_buffer, index=False)
                    st.download_button(
                        label="📋 Download Mapping CSV",
                        data=mapping_csv_buffer.getvalue(),
                        file_name=f"title_department_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            # Additional info about Excel formatting
            if st.session_state['ad_output']:
                st.info("📝 **Note:** Phone numbers in the CSV are prefixed with a single quote (') to preserve the + sign when opening in Excel.")

    elif selected_tool == "single_user":
        st.markdown("---")
        st.markdown('<div class="tool-card"><h2>👤 Single User Creator</h2></div>', unsafe_allow_html=True)
        
        # Account type selection
        account_type = st.radio(
            "Select Account Type:",
            ["User", "Vendor"],
            index=0
        )
        
        # File upload for existing users
        existing_file = st.file_uploader("Upload Existing Users File (Excel)", type=['xlsx'], key="single_user_existing_file")
        
        if existing_file:
            st.success("✅ Existing Users file uploaded")
        
        # SOL ID dropdown
        sol_options = [
            "0999 - NGA_0999 - UBA House, 57 Marina, Lagos Island, Lagos",
            "0462 - NGA_0462 - 53,Lagos Rd. Ikorodu Town, Lagos",
            "0049 - NGA_0049 - Ado-Owo Rd Op Fire Brgde Akure, Ondo",
            "0450 - NGA_0450 - Ajose Adeogun, Lagos",
            "0585 - NGA_0585 - Adeyemi College Of Education, Ondo",
            "0570 - NGA_0570 - Oye Ekiti Business Office, Ekiti",
            "0137 - NGA_0137 - Ikeja G.R.A,Joel Ogunnaike Str., Lagos",
            "0093 - NGA_0093 - 1662 Oyin Jolayemi St VI, Lagos",
            "0269 - NGA_0269 - Agbogbo Oke, Yaba-Ondo, Ondo",
            "0435 - NGA_0435 - 45, Airport Rd. Benin, Edo",
            "0069 - NGA_0069 - 8, Ojo-Igbede Road, Lagos",
            "0627 - NGA_0627 - Agric Isawo Rd. Ikorodu, Lagos",
            "0595 - NGA_0595 - Kofo Ridua Street, Wuse Zone 5, Abuja",
            "0190 - NGA_0190 - Near Motor Park Sardauna LGA, Taraba",
            "0039 - NGA_0039 - NAS Complex 3 Arms Zone, Maitama, Abuja",
            "0155 - NGA_0155 - Km 18 Lekki-Epe Exp. Way Lekki, Lagos",
            "0214 - NGA_0214 - Behind Bokkos LG Sec, Bokkos, Plateau",
            "0063 - NGA_0063 - 37, Abdulkadir Ahmed Way, Bauchi",
            "0465 - NGA_0465 - University Of Nigeria Nsukka, Enugu",
            "0493 - NGA_0493 - Area 8 Garki, Abuja",
            "0024 - NGA_0024 - Plot A 59 CBD Swali Rd Yenagoa, Bayelsa",
            "0630 - NGA_0630 - Plot 12, 341 Road, 3rd Avenue, Gwarinpa Estate, Abuja",
            "0021 - NGA_0021 - Plot 15, Blk 1 Abak Rd Uyo, Akwa-Ibom",
            "0521 - NGA_0521 - Esuene Drive,Ikot-Ekpene, Akwa-Ibom",
            "0360 - NGA_0360 - 12 Grace Bill Rd Eket, Akwa-Ibom",
            "0538 - NGA_0538 - Banking Layout Udo Udoma Avenue, Akwa-Ibom",
            "0033 - NGA_0033 - 25 Trans Amadi Layout PH, Rivers",
            "0242 - NGA_0242 - 5 Factory Road Aba, Abia",
            "0447 - NGA_0447 - 43 Lokoja-Okene Rd Okene, Kogi",
            "0558 - NGA_0558 - 85, Abeokuta Express Way, Dopemu, Lagos",
            "0208 - NGA_0208 - Lagos - Kaduna Road, Mokwa, Niger",
            "0062 - NGA_0062 - 31 Obafemi Awolowo Wy, Osogbo, Osun",
            "0334 - NGA_0334 - 58 Ayegunle Str Agbado, Ekiti",
            "0434 - NGA_0434 - 135, Ikorodu Road, Onipanu, Lagos",
            "0157 - NGA_0157 - Babs Animashaun Str Surulere, Lagos",
            "0022 - NGA_0022 - 10, Osolo Way, Lagos",
            "0404 - NGA_0404 - 145, Murtala Mohammed Rd,Lokoja, Kogi",
            "0138 - NGA_0138 - Gbagada Expressway, Lagos",
            "0432 - NGA_0432 - 89C, Ekenwan Rd. Benin, Edo",
            "0042 - NGA_0042 - 1 Taylor Road, G. Cappa Iddo, Lagos",
            "0460 - NGA_0460 - 73, Oluwole Area, Saki Road, Iseyin, Oyo",
            "0342 - NGA_0342 - UBA Pensions, 3rd Floor, 22B Idowu Taylor Street, V/Island, Lagos",
            "0092 - NGA_0092 - 23 Rd/72 Junction Festac Town, Lagos",
            "0437 - NGA_0437 - Lautech Ogbomosho, Oyo",
            "0160 - NGA_0160 - 97-105 Broad Street, Lagos",
            "0048 - NGA_0048 - Sani Abacha Way, Kiyawa Rd, Jigawa",
            "0640 - NGA_0640 - Kofar Ruwa, Kano",
            "0329 - NGA_0329 - Baga Rd Maiduguri, Borno",
            "0305 - NGA_0305 - Kankia Bye Pass, Dutsin-Ma, Katsina",
            "0045 - NGA_0045 - 146-148, Zaria Road, Funtua, Katsina",
            "0225 - NGA_0225 - Aliyu Jodi Road, Sokoto",
            "0310 - NGA_0310 - 56, Ahmadu Bello Way, Adamawa",
            "0229 - NGA_0229 - Tashar Nana Road, Argungu, Kebbi",
            "0028 - NGA_0028 - 1 Government House Rd S.Abacha Way Gusua, Zamfara",
            "0345 - NGA_0345 - 161-162 Sokoto Rd Opp. Abu Samaru, Kaduna",
            "0362 - NGA_0362 - 31, Ado Bayero Road, Kano",
            "0181 - NGA_0181 - No 1 Kano Road, Sokoto",
            "0547 - NGA_0547 - 7,Ukpenu Road, Ekpoma, Edo",
            "0546 - NGA_0546 - Badagry Business Office, Lagos",
            "0219 - NGA_0219 - Kachia Road, Kaduna",
            "0055 - NGA_0055 - 137 Muritala M. Way, Ilorin, Kwara",
            "0162 - NGA_0162 - 9, Wharf Road, Kariko House, Lagos",
            "0040 - NGA_0040 - Plot 1347 A. Bello Way Garki2, Abuja",
            "0614 - NGA_0614 - Nawa Complex, 106/107 Ahmadu Bello way, Kado Kuchi District, Abuja",
            "0215 - NGA_0215 - 4B, Bank Road, Kano",
            "0415 - NGA_0415 - 473B,Abeokuta Express Rd, Lagos",
            "0088 - NGA_0088 - 1 Julius Nyerere Asokoro, Abuja",
            "0061 - NGA_0061 - 1 Kasim Ibrahim Way Damaturu, Yobe",
            "0540 - NGA_0540 - Ayingba Opp. Kogi State University, Kogi",
            "0537 - NGA_0537 - Abubakar Burga Street Keffi, Nasarawa",
            "0505 - NGA_0505 - 24 Sir Kashim Ibrahim, Maiduguri, Borno",
            "0041 - NGA_0041 - 20 Ijaiye Str Okearin, Lagos",
            "0452 - NGA_0452 - 220 Ikorodu Rd Palmgrove, Lagos",
            "0217 - NGA_0217 - 3, Yakubu Gowon, Kaduna, Nigeria.",
            "0132 - NGA_0132 - National Hospital Garki, Abuja",
            "0634 - NGA_0634 - Kawo, Kaduna State",
            "0401 - NGA_0401 - 3, Wahab Folawiyo Road, Ilorin, Kwara",
            "0035 - NGA_0035 - 165, IBB Way, Katsina",
            "0280 - NGA_0280 - Kano Road, Hadejia, Jigawa",
            "0204 - NGA_0204 - 123 Mur. Mohammed Way Ilorin, Kwara",
            "0266 - NGA_0266 - 89C, Ayegba Omaidoko Way, Idah, Kogi",
            "0393 - NGA_0393 - 550 Ikorodu Rd Mile 12 Ketu, Lagos",
            "0142 - NGA_0142 - 29 Badagry Exp-Way Odunade",
            "0430 - NGA_0430 - University Of Ilorin, Kwara",
            "0148 - NGA_0148 - 1607 Adeola Hopewell Street Vi, Lagos",
            "0372 - NGA_0372 - 3 Ziks Avenue Abakaliki, Ebonyi",
            "0344 - NGA_0344 - Kafanchan Road, Kaduna",
            "0304 - NGA_0304 - K1, Polytechnic Road, Tudun Wada, Kaduna",
            "0419 - NGA_0419 - 60,Marina,Marine View Plaza, Lagos",
            "0026 - NGA_0026 - F11, Kaduna Road, Zaria, Kaduna",
            "0220 - NGA_0220 - F1, Kaduna Road, Zaria, Kaduna",
            "0459 - NGA_0459 - Saki Business Office, Oyo",
            "0103 - NGA_0103 - 18 Adetokunbo Ademola Wuse II, Abuja",
            "0210 - NGA_0210 - 5 Onikolobo Rd Paseke Abeokuta, Ogun",
            "0116 - NGA_0116 - Adankolo Junction Lokoja, Kogi",
            "0602 - NGA_0602 - Aiyedun Road Egosi Ile Kwara, Kwara",
            "0034 - NGA_0034 - 134, Hammaruwa Way, Jalingo, Taraba",
            "0150 - NGA_0150 - 62, Jattu Rd, Auchi, Edo",
            "0303 - NGA_0303 - Biu Road, Gombe",
            "0029 - NGA_0029 - 10, Kano Road, Sokoto",
            "0550 - NGA_0550 - Ceddi Plaza, Abuja",
            "0001 - NGA_0001 - 33B Bishop Aboyade Cole St, VI, Lagos",
            "0506 - NGA_0506 - 165 Maiduguri Rd, Hotoro, Kano",
            "0097 - NGA_0097 - 3A, France Road, Sabon Gari, Kano",
            "0051 - NGA_0051 - Plaza Road, Kantin Kwari, Kano",
            "0589 - NGA_0589 - Kaduna By-Pass, Kaduna",
            "0004 - NGA_0004 - 15S, Bello Road, Kano",
            "0188 - NGA_0188 - 36, Gal. Aminu Way, Jimeta Yola, Adamawa",
            "0350 - NGA_0350 - 28 Makama Dogo Rd, Nasarawa",
            "0199 - NGA_0199 - 4, Akpakpava Road, Benin, Edo",
            "0458 - NGA_0458 - Obafemi Awolowo University,Ile Ife,Osun",
            "0601 - NGA_0601 - Silverbird Galleria, Abuja",
            "0405 - NGA_0405 - Mogadishu Layout, Kaduna",
            "0081 - NGA_0081 - Anaye Street, Odigbo LG. Ore, Ondo State",
            "0235 - NGA_0235 - Bida-Zungeru Road, Wushishi, Niger",
            "0129 - NGA_0129 - 10 Burka Abba Ibrahim Damaturu,Yobe",
            "0426 - NGA_0426 - Mogadishu Cantonment, Asokoro,Abuja",
            "0205 - NGA_0205 - Ibrahim Taiwo Rd N/Bussa, Niger",
            "0351 - NGA_0351 - No.2 Canteen,Gusau, Zamfara",
            "0472 - NGA_0472 - Court of Appeal Complex Shehu Shagari Way, Three Arms Zone, Abuja",
            "0222 - NGA_0222 - 2 Sir Kas Ibrahim Rd Maiduguri, Borno",
            "0333 - NGA_0333 - Dolphin Estate, Lagos",
            "0186 - NGA_0186 - 10, Bank Rd Commercial Area, Bauchi",
            "0133 - NGA_0133 - By Ashaka Cem Plc Gate, Gombe",
            "0020 - NGA_0020 - 8, Baga Rd, Maiduguri, Borno",
            "0526 - NGA_0526 - Ibrahim Taiwo Road, Offa, Kwara",
            "0218 - NGA_0218 - Mei-Deribe Shopping Complex, Rano, Kano",
            "0455 - NGA_0455 - Mutun Biyu, Taraba",
            "0279 - NGA_0279 - 23, IBB Way, Katsina",
            "0470 - NGA_0470 - Abuja Keffi Rd, Abuja",
            "0119 - NGA_0119 - Monday Mkt Maiduguri, Borno",
            "0323 - NGA_0323 - Ijan Essie Road, Essie, Kwara",
            "0311 - NGA_0311 - Oke-Apake Area, Ogbomoso, Oyo",
            "0163 - NGA_0163 - 24 Oba Akran Avenue, Ikeja, Lagos",
            "0057 - NGA_0057 - 67,Tinubu St, Ita-Eko Abeokuta, Ogun",
            "0496 - NGA_0496 - No 43, Monrovia Street, Wuse 2, Abuja",
            "0504 - NGA_0504 - 34 Barde Way Turaki Ward Jalingo, Taraba",
            "0292 - NGA_0292 - Geregu Camp, Ajaokuta, Kogi",
            "0549 - NGA_0549 - 10 Zambezi Crescent WAEC Maitama, Abuja",
            "0002 - NGA_0002 - 55, Marina Lagos Island, Lagos",
            "0289 - NGA_0289 - Sharada Ind. Estate, Phase 1, Kano",
            "0528 - NGA_0528 - Prestige Abuja Bank, Abuja",
            "0136 - NGA_0136 - Ogudu GRA, Lagos",
            "0030 - NGA_0030 - B1 Sultan Abubakar Rd B-Kebbi, Kebbi",
            "0594 - NGA_0594 - Powa Plaza Business Office, Nyanya, Abuja",
            "0117 - NGA_0117 - 35 Apapa Road, Ebute Metta, Lagos",
            "0201 - NGA_0201 - 4, Court Road, Sapele, Delta",
            "0513 - NGA_0513 - 169, Ibrahim Taiwo Road, Ilorin, Kwara",
            "0196 - NGA_0196 - Lapai, Niger",
            "0027 - NGA_0027 - 8, New Mkt Rd Off Biu Rd, Gombe",
            "0610 - NGA_0610 - Idi Iroko Border, Ogun State",
            "0395 - NGA_0395 - Sakponba Road Benin, Edo",
            "0017 - NGA_0017 - 47 Murtala Mohammed Way, Jos, Plateau",
            "0060 - NGA_0060 - 7A IBB Way Okene-Kaba Rd Lokoja, Kogi",
            "0046 - NGA_0046 - 42 Galadima Aminu Way Jimeta, Yola, Adamawa",
            "0151 - NGA_0151 - 7 Mission Rd, Uromi, Edo",
            "0054 - NGA_0054 - Mtd8 Paiko Rd, Minna, Niger",
            "0471 - NGA_0471 - Abuja Owena House, Abuja",
            "0012 - NGA_0012 - 52, Adetokunbo Ademola Wuse II, Abuja",
            "0268 - NGA_0268 - 39 Faskari St Area 3 Garki, Abuja",
            "0624 - NGA_0624 - No 63 Gado Nasko Street Kubwa, Abuja",
            "0388 - NGA_0388 - 14, Ogbomosho Road, Kaduna",
            "0189 - NGA_0189 - 39 Effu-Sapele Rd Efurun, Delta",
            "0259 - NGA_0259 - Market Square Oyan, Osun",
            "0295 - NGA_0295 - 300 Ikorodu Rd, Anthony, Lagos",
            "0583 - NGA_0583 - Lagos-Ibadan Expressway, Ibafo, Lagos",
            "0325 - NGA_0325 - 171, Nnebisi Road, Asaba, Delta",
            "0018 - NGA_0018 - 15 Calabar Road, Calabar, Cross River",
            "0625 - NGA_0625 - Federal Housing Authority Lugbe, Abuja",
            "0609 - NGA_0609 - Federal College of Education Osiele, Abeokuta, Ogun State",
            "0517 - NGA_0517 - Canaanland Ota, Ogun",
            "0284 - NGA_0284 - St Gregory Road Obalende, Lagos",
            "0141 - NGA_0141 - Babcock Uni campus Ilisan Remo, Ogun state",
            "0140 - NGA_0140 - Ojodu Bo, Plot 104 Isheri Rd",
            "0629 - NGA_0629 - Sangotedo, Lekki Peninsula, Lagos",
            "0096 - NGA_0096 - 22 Mobolaji Bank Anthony Ikeja, Lagos",
            "0008 - NGA_0008 - 5, Obafemi Awolowo Way, Ibadan, Oyo",
            "0413 - NGA_0413 - 176, Arakale Road Akure Ondo State",
            "0473 - NGA_0473 - Oluwalogbon House Ikeja, Lagos",
            "0164 - NGA_0164 - 15, Industrial Avenue, Ilupeju, Lagos",
            "0617 - NGA_0617 - 18 Lagos Road, Epe Town, Lagos",
            "0374 - NGA_0374 - 21A Acme Rd Ogba Ikeja, Lagos",
            "0536 - NGA_0536 - University Of Ado-Ekiti, Ekiti",
            "0494 - NGA_0494 - Seme Border",
            "0518 - NGA_0518 - Balewa Road Opposite Inec Office, Ankpa, Kogi",
            "0180 - NGA_0180 - 7 - 13 Aka Rd Uyo, Akwa-Ibom",
            "0015 - NGA_0015 - 1A, Factory Road, Aba, Abia",
            "0203 - NGA_0203 - 65 Warri-Sapele Rd Warri, Delta",
            "0456 - NGA_0456 - Takum Business Office, Taraba",
            "0182 - NGA_0182 - 11-13, Warehouse Road Apapa, Lagos",
            "0086 - NGA_0086 - 15 Aggrey Road Port Harcourt",
            "0176 - NGA_0176 - Beside Akwanga Ultra Modern Market,Lafia Road, Akwanga LGC, Nasarawa, Nigeria",
            "0104 - NGA_0104 - 86B Olu Obasanjo Road, PH, Rivers",
            "0369 - NGA_0369 - Atiku Abubakar Hall, Lagos",
            "0072 - NGA_0072 - 27, Wharf Road Apapa, Lagos",
            "0025 - NGA_0025 - 2, Nnamdi Azikiwe Avenue, Awka, Anambra",
            "0099 - NGA_0099 - 218 Uselu-Lagos Road Ugbowo, Edo",
            "0433 - NGA_0433 - 100, Textile Mill Rd, Benin, Edo",
            "0354 - NGA_0354 - 1 Aguiyi Ironsi St Maitama, Abuja",
            "0631 - NGA_0631 - Opposite Ohaozara LGA Secretariat Uburu, Ebonyi State",
            "0346 - NGA_0346 - UBA House, 35 Broad Street, Lagos Island, Lagos",
            "0110 - NGA_0110 - 13 Allen Avenue, Ikeja, Lagos",
            "0171 - NGA_0171 - 58/60 Broad Street, Lagos",
            "0392 - NGA_0392 - Sam Ethnan NAF Base Ikeja, Lagos",
            "0056 - NGA_0056 - New Secretariat Rd, Ado-Ekiti",
            "0400 - NGA_0400 - Gateway Plaza Zone A, Abuja",
            "0588 - NGA_0588 - Imani Estate-Maitama, Abuja",
            "0533 - NGA_0533 - 51, Ikosi Road, Ketu, Lagos",
            "0608 - NGA_0608 - 61, Lagos Abeokuta Express way Otta Ogun",
            "0170 - NGA_0170 - 172, Awolowo Road, Falomo, Ikoyi, Lagos",
            "0424 - NGA_0424 - 23,Oke Arin Street, Lagos Island, Lagos",
            "0383 - NGA_0383 - Akure-Ilesa Wy, Akure, Ondo",
            "0514 - NGA_0514 - 42A UI/SEC Ro",
            "0347 - NGA_0347 - 68 Western Avenue Rd, Surulere, Lagos",
            "0364 - NGA_0364 - 72 Ajilosun St Ikere Rd Ado/Ek, Ekiti",
            "0543 - NGA_0543 - 25/27A Charity Raod, New Oko-Aba Agege, Lagos",
            "0497 - NGA_0497 - Plot 701 Usuma Maitama, Abuja",
            "0382 - NGA_0382 - Ikoku Road Port Harcourt, Rivers",
            "0553 - NGA_0553 - Ahoada Close Area 11, Abuja",
            "0195 - NGA_0195 - Lebanon St Bank Road Dugbe Ibadan, Oyo",
            "0007 - NGA_0007 - 17 Ereko Street Idumota Lagos",
            "0520 - NGA_0520 - NASS-Senate, Abuja",
            "0468 - NGA_0468 - Okota Business Office, Lagos",
            "0453 - NGA_0453 - Redeemed Camp Bus. Office, Lagos",
            "0542 - NGA_0542 - 50, Ijaiye Road, Ogba, Lagos",
            "0621 - NGA_0621 - Adeti Street, Ilesa, Osun State",
            "0168 - NGA_0168 - University Of Lagos, Akoka, Lagos",
            "0348 - NGA_0348 - Odo Aro Quarters, Oyo",
            "0376 - NGA_0376 - 9 Oremeji St Computer Village Ikeja, Lagos",
            "0605 - NGA_0605 - Akute Business Office, Ogun",
            "0194 - NGA_0194 - 91, Idiroko Rd Otta, Ogun",
            "0349 - NGA_0349 - New-Gbagi Mkt, Gbagi, Ibadan, Oyo",
            "0500 - NGA_0500 - 138 Oba Akran Ikeja, Lagos",
            "0082 - NGA_0082 - Challenge-Molete Road, Ibadan, Oyo",
            "0197 - NGA_0197 - Sw8-1137 Awolowo Rd Molete Ibadan, Oyo",
            "0421 - NGA_0421 - 1,Simbiat Abiola Rd Ikeja, Lagos",
            "0252 - NGA_0252 - C-O 16-17 Beach Road, Jos, Plateau",
            "0375 - NGA_0375 - Ikota Shoping Cmplex VGC Lekki, Lagos",
            "0043 - NGA_0043 - Aspamda Plaza Tradefair 2, Lagos",
            "0178 - NGA_0178 - Opp.Osogbo City Hall, Osogbo, Osun",
            "0562 - NGA_0562 - Nnamdi Azikiwe Airport, Abuja",
            "0011 - NGA_0011 - 73, Allen Avenue, Ikeja, Lagos",
            "0317 - NGA_0317 - Idi-Ape Junction Iwo Rd Ibadan, Oyo",
            "0107 - NGA_0107 - 300, Wharf Road Apapa, Lagos",
            "0074 - NGA_0074 - 2097 Herbert Macaulay Way Wuse4, Abuja",
            "0286 - NGA_0286 - 59, Ibadan Rd, Ijebu-Ode, Ogun",
            "0036 - NGA_0036 - 11B Akin Adesola St, Vi, Lagos",
            "0556 - NGA_0556 - 96 Iju Road, Lagos",
            "0353 - NGA_0353 - 1115 Adeola Odeku St Vi, Lagos",
            "0632 - NGA_0632 - Ogo-Oluwa Area, Gbongan Road, Osogbo",
            "0095 - NGA_0095 - 128 Isolo Rd, Mushin, Lagos",
            "0091 - NGA_0091 - 147 Ladipo St Matori Mushin, Lagos",
            "0499 - NGA_0499 - Apapa-Oshodi Expres. Berger, Lagos",
            "0083 - NGA_0083 - Akowonjo-Egbeda Rd, Lagos",
            "0577 - NGA_0577 - 241 Old Ipaja Road, Near NYSC, Iyana Ipaja, Lagos",
            "0067 - NGA_0067 - 61 Iwo Road Ibadan, Oyo",
            "0461 - NGA_0461 - 20A,Oshodi-Apapa Expressway, Lagos",
            "0165 - NGA_0165 - 10 Causeway Ijora, Lagos",
            "0477 - NGA_0477 - 26 Isheri Rd,Ojodu, Lagos",
            "0297 - NGA_0297 - Lokoja-Kabba Rd, Odo-Ere, Kogi",
            "0080 - NGA_0080 - 20 Bode Thomas St Surulere, Lagos",
            "0633 - NGA_0633 - Lagere Road Ile Ife, Osun",
            "0291 - NGA_0291 - Ilaro Rd Agbara Ind Est. Ogun",
            "0402 - NGA_0402 - Oja Oba, Ilorin, Kwara",
            "0575 - NGA_0575 - 101, Abeokuta Expressway Dopemu, Lagos",
            "0356 - NGA_0356 - Elephant Cem Hse Alausa Ikeja, Lagos",
            "0191 - NGA_0191 - 2 Ahmadu Bello Wy Sardauna LGA, Taraba",
            "0111 - NGA_0111 - 4, Ali Akilu Road, Kaduna",
            "0059 - NGA_0059 - Jos Road, Lafia, Nasarawa",
            "0568 - NGA_0568 - 1B Niger Street, Kano",
            "0145 - NGA_0145 - Nicon Luxury Plot 903, Tafawa Balewa Way, Area 11, Garki Abuja",
            "0320 - NGA_0320 - Mallam Aminu Kano Intl Airport, Kano",
            "0491 - NGA_0491 - 366, H/M Street, St Agnes Sabo, Yaba, Lagos",
            "0272 - NGA_0272 - Yelwa Road, Shendam, Plateau",
            "0224 - NGA_0224 - Gombi Rd, PMB 1501, Biu, Borno",
            "0503 - NGA_0503 - 15B Post Office Rd, Kano",
            "0379 - NGA_0379 - Plot 63 Uni Abuja Teaching Hospital Rd, Gwagwalada,Abuja",
            "0013 - NGA_0013 - 37, New Market Road, Onitsha, Anambra",
            "0227 - NGA_0227 - Along Bauchi-Kano Rd Ningi, Bauchi",
            "0298 - NGA_0298 - Kontagora, Niger",
            "0622 - NGA_0622 - Federal Housing Authority Kuje, Abuja",
            "0159 - NGA_0159 - Alibro Atrium No. 32 Ekikunam Street Utako Abuja",
            "0569 - NGA_0569 - Kabba, Kogi",
            "0010 - NGA_0010 - 6, Okumagba Avenue, Warri, Delta",
            "0009 - NGA_0009 - 1A, Ahmadu Bello Way, Kaduna",
            "0368 - NGA_0368 - New Tyre Market Nkpor",
            "0557 - NGA_0557 - 97 Isoko Road Ughelli, Delta",
            "0121 - NGA_0121 - Ebe-Ano Housing Estate, Enugu",
            "0238 - NGA_0238 - 10, Station Rd, Enugu, Enugu",
            "0241 - NGA_0241 - 34, Douglas Road, Owerri, Imo",
            "0123 - NGA_0123 - State Secretariat Buildng Awka, Anambra",
            "0576 - NGA_0576 - Rumuokwuta Port Harcourt, Rivers",
            "0321 - NGA_0321 - 146-148 Aba-Owerri Rd Aba, Abia",
            "0254 - NGA_0254 - Orlu-Owerri Rd, Umuaka, Imo",
            "0638 - NGA_0638 - Plot 40, Naze International Market, Owerri, Imo State",
            "0075 - NGA_0075 - No 4, Okosisi Lane Nkpor, Anambra",
            "0277 - NGA_0277 - University Of Nigeria, Enugu Campus, Enugu",
            "0408 - NGA_0408 - 3A Bida Road Onitsha, Anambra",
            "0293 - NGA_0293 - 68 Aba Rd, Umuahia, Abia",
            "0618 - NGA_0618 - Addo Roundabout, along Addo � Badore Road, Ajah, Lagos",
            "0234 - NGA_0234 - 14 Azikiwe Road, Port Harcourt, Rivers",
            "0187 - NGA_0187 - 28, Otukpo Rd, Makurdi, Benue",
            "0052 - NGA_0052 - Ogiri Oko Rd Opp CBN Makurdi, Benue",
            "0169 - NGA_0169 - 10 Abebe Village Road, Iganmu, Lagos",
            "0469 - NGA_0469 - Okokomaiko B/O, Lagos",
            "0161 - NGA_0161 - 12-14 Broad Street, Lagos Island, Lagos",
            "0253 - NGA_0253 - Paiko Road, Minna, Niger",
            "0233 - NGA_0233 - 2 Suleiman Barau Rd Suleja, Abuja",
            "0221 - NGA_0221 - Bayero University, Kano",
            "0478 - NGA_0478 - 24 Idowu Taylor Str VI, Lagos",
            "0239 - NGA_0239 - Km42 Abakalki Afikpo Rd Ebonyi",
            "0068 - NGA_0068 - 133,Ejigbo Ikotun Rd,Ejigbo, Lagos",
            "0124 - NGA_0124 - 30A PHC Rd Bridgehead Onitsha, Anambra",
            "0315 - NGA_0315 - 47, Zik Avenue, Awka, Anambra",
            "0596 - NGA_0596 - Station Road PH, Rivers",
            "0301 - NGA_0301 - 53 Marina, Lagos",
            "0545 - NGA_0545 - Ugwuagba Obosi, Anambra",
            "0551 - NGA_0551 - 646 Ikwerre Road Rumuokoro, Rivers",
            "0156 - NGA_0156 - 4, Mbari Street, Owerri, Imo",
            "0539 - NGA_0539 - LASU Campus Ojo Town",
            "0512 - NGA_0512 - 72, Effunrun Sapele Road, Warri, Delta",
            "0023 - NGA_0023 - 6, Oraifite-Ogbufor Rd, Nnewi, Anambra",
            "0326 - NGA_0326 - 143, Agbani Rd, Enugu, Enugu",
            "0084 - NGA_0084 - 21 Faulks Road Aba, Abia",
            "0381 - NGA_0381 - 312 PH-Aba Way, Rumukwurushi, Rivers",
            "0422 - NGA_0422 - 20, Palm Avenue Mushin, Lagos",
            "0352 - NGA_0352 - Ibekwe Road, Ikot Abasi, Akwa-Ibom",
            "0313 - NGA_0313 - Ikirun-Ila Orangun Road. Iree, Osun",
            "0090 - NGA_0090 - Road 1 LUTH Premises Idi Araba, Lagos",
            "0639 - NGA_0639 - Plot 4, Elevate Commercial Park, Near Lagos Free Zone, Ibeju- Lekki, Lagos",
            "0398 - NGA_0398 - 11 Adetokunbo Ademola Street Victoria Island, Lagos",
            "0623 - NGA_0623 - Odogunyan Ikorodu",
            "0149 - NGA_0149 - 80A Admiralty Way Lekki Phase1, Lagos",
            "0641 - NGA_0641 - Ojoo, Ibadan Business Office, Oyo",
            "0467 - NGA_0467 - Murtala Muhommed Airport, Lagos",
            "0211 - NGA_0211 - Alagbaka Quarters, Akure, Ondo",
            "0616 - NGA_0616 - 131T AM Dung Street, Dadin Kowa, Jos, Plateau State",
            "0153 - NGA_0153 - UBA Pensions, 3rd Floor, 22B Idowu Taylor Street, V/Island, Lagos",
            "0212 - NGA_0212 - 77D Ipogun Road, Ilaramokin, Ondo",
            "0580 - NGA_0580 - Osun State College Of Education Ilesha",
            "0127 - NGA_0127 - 261, Nnebisi Road, Asaba, Delta",
            "0322 - NGA_0322 - Broad Street, Okitipupa, Ondo State",
            "0073 - NGA_0073 - 37 Oba Akran Avenue, Ikeja, Lagos",
            "0154 - NGA_0154 - Chevron Drive, Lekki Peninsula, Lagos",
            "0584 - NGA_0584 - 51A Adeniyi Jones, Ikeja, Lagos",
            "0414 - NGA_0414 - 81/83 Iwo Road Ibadan, Oyo",
            "0167 - NGA_0167 - 43, Idumagbo Avenue, Lagos",
            "0076 - NGA_0076 - Opp NNPC Depot Apata Ibadan",
            "0032 - NGA_0032 - 21 Fatai Atere Road, Mushin, Lagos",
            "0440 - NGA_0440 - 14 Js Tarka Rd Gboko, Benue",
            "0240 - NGA_0240 - 40 New Mkt Rd Onitsha, Anambra",
            "0420 - NGA_0420 - 21/23 Docemo Street Lagos Island, Lagos",
            "0147 - NGA_0147 - Col Of Medicine UCH Ibadan, Oyo",
            "0166 - NGA_0166 - 86 Murtala Muh Way Ebute-Metta, Lagos",
            "0492 - NGA_0492 - Joseph Street Igbosere, Lagos",
            "0615 - NGA_0615 - Ire-Akari Iyana Isolo, 142/146 Oshodi/Apapa Expressway Lagos",
            "0423 - NGA_0423 - 81,Ojuelegba Rd Surulere, Lagos",
            "0290 - NGA_0290 - 38, Murtala Mohammed Way, Kano",
            "0515 - NGA_0515 - 21 Obun Eko Str. Idumota, Lagos",
            "0071 - NGA_0071 - NNS Quorra Navy Compound Apapa, Lagos",
            "0535 - NGA_0535 - Shell Industrial Area, Rumuomasi, Rivers",
            "0139 - NGA_0139 - 191 Akarigbo Str. Sabo Sagamu, Ogun",
            "0113 - NGA_0113 - 33 Issa William Str Okearin, Lagos",
            "0574 - NGA_0574 - Fed Poly, Ilaro, Ogun",
            "0109 - NGA_0109 - 28 Obun Eko Str Idumota, Lagos",
            "0158 - NGA_0158 - 74 Ikotun-Idimu Rd Ikotun, Lagos",
            "0126 - NGA_0126 - Rwangpam Street, Jos, Plateau",
            "0620 - NGA_0620 - Adekunle Ajasin Univ, Campus, Akungba Akoko Ondo State",
            "0098 - NGA_0098 - 11, Agbor Road, Benin, Edo",
            "0524 - NGA_0524 - Woji Road, GRA, Port Harcourt, Rivers",
            "0628 - NGA_0628 - Ebute Ipakodo Ikorodu, Lagos",
            "0367 - NGA_0367 - 144 Nnamdi Azikiwe Str Idumota, Lagos",
            "0058 - NGA_0058 - 21, Road Festac Area, Lagos",
            "0044 - NGA_0044 - PPMC Area Complex Warri, Delta",
            "0309 - NGA_0309 - Jarmai, Kanam LGC, Plateau",
            "0172 - NGA_0172 - 56 Kudirat Abiola Way Oregun Ikeja, Lagos",
            "0531 - NGA_0531 - 52, Upper Sakponba Road Benin, Edo",
            "0619 - NGA_0619 - Awaye coker , Orile, Lagos",
            "0636 - NGA_0636 - Law School Road Bwari, Abuja",
            "0037 - NGA_0037 - Ogunlana Drive, Lagos",
            "0572 - NGA_0572 - 16 Burma Road Apapa, Lagos",
            "0363 - NGA_0363 - 3 Agudosi Str Alaba Intl Mkt, Lagos",
            "0487 - NGA_0487 - 73,Ikwere Road, PH, Rivers",
            "0064 - NGA_0064 - Apapa Oshodi Way Coconut B/Stop, Lagos",
            "0444 - NGA_0444 - 55, Okpe Rd. Sapele, Delta",
            "0457 - NGA_0457 - Wukari Business Office, Taraba",
            "0173 - NGA_0173 - Abbi, Delta",
            "0050 - NGA_0050 - Km 16 Kachia Road, NNPC Depot, Kaduna",
            "0019 - NGA_0019 - 53, Okpara Avenue, Enugu",
            "0265 - NGA_0265 - Uniport Shopping Complex PH, Rivers",
            "0626 - NGA_0626 - Beside Akwanga Ultra Modern Market,Lafia Road, Nasarawa",
            "0358 - NGA_0358 - Finima Road Bonny, Rivers",
            "0255 - NGA_0255 - Oron- Mbo Road, Ebughu, Akwa-Ibom",
            "0271 - NGA_0271 - 302 Uselu-Lagos Rd Ugbow Benin, Edo",
            "0336 - NGA_0336 - Ohuhu Owo Oju LGA, Benue",
            "0571 - NGA_0571 - Elelenwo Business Office GRA Port-Harcourt, Rivers",
            "0328 - NGA_0328 - Issele-Uku,Old Lagos-Asaba Rd, Delta",
            "0507 - NGA_0507 - 186 Mbiama Rd, Onupa Yenagoa, Bayelsa",
            "0066 - NGA_0066 - 59 Old Rd Boji-Boji Owa Agbor, Delta",
            "0522 - NGA_0522 - Oghara, Ajagbodudu Road Ogare Efe, Delta",
            "0016 - NGA_0016 - 238, Nnebisi Road, Asaba, Delta",
            "0262 - NGA_0262 - Owerri-Orlu Rd Nwaorieubi, Imo",
            "0365 - NGA_0365 - Abraka Ere House Yenezue-Gene, Bayelsa",
            "0411 - NGA_0411 - 14, Azikwe Road, Port-Harcourt, Rivers",
            "0053 - NGA_0053 - 1, Factory Rd, Umuahia, Abia",
            "0006 - NGA_0006 - 46, Warehouse Road Apapa, Lagos",
            "0552 - NGA_0552 - Ministry Of Justice, Abuja",
            "0102 - NGA_0102 - 19, Adeyemo Alakija Street, VI, Lagos",
            "0089 - NGA_0089 - 123 Ojuelega Rd, Surulere, Lagos",
            "0135 - NGA_0135 - 38 Ajayi Aina St Ifako Gbagada, Lagos",
            "0484 - NGA_0484 - 3 Ogoja Road, Abakaliki, Ebonyi",
            "0047 - NGA_0047 - 4B Ogoja Rd, Abakaliki, Ebonyi",
            "0179 - NGA_0179 - 18 Okim Osabor St Ikom, Cross River",
            "0243 - NGA_0243 - 9th Mile Corner",
            "0564 - NGA_0564 - Market Road Junction North Bridge Makurdi, Benue",
            "0385 - NGA_0385 - 25, Hammaruwa Way, Jalingo, Taraba",
            "0273 - NGA_0273 - Katsina Ala Rd Zaki Biam",
            "0248 - NGA_0248 - 14 Calabar Road, Calabar, Cross River",
            "0120 - NGA_0120 - 34 Nwaniba Road Uyo, A.K.S",
            "0559 - NGA_0559 - Petroleum Training Institute, Effurun, Delta",
            "0236 - NGA_0236 - 4 Hospital Road Port Harcourt, Rivers",
            "0578 - NGA_0578 - Rivers State Secretariat, Rivers",
            "0412 - NGA_0412 - 144 Mbiama Yenagoa, Bayelsa",
            "0390 - NGA_0390 - NAOC Premise Rumueme Mile4 PH, Rivers",
            "0125 - NGA_0125 - 12 Calabar Road, Calabar, Cross River",
            "0230 - NGA_0230 - Kutigi, Niger",
            "0274 - NGA_0274 - Igumale Ado LGA, Benue",
            "0308 - NGA_0308 - Mayo-Selbe Rd, Taraba",
            "0003 - NGA_0003 - Plot 137 Olu Obasanjo Rd PH, Rivers",
            "0361 - NGA_0361 - 3A Cemetry Rd Eziukwu Mkt Aba, Abia",
            "0544 - NGA_0544 - Refinery Road, Eleme, Rivers",
            "0384 - NGA_0384 - 3 Assumpta Avenue, Owerri, Imo",
            "0193 - NGA_0193 - Ogbete Main Market, Enugu",
            "0581 - NGA_0581 - Electronics Market Onitsha, Anambra",
            "0466 - NGA_0466 - 2nd Avenue, Navy Town, Ojo, Lagos",
            "0436 - NGA_0436 - Obajana, Kogi",
            "0407 - NGA_0407 - 49 Uga Street Bridge Head Onitsha, Anambra",
            "0464 - NGA_0464 - 399 Agbani Road Gariki, Enugu",
            "0523 - NGA_0523 - Nnamdi Azikiwe University Awka, Anambra",
            "0399 - NGA_0399 - 49 Nike Lake Resort Rd, Enugu",
            "0409 - NGA_0409 - 31 Asa Road Aba, Abia",
            "0606 - NGA_0606 - 44A Govt Station Road Orlu, Imo",
            "0130 - NGA_0130 - 20 Okpara Avenue, Enugu",
            "0031 - NGA_0031 - 60, Wetheral Rd, Owerri, Imo",
            "0587 - NGA_0587 - Aminu Kano, Abuja",
            "0600 - NGA_0600 - NNPC, Abuja",
            "0105 - NGA_0105 - 9, Okigwe Road, Aba, Abia",
            "0391 - NGA_0391 - Mobil House, Lagos",
            "0371 - NGA_0371 -  Iponri, Lagos",
            "0519 - NGA_0519 - Relief-Market 267 Obodo-Ukwu Rd, Anambra",
            "0377 - NGA_0377 - Enugu-Onitsha Exp Ogidi, Anambra",
            "0486 - NGA_0486 - 20, Trans Amadi, PH, Rivers",
            "0213 - NGA_0213 - Zonkwa, Kaduna",
            "0267 - NGA_0267 - 22 Edo-Ezemewi Rd Nnewi2, Anambra",
            "0114 - NGA_0114 - 8B New Mkt Rd, Onitsha, Anambra",
            "0534 - NGA_0534 - Independence Layout, Enugu",
            "0014 - NGA_0014 - 81, Akpakpava Road, Benin, Edo",
            "0100 - NGA_0100 - 100, Sapele Road, Benin, Edo",
            "0237 - NGA_0237 - 94 Trans Amadi Ind. Layout PH, Rivers",
            "0246 - NGA_0246 - PHC- Owerri Rd, Isiokpo Ikwerre LGA, Rivers",
            "0339 - NGA_0339 - Eke-Ahiara Mbaise",
            "0607 - NGA_0607 - Federal University Otuoke, Bayelsa",
            "0079 - NGA_0079 - 134 Upper Mission Rd Benin, Edo",
            "0065 - NGA_0065 - 36, Kenyetta Str, Uwani, Enugu",
            "0038 - NGA_0038 - 16 PHC Rd, Bridgehead, Onitsha, Anambra",
            "0327 - NGA_0327 - Ukpor, Nnewi South LGA, Anambra",
            "0281 - NGA_0281 - 4 Wharf Road, Lokoja, Kogi",
            "0441 - NGA_0441 - 1,Commercial Rd Opp Texaco, Makurdi, Benue",
            "0509 - NGA_0509 - 147 Trans-Amadi PH, Rivers",
            "0510 - NGA_0510 - Motorcycle Spare Part, Nnewi, Anambra",
            "0294 - NGA_0294 - 56 Ph Rd Bridgehead Onitsha, Anambra",
            "0257 - NGA_0257 - Near Akukutoru LGA, Abonnema, Rivers",
            "0635 - NGA_0635 -  Okpanam Road, Asaba, Delta",
            "0299 - NGA_0299 - 354 New Ogorode Industrial Estate, Sapele, Delta",
            "0443 - NGA_0443 - Rivers State University PH, Rivers",
            "0278 - NGA_0278 - 73 Ahoada Rd, Omoku, Rivers",
            "0378 - NGA_0378 - 96B Iweka Rd Onitsha, Anambra",
            "0599 - NGA_0599 - Pankshin, Plateau",
            "0525 - NGA_0525 - Old Agbor Rd,Ekrejeta Abraka, Delta",
            "0312 - NGA_0312 - 146-148 Aba-Owerri Rd Aba Abia",
            "0613 - NGA_0613 - Akwa Ibom - ExxonMobil QIT, Ibeno",
            "0144 - NGA_0144 - 66 Lawanson Rd Itire, Surulere, Lagos",
            "0637 - NGA_0637 - PH Road New Owerri, Owerri West LGA, Imo State",
            "0258 - NGA_0258 - Ekwulobia Rd, Agulu, Anambra",
            "0005 - NGA_0005 - 810-811 Bank Road Daleko, Mushin, Lagos"
        ]
        
        sol_choice = st.selectbox("Select SOL ID", sol_options)
        
        # Extract SOL ID and office name from selection
        sol_id = sol_choice.split(" - ")[0]
        office_name = sol_choice.split(" - ")[1]
        
        # Input fields
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name").strip()
            middle_name = st.text_input("Middle Name (Optional)").strip()
            last_name = st.text_input("Last Name").strip()
            phone_number = st.text_input("Phone Number").strip()
        
        with col2:
            staff_id = st.text_input("Staff ID").strip()
            job_role = st.text_input("Job Role").strip()
            
            # Password option
            password_option = st.radio(
                "Password Option:",
                ["Use Default Password", "Set Custom Password"],
                index=0
            )
            
            if password_option == "Set Custom Password":
                custom_password = st.text_input("Custom Password", type="password")
                password_feedback = st.empty()
                
                def validate_password(pw):
                    if len(pw) < 10:
                        return False, "❌ Password must be at least 10 characters long."
                    if not pw[0].isupper():
                        return False, "❌ First letter must be capital."
                    if not all(c.islower() or c.isdigit() for c in pw[1:]):
                        return False, "❌ Remaining characters must be lowercase letters or numbers."
                    return True, "✅ Password meets all criteria."
                
                if custom_password:
                    valid, msg = validate_password(custom_password)
                    if valid:
                        password_feedback.success(msg)
                    else:
                        password_feedback.error(msg)
            else:
                custom_password = "Developer2378"  # Default password
        
        # Additional field for Vendor type
        responsible_party = ""
        if account_type == "Vendor":
            responsible_party = st.text_input("Responsible Party (e.g., emmanuel.imafidon@ubagroup.com)").strip()
        
        # Process button
        if st.button("🚀 Create User", type="primary", use_container_width=True):
            # Validate inputs
            required_fields = [first_name, last_name, phone_number, staff_id, job_role, sol_choice]
            if account_type == "Vendor":
                required_fields.append(responsible_party)
            
            if not all(required_fields):
                st.error("Please fill all required fields.")
            elif password_option == "Set Custom Password" and (not custom_password or not validate_password(custom_password)[0]):
                st.error("Please provide a valid custom password.")
            elif not existing_file:
                st.error("Please upload the existing users file.")
            else:
                start_time = time.time()
                
                with st.spinner("Creating user..."):
                    try:
                        # Load existing users
                        xls = pd.ExcelFile(existing_file)
                        existing = None
                        for sheet in xls.sheet_names:
                            try:
                                df_temp = pd.read_excel(existing_file, sheet_name=sheet, skiprows=6, header=0)
                                if "SAM Account Name" in df_temp.columns and "Employee ID" in df_temp.columns:
                                    existing = df_temp
                                    break
                            except:
                                continue
                        
                        if existing is None:
                            st.error("Could not find required sheet in existing users file")
                            st.stop()
                        
                        existing_sam = set(existing["SAM Account Name"].str.lower().dropna())
                        existing_staff_ids = set(existing["Employee ID"].dropna().astype(str))
                        
                        # Build title-department mapping from existing users
                        title_dept_mapping = build_title_department_mapping(existing)
                        
                        # Normalize names
                        fname = normalize_name(first_name, "title")
                        mname = normalize_name(middle_name, "title") if middle_name else ""
                        lname = normalize_name(last_name, "title")
                        fname_lc = normalize_name(first_name, "lower")
                        mname_lc = normalize_name(middle_name, "lower") if middle_name else ""
                        lname_lc = normalize_name(last_name, "lower")
                        
                        # Skip if LAST NAME missing
                        if not lname:
                            st.error("Last Name is required.")
                            st.stop()
                        
                        # Skip if both FIRST NAME and MIDDLE NAME missing
                        if not fname and not mname:
                            st.error("At least First Name or Middle Name is required.")
                            st.stop()
                        
                        role = proper_case(job_role)
                        department = clean_department("", job_role, title_dept_mapping)
                        phone = format_phone(phone_number)
                        
                        if staff_id in existing_staff_ids:
                            st.error("Staff ID already exists in the system.")
                            st.stop()
                        
                        base_upn, given_name, fail_reason = choose_upn(fname_lc, mname_lc, lname_lc, existing_sam)
                        if not base_upn:
                            st.error(f"Cannot create user: {fail_reason}")
                            st.stop()
                        
                        # Extract SOL info
                        sol_id = sol_choice.split(" - ")[0]
                        office = sol_choice.split(" - ", 1)[1]  # Get everything after the first " - "
                        address = office.split(" - ", 1)[1] if " - " in office else office  # Get address part
                        
                        display_name = f"{given_name.title()} {lname}".strip()
                        
                        # Fixed fields based on account type
                        if account_type == "User":
                            FIXED_FIELDS = {
                                "OUName": "CN=Users,DC=ubagroup,DC=com",
                                "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
                                "msExchOmaAdminWirelessEnable": "0",
                                "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
                                "memberOf": "All Staff Nigeria;UBAMicrosoftCloud;NG_Normal",
                                "pwdLastSet": "0"
                            }
                            description = staff_id
                        else:  # Vendor
                            FIXED_FIELDS = {
                                "OUName": "CN=Users,DC=ubagroup,DC=com",
                                "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
                                "msExchOmaAdminWirelessEnable": "0",
                                "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
                                "memberOf": "Remote Support",
                                "pwdLastSet": "0"
                            }
                            
                            # Get responsible party info
                            staff_name = ""
                            staff_emp_id = ""
                            staff_dept = ""
                            
                            if existing is not None:
                                email_col = None
                                for col in existing.columns:
                                    if re.search(r"(mail|email|userprincipalname)", col, re.I):
                                        email_col = col
                                        break
                                
                                if email_col:
                                    staff_row = existing[existing[email_col].str.lower() == responsible_party.lower()]
                                    if not staff_row.empty:
                                        staff_row = staff_row.iloc[0]
                                        staff_name = staff_row.get("displayName", staff_row.get("name", ""))
                                        staff_emp_id = staff_row.get("Employee ID", staff_row.get("employeeID", ""))
                                        staff_dept = staff_row.get("Department", "")
                            
                            description = f"Responsible party to the Account is {staff_name} / {staff_emp_id} / {staff_dept}"
                        
                        # Create user record
                        user_record = {
                            "givenName": given_name.title(),
                            "sn": lname,
                            "userPrincipalName": base_upn,
                            "displayName": display_name,
                            "description": description,
                            "title": role,
                            "department": department,
                            "sAMAccountName": base_upn,
                            "physicalDeliveryOfficeName": office,
                            "streetAddress": address,
                            "telephoneNumber": phone,
                            "name": display_name,
                            "mail": f"{base_upn}@ubagroup.com",
                            "company": "United Bank for Africa Plc",
                            "co": "Nigeria",
                            "mobile": phone,
                            "OUName": FIXED_FIELDS["OUName"],
                            "homeMDB": FIXED_FIELDS["homeMDB"],
                            "msExchOmaAdminWirelessEnable": FIXED_FIELDS["msExchOmaAdminWirelessEnable"],
                            "msExchHomeServerName": FIXED_FIELDS["msExchHomeServerName"],
                            "mailNickName": base_upn,
                            "memberOf": FIXED_FIELDS["memberOf"],
                            "employeeID": staff_id,
                            "password": custom_password,
                            "displayNamePrintable": display_name,
                            "pwdLastSet": FIXED_FIELDS["pwdLastSet"]
                        }
                        
                        end_time = time.time()
                        execution_time = round(end_time - start_time, 2)
                        
                        # Store results in session state
                        st.session_state['single_user_output'] = [user_record]
                        st.session_state['single_user_execution_time'] = execution_time
                        
                        st.success(f"✅ User created successfully in {execution_time}s!")
                        
                        # Generate HTML report
                        html_content = "<html><body>"
                        html_content += "<p><b>User has been created as:</b></p>"
                        html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
                        html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>Official Mail</th></tr>"
                        email = f"{user_record['userPrincipalName']}@ubagroup.com"
                        html_content += f"<tr><td>{user_record['employeeID']}</td><td><a href='mailto:{email}'>{email}</a></td></tr>"
                        html_content += "</table>"
                        html_content += "<p>Please contact ITCARE on 0201-2807200 Ext.18200 for login details.</p><br>"
                        html_content += "</body></html>"
                        
                        st.session_state['single_user_html'] = html_content
                        
                    except Exception as e:
                        st.error(f"❌ Error creating user: {str(e)}")
        
        # Display results if available
        if 'single_user_output' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Results")
            
            # Output preview
            if st.session_state['single_user_output']:
                st.markdown("#### 👥 Created User Preview")
                output_df = pd.DataFrame(st.session_state['single_user_output'])
                st.dataframe(output_df[['givenName', 'sn', 'userPrincipalName', 'employeeID', 'department', 'physicalDeliveryOfficeName']], use_container_width=True)
            
            # Download section
            st.markdown("### 📥 Download Files")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state['single_user_output']:
                    # CSV download with all fields
                    all_fields = [
                        "givenName", "sn", "userPrincipalName", "displayName", "description", 
                        "title", "department", "sAMAccountName", "physicalDeliveryOfficeName", 
                        "streetAddress", "telephoneNumber", "name", "mail", "company", "co", 
                        "mobile", "OUName", "homeMDB", "msExchOmaAdminWirelessEnable", 
                        "msExchHomeServerName", "mailNickName", "memberOf", "employeeID", 
                        "password", "displayNamePrintable", "pwdLastSet"
                    ]
                    csv_buffer = io.StringIO()
                    pd.DataFrame(st.session_state['single_user_output'])[all_fields].to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="📁 Download User CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"single_user_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if 'single_user_html' in st.session_state:
                    st.download_button(
                        label="📄 Download HTML Report",
                        data=st.session_state['single_user_html'],
                        file_name=f"single_user_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        use_container_width=True
                    )

    elif selected_tool == "generic_email":
        st.markdown("---")
        st.markdown('<div class="tool-card"><h2>📧 Generic Email Creator</h2></div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Create and export generic email accounts effortlessly</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Input fields
        col1, col2 = st.columns(2)
        
        with col1:
            generic_email_full = st.text_input("📧 Generic Email ID (e.g., generictestmail@ubagroup.com)").strip()
            display_name = st.text_input("📝 Generic Display Name (e.g., Generic Test Mail)").strip()
            staff_name = st.text_input("👤 Name of Staff (e.g., Emmanuel Imafidon)").strip()
        
        with col2:
            staff_email = st.text_input("📧 Staff Email Address (e.g., emmanuel.imafidon@ubagroup.com)").strip()
            password = st.text_input("🔒 Password for the generic account", type="password").strip()
            password_feedback = st.empty()
            ad_file = st.file_uploader("📂 Upload Existing AD Excel file", type=["xlsx"])
        
        def validate_password(pw, generic_email_full, display_name, staff_email):
            if len(pw) < 10:
                return False, "❌ Password must be at least 10 characters long."
            if not pw[0].isupper():
                return False, "❌ First letter must be capital."
            if not all(c.islower() or c.isdigit() for c in pw[1:]):
                return False, "❌ Remaining characters must be lowercase letters or numbers."
            
            # Check if password contains parts of any email or display name
            lower_pw = pw.lower()
            forbidden = re.findall(r'\w+', generic_email_full) + re.findall(r'\w+', display_name) + re.findall(r'\w+', staff_email)
            for word in forbidden:
                if word.lower() in lower_pw:
                    return False, f"❌ Password cannot contain '{word}'."
            return True, "✅ Password meets all criteria."
        
        # Live feedback
        if password:
            valid, msg = validate_password(password, generic_email_full, display_name, staff_email)
            if valid:
                password_feedback.success(msg)
            else:
                password_feedback.error(msg)
        
        # Live length check
        if generic_email_full:
            local_part = generic_email_full.split('@')[0]
            if len(local_part) > 20:
                st.warning(f"❌ Generic Email exceeds 20 characters ({len(local_part)}). Please shorten before proceeding.")
            else:
                st.success(f"✅ Generic Email meets the 20-character criteria ({len(local_part)} chars).")
        
        # Generate button
        if st.button("🚀 Generate CSV"):
            # Validate inputs
            if not all([generic_email_full, display_name, staff_name, staff_email, password, ad_file]):
                st.warning("⚠️ Please fill all fields and upload the AD Excel file.")
                st.stop()

            local_part = generic_email_full.split('@')[0]
            if len(local_part) > 20:
                st.error("❌ Generic Email still exceeds 20 characters. Please shorten it first.")
                st.stop()

            # Validate password
            valid, msg = validate_password(password, generic_email_full, display_name, staff_email)
            if not valid:
                st.error(msg)
                st.stop()

            user_principal_name = local_part

            # Read AD Excel
            try:
                ad_df = pd.read_excel(ad_file, sheet_name=1, skiprows=6)
                ad_df.columns = [str(c).strip() for c in ad_df.columns]
                st.success("✅ AD Excel loaded successfully!")
            except Exception as e:
                st.error(f"❌ Failed to read Excel: {e}")
                st.stop()

            # Check if Email Already Exists
            email_col = None
            for col in ad_df.columns:
                if re.search(r"(mail|email|userprincipalname)", col, re.I):
                    email_col = col
                    break
            if email_col is None:
                st.error("❌ Could not find any email column in the AD file.")
                st.stop()
            if any(ad_df[email_col].str.lower() == f"{user_principal_name}@ubagroup.com".lower()):
                st.error(f"❌ Cannot be created. Email already exists: {user_principal_name}@ubagroup.com")
                st.stop()

            # Lookup Staff Info
            staff_row = ad_df[ad_df[email_col].str.lower() == staff_email.lower()]
            if staff_row.empty:
                st.error(f"❌ Staff email not found in AD: {staff_email}")
                st.stop()
            staff_row = staff_row.iloc[0]

            employee_id = staff_row.get("Employee ID", "")
            department = staff_row.get("Department", "")
            office_full = staff_row.get("Office", staff_row.get("physicalDeliveryOfficeName", ""))
            street_address = ""
            if isinstance(office_full, str) and "-" in office_full:
                street_address = office_full.split("-", 1)[1].strip()
            mobile = staff_row.get("Telephone Number", "")

            # Build Export Row
            export_row = {
                "givenName": '',
                "sn": '',
                "userPrincipalName": user_principal_name,
                "displayName": display_name,
                "description": f"Responsible party to the Generic Account is {staff_name} / {employee_id} / {department}",
                "title": "",
                "department": department,
                "sAMAccountName": user_principal_name,
                "physicalDeliveryOfficeName": office_full,
                "streetAddress": street_address,
                "telephoneNumber": mobile,
                "name": display_name,
                "mail": user_principal_name,
                "company": "United Bank for Africa Plc",
                "co": staff_row.get("Country", "Nigeria"),
                "mobile": mobile,
                "employeeID": '',
                "OUName": "CN=Users,DC=ubagroup,DC=com",
                "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
                "msExchOmaAdminWirelessEnable": "0",
                "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
                "memberOf": "UBAMicrosoftCloud;NG_Normal",
                "pwdLastSet": "0",
                "password": password
            }

            # Export CSV
            export_df = pd.DataFrame([export_row])
            st.success("✅ Export ready!")
            st.download_button(
                label="⬇️ Download CSV",
                data=export_df.to_csv(index=False),
                file_name="generic_email_export.csv",
                mime="text/csv"
            )

            with st.expander("📋 Preview Export Table"):
                st.dataframe(export_df)

    elif selected_tool == "service_email":
        st.markdown("---")
        st.markdown('<div class="tool-card"><h2>🔧 Service Email Creator</h2></div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Create and export service email accounts effortlessly</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Input fields
        col1, col2 = st.columns(2)
        
        with col1:
            service_email_full = st.text_input("📧 Service Account Email (e.g., serviceaccounttest@ubagroup.com)").strip()
            display_name = st.text_input("📝 SERVICE ACCOUNT NAME (e.g., service Test Mail)").strip()
            staff_name = st.text_input("👤 Responsible Party (e.g., Emmanuel Imafidon)").strip()
        
        with col2:
            staff_email = st.text_input("📧 Responsible Party's Email (e.g., emmanuel.imafidon@ubagroup.com)").strip()
            password = st.text_input("🔒 Password for the Service Account", type="password").strip()
            password_feedback = st.empty()
            ad_file = st.file_uploader("📂 Upload Existing AD Excel file", type=["xlsx"])
        
        def validate_password(pw, service_email_full, display_name, staff_email):
            if len(pw) < 10:
                return False, "❌ Password must be at least 10 characters long."
            if not pw[0].isupper():
                return False, "❌ First letter must be capital."
            if not all(c.islower() or c.isdigit() for c in pw[1:]):
                return False, "❌ Remaining characters must be lowercase letters or numbers."
            
            # Check if password contains parts of any email or display name
            lower_pw = pw.lower()
            forbidden = re.findall(r'\w+', service_email_full) + re.findall(r'\w+', display_name) + re.findall(r'\w+', staff_email)
            for word in forbidden:
                if word.lower() in lower_pw:
                    return False, f"❌ Password cannot contain '{word}'."
            return True, "✅ Password meets all criteria."
        
        # Live feedback
        if password:
            valid, msg = validate_password(password, service_email_full, display_name, staff_email)
            if valid:
                password_feedback.success(msg)
            else:
                password_feedback.error(msg)

        # Live length check
        if service_email_full:
            local_part = service_email_full.split('@')[0]
            if len(local_part) > 20:
                st.warning(f"❌ Local part exceeds 20 characters ({len(local_part)}). Please shorten before proceeding.")
            else:
                st.success(f"✅ Service Account Email meets the 20-character criteria ({len(local_part)} chars).")
        
        # Generate button
        if st.button("🚀 Generate CSV", key="service_generate"):
            # Validate inputs
            if not all([service_email_full, display_name, staff_name, staff_email, password, ad_file]):
                st.warning("⚠️ Please fill all fields and upload the AD Excel file.")
                st.stop()

            local_part = service_email_full.split('@')[0]
            if len(local_part) > 20:
                st.error("❌ Service Account still exceeds 20 characters. Please shorten it first.")
                st.stop()

            # Validate password
            valid, msg = validate_password(password, service_email_full, display_name, staff_email)
            if not valid:
                st.error(msg)
                st.stop()

            user_principal_name = local_part

            # Read AD Excel
            try:
                ad_df = pd.read_excel(ad_file, sheet_name=1, skiprows=6)
                ad_df.columns = [str(c).strip() for c in ad_df.columns]
                st.success("✅ AD Excel loaded successfully!")
            except Exception as e:
                st.error(f"❌ Failed to read Excel: {e}")
                st.stop()

            # Check if Email Already Exists
            email_col = None
            for col in ad_df.columns:
                if re.search(r"(mail|email|userprincipalname)", col, re.I):
                    email_col = col
                    break
            if email_col is None:
                st.error("❌ Could not find any email column in the AD file.")
                st.stop()
            if any(ad_df[email_col].str.lower() == f"{user_principal_name}@ubagroup.com".lower()):
                st.error(f"❌ Cannot be created. Email already exists: {user_principal_name}@ubagroup.com")
                st.stop()

            # Lookup Staff Info
            staff_row = ad_df[ad_df[email_col].str.lower() == staff_email.lower()]
            if staff_row.empty:
                st.error(f"❌ Staff email not found in AD: {staff_email}")
                st.stop()
            staff_row = staff_row.iloc[0]

            employee_id = staff_row.get("Employee ID", "")
            department = staff_row.get("Department", "")
            office_full = staff_row.get("Office", staff_row.get("physicalDeliveryOfficeName", ""))
            street_address = ""
            if isinstance(office_full, str) and "-" in office_full:
                street_address = office_full.split("-", 1)[1].strip()
            mobile = staff_row.get("Telephone Number", "")

            # Build Export Row
            export_row = {
                "givenName": '',
                "sn": '',
                "userPrincipalName": user_principal_name,
                "displayName": display_name,
                "description": f"Responsible party to the Service Account is {staff_name} / {employee_id} / {department}",
                "title": "",
                "department": department,
                "sAMAccountName": user_principal_name,
                "physicalDeliveryOfficeName": office_full,
                "streetAddress": street_address,
                "telephoneNumber": mobile,
                "name": display_name,
                "mail": user_principal_name,
                "company": "United Bank for Africa Plc",
                "co": staff_row.get("Country", "Nigeria"),
                "mobile": mobile,
                "employeeID": '',
                "OUName": "CN=Users,DC=ubagroup,DC=com",
                "homeMDB": "",
                "msExchOmaAdminWirelessEnable": "0",
                "msExchHomeServerName": "",
                "memberOf": "UBAMicrosoftCloud;NG_Normal",
                "pwdLastSet": "0",
                "password": password
            }

            # Export CSV
            export_df = pd.DataFrame([export_row])
            st.success("✅ Export ready!")
            st.download_button(
                label="⬇️ Download CSV",
                data=export_df.to_csv(index=False),
                file_name="service_email_export.csv",
                mime="text/csv"
            )

            with st.expander("📋 Preview Export Table"):
                st.dataframe(export_df)

    elif selected_tool == "grp_script":
        st.markdown("---")
        st.markdown('<div class="grp-card"><h2>🗄️ GRP Script Generator</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📁 File Upload")
            grp_file = st.file_uploader("Upload GRP Excel File", type=['xlsx'], key="grp_file")
            
            if grp_file:
                st.markdown("#### 👀 File Preview")
                grp_df = pd.read_excel(grp_file, dtype=str)  # Keep as strings to preserve leading zeros
                st.dataframe(grp_df.head(), use_container_width=True)
                
                # Show required columns
                st.markdown("#### ✅ Required Columns Check")
                required_cols = ['EMAIL_ADDRESS', 'SURNAME', 'FIRST_NAME', 'BRANCH', 'PHONE', 'COUNTRY', 'EMPLOYEE_ID']
                
                col_status = []
                for col in required_cols:
                    if col in grp_df.columns:
                        col_status.append(f"✅ {col}")
                    else:
                        col_status.append(f"❌ {col}")
                
                st.text("\n".join(col_status))
        
        with col2:
            st.markdown("### ⚡ Execution")
            
            if st.button("🚀 Generate Script", type="primary", use_container_width=True):
                if grp_file:
                    start_time = time.time()
                    
                    with st.spinner("Generating SQL statements..."):
                        try:
                            grp_df = pd.read_excel(grp_file, dtype=str)
                            
                            # SQL template
                            sql_template = """INSERT INTO CSSERVICE.UBACS_APPUSERS
   (EMAIL_ADDRESS, SURNAME, FIRST_NAME, MIDDLE_NAME, BRANCH,
    ROLE, CREATION_DATE, PASSWORD, ACTIVE, CHANGE_PWD_ON_LOGON,
    LAST_LOGON_DATE, DELETED, CHECKED, FLOOR, SERVICE_GROUP_ID,
    PHONE, COUNTRY, EMPLOYEE_ID, STATE)
VALUES
   ('{EMAIL_ADDRESS}', '{SURNAME}', '{FIRST_NAME}', 'NA', '{BRANCH}',
    1, sysdate, 'MEFX6Mg1W0', 1, 0,
    sysdate, 0, 0, NULL, -1,
    '{PHONE}', '{COUNTRY}', '{EMPLOYEE_ID}', NULL);
"""
                            
                            # Generate SQL statements
                            sql_statements = []
                            for _, row in grp_df.iterrows():
                                sql_statements.append(sql_template.format(**row))
                            
                            sql_content = "\n".join(sql_statements)
                            
                            end_time = time.time()
                            execution_time = round(end_time - start_time, 2)
                            
                            # Store in session state
                            st.session_state['grp_sql'] = sql_content
                            st.session_state['grp_count'] = len(grp_df)
                            st.session_state['grp_execution_time'] = execution_time
                            
                            st.success(f"✅ Script generated in {execution_time}s!")
                            
                        except Exception as e:
                            st.error(f"❌ Error generating script: {str(e)}")
                else:
                    st.warning("Please upload a GRP Excel file")
        
        # Display results
        if 'grp_sql' in st.session_state:
            st.markdown("---")
            st.markdown("### 📊 Results")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("📝 Records Processed", st.session_state['grp_count'])
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("⚡ SQL Statements", st.session_state['grp_count'])
                st.markdown('</div>', unsafe_allow_html=True)
            with col3:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("⏱️ Processing Time", f"{st.session_state['grp_execution_time']}s")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # SQL preview
            st.markdown("#### 📝 Generated SQL Script Preview")
            sql_lines = st.session_state['grp_sql'].split('\n')
            preview_lines = sql_lines[:50]  # Show first 50 lines
            st.code('\n'.join(preview_lines), language='sql')
            
            if len(sql_lines) > 50:
                st.info(f"Showing first 50 lines. Full script contains {len(sql_lines)} lines.")
            
            # Download section
            st.markdown("### 📥 Download Script File")
            st.download_button(
                label="📁 Download SQL Script",
                data=st.session_state['grp_sql'],
                file_name=f"grp_sql_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    elif selected_tool == "exit_file":
        st.markdown("---")
        st.markdown('<div class="tool-card"><h2>📤 Exit File Converter</h2></div>', unsafe_allow_html=True)
        st.write("Upload an Exit Portal Excel/CSV file and download it in the required template format.")
        
        uploaded_file = st.file_uploader("Upload Exit File", type=["xlsx", "xls", "csv"])
        
        if uploaded_file:
            # Read file
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Pre-process Mobile Phone
            if "Mobile Phone" in df.columns:
                df["Mobile Phone"] = (
                    pd.to_numeric(df["Mobile Phone"], errors="coerce")
                    .astype("Int64")
                    .astype(str)
                    .replace("<NA>", "")
                    .str.replace(r"\.0$", "", regex=True)
                    .str.strip()
                )
            
            # Column Mapping
            mapping = {
                "Employee ID": "EmployeeNumber",
                "Full Name": "EmployeeName",
                "Gender": "Gender",
                "Grade": "JobGrade",
                "Job Role": "JobRole",
                "Directorate": "Directorate",
                "Date Of Employment": "DateofEmployment",
                "Effective Date": "EffectiveDate",
                "Mobile Phone": "MobilePhone",
                "Sub-reason": "ReasonForLeaving1",
                "Reason for Leaving": "OtherReasonForLeaving",
                "Work Address SolId": "SolID",
            }
            
            # Apply mapping
            df = df.rename(columns={k: v for k, v in mapping.items() if k in df.columns})
            
            # Required Columns Order
            required_cols = [
                "EmployeeNumber",
                "EmployeeName",
                "Gender",
                "JobGrade",
                "JobRole",
                "Directorate",
                "DateofEmployment",
                "EffectiveDate",
                "InitiationDate",
                "MobilePhone",
                "ReasonForLeaving1",
                "OtherReasonForLeaving",
                "SolID",
                "DateOfDeactivation",
            ]
            
            # Initialize output dataframe
            output_df = pd.DataFrame(columns=required_cols)
            
            for col in required_cols:
                if col in df.columns:
                    output_df[col] = df[col]
                else:
                    output_df[col] = ""
            
            # Derived / Cleaned Columns
            output_df["InitiationDate"] = output_df["EffectiveDate"]
            output_df["DateOfDeactivation"] = output_df["EffectiveDate"]
            
            # Clean SolID column
            if "SolID" in output_df.columns:
                output_df["SolID"] = output_df["SolID"].apply(clean_solid)
            
            # Download
            output_file = "converted_exit_file.xlsx"
            with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                output_df.to_excel(writer, index=False, sheet_name="ExitData")
            
            with open(output_file, "rb") as f:
                st.download_button(
                    label="📥 Download Converted File",
                    data=f,
                    file_name=output_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            
            st.success("✅ File converted successfully!")
            
            # Preview
            with st.expander("📋 Preview Converted Data"):
                st.dataframe(output_df)

    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚡ <strong>ITCare Hub</strong> | Created by Emmanuel Imafidon 2025</p>
        <p>Streamlining IT processes with modern technology</p>
    </div>
    """, unsafe_allow_html=True)
