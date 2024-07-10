import streamlit as st
import pandas as pd
import wikipedia
import json
import re

# Thiết lập ngôn ngữ Wikipedia
wikipedia.set_lang("vi")

# Bảng tra cứu chữ cái và số tương ứng theo bảng chữ cái tiếng Việt
char_to_num = {
    'A': 1, 'Ă': 2, 'Â': 3, 'B': 4, 'C': 5, 'D': 6, 'Đ': 7, 'E': 8, 'Ê': 9, 'G': 10,
    'H': 11, 'I': 12, 'K': 13, 'L': 14, 'M': 15, 'N': 16, 'O': 17, 'Ô': 18, 'Ơ': 19,
    'P': 20, 'Q': 21, 'R': 22, 'S': 23, 'T': 24, 'U': 25, 'Ư': 26, 'V': 27, 'X': 28, 'Y': 29
}

# Hàm để xử lý nội dung trước khi hiển thị
def format_content(content):
    cleaned_content = re.sub(r'==.*?==', '', content)
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_content)
    lines = cleaned_text.split("\n")
    cleaned_lines = [line.strip() for line in lines]
    formatted_content = "\n\n".join(cleaned_lines)
    return formatted_content

# Hàm để chuyển các ký tự thành số dựa trên bảng tra cứu và giới hạn số tối đa là 4
def chars_to_nums(s):
    return ''.join(str((char_to_num.get(char.upper(), 0) % 4) + 1) for char in s if char.upper() in char_to_num)

# Hàm để tạo ID từ tiêu đề và chủ đề
def create_id(title, topic):
    # Lấy các ký tự đầu của các từ trong title và topic
    title_abbr = ''.join([word[0] for word in title.split() if word])
    topic_abbr = ''.join([word[0] for word in topic.split() if word])
    # Chuyển các ký tự thành số và giới hạn số tối đa là 4
    title_num = chars_to_nums(title_abbr)
    topic_num = chars_to_nums(topic_abbr)
    # Kết hợp các số với nhau bằng dấu gạch dưới
    article_id = f'uit_{topic_num}_{title_num}'
    return article_id

# Hàm để tách câu từ tóm tắt, tính cả dấu ...
def split_sentences(text):
    # Thay thế dấu ba chấm bằng một ký tự đặc biệt tạm thời
    text = text.replace('...', '§§§')
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!|。|！|？)\s+', text)
    # Khôi phục dấu ba chấm
    sentences = [sentence.replace('§§§', '...') for sentence in sentences]
    return sentences

# Hàm để lấy thông tin từ Wikipedia dựa trên tiêu đề và index
def wikipedia_scrape(title_input, index, filename):
    try:
        # Lấy trang Wikipedia tương ứng với tiêu đề nhập vào
        page = wikipedia.page(title_input)
        title = page.title
        # Lấy tóm tắt và liên kết của trang Wikipedia
        summary = wikipedia.summary(title_input, sentences=10)
        format_summary = format_content(summary)
        url = page.url
        # Tạo ID từ tiêu đề và chủ đề
        topic = filename.split(".")[0]
        article_id = create_id(title, topic)
        # Tạo danh sách câu từ tóm tắt
        sentences = split_sentences(format_summary)
        return {"ID": article_id, "Title": title, "Topic": topic, "Summary": format_summary, "Sentences": sentences, "URL": url}
    except wikipedia.exceptions.DisambiguationError as e:
        return None
    except wikipedia.exceptions.PageError as e:
        return None

@st.cache
def convert_df_to_csv(df):
    # Chuyển DataFrame thành dữ liệu CSV và mã hóa UTF-8
    return df.to_csv(index=False).encode("utf-8")

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
            if title:  # Kiểm tra tiêu đề không trống
                article_info = wikipedia_scrape(title, index, uploaded_file.name)
                if article_info:
                    articles_info.append(article_info)
            else:
                st.warning(f"Dòng {index + 1}: Tiêu đề trống")

        # Kiểm tra nếu không có thông tin bài viết nào được thu thập
        if not articles_info:
            st.error("Không có bài viết nào được thu thập từ Wikipedia.")

        else:
            # Tạo DataFrame từ thông tin bài viết
            df = pd.DataFrame(articles_info)

            # Hiển thị DataFrame trước khi chọn các tiêu đề từ checkbox
            st.subheader("Danh sách bài viết từ Wikipedia:")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Tạo CSV từ DataFrame và tải xuống
            csv = convert_df_to_csv(df)
            csv_filename = "uit_" + uploaded_file.name.split(".")[0] + ".csv"
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=csv_filename,
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
