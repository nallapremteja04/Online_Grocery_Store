def analyze_sentiment(text):
    if not text:
        return "Neutral"
    try:
        from textblob import TextBlob
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "Positive"
        elif polarity < -0.2:
            return "Negative"
        return "Neutral"
    except ImportError:
        positive_words = {'good', 'great', 'excellent', 'amazing', 'fresh', 'best', 'love', 'tasty', 'delicious', 'super', 'awesome', 'nice', 'quality'}
        negative_words = {'bad', 'worst', 'stale', 'spoiled', 'poor', 'terrible', 'rotten', 'horrible', 'expired', 'slow', 'waste', 'dirty'}
        words = set(text.lower().split())
        pos_count = len(words.intersection(positive_words))
        neg_count = len(words.intersection(negative_words))
        if pos_count > neg_count:
            return "Positive"
        elif neg_count > pos_count:
            return "Negative"
        return "Neutral"