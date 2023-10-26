from utils.web_crawler import crawler

new_crawler = crawler()
html_content = new_crawler.main_html_content

new_crawler._url_parser(html_content=html_content)