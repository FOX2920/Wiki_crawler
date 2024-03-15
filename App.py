import wikipedia
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def wikipediaScrap(article_name):
    wikipedia.set_lang("vi")  # Set language to Vietnamese
    try:
        page = wikipedia.page(article_name)
        title = page.title
        content = page.content
        page_url = page.url
        linked_pages = page.links

        # Generate WordCloud
        wordcloud = WordCloud(font_path="HelveticaWorld-Regular.ttf").generate(content)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Display WordCloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()

        return title, content, page_url, "\n".join(linked_pages)
    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"Xin lỗi, có quá nhiều kết quả phù hợp cho '{article_name}'. Vui lòng cung cấp thông tin chính xác hơn.")

st.title("Wikipedia Article Scrape")
article_name = st.text_input("Nhập tên bài viết trên Wikipedia", "")
if st.button("Bắt đầu lấy thông tin"):
    if article_name:
        title, content, url, linked = wikipediaScrap(article_name)
        st.subheader("Tiêu đề:")
        st.write(title)
        st.subheader("Nội dung:")
        st.write(content)
        st.subheader("URL:")
        st.write(url)
        st.subheader("Các bài viết liên kết:")
        st.write(linked)
    else:
        st.warning("Vui lòng nhập tên bài viết trước khi bắt đầu lấy thông tin.")
