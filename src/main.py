from dotenv import load_dotenv
import openai
import os

import scraper, graph_builder, database

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    articles = scraper.fetch_articles()

    conn = database.get_connection()
    cursor = conn.cursor()

    for article_data in [scraper.scrape_article(a) for a in articles]:
        print(f"Processing: {article_data['title']}")
        article_id = database.insert_article(cursor, article_data['title'], article_data['date'], article_data['content'], article_data['url'])

        for ent in article_data['entities']:
            database.insert_entity(cursor, article_id, ent[0], ent[1])

        # Skip relationship inference for now (but you can plug in GPT/NetworkX here)
        relationships = []

        for rel in relationships:
            database.insert_relationship(cursor, article_id, rel['entity_1'], rel['relationship'], rel['entity_2'])

        graph_builder.build_and_plot_graph(article_data['title'], relationships)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
