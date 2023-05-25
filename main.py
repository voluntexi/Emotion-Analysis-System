import streamlit as st
from st_pages import Page, show_pages, add_page_title
show_pages(
    [
        Page("index.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("getdata.py", "Get Data", ""),
        # The pages appear in the order you pass them
        Page("dataAnalysis.py", "Data Analysis", ""),
        Page("excelUpload.py", "Excel Upload", "")
        ])
add_page_title()



