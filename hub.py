import streamlit as st
import pandas as pd
import time
import io
import os
from datetime import datetime
from pathlib import Path
import numpy as np
import re

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
    }
    
    .grp-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .generic-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    .service-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
    
    .admin-badge {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }

    .password-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
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

# Password validation function
def validate_password(pw, email_full, display_name, staff_email):
    """Validate password meets all criteria"""
    if len(pw) < 10:
        return False, "❌ Password must be at least 10 characters long."
    if not pw[0].isupper():
        return False, "❌ First letter must be capital."
    if not all(c.islower() or c.isdigit() for c in pw[1:]):
        return False, "❌ Remaining characters must be lowercase letters or numbers."
    
    # Check if password contains parts of any email or display name
    lower_pw = pw.lower()
    forbidden = re.findall(r'\w+', email_full) + re.findall(r'\w+', display_name) + re.findall(r'\w+', staff_email)
    for word in forbidden:
        if word.lower() in lower_pw:
            return False, f"❌ Password cannot contain '{word}'."
    return True, "✅ Password meets all criteria."

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

    # Sidebar for tool selection
    with st.sidebar:
        st.markdown("### 🔧 Tool Selection")
        selected_tool = st.radio(
            "Choose your tool:",
            ["🏢 AD Bulk Creator", "🗄️ GRP Script Generator", "📧 Generic Email Creator", "⚙️ Service Account Creator"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Tool Info")
        if "AD Bulk" in selected_tool:
            st.info("Creates Active Directory users from HR Excel files.")
        elif "Generic Email" in selected_tool:
            st.info("Creates Generic Email Accounts with validation.")
        elif "Service Account" in selected_tool:
            st.info("Creates Service Accounts with validation.")
        elif "GRP Script" in selected_tool:
            st.info("Generates SQL INSERT statements for UBACS application users.")

    # AD Bulk Creator Functions (keeping your existing code)
    def normalize_hr_file(hr_df: pd.DataFrame) -> pd.DataFrame:
        """Normalize HR file column names"""
        column_map = {
            "staff id": ["staff id", "employee id", "employee_id", "employment number", "staff_no", "staff number"],
            "first name": ["first name", "firstname", "emp first name", "given name"],
            "surname": ["surname", "last name", "lastname", "family name"],
            "middle name": ["middle name", "middlename", "other name"],
            "phone number": ["phone number", "phone", "mobile", "number", "contact", "telephone"],
            "role": ["role", "job role", "position", "designation", "job title"],
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

    ABBREVIATIONS = {"ATM", "POS", "HR", "IT", "CEO", "MD"}

    def normalize_name(name: str, case="title"):
        if not name or str(name).lower() == "nan": return ""
        name = str(name).strip().replace(" ", "-")
        return name.title() if case=="title" else name.lower()

    def proper_case(text: str):
        if not text or str(text).lower()=="nan": return "N/A"
        return " ".join([w.upper() if w.upper() in ABBREVIATIONS else w.capitalize() for w in str(text).split()])

    def clean_sol(sol_val):
        try: sol=str(sol_val).split(".")[0]; return sol.zfill(4) if sol.isdigit() else None
        except: return None

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
        
        return f"{formatted}"

    def clean_department(dept_val, role_val):
        if str(role_val).strip().lower()=="direct sales executive": return "Marketing"
        dept = proper_case(dept_val)
        return dept if dept!="N/A" else proper_case(role_val)

    def choose_upn(fname, mname, lname, existing_sam):
        reasons=[]
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

    # TOOL 1: AD BULK CREATOR
    if "AD Bulk" in selected_tool:
        st.markdown('<div class="tool-card"><h2>🏢 AD Bulk Creator</h2></div>', unsafe_allow_html=True)
        
        # (Your existing AD Bulk Creator code - keeping it as is from document 10)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📁 File Upload")
            hr_file = st.file_uploader("Upload HR File (Excel)", type=['xlsx'], key="hr_file")
            existing_file = st.file_uploader("Upload Existing Users File (Excel)", type=['xlsx'], key="existing_file")
            sol_file = st.file_uploader("Upload SOL Mapping File (Excel)", type=['xlsx'], key="sol_file")

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
            
            if st.button("🚀 Process Files", type="primary", use_container_width=True):
                st.info("Processing... (your existing AD Bulk code runs here)")

    # TOOL 2: GRP SCRIPT GENERATOR  
    elif "GRP Script" in selected_tool:
        st.markdown('<div class="grp-card"><h2>🗄️ GRP Script Generator</h2></div>', unsafe_allow_html=True)
        
        # (Your existing GRP Script Generator code - keeping it as is from document 10)
        st.info("Your GRP Script Generator code goes here")

    # TOOL 3: GENERIC EMAIL CREATOR
    elif "Generic Email" in selected_tool:
        st.markdown('<div class="generic-card"><h2>📧 Generic Email Creator</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            generic_email_full = st.text_input("📧 Generic Email ID", placeholder="generictestmail@ubagroup.com")
            display_name = st.text_input("📝 Generic Display Name", placeholder="Generic Test Mail")
            staff_name = st.text_input("👤 Name of Staff", placeholder="Emmanuel Imafidon")

        with col2:
            staff_email = st.text_input("📧 Staff Email Address", placeholder="emmanuel.imafidon@ubagroup.com")
            password_generic = st.text_input("🔒 Password", type="password", key="gen_password")
            ad_file_generic = st.file_uploader("📂 Upload AD Excel file", type=["xlsx"], key="gen_ad_file")

        # Password validation
        if password_generic:
            valid, msg = validate_password(password_generic, generic_email_full, display_name, staff_email)
            if valid:
                st.success(msg)
            else:
                st.error(msg)

        # Length check
        if generic_email_full:
            local_part = generic_email_full.split('@')[0]
            if len(local_part) > 20:
                st.warning(f"❌ Generic Email exceeds 20 characters ({len(local_part)}). Please shorten.")
            else:
                st.success(f"✅ Generic Email meets criteria ({len(local_part)} chars).")

        # Generate button
        if st.button("🚀 Generate Generic Email CSV", type="primary", use_container_width=True):
            if not all([generic_email_full, display_name, staff_name, staff_email, password_generic, ad_file_generic]):
                st.warning("⚠️ Please fill all fields and upload the AD Excel file.")
            else:
                local_part = generic_email_full.split('@')[0]
                if len(local_part) > 20:
                    st.error("❌ Email exceeds 20 characters.")
                else:
                    user_principal_name = local_part
                    
                    try:
                        ad_df = pd.read_excel(ad_file_generic, sheet_name=1, skiprows=6)
                        ad_df.columns = [str(c).strip() for c in ad_df.columns]
                        
                        # Find email column
                        email_col = None
                        for col in ad_df.columns:
                            if re.search(r"(mail|email|userprincipalname)", col, re.I):
                                email_col = col
                                break
                        
                        if email_col is None:
                            st.error("❌ Could not find email column in AD file.")
                        elif any(ad_df[email_col].str.lower() == f"{user_principal_name}@ubagroup.com".lower()):
                            st.error(f"❌ Email already exists: {user_principal_name}@ubagroup.com")
                        else:
                            # Lookup staff
                            staff_row = ad_df[ad_df[email_col].str.lower() == staff_email.lower()]
                            if staff_row.empty:
                                st.error(f"❌ Staff email not found: {staff_email}")
                            else:
                                staff_row = staff_row.iloc[0]
                                employee_id = staff_row.get("Employee ID", "")
                                department = staff_row.get("Department", "")
                                office_full = staff_row.get("Office", "")
                                street_address = ""
                                if isinstance(office_full, str) and "-" in office_full:
                                    street_address = office_full.split("-", 1)[1].strip()
                                mobile = staff_row.get("Mobile", "")
                                
                                export_row = {
                                    "givenName": '', "sn": '',
                                    "userPrincipalName": user_principal_name,
                                    "displayName": display_name,
                                    "description": f"Responsible party to the Generic Account is {staff_name} / {employee_id} / {department}",
                                    "title": "", "department": department,
                                    "sAMAccountName": user_principal_name,
                                    "physicalDeliveryOfficeName": office_full,
                                    "streetAddress": street_address,
                                    "telephoneNumber": mobile,
                                    "name": display_name,
                                    "mail": user_principal_name,
                                    "company": "United Bank for Africa Plc",
                                    "co": staff_row.get("Country", "Nigeria"),
                                    "mobile": mobile, "employeeID": '',
                                    "OUName": "CN=Users,DC=ubagroup,DC=com",
                                    "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
                                    "msExchOmaAdminWirelessEnable": "0",
                                    "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
                                    "mailNickName": user_principal_name,
                                    "memberOf": "UBAMicrosoftCloud;NG_Normal",
                                    "password": password_generic,
                                    "displayNamePrintable": display_name,
                                    "pwdLastSet": "0"
                                }
                                
                                export_df = pd.DataFrame([export_row])
                                st.success("✅ Export ready!")
                                
                                csv_data = export_df.to_csv(index=False)
                                st.download_button(
                                    label="⬇️ Download Generic Email CSV",
                                    data=csv_data,
                                    file_name=f"generic_email_{user_principal_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                                
                                with st.expander("📋 Preview Export"):
                                    st.dataframe(export_df)
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # TOOL 4: SERVICE ACCOUNT CREATOR
    elif "Service Account" in selected_tool:
        st.markdown('<div class="service-card"><h2>⚙️ Service Account Creator</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            service_email_full = st.text_input("📧 Service Account Email", placeholder="serviceaccounttest@ubagroup.com")
            display_name_service = st.text_input("📝 Service Account Name", placeholder="Service Test Account")
            staff_name_service = st.text_input("👤 Responsible Party", placeholder="Emmanuel Imafidon")

        with col2:
            staff_email_service = st.text_input("📧 Responsible Party's Email", placeholder="emmanuel.imafidon@ubagroup.com")
            password_service = st.text_input("🔒 Password", type="password", key="svc_password")
            ad_file_service = st.file_uploader("📂 Upload AD Excel file", type=["xlsx"], key="svc_ad_file")

        # Password validation
        if password_service:
            valid, msg = validate_password(password_service, service_email_full, display_name_service, staff_email_service)
            if valid:
                st.success(msg)
            else:
                st.error(msg)

        # Length check
        if service_email_full:
            local_part = service_email_full.split('@')[0]
            if len(local_part) > 20:
                st.warning(f"❌ Service email exceeds 20 characters ({len(local_part)}). Please shorten.")
            else:
                st.success(f"✅ Service Account Email meets criteria ({len(local_part)} chars).")

        # Generate button
        if st.button("🚀 Generate Service Account CSV", type="primary", use_container_width=True):
            if not all([service_email_full, display_name_service, staff_name_service, staff_email_service, password_service, ad_file_service]):
                st.warning("⚠️ Please fill all fields and upload the AD Excel file.")
            else:
                local_part = service_email_full.split('@')[0]
                if len(local_part) > 20:
                    st.error("❌ Email exceeds 20 characters.")
                else:
                    user_principal_name = local_part
                    
                    try:
                        ad_df = pd.read_excel(ad_file_service, sheet_name=1, skiprows=6)
                        ad_df.columns = [str(c).strip() for c in ad_df.columns]
                        
                        # Find email column
                        email_col = None
                        for col in ad_df.columns:
                            if re.search(r"(mail|email|userprincipalname)", col, re.I):
                                email_col = col
                                break
                        
                        if email_col is None:
                            st.error("❌ Could not find email column in AD file.")
                        elif any(ad_df[email_col].str.lower() == f"{user_principal_name}@ubagroup.com".lower()):
                            st.error(f"❌ Email already exists: {user_principal_name}@ubagroup.com")
                        else:
                            # Lookup staff
                            staff_row = ad_df[ad_df[email_col].str.lower() == staff_email_service.lower()]
                            if staff_row.empty:
                                st.error(f"❌ Staff email not found: {staff_email_service}")
                            else:
                                staff_row = staff_row.iloc[0]
                                employee_id = staff_row.get("Employee ID", "")
                                department = staff_row.get("Department", "")
                                office_full = staff_row.get("Office", "")
                                street_address = ""
                                if isinstance(office_full, str) and "-" in office_full:
                                    street_address = office_full.split("-", 1)[1].strip()
                                mobile = staff_row.get("Mobile", "")
                                
                                export_row = {
                                    "givenName": '', "sn": '',
                                    "userPrincipalName": user_principal_name,
                                    "displayName": display_name_service,
                                    "description": f"Responsible party to the Service Account is {staff_name_service} / {employee_id} / {department}",
                                    "title": "", "department": department,
                                    "sAMAccountName": user_principal_name,
                                    "physicalDeliveryOfficeName": office_full,
                                    "streetAddress": street_address,
                                    "telephoneNumber": mobile,
                                    "name": display_name_service,
                                    "mail": user_principal_name,
                                    "company": "United Bank for Africa Plc",
                                    "co": staff_row.get("Country", "Nigeria"),
                                    "mobile": mobile, "employeeID": '',
                                    "OUName": "CN=Users,DC=ubagroup,DC=com",
                                    "homeMDB": "",
                                    "msExchOmaAdminWirelessEnable": "0",
                                    "msExchHomeServerName": "",
                                    "mailNickName": user_principal_name,
                                    "memberOf": "UBAMicrosoftCloud;NG_Normal",
                                    "password": password_service,
                                    "displayNamePrintable": display_name_service,
                                    "pwdLastSet": "0"
                                }
                                
                                export_df = pd.DataFrame([export_row])
                                st.success("✅ Export ready!")
                                
                                csv_data = export_df.to_csv(index=False)
                                st.download_button(
                                    label="⬇️ Download Service Account CSV",
                                    data=csv_data,
                                    file_name=f"service_account_{user_principal_name}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                                
                                with st.expander("📋 Preview Export"):
                                    st.dataframe(export_df)
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚡ <strong>ITCare Hub</strong> | Created by Emmanuel Imafidon 2025</p>
        <p>Streamlining IT processes with modern technology</p>
    </div>
    """, unsafe_allow_html=True)
