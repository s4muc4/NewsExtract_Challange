from robocorp.tasks import task
from robocorp import workitems
from src.Latimes import LatimesExtractor

@task
def news_extract():

    for item in workitems.inputs:
        phrase = item.payload["phrase"]
        topic = item.payload["topic"]
        history = item.payload["history"]

        print("Searching phrase ("+phrase+") in topic ("+topic+") since ("+str(history)+") months")
        extractor = LatimesExtractor()
        extractor.open_specific_browser()
        news_count = extractor.search_by_phrase(phrase)
        if news_count > 0:
            extractor.get_page_news()
        extractor.close_browser()
