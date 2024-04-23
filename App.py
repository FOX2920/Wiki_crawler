import streamlit as st
import wikipedia
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Function to scrape Wikipedia article and generate word cloud
def wikipediaScrap(article_name, wikipedia_language):
    # Set Wikipedia language
    wikipedia.set_lang(wikipedia_language)

    # Scrape Wikipedia page
    et_page = wikipedia.page(article_name)
    title = et_page.title
    content = et_page.content
    page_url = et_page.url
    linked_pages = et_page.links

    # Generate word cloud
    wordcloud = WordCloud(font_path="HelveticaWorld-Regular.ttf").generate(content)

    return title, content, page_url, "\n".join(linked_pages), wordcloud

# CSS styles
css = """
<style>
footer {display:none !important}
.stButton>button {
    z-index: 14;
    width: 113px;
    height: 30px;
    padding: 0px;
    cursor: pointer !important;
    background: none rgb(17, 20, 45) !important;
    border: none !important;
    text-align: center !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: rgb(255, 255, 255) !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    transition: box-shadow 200ms ease 0s, background 200ms ease 0s !important;
    box-shadow: none !important;
}
.stButton>button:hover{
    background: none rgb(66, 133, 244) !important;
    box-shadow: rgb(0 0 0 / 23%) 0px 1px 7px 0px !important;
}
.stTextArea {
    height: 178px !important;
}
.stPlotlyChart {
    max-height: 11rem !important;
}
.stMarkdown a {
    color: rgb(66, 133, 244) !important;
}
</style>
"""

# Streamlit app
st.markdown(css, unsafe_allow_html=True)

st.title("Wikipedia Article Scrape | Data Science Dojo")

article_name = st.text_input("Wikipedia article name", "")
wikipedia_language = st.selectbox("Select Language", ["en", "vi"])

if st.button("Start scraping"):
    if article_name:
        title, content, url, linked_pages, wordcloud = wikipediaScrap(article_name, wikipedia_language)

        st.subheader("About")
        st.text("Article title:")
        st.write(title)
        st.text("Article URL:")
        st.write(url)

        st.subheader("Content")
        st.textarea("Content", content)

        st.subheader("Linked Articles")
        st.textarea("Linked Articles", linked_pages)

        st.subheader("Wordcloud")
        st.image(wordcloud.to_array(), use_column_width=True)

# Examples
st.markdown("### Examples")
example_articles = [["Eiffel Tower", "en"], ["Eiffel tower", 'vi']]
for example in example_articles:
    if st.button(example[0]):
        article_name = example[0]
        wikipedia_language = example[1]
        title, content, url, linked_pages, wordcloud = wikipediaScrap(article_name, wikipedia_language)

        st.subheader("About")
        st.text("Article title:")
        st.write(title)
        st.text("Article URL:")
        st.write(url)

        st.subheader("Content")
        st.textarea("Content", content)

        st.subheader("Linked Articles")
        st.textarea("Linked Articles", linked_pages)

        st.subheader("Wordcloud")
        st.image(wordcloud.to_array(), use_column_width=True)
