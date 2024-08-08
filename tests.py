from src.Latimes import LatimesExtractor

extractor = LatimesExtractor(count_news=15, phrase="Sport", sort_by="sort_by", date="9")

titles, descriptions = extractor.count_phrases("The Sports Report: Simone Biles shows why she’s the best sport", "Simone Biles wins the Olympics trial all-around women’s gymnastics titles and will lead the U.S. team in the Paris Olympics. ")
print(titles)
print(descriptions)