import streamlit as st
import pandas as pd
import wikipedia
import json

# Thiết lập ngôn ngữ Wikipedia
wikipedia.set_lang("vi")

# Hàm để xử lý nội dung trước khi hiển thị
def format_content(content):
    # Tách nội dung thành các đoạn
    paragraphs = content.split('\n')
    # Thêm một dòng trống sau mỗi đoạn
    formatted_content = '\n\n'.join(paragraphs)
    return formatted_content

# Hàm để tạo ID từ tiêu đề và index
def create_id(title, filename):
    # Lấy chữ cái đầu của từng từ trong tiêu đề
    initials = ''.join(word[0] for word in title.split())

    name = ''.join(word[0] for word in filename.split())
    # Kết hợp với index
    article_id = initials + '_' + name
    # Thêm 'uit_' vào đầu ID
    return 'uit_' + article_id

# Hàm để lấy thông tin từ Wikipedia dựa trên tiêu đề và index
def wikipediaScrap(title_input, filename):
    try:
        # Lấy trang Wikipedia tương ứng với tiêu đề nhập vào
        page = wikipedia.page(title_input)
        title = page.title
        # Lấy tóm tắt và liên kết của trang Wikipedia
        summary = wikipedia.summary(title_input, sentences=10)
        format_summary = format_content(summary)
        url = page.url
        # Tạo ID từ tiêu đề và index
        article_id = create_id(title, filename)
        return {"ID": article_id, "Title": title, "Topic": filename.split(".")[0],"Summary": format_summary, "URL": url}
    except wikipedia.exceptions.DisambiguationError as e:
        return None
    except wikipedia.exceptions.PageError as e:
        return None
    
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


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
        for index, title in enumerate(titles):
            title = title.strip()
            article_info = wikipediaScrap(title, uploaded_file.name)
            if article_info:
                articles_info.append(article_info)

        # Tạo DataFrame từ thông tin bài viết
        df = pd.DataFrame(articles_info)

        # Hiển thị DataFrame trước khi chọn các tiêu đề từ checkbox
        st.subheader("Danh sách bài viết từ Wikipedia:")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = convert_df(df)
        name = ''.join(word[0] for word in uploaded_file.name.split())
        csv_filename = "uit_" + name + ".csv"
        st.download_button(
            label="Download",
            data=csv,
            file_name= csv_filename,
            mime="text/csv",
        )

        
        

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
