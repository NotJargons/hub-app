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
    }
    
    .grp-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
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

    # Sidebar for tool selection
    with st.sidebar:
        st.markdown("### 🔧 Tool Selection")
        selected_tool = st.radio(
            "Choose your tool:",
            ["🏢 AD Bulk Creator", "🗄️ GRP Script Generator", "📧 Generic Email Creator", 
             "🔧 Service Email Creator", "🏦 Vendor Creator", "📤 Exit File Converter"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Tool Info")
        if "AD Bulk" in selected_tool:
            st.info("Creates Active Directory users from HR Excel files.")
        elif "GRP Script" in selected_tool:
            st.info("Generates SQL INSERT statements for UBACS application users from Excel data.")
        elif "Generic Email" in selected_tool:
            st.info("Creates generic email accounts for specific purposes.")
        elif "Service Email" in selected_tool:
            st.info("Creates service email accounts for applications.")
        elif "Vendor Creator" in selected_tool:
            st.info("Creates vendor accounts with manual entry.")
        elif "Exit File" in selected_tool:
            st.info("Converts exit portal files to the required template format.")

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

    ABBREVIATIONS = {"ATM", "POS", "HR", "IT", "CEO", "MD"}

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
        """Format phone with Excel-friendly leading single quote to preserve + sign"""
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
        return f"'{formatted}"

    def build_title_department_mapping(existing_df):
        """Build a smart mapping of job titles to departments from existing users data"""
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
        """Clean department value using smart title-department mapping from existing users"""
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

    # Main application logic
    if "AD Bulk" in selected_tool:
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

    elif "GRP Script" in selected_tool:
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

    elif "Generic Email" in selected_tool:
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

    elif "Service Email" in selected_tool:
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

    elif "Vendor Creator" in selected_tool:
        st.markdown('<div class="tool-card"><h2>🏦 Vendor Creator (Manual Entry)</h2></div>', unsafe_allow_html=True)
        st.write("Fill details below, choose SOL, click **Add User** for each vendor. When finished click **Export CSV**.")
        
        # Constants
        CONSTANTS = {
            "OUName": "CN=Users,DC=ubagroup,DC=com",
            "homeMDB": "CN=MDB35,CN=Databases,CN=Exchange Administrative Group (FYDIBOHF23SPDLT),CN=Administrative Groups,CN=UBAGROUP,CN=Microsoft Exchange,CN=Services,CN=Configuration,DC=ubagroup,DC=com",
            "msExchOmaAdminWirelessEnable": "0",
            "msExchHomeServerName": "/o=UBAGROUP/ou=Exchange Administrative Group (FYDIBOHF23SPDLT)/cn=Configuration/cn=Servers/cn=HQMBX01",
            "memberOf": "Remote Support",
            "company": "United Bank for Africa Plc",
            "co": "Nigeria",
            "pwdLastSet": "0"
        }

        EXPORT_COLUMNS = [
            "givenName", "sn", "userPrincipalName", "displayName", "description", "title", "department",
            "sAMAccountName", "physicalDeliveryOfficeName", "streetAddress", "telephoneNumber", "name", "mail",
            "company", "co", "mobile", "OUName", "homeMDB", "msExchOmaAdminWirelessEnable", "msExchHomeServerName",
            "mailNickName", "memberOf", "employeeID", "password", "displayNamePrintable", "pwdLastSet"
        ]
        
        # Helper functions
        def detect_sol_columns(df: pd.DataFrame):
            cols = [c for c in df.columns]
            sol_id_col, sol_name_col, street_col = None, None, None
            for c in cols:
                lc = c.lower()
                if any(k in lc for k in ["sol", "sol id", "solid", "nga_"]) and sol_id_col is None:
                    sol_id_col = c
                if any(k in lc for k in ["physical", "delivery", "office"]) and sol_name_col is None:
                    sol_name_col = c
                if any(k in lc for k in ["street", "address"]) and street_col is None:
                    street_col = c
            if sol_id_col is None and cols: sol_id_col = cols[0]
            if sol_name_col is None and len(cols) > 1: sol_name_col = cols[1]
            if street_col is None and len(cols) > 2: street_col = cols[2]
            return sol_id_col, sol_name_col, street_col

        def load_sol_list(sol_file):
            if sol_file is None:
                return pd.DataFrame(), [], "", "", ""
            try:
                df = pd.read_excel(sol_file)
                sol_id_col, sol_name_col, street_col = detect_sol_columns(df)
                df["SOL_ID"] = df[sol_id_col].astype(str).str.strip()
                df["SOL_NAME"] = df[sol_name_col].astype(str).str.strip()
                df["DISPLAY"] = df["SOL_ID"] + " - " + df["SOL_NAME"]
                return df, df["DISPLAY"].dropna().unique().tolist(), sol_id_col, sol_name_col, street_col
            except Exception as e:
                st.error(f"❌ Failed to read SOL mapping: {e}")
                return pd.DataFrame(), [], "", "", ""

        def load_existing_users(existing_file):
            if existing_file is None:
                return None
            try:
                return pd.read_excel(existing_file)
            except Exception as e:
                st.warning(f"Could not read existing users file: {e}")
                return None

        def get_next_con(existing_df, session_ids):
            max_num = 10000
            if existing_df is not None:
                id_col = next((c for c in existing_df.columns if c.strip().lower() in ["employeeid", "employee id"]), None)
                if id_col:
                    vals = existing_df[id_col].dropna().astype(str)
                    nums = [int(re.findall(r"CON(\d+)", v)[0]) for v in vals if re.match(r"CON\d+", v)]
                    if nums:
                        max_num = max(max_num, max(nums))
            if session_ids:
                nums2 = [int(re.findall(r"CON(\d+)", v)[0]) for v in session_ids if re.match(r"CON\d+", v)]
                if nums2:
                    max_num = max(max_num, max(nums2))
            return f"CON{max_num + 1:05d}"

        def validate_password(pw, first_name, surname):
            if not pw:
                return False, "❌ Password required."
            if len(pw) < 10:
                return False, "❌ Password must be at least 10 characters long."
            if not pw[0].isupper():
                return False, "❌ First letter must be capital."
            if not all(c.islower() or c.isdigit() for c in pw[1:]):
                return False, "❌ Remaining characters must be lowercase letters or numbers."
            lower_pw = pw.lower()
            for w in [first_name, surname]:
                if w and w.lower() in lower_pw:
                    return False, f"❌ Password cannot contain '{w}'."
            return True, "✅ Password meets all criteria."

        def make_username(first_name, surname):
            uname = f"{first_name.strip()}.{surname.strip()}".lower()
            return re.sub(r"[^a-z0-9.]", "", uname)
        
        # File uploads
        st.sidebar.subheader("📂 File Uploads")
        sol_file = st.sidebar.file_uploader("Upload SOL mapping file", type=["xlsx", "xls", "csv"])
        existing_file = st.sidebar.file_uploader("Upload existing_users.xlsx (optional)", type=["xlsx", "xls", "csv"])
        
        # Load files
        sol_df, sol_list, sol_id_col, sol_name_col, street_col = load_sol_list(sol_file)
        existing_df = load_existing_users(existing_file)
        
        # Session storage
        if "vendor_new_users" not in st.session_state:
            st.session_state["vendor_new_users"] = []
        
        # UI
        left, right = st.columns([2, 1])
        
        with left:
            st.subheader("User details")
            first_name = st.text_input("First Name (givenName)").strip()
            surname = st.text_input("Surname / Last Name (sn)").strip()
            job_title = st.text_input("Job Title (title)").strip()
            department = st.text_input("Department").strip()
            phone = st.text_input("Phone Number (telephoneNumber & mobile)").strip()
            password = st.text_input("Password (meets rules)", type="password")
            staff_email = st.text_input("Responsible Party Email (for description)").strip()
        
        with right:
            st.subheader("SOL / Branch")
            if sol_list:
                sol_choice = st.selectbox("Select SOL", sol_list)
                street_address = ""
                sr = sol_df.loc[sol_df["DISPLAY"] == sol_choice]
                if not sr.empty and street_col:
                    street_address = sr.iloc[0].get(street_col, "")
            else:
                st.warning("SOL list empty or not found.")
                sol_choice, street_address = "", ""

            st.markdown("---")
            if existing_df is None:
                st.warning("No existing users file loaded. Employee IDs will start at CON10001.")
            else:
                st.info(f"Loaded existing users ({len(existing_df)} rows). Using their Employee IDs to continue CON series.")
        
        session_empids = [u["employeeID"] for u in st.session_state["vendor_new_users"]]
        next_emp_preview = get_next_con(existing_df, session_empids)
        st.info(f"Next available Employee ID: **{next_emp_preview}**")
        
        # Password validation
        pw_ok = True
        if password:
            pw_ok, pw_msg = validate_password(password, first_name, surname)
            st.success(pw_msg) if pw_ok else st.error(pw_msg)
        
        # Add User button
        if st.button("➕ Add User", key="vendor_add"):
            required = [first_name, surname, job_title, department, sol_choice, password, staff_email]
            if not all(required):
                st.error("Please fill all required fields.")
            elif not pw_ok:
                st.error("Password invalid.")
            else:
                emp_id = get_next_con(existing_df, session_empids)
                username = make_username(first_name, surname)
                display_name = f"{first_name} {surname}".strip()
                description = f"{emp_id}.....Responsible party to the Account is {staff_email} / {emp_id} / {department}"

                record = {
                    "givenName": first_name,
                    "sn": surname,
                    "userPrincipalName": username,
                    "displayName": display_name,
                    "description": description,
                    "title": job_title,
                    "department": department,
                    "sAMAccountName": username,
                    "physicalDeliveryOfficeName": sol_choice,
                    "streetAddress": street_address,
                    "telephoneNumber": phone,
                    "name": display_name,
                    "mail": username,
                    "company": CONSTANTS["company"],
                    "co": CONSTANTS["co"],
                    "mobile": phone,
                    "OUName": CONSTANTS["OUName"],
                    "homeMDB": CONSTANTS["homeMDB"],
                    "msExchOmaAdminWirelessEnable": CONSTANTS["msExchOmaAdminWirelessEnable"],
                    "msExchHomeServerName": CONSTANTS["msExchHomeServerName"],
                    "mailNickName": username,
                    "memberOf": CONSTANTS["memberOf"],
                    "employeeID": emp_id,
                    "password": password,
                    "displayNamePrintable": display_name,
                    "pwdLastSet": CONSTANTS["pwdLastSet"]
                }

                st.session_state["vendor_new_users"].append(record)
                st.success(f"Added {display_name} (Employee ID: {emp_id})")
        
        # Preview & Export
        st.markdown("---")
        st.subheader("Preview - Users to be created")
        
        if st.session_state["vendor_new_users"]:
            preview_df = pd.DataFrame(st.session_state["vendor_new_users"])
            preview_df = preview_df.assign(
                userPrincipalName=preview_df["userPrincipalName"].astype(str) + "@ubagroup.com",
                mail=preview_df["mail"].astype(str) + "@ubagroup.com"
            )
            st.dataframe(preview_df[EXPORT_COLUMNS], use_container_width=True)
        else:
            st.info("No users added yet.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("↩️ Remove Last", key="vendor_remove"):
                if st.session_state["vendor_new_users"]:
                    removed = st.session_state["vendor_new_users"].pop()
                    st.warning(f"Removed {removed['displayName']} (Employee ID: {removed['employeeID']})")
        with c2:
            if st.button("🧹 Clear All", key="vendor_clear"):
                st.session_state["vendor_new_users"] = []
                st.info("Cleared all staged users.")
        with c3:
            if st.button("💾 Export CSV", key="vendor_export"):
                if not st.session_state["vendor_new_users"]:
                    st.error("No users to export.")
                else:
                    export_df = pd.DataFrame(st.session_state["vendor_new_users"])
                    export_df["userPrincipalName"] = export_df["userPrincipalName"] + "@ubagroup.com"
                    export_df["mail"] = export_df["mail"] + "@ubagroup.com"
                    for col in EXPORT_COLUMNS:
                        if col not in export_df.columns:
                            export_df[col] = ""
                    export_df = export_df[EXPORT_COLUMNS]
                    buf = BytesIO()
                    export_df.to_csv(buf, index=False)
                    buf.seek(0)
                    st.download_button("⬇️ Download Export CSV", buf.getvalue(), file_name="vendor_export.csv", mime="text/csv")
                    st.success(f"Export ready — {len(export_df)} user(s).")

    elif "Exit File" in selected_tool:
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
            def clean_solid(v):
                if pd.isna(v) or v == "":
                    return ""
                s = str(v).strip()
                s = re.sub(r"\D", "", s)
                if s and not s.startswith("0"):
                    s = "0" + s
                return s
            
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
