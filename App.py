import wikipedia
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def wikipediaScrap(article_name, wikipedia_language="en"):
    wikipedia.set_lang(wikipedia_language)
    et_page = wikipedia.page(article_name)
    title = et_page.title
    content = et_page.content
    page_url = et_page.url
    linked_pages = et_page.links

    return title, content, page_url, "\n".join(linked_pages)

st.title("Wikipedia Article Crawler")
c1 = st.container(border=True)
with c1:
    article_name, wi_ln = st.columns(2)
    with article_name:
        article_name_input = st.text_input("Enter the name of wikipedia article")
    with wi_ln:
         ln = st.selectbox("Select Language", ["en - English", "vi - Tiếng Việt"])

if st.button("Start scraping"):
    title, content, url, linked_pages = wikipediaScrap(article_name_input, ln.split(" - ")[0])
    st.subheader("About")
    c2 = st.container(border=True)
    with c2:
        title_col, plot_col = st.columns(2)
        with title_col:
            st.text("Article title:")
            st.write(title)
            st.text("Article URL:")
            st.write(url)
        with plot_col:
            # Create and generate a word cloud image:
            text = content
            wordcloud = WordCloud(font_path="HelveticaWorld-Regular.ttf").generate(text)
            # Display the generated image:
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            st.pyplot() 
    st.subheader("Content")
    st.text_area('', value=content)
    st.subheader("Linked Articles")
    st.write(linked_pages)
