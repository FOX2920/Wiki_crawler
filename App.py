import gradio as gr
import wikipedia
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

def wikipediaScrap(article_name, wikipedia_language="vi"):
    wikipedia_language = wikipedia_language.split(" - ")[0]
  
    if wikipedia_language:
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
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    return title, content, page_url, "\n".join(linked_pages), plt

css = """
footer {display:none !important}
.output-markdown{display:none !important}
footer {visibility: hidden} 
.gr-button-lg {
    z-index: 14;
    width: 113px;
    height: 30px;
    left: 0px;
    top: 0px;
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
.gr-button-lg:hover{
    z-index: 14;
    width: 113px;
    height: 30px;
    left: 0px;
    top: 0px;
    padding: 0px;
    cursor: pointer !important; 
    background: none rgb(66, 133, 244) !important;
    border: none !important;
    text-align: center !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: rgb(255, 255, 255) !important;
    line-height: 1 !important;
    border-radius: 6px !important;
    transition: box-shadow 200ms ease 0s, background 200ms ease 0s !important;
    box-shadow: rgb(0 0 0 / 23%) 0px 1px 7px 0px !important;
}
#component-14 textarea[data-testid="textbox"] { height: 178px !important}
#component-17 textarea[data-testid="textbox"] { height: 178px !important}
#component-21 textarea[data-testid="textbox"] { height: 178px !important}
#component-20 tr:hover{
    background-color: rgb(229,225,255) !important;
}
.output-image {max-height: 11rem !important;}
.output-image img {max-height: 17rem !important;}
.hover\:bg-orange-50:hover {
    --tw-bg-opacity: 1 !important;
    background-color: rgb(229,225,255) !important;
}
"""

# Lấy danh sách ngôn ngữ Wikipedia
ini_dict = wikipedia.languages()

# Chuyển đổi từ điển thành danh sách các keys và values
keys = []
values = []
language = []

items = ini_dict.items()
for item in items:
    keys.append(item[0]), values.append(item[1])
    language.append(item[0] + " - " + item[1])

# Thêm lựa chọn tiếng Việt vào danh sách ngôn ngữ
language.append("vi - Vietnamese")

with gr.Blocks(title="Wikipedia Article Scrape | Data Science Dojo", css=css) as demo:
    with gr.Row():
        inp = gr.Textbox(placeholder="Nhập tên bài viết trên Wikipedia", label="Tên bài viết trên Wikipedia")
        lan = gr.Dropdown(label="Chọn Ngôn ngữ", choices=language, value="vi - Vietnamese", interactive=True)

    btn = gr.Button("Bắt đầu thu thập", elem_id="dsd_button")
    with gr.Row():
        with gr.Column():
            gr.Markdown("""## Thông tin""")
            title = gr.Textbox(label="Tiêu đề bài viết")
            url = gr.Textbox(label="Đường dẫn bài viết")
        with gr.Column():
            gr.Markdown("""## Wordcloud""")
            wordcloud = gr.Plot()
    gr.Markdown("""### Nội dung""")
    with gr.Row():
        content = gr.Textbox(label="Nội dung")
    gr.Markdown("""### Các Bài viết liên kết""")
    with gr.Row():
        linked = gr.Textbox(label="Các Bài viết liên kết")
    btn.click(fn=wikipediaScrap, inputs=[inp, lan], outputs=[title, content, url, linked, wordcloud])
    with gr.Row():
        gr.Examples(examples=[["Tháp Eiffel", "vi - Vietnamese"], ["Đại học Harvard", "vi - Vietnamese"]],
                    fn=wikipediaScrap, inputs=[inp, lan], outputs=[title, content, url, linked, wordcloud],
                    cache_examples=True)

demo.launch(share=True)
