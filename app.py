import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import zipfile
import io
import os

from helper import most_commonwords, montly_data, daily_data

# Basic page setup - just making it look decent
# CHANGED: Collapse sidebar by default to fix mobile overlap issue
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"  # Changed from "expanded" to prevent mobile overlap
)

# Some custom CSS to make things look nicer
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem 1rem;
    }
    
    /* Hero section styling */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem;
        margin: 2rem 0;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: var(--text-color-secondary);
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* Card styling for stats */
    .stat-card {
        background: var(--background-color);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: var(--primary-color);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-color-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    /* Chart container styling */
    .chart-container {
        background: var(--background-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    /* Sidebar improvements */
    [data-testid="stSidebar"] {
        background: var(--sidebar-background-color);
    }
    
    /* Better spacing */
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .stat-value {
            font-size: 2rem;
        }
    }
    
    /* CHANGED: Ensure sidebar toggle button is easily accessible on mobile */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            z-index: 999;
            position: fixed;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def decode_bytes(raw_bytes):
    """Tries different encodings since Android and iPhone export chats differently"""
    for encoding in ["utf-8", "utf-16", "latin-1"]:
        try:
            return raw_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    st.error("❌ Unable to decode chat file (unsupported encoding)")
    st.stop()

def get_image_path(filename):
    """Tries to find the image file, works with both relative and absolute paths"""
    relative_path = filename
    if os.path.exists(relative_path):
        return relative_path
    return filename

# Sidebar stuff
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='font-size: 2rem; margin: 0;'>💬</h1>
            <h2 style='font-size: 1.5rem; margin: 0.5rem 0;'>Chat Analyzer</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📤 Upload Chat")
    st.caption("Upload your WhatsApp chat export (.txt or .zip)")
    uploaded_file = st.file_uploader(
        "Choose WhatsApp chat file",
        type=["txt", "zip"],
        label_visibility="collapsed",
        help="Export your WhatsApp chat without media from WhatsApp settings"
    )
    
    st.markdown("---")
    
    if uploaded_file is not None:
        st.markdown("### 👤 Analysis Options")
        st.info("📊 Processing your chat file...")

# Main page content

# Show welcome screen when no file is uploaded yet
if uploaded_file is None:
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">WhatsApp Chat Analyzer</h1>
            <p class="hero-subtitle">
                Get insights from your WhatsApp chats<br>
                See your messaging patterns, most used words, emojis, and more
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Show intro images if they exist
    col1, col2 = st.columns([2, 1])
    with col1:
        try:
            img1_path = get_image_path("intro_img2.jpeg")
            if os.path.exists(img1_path):
                st.image(img1_path, use_container_width=True)
        except:
            pass
    
    with col2:
        try:
            img2_path = get_image_path("intro_img1.jpeg")
            if os.path.exists(img2_path):
                st.image(img2_path, use_container_width=True)
        except:
            pass
    
    # Quick instructions
    st.markdown("""
        <div style='text-align: center; padding: 2rem; margin: 2rem 0; background: var(--background-color); border-radius: 12px; border: 1px solid var(--border-color);'>
            <h3 style='margin-bottom: 1rem;'>📂 How to Get Started</h3>
            <ol style='text-align: left; display: inline-block; max-width: 500px;'>
                <li>Open WhatsApp on your phone</li>
                <li>Go to the chat you want to analyze</li>
                <li>Tap the three dots → Export Chat</li>
                <li>Select "Without Media" (makes the file smaller)</li>
                <li>Upload the file using the sidebar on the left</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# Process the uploaded file
if uploaded_file is not None:
    with st.spinner("🔄 Processing your chat file..."):
        # Handle zip files (iPhone exports sometimes come as zip)
        if uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as z:
                txt_file = None
                for name in z.namelist():
                    if name.endswith(".txt"):
                        txt_file = name
                        break

                if txt_file is None:
                    st.error("❌ No WhatsApp chat .txt file found inside ZIP")
                    st.stop()

                raw_bytes = z.read(txt_file)
                data = decode_bytes(raw_bytes)

        # Regular txt file (most common)
        else:
            raw_bytes = uploaded_file.getvalue()
            data = decode_bytes(raw_bytes)

        # Clean up the data
        df = preprocessor.preprocess(data)
        
        st.success(f"✅ Successfully loaded {len(df)} messages!")

    # Get list of users for the dropdown
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    # Update sidebar with user selection
    with st.sidebar:
        st.markdown("---")
        selected_user = st.selectbox(
            "👤 Analyze for:",
            user_list,
            help="Select a user to analyze their individual stats, or 'Overall' for group analysis"
        )
        
        st.markdown("---")
        
        analyze_button = st.button(
            "🚀 Show Analysis",
            type="primary",
            use_container_width=True,
            help="Click to generate comprehensive chat analysis"
        )

    # Show the analysis when button is clicked
    if analyze_button:
        # Get basic stats
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        # Display stats in cards
        st.markdown("""
            <div class="section-header">📊 Overview Statistics</div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">💬 Total Messages</div>
                    <div class="stat-value">{num_messages:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">📝 Total Words</div>
                    <div class="stat-value">{words:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">🖼️ Media Shared</div>
                    <div class="stat-value">{num_media_messages:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">🔗 Links Shared</div>
                    <div class="stat-value">{num_links:,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Show most active users only when analyzing overall group stats
        if selected_user == "Overall":
            st.markdown("""
                <div class="section-header">👥 Most Active Users</div>
            """, unsafe_allow_html=True)
            
            x, new_df = helper.most_busy_users(df)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                fig, ax = plt.subplots(figsize=(10, 6))
                colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
                bars = ax.bar(x.index, x.values, color=colors)
                ax.set_xlabel('Users', fontsize=12, fontweight='bold')
                ax.set_ylabel('Message Count', fontsize=12, fontweight='bold')
                ax.set_title('Messages by User', fontsize=14, fontweight='bold', pad=20)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                st.pyplot(fig)
            
            with col2:
                st.markdown("### 📈 User Contribution")
                st.dataframe(
                    new_df,
                    use_container_width=True,
                    hide_index=True
                )

        # Word cloud visualization
        st.markdown("""
            <div class="section-header">☁️ Word Cloud</div>
        """, unsafe_allow_html=True)
        
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout()
        st.pyplot(fig)

        # Most common words
        st.markdown("""
            <div class="section-header">📚 Most Used Words</div>
        """, unsafe_allow_html=True)
        
        most_common_df = helper.most_commonwords(selected_user, df)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = plt.cm.plasma(np.linspace(0, 1, len(most_common_df)))
            bars = ax.barh(most_common_df[0], most_common_df[1], color=colors)
            ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_ylabel('Words', fontsize=12, fontweight='bold')
            ax.set_title('Top 20 Most Common Words', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("### 📊 Word Frequency Table")
            st.dataframe(
                most_common_df,
                use_container_width=True,
                hide_index=True
            )

        # Emoji analysis
        st.markdown("""
            <div class="section-header">😊 Most Used Emojis</div>
        """, unsafe_allow_html=True)
        
        emoji_func = helper.commonly_used_emojis(selected_user, df)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Emoji Frequency")
            st.dataframe(
                emoji_func.head(10),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 8))
            top_emojis = emoji_func.head(10)
            colors = plt.cm.Set3(np.linspace(0, 1, len(top_emojis)))
            ax.pie(
                top_emojis[1],
                labels=top_emojis[0],
                autopct="%1.1f%%",
                colors=colors,
                startangle=90
            )
            ax.set_title('Top 10 Emojis Distribution', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)

        # Monthly timeline
        st.markdown("""
            <div class="section-header">📅 Monthly Timeline</div>
        """, unsafe_allow_html=True)
        
        monthly_Func = helper.montly_data(selected_user, df)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Monthly Data")
            st.dataframe(
                monthly_Func,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(monthly_Func['time'], monthly_Func['message'], 
                   marker='o', linewidth=2, markersize=8, color='#667eea')
            ax.fill_between(monthly_Func['time'], monthly_Func['message'], alpha=0.3, color='#667eea')
            ax.set_xlabel('Month-Year', fontsize=12, fontweight='bold')
            ax.set_ylabel('Message Count', fontsize=12, fontweight='bold')
            ax.set_title('Messages Over Time', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

        # Daily timeline
        st.markdown("""
            <div class="section-header">📆 Daily Timeline</div>
        """, unsafe_allow_html=True)
        
        daily_data_df = helper.daily_data(selected_user, df)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📊 Daily Data")
            # Only showing last 10 days to keep it readable
            st.dataframe(
                daily_data_df.tail(10),
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(daily_data_df['day-date'], daily_data_df['message'], 
                   marker='o', linewidth=2, markersize=4, color='#764ba2', alpha=0.7)
            ax.fill_between(range(len(daily_data_df)), daily_data_df['message'], 
                           alpha=0.3, color='#764ba2')
            ax.set_xlabel('Day', fontsize=12, fontweight='bold')
            ax.set_ylabel('Message Count', fontsize=12, fontweight='bold')
            ax.set_title('Daily Message Activity', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

        # Activity patterns
        st.markdown("""
            <div class="section-header">🗓️ Activity Map</div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Most Active Days")
            active_day = helper.week_activity(selected_user, df)
            
            st.dataframe(
                active_day.reset_index(),
                use_container_width=True,
                hide_index=True
            )
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = plt.cm.coolwarm(np.linspace(0, 1, len(active_day)))
            bars = ax.bar(active_day.index, active_day.values, color=colors)
            ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
            ax.set_ylabel('Message Count', fontsize=12, fontweight='bold')
            ax.set_title('Weekly Activity Pattern', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("### 📊 Most Active Months")
            active_months = helper.month_activity(selected_user, df)
            
            st.dataframe(
                active_months.reset_index(),
                use_container_width=True,
                hide_index=True
            )
            
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = plt.cm.spring(np.linspace(0, 1, len(active_months)))
            bars = ax.bar(active_months.index, active_months.values, color=colors)
            ax.set_xlabel('Month', fontsize=12, fontweight='bold')
            ax.set_ylabel('Message Count', fontsize=12, fontweight='bold')
            ax.set_title('Monthly Activity Pattern', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)

        # Hourly heatmap
        st.markdown("""
            <div class="section-header">⏰ Hourly Activity Heatmap</div>
        """, unsafe_allow_html=True)
        
        heat_map = helper.hourly_activity(selected_user, df)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(
            heat_map,
            annot=True,
            fmt='.0f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Message Count'},
            linewidths=0.5,
            linecolor='gray'
        )
        ax.set_xlabel('Hour Period', fontsize=12, fontweight='bold')
        ax.set_ylabel('Day of Week', fontsize=12, fontweight='bold')
        ax.set_title('Hourly Activity Heatmap', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; padding: 2rem; color: var(--text-color-secondary);'>
                <p>✨ Analysis complete! Explore the insights above.</p>
            </div>
        """, unsafe_allow_html=True)
