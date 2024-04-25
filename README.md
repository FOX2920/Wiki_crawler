# Wikipedia Scraper

## Overview
This Python application allows users to scrape Wikipedia articles. It provides a simple web interface built with Streamlit, where users can input a topic of interest and retrieve information from the corresponding Wikipedia page. The retrieved information includes the article title, summary, URL, and linked articles. Additionally, the application generates a word cloud based on the content of the article and displays the summary broken down into sentences.

## Installation
To run this application locally, follow these steps:

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/FOX2920/Wiki_crawler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd path/to/Wiki_crawler
    ```

3. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    streamlit run app.py
    ```

## Usage
Once the application is running, users can interact with it through their web browser. Here's how to use it:

1. Enter the topic you want to search for on Wikipedia in the text input field.
2. Click the "Start scraping" button to initiate the scraping process.
3. The application will display the article title, URL, linked articles, word cloud, and summary of the Wikipedia page.
4. Users can explore the summary further by viewing the sentences in a DataFrame.

## Dependencies
- wikipedia
- streamlit
- pandas
- nltk
- matplotlib
- wordcloud

## Demo
You can try out a live demo of this application [here](https://wikicrawler.streamlit.app/).

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
