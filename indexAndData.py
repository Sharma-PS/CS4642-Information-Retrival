import codecs
import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()

client = Elasticsearch(hosts=["http://localhost"], http_auth=("elastic", os.getenv('ELASTCSEARCH_PASSWORD')), port=os.getenv('ELASTCSEARCH_PORT'))
INDEX = os.getenv('ELASTCSEARCH_INDEX')

# Creating index if not manually created
def createIndex():
    # Create an index
    res = client.indices.create(index=INDEX)

     # Read mappings from a JSON file
    with codecs.open('analyzers/mapping_file.json', 'r', encoding="utf-8") as file:
        mappings = json.load(file)
    
    # Read a settings from a JSON file
    with codecs.open('analyzers/settings.json', 'r', encoding="utf-8") as settings_file:
        settings = settings_file.read()

    # Add settings to the index
    client.indices.close(index=INDEX)
    client.indices.put_settings(index=INDEX, body=settings, pretty=True)
    client.indices.open(index=INDEX)

    # Add mappings to the index
    client.indices.put_mapping(index=INDEX, body=mappings, pretty=True)
    
    print(res)

def read_all_songs():
    with open('corpus/Tamil New Songs Lyrics_MetapourAdded.json', 'r', encoding='utf-8-sig') as f:
        all_songs = json.loads("[" + f.read().replace("}\n{", "},\n{") + "]")
        res_list = [i for n, i in enumerate(all_songs) if i not in all_songs[n + 1:]]

        return res_list

def genData(song_array):
    for song in song_array:
        # Fields-capturing
        title = song.get("பாடல்", None)
        movie = song.get("படம்",None)
        year = song.get("வருடம்", None)
        composer = song.get("இசை", None)
        lyricist = song.get("பாடலாசிரியர்", None)
        singers = song.get("பாடகர்", None)
        lyrics = song.get("வரி", None)
        metaphorType = song.get("உருவகம்", None)
        source = song.get("உவமானம்", None)
        target = song.get("உவமேயம்", None)
        metaphor = song.get("விளக்கம்", None)

        yield {
            "_index": INDEX,
            "_source": {
                "பாடல்": title,
                "படம்": movie,
                "வருடம்": year,
                "இசை": composer,
                "பாடலாசிரியர்": lyricist,
                "பாடகர்": singers,
                "வரி": lyrics,
                "உருவகம்": metaphorType,
                "உவமானம்": source,
                "உவமேயம்": target,
                "விளக்கம்": metaphor
            },
        }

createIndex()
all_songs = read_all_songs()
helpers.bulk(client, genData(all_songs))