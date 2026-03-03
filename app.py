import streamlit as st
from storage import load_items, save_items
from scanner import run_scan

st.set_page_config(page_title="DTI Fashion Ledger", layout="wide")

st.title("🏦 DTI Cooperative Fashion Ledger")

tab = st.sidebar.radio(
    "Navigate",
    ["Browse Wardrobe", "Upload & Scan"]
)

# ==========================
# Browse Tab
# ==========================
if tab == "Browse Wardrobe":
    st.subheader("👗 Your Items")

    items = load_items()

    if not items:
        st.info("No items logged yet.")
    else:
        for item in items:
            st.markdown(f"""
            **{item['name']}**
            - Type: {item['item_type']}
            - Platform: {item['platform']}
            - Acquisition: {item['acquisition_type']}
            - Price: {item['price']}
            ---
            """)

# ==========================
# Upload & Scan Tab
# ==========================
elif tab == "Upload & Scan":
    st.subheader("📸 Upload Screenshot")

    uploaded_file = st.file_uploader(
        "Upload DTI Screenshot",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        with open("temp.png", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="Uploaded Screenshot")

        if st.button("Run Scan"):
            new_items = run_scan("temp.png")

            if new_items:
                save_items(new_items)
                st.success(f"{len(new_items)} items added!")
            else:
                st.warning("No items detected.")
