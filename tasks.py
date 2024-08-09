from robocorp.tasks import task
from robocorp import workitems
from src.Latimes import LatimesExtractor
from src.Logging import Log_Message

@task
def news_extract():
    log_message  = Log_Message()
    log_message.log_info("Process started")
    max_news_count = 50
    
    for item in workitems.inputs:
        phrase = item.payload["phrase"]
        sort_by = item.payload["sort_by"]
        history = item.payload["history"]
        log_message.log_info(f"Processing {phrase}")
        extractor = LatimesExtractor(max_news_count, phrase=phrase, sort_by=sort_by, date=history)
        extractor.open_specific_browser()
        news_count = extractor.search_by_phrase()
        if news_count > 0:
            extractor.get_page_news()
        extractor.close_browser()
