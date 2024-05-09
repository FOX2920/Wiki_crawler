import streamlit as st
import pandas as pd
import wikipedia
import json
import uuid

# Thiết lập ngôn ngữ Wikipedia
wikipedia.set_lang("vi")


# Hàm để xử lý nội dung trước khi hiển thị
def format_content(content):
    # Tách nội dung thành các đoạn
    paragraphs = content.split('\n')
    # Thêm một dòng trống sau mỗi đoạn
    formatted_content = '\n\n'.join(paragraphs)
    return formatted_content

# Hàm để lấy thông tin từ Wikipedia dựa trên tiêu đề
def wikipediaScrap(title_input):
    try:
        # Lấy trang Wikipedia tương ứng với tiêu đề nhập vào
        page = wikipedia.page(title_input)
        title = page.title
        # Lấy tóm tắt và liên kết của trang Wikipedia
        summary = wikipedia.summary(title_input, sentences=10)
        format_summary = format_content(summary)
        url = page.url
        return {"ID": str(uuid.uuid4()), "Title": title, "Summary": format_summary, "URL": url}
    except wikipedia.exceptions.DisambiguationError as e:
        return None
    except wikipedia.exceptions.PageError as e:
        return None



# Ứng dụng Streamlit
def main():
    st.title("Ứng dụng crawl data wiki tiếng việt")

    # Upload file văn bản
    uploaded_file = st.file_uploader("Tải lên tệp văn bản (txt)", type=["txt"])

    if uploaded_file is not None:
        # Đọc nội dung của tệp văn bản
        file_contents = uploaded_file.getvalue().decode("utf-8")
        # Tách các dòng thành danh sách các tiêu đề
        titles = file_contents.split("\n")

        # Danh sách chứa thông tin các bài viết
        articles_info = []

        # Lặp qua từng tiêu đề và lấy thông tin từ Wikipedia
        for title in titles:
            title = title.strip()
            article_info = wikipediaScrap(title)
            if article_info:
                articles_info.append(article_info)

        # Tạo DataFrame từ thông tin bài viết
        df = pd.DataFrame(articles_info)

        # Hiển thị DataFrame trước khi chọn các tiêu đề từ checkbox
        st.subheader("Danh sách bài viết từ Wikipedia:")
        st.dataframe(df, use_container_width=True, hide_index = True)

        # Hiển thị selectbox để chọn một tiêu đề
        selected_title = st.selectbox("Chọn một tiêu đề:", df["Title"])

        # Lọc DataFrame theo tiêu đề được chọn
        selected_df = df[df["Title"] == selected_title]

        # Chuyển DataFrame thành JSON
        selected_json = selected_df.to_json(orient="records", lines=True)

        # Hiển thị JSON nếu có tiêu đề được chọn
        if selected_title:
            st.subheader("Dữ liệu JSON của bài viết được chọn:")
            st.json(json.loads(selected_json))

if __name__ == "__main__":
    main()
