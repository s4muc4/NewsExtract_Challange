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
        data = item.payload["data"]
        phrase = data["phrase"]
        sort_by = data["sort_by"]
        history = data["history"]
        log_message.log_info(f"Processing {phrase}")
        extractor = LatimesExtractor(max_news_count, phrase=phrase, sort_by=sort_by, date=history)
        extractor.open_specific_browser()
        news_count = extractor.search_by_phrase()
        if news_count > 0:
            get_news_status, get_news_message = extractor.get_page_news()
            if(get_news_status==True):
                item.done()
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code="GET_NEWS_FAILED",
                    message=get_news_message,
                )
            extractor.close_browser()   
        else:
            extractor.close_browser()
            item.fail(
                exception_type="BUSINESS",
                code="NEWS_NOT_FOUND",
                message=f"Zero results to phrase {phrase}",
            )
        
