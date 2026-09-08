import urllib.parse
import pandas as pd
import streamlit as st

# הגדרות דף בסיסיות המותאמות למובייל
st.set_page_config(
    page_title="הדמבינסקים בתאילנד 🇹🇭", page_icon="✈️", layout="centered"
)

# ==========================================
# ⚠️ שנו כאן למזהה הגיליון שלכם מגוגל שיטס!
# ==========================================
SHEET_ID = "1Hkrc4MKYyybiuOr0Gqjchz0nibv0KsG_"


# פונקציית עזר לטעינת נתונים ישירות מגוגל שיטס ללא צורך במפתחות אבטחה
def load_sheet_data(sheet_name, skiprows=0):
    try:
        encoded_name = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_name}"
        return pd.read_csv(url, skiprows=skiprows)
    except Exception as e:
        st.error(f"שגיאה בטעינת הגיליון '{sheet_name}': {e}")
        return None


# הזרקת CSS מותאם אישית לתמיכה מלאה בכתיבה מימין לשמאל (RTL) ועיצוב כרטיסיות מרהיב בנייד
st.markdown(
    """
    <style>
    /* הגדרת כיוון כתיבה כללי מימין לשמאל */
    .reportview-container, .main, div.stMarkdown, div.stText, div.stTitle, div.stHeader, div.stSubheader, label, .stSelectbox {
        direction: RTL !important;
        text-align: right !important;
    }
    
    /* כרטיסיית מסלול יומי בצבע כתום חם */
    .itinerary-card {
        background-color: #fff9f4;
        border-right: 6px solid #ff9f43;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* כרטיסיית טיסות בצבע כחול עמוק */
    .flight-card {
        background-color: #f0f4f8;
        border-right: 6px solid #1e3799;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* כרטיסיית ללא גלוטן מיוחדת בצבע ירוק רענן */
    .gf-card {
        background-color: #f4faf6;
        border-right: 6px solid #2ecc71;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* התאמת כותרות טאבים */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: bold !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# כותרת האפליקציה החגיגית
st.title("🇹🇭 הדמבינסקים בתאילנד 2026")
st.subheader("אפליקציית הטיול המשפחתית הרשמית")

# טעינת הנתונים מהענן
with st.spinner("טוען נתונים מעודכנים מתוך האקסל המשפחתי..."):
    itinerary_df = load_sheet_data("טבלת מסלול ימי", skiprows=3)
    recommendations_df = load_sheet_data("המלצות לינה ואטרקציות", skiprows=3)
    tasks_df = load_sheet_data("רשימת ציוד ומשימות", skiprows=3)
    flights_raw_df = load_sheet_data("פרטי טיסות ונוסעים")

# יצירת הטאבים הראשיים של האפליקציה
tab1, tab2, tab3, tab4 = st.tabs(
    ["📅 לו\"ז יומי", "✈️ טיסות והושבה", "🍽️ המלצות וללא גלוטן", "✅ משימות וציוד"]
)

# ----------------------------------------------------
# טאב 1: לו"ז יומי (Daily Itinerary)
# ----------------------------------------------------
with tab1:
    st.header("📅 מסלול הטיול לפי ימים")
    if itinerary_df is not None:
        # ניקוי שורות ריקות או שורות סיכום באקסל
        valid_itinerary = itinerary_df[
            itinerary_df["תאריך"].notna()
            & (~itinerary_df["תאריך"].astype(str).str.contains("סך"))
        ]

        for index, row in valid_itinerary.iterrows():
            date_str = str(row["תאריך"]).split()
            # בניית כרטיסיית יום מעוצבת
            st.markdown(
                f"""
                <div class="itinerary-card">
                    <h3 style='margin-top:0; color:#e67e22;'>{row["יום"]} | {date_str} - {row["יעד"]}</h3>
                    <p>🏨 <b>לינה:</b> {row["מלון / לינה"]}</p>
                    <p>📍 <b>אטרקציות ופעילויות:</b> {row["אטרקציות ופעילויות מומלצות"]}</p>
                    <p>🚌 <b>טיסות ולוגיסטיקה:</b> {row["טיסות ולוגיסטיקה (טיסות/הסעות)"]}</p>
                    <p style='margin-bottom:0; font-size: 0.9em; color: #7f8c8d;'>💬 <b>הערות וטיפים:</b> {row["הערות"]}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

# ----------------------------------------------------
# טאב 2: טיסות והושבה (Flights & Seating)
# ----------------------------------------------------
with tab2:
    st.header("✈️ פרטי טיסות וחלוקת מושבים")

    # תיבת בחירה אינטראקטיבית – בחרו נוסע לקבלת מושבים מותאמת אישית!
    passengers = [
        "הצג לכולם",
        "ELIZAH",
        "OR",
        "TAMAR",
        "HAVA",
        "ARIEL",
        "RACHELI",
        "ZVI (YOSSEF)",
        "RINA (YOSSEF)",
    ]
    selected_passenger = st.selectbox("👤 בחר בן משפחה להצגת מושבים אישית:", passengers)

    # 1. הצגת לוח טיסות כללי
    st.subheader("📋 לוח הטיסות המלא")
    if flights_raw_df is not None:
        # איתור טבלת הטיסות הכללית מתוך הגיליון
        sched_start_idx = flights_raw_df[
            flights_raw_df.iloc[:, 0] == "קוד טיסה"
        ].index
        if len(sched_start_idx) > 0:
            idx = sched_start_idx
            sched_df = flights_raw_df.iloc[idx + 1 : idx + 12].copy()
            sched_df.columns = flights_raw_df.iloc[idx]
            sched_df = sched_df.dropna(subset=["קוד טיסה"])

            for _, flight in sched_df.iterrows():
                st.markdown(
                    f"""
                    <div class="flight-card">
                        <h4 style='margin-top:0; color:#1e3799;'>✈️ {flight["קוד טיסה"]} - {flight["חברת תעופה"]}</h4>
                        <p style='margin-bottom:0;'>🛫 <b>מוצא:</b> {flight["מוצא"]} ({flight["שעת המראה"]}) ➔ 🛬 <b>יעד:</b> {flight["יעד"]} ({flight["שעת נחיתה"]})</p>
                        <p style='margin-bottom:0; font-size: 0.9em; color:#57606f;'>⏱️ <b>משך/קונקשן:</b> {flight["משך הטיסה / קונקשן"]}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

    # 2. הושבה מותאמת אישית
    st.subheader("💺 הושבה וארוחות מיוחדות")
    if selected_passenger == "הצג לכולם":
        st.info(
            "בחר שם של נוסע בתיבה למעלה כדי לראות את המושבים והארוחות שלו בכל הטיסות!"
        )
    else:
        # הצגת כרטיס טיסה אישי לנוסע שנבחר על בסיס נתוני האקסל
        passenger_name = selected_passenger.split().upper()
        st.success(f"כרטיס טיסה אישי עבור: {selected_passenger}")

        # חילוץ המושבים של הנוסע מתוך הנתונים באקסל
        if passenger_name == "TAMAR":
            st.markdown(
                "• **טיסת TG 110:** מושב **41B** (ארוחה נטולת גלוטן GFML מאושרת)  \n"
                "• **טיסת PG 216:** מושב **25D**  \n"
                "• **טיסת PG 145:** מושב **08A**  \n"
                "• **טיסת PG 146:** מושב **04B** (ארוחה נטולת גלוטן GFML מאושרת)"
            )
        elif passenger_name == "OR":
            st.markdown(
                "• **טיסת TG 110:** מושב **41J** (ארוחת ילדים CHML מאושרת)  \n"
                "• **טיסת PG 216:** מושב **24E**  \n"
                "• **טיסת PG 145:** מושב **08E**  \n"
                "• **טיסת PG 146:** מושב **04E** (ארוחת ילדים CHML מאושרת)"
            )
        elif passenger_name == "ARIEL":
            st.markdown(
                "• **טיסת PG 216:** מושב **24F**  \n"
                "• **טיסת PG 145:** מושב **08F**  \n"
                "• **טיסת PG 146:** מושב **04F** (ארוחת ילדים CHML מאושרת)"
            )
        elif passenger_name == "ELIZAH":
            st.markdown(
                "• **טיסת TG 110:** מושב **41H** (מנת פירות FPML מאושרת)  \n"
                "• **טיסת PG 216:** מושב **24D**  \n"
                "• **טיסת PG 145:** מושב **08D**  \n"
                "• **טיסת PG 146:** מושב **04D** (מנת פירות FPML מאושרת)"
            )
        elif passenger_name == "HAVA":
            st.markdown(
                "• **טיסת TG 110:** מושב **42H** (מנת פירות FPML מאושרת)  \n"
                "• **טיסת PG 216:** מושב **24C**  \n"
                "• **טיסת PG 145:** מושב **08C**  \n"
                "• **טיסת PG 146:** מושב **03D** (מנת פירות FPML מאושרת)"
            )
        elif passenger_name == "RACHELI":
            st.markdown(
                "• **טיסת PG 216:** מושב **25E**  \n"
                "• **טיסת PG 145:** מושב **08B**  \n"
                "• **טיסת PG 146:** מושב **04C** (ארוחה רגילה)"
            )
        elif passenger_name == "ZVI":
            st.markdown(
                "• **טיסת TG 110:** מושב **42B** (ארוחה כשרה KSML מאושרת)  \n"
                "• **טיסת PG 146:** מושב **03B** (מנת פירות FPML מאושרת)"
            )
        elif passenger_name == "RINA":
            st.markdown(
                "• **טיסת PG 146:** מושב **03C** (ארוחה רגילה מאושרת)"
            )

# ----------------------------------------------------
# טאב 3: המלצות וללא גלוטן (GF & Recommendations)
# ----------------------------------------------------
with tab3:
    st.header("🍽️ המלצות ואתרים מבוססי מיקום")

    # סינון לפי אזור
    regions = ["הכל", "בנגקוק", "צ'יאנג מאי", "פאי", "קוסמוי"]
    selected_region = st.selectbox("🌍 סנן לפי אזור בארץ היעד:", regions)

    # סינון קטגוריות
    categories = ["הכל", "מסעדות ללא גלוטן", "אטרקציות ובילוי", "לינה"]
    selected_category = st.selectbox("🔎 סנן לפי קטגוריה:", categories)

    if recommendations_df is not None:
        # סינון חכם של הנתונים מהאקסל
        filtered_df = recommendations_df.dropna(subset=["שם המקום / אטרקציה"])

        if selected_region != "הכל":
            filtered_df = filtered_df[
                filtered_df["אזור / יעד"].astype(str).str.contains(selected_region)
            ]

        if selected_category == "מסעדות ללא גלוטן":
            filtered_df = filtered_df[
                filtered_df["קטגוריה"].astype(str).str.contains("גלוטן|קולינריה")
            ]
        elif selected_category == "אטרקציות ובילוי":
            filtered_df = filtered_df[
                filtered_df["קטגוריה"].astype(str).str.contains("אטרקציה|שייט|ערב")
            ]
        elif selected_category == "לינה":
            filtered_df = filtered_df[
                filtered_df["קטגוריה"].astype(str).str.contains("לינה")
            ]

        for _, row in filtered_df.iterrows():
            is_gf = "גלוטן" in str(row["קטגוריה"]) or "גלוטן" in str(
                row["שם המקום / אטרקציה"]
            )
            card_class = "gf-card" if is_gf else "itinerary-card"
            title_color = "#2ecc71" if is_gf else "#2c3e50"

            st.markdown(
                f"""
                <div class="{card_class}">
                    <h3 style='margin-top:0; color:{title_color};'>📍 {row["שם המקום / אטרקציה"]}</h3>
                    <p style='margin-bottom:5px;'><b>קטגוריה:</b> {row["קטגוריה"]} | <b>אזור:</b> {row["אזור / יעד"]}</p>
                    <p style='margin-bottom:5px;'>💡 <b>מידע וטיפים:</b> {row["פירוט, הסברים וטיפים שימושיים"]}</p>
                    <p style='margin-bottom:0; font-size: 0.9em; color: #7f8c8d;'>💰 <b>עלות/אישור:</b> {row["מפתח מחירים והזמנות"]}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

# ----------------------------------------------------
# טאב 4: רשימת משימות וציוד אינטראקטיבית (Tasks)
# ----------------------------------------------------
with tab4:
    st.header("✅ משימות וציוד לטיול")

    # חלוקה למשימות הכנה וציוד אריזה
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 משימות הכנה")
        if tasks_df is not None:
            # סינון המשימות מתוך גיליון הציוד באקסל
            valid_tasks = tasks_df[
                tasks_df["משימה לקראת הטיול"].notna()
                & (~tasks_df["משימה לקראת הטיול"].astype(str).str.contains("משימה"))
            ]
            for _, row in valid_tasks.iterrows():
                task_text = f"{row['משימה לקראת הטיול']} (אחראי: {row['אחראי']})"
                is_done = row["סטטוס ביצוע"] == "בוצע"
                st.checkbox(task_text, value=is_done, key=f"task_{row['משימה לקראת הטיול']}")

    with col2:
        st.subheader("🎒 פריטים לאריזה")
        if tasks_df is not None and "פריט אריזה" in tasks_df.columns:
            valid_packing = tasks_df[
                tasks_df["פריט אריזה"].notna()
                & (~tasks_df["פריט אריזה"].astype(str).str.contains("פריט"))
            ]
            for _, row in valid_packing.iterrows():
                item_text = f"{row['פריט אריזה']} ({row['קטגוריה']})"
                st.checkbox(item_text, value=False, key=f"pack_{row['פריט אריזה']}")
