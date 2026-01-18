from pprint import pprint

from src.processors.processor import analyze_pbit

data = analyze_pbit("../files/lesson-8/Lesson - 8.pbit")

pprint(data)