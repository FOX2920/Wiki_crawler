import wikipedia
import streamlit as st
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('punkt')
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
# Thiết lập ngôn ngữ Wikipedia
wikipedia.set_lang("vi")

# Trong hàm wikipediaScrap(), chuyển linked_pages thành DataFrame
def wikipediaScrap(title_input):
    try:
        # Lấy trang Wikipedia tương ứng với tiêu đề nhập vào
        page = wikipedia.page(title_input)
        title =page.title
        # Lấy tóm tắt và liên kết của trang Wikipedia
        summary = wikipedia.summary(title_input, sentences=10)
        url = page.url
        linked_pages =page.links
        # Chuyển list thành DataFrame
        linked_df = pd.DataFrame(linked_pages, columns=["Linked Articles"])
        return title, summary, url, linked_df
    except wikipedia.exceptions.DisambiguationError as e:
        st.error("Có nhiều kết quả phù hợp với tiêu đề bạn nhập. Hãy cố gắng chính xác hơn!")
        return None, None
    except wikipedia.exceptions.PageError as e:
        st.error("Không tìm thấy trang Wikipedia cho tiêu đề bạn nhập.")
        return None, None

# Hàm để xử lý nội dung trước khi hiển thị
def format_content(content):
    # Tách nội dung thành các đoạn
    paragraphs = content.split('\n')
    # Thêm một dòng trống sau mỗi đoạn
    formatted_content = '\n\n'.join(paragraphs)
    return formatted_content

def main():
    # Tiêu đề của ứng dụng
    st.title("Ứng dụng Wikipedia Tiếng Việt")
    
    # Hộp nhập tiêu đề từ người dùng
    title_input = st.text_input("Nhập tiêu đề bạn muốn tìm kiếm trên Wikipedia")
    
    # Trong phần hiển thị
    if st.button("Start scraping"):
        title, content, url, linked_df = wikipediaScrap(title_input)
        st.subheader("About")
        c2 = st.container(border=True)
        with c2:
            plot_col, title_col = st.columns(2)
            with title_col:
                st.subheader("Article title:")
                st.write(title)
                st.subheader("Article URL:")
                st.write(url)
                st.subheader("Linked Articles:")
                st.dataframe(linked_df, height=200, use_container_width=True)  # Hiển thị DataFrame thay vì hiển thị list
            with plot_col:
                # Create and generate a word cloud image:
                text = content
                st.subheader("WordCloud")
                wordcloud = WordCloud(font_path="HelveticaWorld-Regular.ttf").generate(text)
                # Display the generated image:
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                st.pyplot() 
        st.subheader("Content")
        c3 = st.container(border=True)
        with c3:
            content_col, df_col = st.columns(2)
            with  content_col:
                st.subheader("Summary:")
                # Xử lý nội dung trước khi hiển thị
                formatted_content = format_content(content)
                st.text_area('',value=formatted_content, height=500, max_chars= 500)
            with df_col:
                # Chia tóm tắt thành các câu
                sentences = nltk.sent_tokenize(content)
                
                # Tạo DataFrame từ các câu
                df = pd.DataFrame(sentences, columns=["Câu"])
                st.subheader("Các câu trong tóm tắt:")
                st.dataframe(df, height=500, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    main()
