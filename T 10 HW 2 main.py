import requests
from collections import defaultdict
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import re
def map_function(text):
    words = re.findall(r'\w+', text.lower())
    return [(word, 1) for word in words if len(word) > 1]
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()
def reduce_function(shuffled_values):
    reduced = {}
    for key, values in shuffled_values:
        reduced[key] = sum(values)
    return reduced
def map_reduce(text):
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, [text]))
    mapped_values = [item for sublist in mapped_values for item in sublist]
    
    shuffled_values = shuffle_function(mapped_values)
    
    with ThreadPoolExecutor() as executor:
        reduced_values = dict(executor.map(lambda x: (x[0], sum(x[1])), shuffled_values))
    
    return reduced_values
def visualize_top_words(word_counts, top_n=10):
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*sorted_words)
    plt.figure(figsize=(12, 6))
    plt.bar(words, counts)
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
def get_text_from_url(url):
    response = requests.get(url)
    return response.text
if __name__ == '__main__':
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Pride and Prejudice by Jane Austen
    
    # Отримання тексту з URL
    text = get_text_from_url(url)
    
    # Виконання MapReduce
    result = map_reduce(text)
    
    # Візуалізація результатів
    visualize_top_words(result)
