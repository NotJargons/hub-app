import streamlit as st
import pandas as pd
import time
import io
import os
from datetime import datetime
from pathlib import Path
import numpy as np

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
            ["🏢 AD Bulk Creator", "🗄️ GRP Script Generator"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Tool Info")
        if "AD Bulk" in selected_tool:
            st.info("Creates Active Directory users from HR Excel files.")
        else:
            st.info("Generates SQL INSERT statements for UBACS application users from Excel data.")

    # AD Bulk Creator Functions
       # ✅ Corrected normalize_hr_file
    def normalize_hr_file(hr_df: pd.DataFrame) -> pd.DataFrame:
        """Normalize HR file column names — handles variations automatically"""
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
        return f"{formatted}"

    def clean_department(dept_val, role_val):
        if str(role_val).strip().lower()=="direct sales executive": return "Marketing"
        dept = proper_case(dept_val)
        return dept if dept!="N/A" else proper_case(role_val)

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
            
            if st.button("🚀 Process Files", type="primary", use_container_width=True):
                if hr_file and existing_file and sol_file:
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
                            
                            sol_dict = {str(r["SOL ID"]).split(".")[0].zfill(4): (
                                            str(r.get("physicalDevliveryOfficeName", "N/A")),
                                            str(r.get("streetAddress", "N/A"))
                                        ) for _, r in solmap.iterrows()}
                            
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
                                department = clean_department(row.get("DEPARTMENT",""), role)
                                sol_id = clean_sol(row["SOL ID"])
                                phone = format_phone(row["PHONE NUMBER"])  # Excel-friendly format
                                
                                if staff_id in existing_staff_ids:
                                    skipped.append({"Staff ID": staff_id, "Reason":"Duplicate Staff ID"})
                                    continue
                                
                                base_upn, given_name, fail_reason = choose_upn(fname_lc, mname_lc, lname_lc, existing_sam)
                                if not base_upn:
                                    skipped.append({"Staff ID": staff_id, "Reason": fail_reason})
                                    continue
                                
                                office, address = sol_dict.get(sol_id, ("N/A","N/A"))
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
                                    "password": "Developer2378",
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
                st.dataframe(output_df[['givenName', 'sn', 'userPrincipalName', 'employeeID', 'department']].head(10), use_container_width=True)
            
            # Skipped users
            if st.session_state['ad_skipped']:
                st.markdown("#### ⚠️ Skipped Users")
                skipped_df = pd.DataFrame(st.session_state['ad_skipped'])
                st.dataframe(skipped_df, use_container_width=True)
            
            # Download section
            st.markdown("### 📥 Download Files")
            col1, col2, col3 = st.columns(3)
            
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
        html_content = "<html><body>"

        # ✅ Created Users Section
        created_count = len(st.session_state['ad_output'])
        if created_count:
            noun = "user has" if created_count == 1 else "users have"
            html_content += f"<p><b>{created_count} {noun} been created as:</b></p>"
            html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
            html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>Official Mail</th></tr>"
            for user in st.session_state['ad_output']:
                email = f"{user['userPrincipalName']}@ubagroup.com"
                html_content += f"<tr><td>{user['employeeID']}</td><td><a href='mailto:{email}'>{email}</a></td></tr>"
            html_content += "</table>"
            html_content += "<p>Please contact ITCARE on 0201-2807200 Ext.18200 for login details.</p><br>"

        # ✅ Skipped Users Section
        skipped_count = len(st.session_state['ad_skipped'])
        if skipped_count:
            noun = "user was" if skipped_count == 1 else "users were"
            html_content += f"<p><b>However, the below {noun} not created due to errors below:</b></p>"
            html_content += '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse;">'
            html_content += "<tr style='background-color:#c00000;color:white;'><th>Staff ID</th><th>First Name</th><th>Last Name</th><th>Middle Name</th><th>Reason</th></tr>"
            for s in st.session_state['ad_skipped']:
                staff = st.session_state['ad_hr'][st.session_state['ad_hr']["STAFF ID"].str.upper() == s["Staff ID"]]
                if not staff.empty:
                    staff = staff.iloc[0]
                    html_content += f"<tr><td>{s['Staff ID']}</td><td>{staff.get('FIRST NAME','')}</td><td>{staff.get('SURNAME','')}</td><td>{staff.get('MIDDLE NAME','')}</td><td>{s['Reason']}</td></tr>"
            html_content += "</table>"
            html_content += "<p>Please review the above errors and revert.</p>"
                    
                    html_content += "</body></html>"
                    
                    st.download_button(
                        label="📄 Download HTML Report",
                        data=html_content,
                        file_name=f"ad_bulk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
            
            # Additional info about Excel formatting
            if st.session_state['ad_output']:
                st.info("📝 **Note:** Phone numbers in the CSV are prefixed with a single quote (') to preserve the + sign when opening in Excel.")

    else:  # GRP Script Generator
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

    # Footer
    st.markdown("""
    <div class="footer">
        <p>⚡ <strong>ITCare Hub</strong> | Created by Emmanuel Imafidon 2025</p>
        <p>Streamlining IT processes with modern technology</p>
    </div>
    """, unsafe_allow_html=True)
