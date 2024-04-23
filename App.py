import wikipedia
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
def wikipediaScrap(article_name, wikipedia_language="en"):
    wikipedia.set_lang(wikipedia_language)
    et_page = wikipedia.page(article_name)
    title = et_page.title
    content = et_page.content
    page_url = et_page.url
    linked_pages = et_page.links
    text = content

    # Create and generate a word cloud image:
    wordcloud = WordCloud(font_path="HelveticaWorld-Regular.ttf").generate(text)

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

    return title, content, page_url, "\n".join(linked_pages)

st.title("Wikipedia Article Scrape | Data Science Dojo")

article_name = st.text_input("Enter the name of wikipedia article")
wikipedia_language = st.selectbox("Select Language", ["en - English", "vi - Tiếng Việt"])

if st.button("Start scraping"):
    title, content, url, linked_pages = wikipediaScrap(article_name, wikipedia_language.split(" - ")[0])
    st.subheader("About")
    st.text("Article title:")
    st.write(title)
    st.text("Article URL:")
    st.write(url)
    st.subheader("Content")
    st.write(content)
    st.subheader("Linked Articles")
    st.write(linked_pages)
