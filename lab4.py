import math

WORDS = ["Шануй", "батька", "й", "матір", "то", "буде", "тобі", "в", "житті", "добре"]

UKR_LETTER_POSITIONS = {
    'А': 1, 'Б': 2, 'В': 3, 'Г': 4, 'Ґ': 5, 'Д': 6, 'Е': 7, 'Є': 8,
    'Ж': 9, 'З': 10, 'И': 11, 'І': 12, 'Ї': 13, 'Й': 14, 'К': 15, 'Л': 16,
    'М': 17, 'Н': 18, 'О': 19, 'П': 20, 'Р': 21, 'С': 22, 'Т': 23, 'У': 24,
    'Ф': 25, 'Х': 26, 'Ц': 27, 'Ч': 28, 'Ш': 29, 'Щ': 30, 'Ь': 31, 'Ю': 32, 'Я': 33
}

def word_key_sum(word):
    total = 0
    for ch in word.upper():
        total += UKR_LETTER_POSITIONS.get(ch, 0)
    return total

def hash_division(word, m=13):
    return word_key_sum(word) % m

def hash_multiplication(word, m=16):
    a = (math.sqrt(5) - 1) / 2
    k = word_key_sum(word)
    frac_part = (k * a) % 1
    return math.floor(m * frac_part)

def build_open_hash_table(words, m, hash_fn):
    hash_table = [[] for _ in range(m)]
    for word in words:
        address = hash_fn(word, m)
        hash_table[address].append(word)
    return hash_table

def search_open_hash(table, key, hash_fn):
    m = len(table)
    address = hash_fn(key, m)
    comparisons = 0
    for item in table[address]:
        comparisons += 1
        if item == key:
            return address, comparisons
    return None, comparisons

def display_open_hash_table(table, title):
    print(f"\n{title} (M={len(table)}):")
    for i, chain in enumerate(table):
        print(f"Індекс {i:02d}: {chain}")

def analyze_open_hash(table, words, hash_fn, name):
    print(f"\nАналіз пошуку ({name}):")
    total_comps = 0
    max_comps = 0
    max_words = []
    for w in words:
        addr, comps = search_open_hash(table, w, hash_fn)
        total_comps += comps
        if comps > max_comps:
            max_comps = comps
            max_words = [w]
        elif comps == max_comps:
            max_words.append(w)
        print(f"Слово '{w}': індекс = {addr:02d}, порівнянь = {comps}")
    print(f"Максимальна кількість порівнянь: {max_comps} ({max_words})")
    print(f"Середня кількість порівнянь: {total_comps / len(words):.2f}")

open_div = build_open_hash_table(WORDS, 13, hash_division)
display_open_hash_table(open_div, "Відкрита хеш-таблиця (метод ділення)")
analyze_open_hash(open_div, WORDS, hash_division, "метод ділення, M=13")

open_mul = build_open_hash_table(WORDS, 16, hash_multiplication)
display_open_hash_table(open_mul, "Відкрита хеш-таблиця (метод множення)")
analyze_open_hash(open_mul, WORDS, hash_multiplication, "метод множення, M=16")

def build_closed_hash_table(words, m, hash_fn):
    hash_table = [None] * m
    for word in words:
        start_address = hash_fn(word, m)
        inserted = False
        for i in range(m):
            address = (start_address + i) % m
            if hash_table[address] is None:
                hash_table[address] = word
                inserted = True
                break
        if not inserted:
            print(f"Помилка: таблиця заповнена, не вдалося додати {word}")
    return hash_table

def search_closed_hash(table, key, hash_fn):
    m = len(table)
    start_address = hash_fn(key, m)
    comparisons = 0
    for i in range(m):
        address = (start_address + i) % m
        if table[address] is None:
            return None, comparisons
        comparisons += 1
        if table[address] == key:
            return address, comparisons
    return None, comparisons

def display_closed_hash_table(table, title):
    print(f"\n{title} (M={len(table)}):")
    for i in range(len(table)):
        if table[i] is not None:
            value = table[i]
        else:
            value = "(NULL)"
        print(f"Індекс {i:02d}: {value}")

def analyze_closed_hash(table, words, hash_fn, name):
    print(f"\nАналіз пошуку ({name}):")
    total_comps = 0
    max_comps = 0
    max_words = []
    for w in words:
        addr, comps = search_closed_hash(table, w, hash_fn)
        total_comps += comps
        if comps > max_comps:
            max_comps = comps
            max_words = [w]
        elif comps == max_comps:
            max_words.append(w)
        print(f"Слово '{w}': комірка = {addr:02d}, порівнянь = {comps}")
    print(f"Максимальна кількість порівнянь: {max_comps} ({max_words})")
    print(f"Середня кількість порівнянь: {total_comps / len(words):.2f}")

closed_div = build_closed_hash_table(WORDS, 13, hash_division)
display_closed_hash_table(closed_div, "Закрита хеш-таблиця (метод ділення)")
analyze_closed_hash(closed_div, WORDS, hash_division, "метод ділення, M=13")

closed_mul = build_closed_hash_table(WORDS, 16, hash_multiplication)
display_closed_hash_table(closed_mul, "Закрита хеш-таблиця (метод множення)")
analyze_closed_hash(closed_mul, WORDS, hash_multiplication, "метод множення, M=16")
