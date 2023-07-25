from wordcloud_fa import WordCloudFa

wordcloud = WordCloudFa(persian_normalize=True, background_color="white",max_font_size=200, max_words=60)
# wordcloud.add_stop_words(['هم'])

text = """
سلام هم نباید در متن باشد. پس ما با سلام کردن به ما و شما و آن‌ها می‌گوییم که می هم نباید باشد.
می
می
می
آنکه آنکه
آنکه آنکه آنکه آنکه
"""

wordcloud.generate(text)

img = wordcloud.to_image()
img.show()
