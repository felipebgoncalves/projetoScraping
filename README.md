# projetoScraping

Para rodar o web scraping

...bash
scrapy crawl mercadolivre -o ../../data/data.jsonl
...


Para rodar o PANDAS tem que dar o seguinte comando dentro da pasta SRC

...bash
python transformacao/main.py
...

Para rodar o Streamlit

...bash
streamlit run dashboard/app.py
...