
import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\Windows\Downloads\HarvardMuseum.db"

# Utility function to run SQL queries
def run_query(query: str) -> pd.DataFrame:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            return pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return pd.DataFrame()

st.title("🏛️ Harvard Museum Artifact Explorer")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗃️ Artifact Metadata", 
    "🖼️ Artifact Media", 
    "🎨 Artifact Colors", 
    "🔗 Join-Based Queries",
    "📊 Classification Explorer"
])


with tab1:
    st.header("🗃️ Artifact Metadata Table")
    
    # Query 1: 11th century Byzantine artifacts
    st.subheader("1. 11th Century Byzantine Artifacts")
    query1 = """
    SELECT * FROM artifact_metadata
    WHERE century = '11th century' AND culture = 'Byzantine';
    """
    df1 = run_query(query1)
    if not df1.empty:
        st.dataframe(df1)
        st.write(f"**Total artifacts:** {len(df1)}")
    else:
        st.info("No 11th century Byzantine artifacts found")

    # Query 2: Unique cultures
    st.subheader("2. Unique Cultures")
    query2 = """
    SELECT DISTINCT culture FROM artifact_metadata
    WHERE culture IS NOT NULL AND TRIM(culture) != ''
    ORDER BY culture;
    """
    df2 = run_query(query2)
    if not df2.empty:
        st.dataframe(df2)
        st.write(f"**Total unique cultures:** {len(df2)}")
    else:
        st.info("No culture data available")

    # Query 3: Archaic Period artifacts
    st.subheader("3. Archaic Period Artifacts")
    query3 = """
    SELECT * FROM artifact_metadata
    WHERE period = 'Archaic';
    """
    df3 = run_query(query3)
    if not df3.empty:
        st.dataframe(df3)
        st.write(f"**Total Archaic period artifacts:** {len(df3)}")
    else:
        st.info("No Archaic period artifacts found")

    # Query 4: Titles by accession year
    st.subheader("4. Artifact Titles by Accession Year")
    query4 = """
    SELECT title, accessionyear FROM artifact_metadata
    WHERE accessionyear IS NOT NULL
    ORDER BY accessionyear DESC;
    """
    df4 = run_query(query4)
    if not df4.empty:
        st.dataframe(df4)
    else:
        st.info("No accession year data available")

    # Query 5: Artifacts per department
    st.subheader("5. Artifacts per Department")
    query5 = """
    SELECT department, COUNT(*) AS artifact_count
    FROM artifact_metadata
    WHERE department IS NOT NULL AND TRIM(department) != ''
    GROUP BY department
    ORDER BY artifact_count DESC;
    """
    df5 = run_query(query5)
    if not df5.empty:
        st.dataframe(df5)
        st.bar_chart(df5.set_index('department'))
    else:
        st.info("No department data available")

with tab2:
    st.header("🖼️ Artifact Media Table")
    
    # Query 1: Artifacts with more than 1 image
    st.subheader("1. Artifacts with Multiple Images")
    query1_media = """
    SELECT objectid, COUNT(*) as image_count
    FROM artifact_media
    GROUP BY objectid
    HAVING COUNT(*) > 1
    ORDER BY image_count DESC;
    """
    df1_media = run_query(query1_media)
    if not df1_media.empty:
        st.dataframe(df1_media)
        st.write(f"**Artifacts with multiple images:** {len(df1_media)}")
    else:
        st.info("No artifacts with multiple images found")

    # Query 2: Average rank
    st.subheader("2. Average Rank of Artifacts")
    query2_media = """
    SELECT AVG(rank) as average_rank FROM artifact_media;
    """
    df2_media = run_query(query2_media)
    if not df2_media.empty:
        avg_rank = df2_media.iloc[0]['average_rank']
        st.metric("Average Rank", f"{avg_rank:.2f}")
    else:
        st.info("No rank data available")

    # Query 3: Colorcount > Mediascount
    st.subheader("3. Artifacts with Colorcount > Mediascount")
    query3_media = """
    SELECT objectid, colorcount, mediacount
    FROM artifact_media
    WHERE colorcount > mediacount;
    """
    df3_media = run_query(query3_media)
    if not df3_media.empty:
        st.dataframe(df3_media)
        st.write(f"**Artifacts with colorcount > mediacount:** {len(df3_media)}")
    else:
        st.info("No artifacts with colorcount greater than mediacount")

    # Query 4: Artifacts from 1500-1600
    st.subheader("4. Artifacts Created Between 1500-1600")
    query4_media = """
    SELECT *FROM artifact_media WHERE datebegin <= 1600 AND dateend >= 1500;"""
    df4_media = run_query(query4_media)
    if not df4_media.empty:
        st.dataframe(df4_media)
        st.write(f"**Artifacts from 1500-1600:** {len(df4_media)}")
    else:
        st.info("No artifacts found from 1500-1600")

    # Query 5: Artifacts with no media
    st.subheader("5. Artifacts with No Media Files")
    query5_media = """
    SELECT meta.id, meta.title
    FROM artifact_metadata meta
    LEFT JOIN artifact_media media ON meta.id = media.objectid
    WHERE media.objectid IS NULL;
    """
    df5_media = run_query(query5_media)
    if not df5_media.empty:
        st.dataframe(df5_media)
        st.write(f"**Artifacts with no media:** {len(df5_media)}")
    else:
        st.info("All artifacts have media files")

with tab3:
    st.header("🎨 Artifact Colors Table")
    
    # Query 1: Distinct hues
    st.subheader("1. Distinct Hues")
    query1_colors = """
    SELECT DISTINCT hue FROM artifact_colors
    WHERE hue IS NOT NULL AND TRIM(hue) != ''
    ORDER BY hue;
    """
    df1_colors = run_query(query1_colors)
    if not df1_colors.empty:
        st.dataframe(df1_colors)
        st.write(f"**Total distinct hues:** {len(df1_colors)}")
    else:
        st.info("No hue data available")

    # Query 2: Top 5 colors by frequency
    st.subheader("2. Top 5 Most Used Colors")
    query2_colors = """
    SELECT hue, COUNT(*) as frequency
    FROM artifact_colors
    WHERE hue IS NOT NULL AND TRIM(hue) != ''
    GROUP BY hue
    ORDER BY frequency DESC
    LIMIT 5;
    """
    df2_colors = run_query(query2_colors)
    if not df2_colors.empty:
        st.dataframe(df2_colors)
        st.bar_chart(df2_colors.set_index('hue'))
    else:
        st.info("No color frequency data available")

    # Query 3: Average coverage by hue
    st.subheader("3. Average Coverage by Hue")
    query3_colors = """
    SELECT hue, AVG(percent) AS avg_coverage
    FROM artifact_colors
    WHERE hue IS NOT NULL AND TRIM(hue) != ''
    GROUP BY hue
    ORDER BY avg_coverage DESC;"""
    df3_colors = run_query(query3_colors)
    if not df3_colors.empty:
        st.dataframe(df3_colors)
    else:
        st.info("No coverage data available")

    # Query 4: Colors for a specific artifact
    st.subheader("4. Colors for a Specific Artifact")
    artifact_id = st.text_input("Enter Artifact ID:", value="12345")
    if artifact_id:
        query4_colors = f"""
        SELECT * FROM artifact_colors
        WHERE objectid = '{artifact_id}'
        ORDER BY coverage DESC;
        """
        df4_colors = run_query(query4_colors)
        if not df4_colors.empty:
            st.dataframe(df4_colors)
            st.write(f"**Colors found:** {len(df4_colors)}")
        else:
            st.info(f"No colors found for artifact ID: {artifact_id}")

    # Query 5: Total color entries
    st.subheader("5. Total Color Entries")
    query5_colors = "SELECT COUNT(*) as total_entries FROM artifact_colors;"
    df5_colors = run_query(query5_colors)
    if not df5_colors.empty:
        total = df5_colors.iloc[0]['total_entries']
        st.metric("Total Color Entries", total)
    else:
        st.info("No color entries found")

with tab4:
    st.header("🔗 Join-Based Queries")
    
    # Query 1: Byzantine artifacts with hues
    st.subheader("1. Byzantine Artifacts with Hues")
    query1_join = """
    SELECT meta.title, colors.hue
    FROM artifact_metadata meta
    JOIN artifact_colors colors ON meta.id = colors.objectid
    WHERE meta.culture = 'Byzantine'
    ORDER BY meta.title, colors.hue;

    """
    df1_join = run_query(query1_join)
    if not df1_join.empty:
        st.dataframe(df1_join)
        st.write(f"**Byzantine artifacts with color data:** {len(df1_join)}")
    else:
        st.info("No Byzantine artifacts with color data found")

    # Query 2: All artifacts with hues
    st.subheader("2. All Artifacts with Associated Hues")
    query2_join = """
    SELECT meta.title, colors.hue
    FROM artifact_metadata meta
    JOIN artifact_colors colors ON meta.id = colors.objectid
    WHERE colors.hue IS NOT NULL AND TRIM(colors.hue) != ''
    ORDER BY meta.title, colors.hue;"""
    df2_join = run_query(query2_join)
    if not df2_join.empty:
        st.dataframe(df2_join)
        st.write("Showing first 1000 results")
    else:
        st.info("No artifact-color associations found")

    # Query 3: Artifacts with period not null
    st.subheader("3. Artifacts with Period Data and Media Ranks")
    query3_join = """
    SELECT meta.title, meta.culture, media.rank
    FROM artifact_metadata meta
    JOIN artifact_media media ON meta.id = media.objectid
    WHERE meta.period IS NOT NULL AND TRIM(meta.period) != ''
    ORDER BY media.rank DESC
    LIMIT 500;
    """
    df3_join = run_query(query3_join)
    if not df3_join.empty:
        st.dataframe(df3_join)
        st.write("Showing top 500 results by rank")
    else:
        st.info("No artifacts with period data found")

    # Query 4: Top 10 artifacts with Grey hue
    st.subheader("4. Top 10 Artifacts with Grey Color")
    query4_join = """
    SELECT meta.title, media.rank, colors.hue
    FROM artifact_metadata meta
    JOIN artifact_media media ON meta.id = media.objectid
    JOIN artifact_colors colors ON meta.id = colors.objectid
    WHERE colors.hue = 'Grey'
    ORDER BY media.rank ASC
    LIMIT 10;

    """
    df4_join = run_query(query4_join)
    if not df4_join.empty:
        st.dataframe(df4_join)
    else:
        st.info("No artifacts with Grey color found")

    # Query 5: Artifacts per classification with avg media count
    st.subheader("5. Artifacts per Classification with Average Media Count")
    query5_join = """
    SELECT 
        meta.classification,
        COUNT(*) as artifact_count,
        AVG(media.mediacount) as avg_media_count
    FROM artifact_metadata meta
    JOIN artifact_media media ON meta.id = media.objectid
    WHERE meta.classification IS NOT NULL AND TRIM(meta.classification) != ''
    GROUP BY meta.classification
    ORDER BY artifact_count DESC;
    """
    df5_join = run_query(query5_join)
    if not df5_join.empty:
        st.dataframe(df5_join)
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(df5_join.set_index('classification')['artifact_count'])
        with col2:
            st.bar_chart(df5_join.set_index('classification')['avg_media_count'])
    else:
        st.info("No classification data available")

# Add debug section to check database connection
with st.sidebar:
    st.header("🔧 Database Info")
    if st.button("Check Database Connection"):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                st.write("Available tables:")
                st.dataframe(tables)
                
                # Show sample data from each table
                for table in tables['name']:
                    sample = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 1;", conn)
                    st.write(f"Sample from {table}:")
                    st.dataframe(sample)
                    
        except Exception as e:
            st.error(f"Database connection failed: {e}")

with tab5:
    st.subheader("📌 Classification-Based Artifact Explorer")
    st.markdown("Select a classification, fetch data from the API, store it in SQL, and run insightful queries.")

    # Dropdown for classification
    classification = st.selectbox(
        "Select Artifact Classification",
        ["Coins", "Paintings", "Scriptures", "Jewellery", "Drawings"]
    )

    # Simulated data fetch (replace with real API logic)
    def fetch_classification_data(classification):
        return pd.DataFrame({
            "title": [f"{classification} Artifact {i}" for i in range(1, 2501)],
            "classification": [classification]*2500,
            "culture": ["Byzantine"]*2500,
            "period": ["16th Century"]*2500
        })

    # Session state to persist data
    if "fetched_df" not in st.session_state:
        st.session_state.fetched_df = pd.DataFrame()

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Collect Data"):
            st.session_state.fetched_df = fetch_classification_data(classification)
            st.success(f"Collected {len(st.session_state.fetched_df)} records for {classification}.")

    with col2:
        if st.button("Show Data"):
            if not st.session_state.fetched_df.empty:
                st.dataframe(st.session_state.fetched_df)
            else:
                st.warning("No data collected yet.")

    with col3:
        if st.button("Insert into SQL"):
            if not st.session_state.fetched_df.empty:
                try:
                    with sqlite3.connect(DB_PATH) as conn:
                        st.session_state.fetched_df.to_sql("artifact_classification", conn, if_exists="append", index=False)
                    st.success("Data inserted into SQL successfully.")
                except Exception as e:
                    st.error(f"Insertion failed: {e}")
            else:
                st.warning("No data to insert.")

    # Query & Visualization Section
    st.markdown("---")
    st.subheader("🔍 Query & Visualization")

    query_options = {
        "Artifacts from 1500–1600": """
            SELECT meta.title, media.datebegin, media.dateend
            FROM artifact_metadata meta
            JOIN artifact_media media ON meta.id = media.objectid
            WHERE media.datebegin <= 1600 AND media.dateend >= 1500;
        """,
        "Top 10 Ranked Artifacts with Hue 'Grey'": """
            SELECT meta.title, media.rank, colors.hue
            FROM artifact_metadata meta
            JOIN artifact_media media ON meta.id = media.objectid
            JOIN artifact_colors colors ON meta.id = colors.objectid
            WHERE colors.hue = 'Grey'
            ORDER BY media.rank ASC
            LIMIT 10;
        """,
        "Average Coverage by Hue": """
            SELECT hue, AVG(percent) AS avg_coverage
            FROM artifact_colors
            WHERE hue IS NOT NULL AND TRIM(hue) != ''
            GROUP BY hue
            ORDER BY avg_coverage DESC;
        """
    }

    selected_query = st.selectbox("Choose a Query", list(query_options.keys()))

    if st.button("Run Query"):
        result_df = run_query(query_options[selected_query])
        if not result_df.empty:
            st.dataframe(result_df)
            if selected_query == "Average Coverage by Hue":
                st.bar_chart(result_df.set_index("hue"))
        else:
            st.warning("No results found.")


