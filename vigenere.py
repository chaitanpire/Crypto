import itertools
import string
import textwrap

# Define the Vigenere encryption and decryption functions

def custom_vigenere(plaintext, secret_key, a_is_zero=True):
    secret_key = secret_key.lower()
    if not all(k in string.ascii_lowercase for k in secret_key):
        raise ValueError("Invalid key {!r}; the key can only consist of English letters".format(secret_key))
    key_iter = itertools.cycle(map(ord, secret_key))
    return "".join(
        chr(ord('a') + (
            (next(key_iter) - ord('a') + ord(letter) - ord('a'))    # Calculate shifted value
            + (0 if a_is_zero else 2)                               # Account for non-zero indexing
            ) % 26) if letter in string.ascii_lowercase             # Ignore non-alphabetic chars
        else letter
        for letter in plaintext.lower()
    )

def custom_vigenere_decrypt(ciphertext, secret_key, a_is_zero=True):
    key_ind = [ord(k) - ord('a') for k in secret_key.lower()]
    inverse = "".join(chr(ord('a') +
            ((26 if a_is_zero else 22) -
                (ord(k) - ord('a'))
            ) % 26) for k in secret_key)
    return custom_vigenere(ciphertext, inverse, a_is_zero)

# Test that the custom Vigenere encrypt and decrypt functions work

def test_custom_vigenere(text, secret_key, a_is_zero=True):
    ciphertext = custom_vigenere(text, secret_key, a_is_zero)
    plaintext  = custom_vigenere_decrypt(ciphertext, secret_key, a_is_zero)
    assert plaintext == text, "{!r} -> {!r} -> {!r} (a {}= 0)".format(
        text, ciphertext, plaintext, "" if a_is_zero else "!")
    
for text in ["example", "text with spaces", "punctuation", "numbers"]:
    for secret_key in ["key", "cipher", "secret", "code"]:
        test_custom_vigenere(text, secret_key, True)
        test_custom_vigenere(text, secret_key, False)

# Now that we're sure that all the custom Vigenere stuff is working...

# Define a custom English letter frequency distribution

CUSTOM_ENGLISH_FREQ = (0.071, 0.013, 0.035, 0.038, 0.14, 0.022, 0.018, 0.043, 0.065, 0.002, 0.005,
                       0.035, 0.034, 0.067, 0.074, 0.024, 0.002, 0.061, 0.070, 0.097, 0.030, 0.011,
                       0.017, 0.003, 0.016, 0.001)

def compare_custom_freq(text):
    """
    Compare the letter distribution of the given text with a custom English distribution. Lower is closer.
    Performs a simple sum of absolute difference for each letter
    """
    if not text:
        return None
    text = [t for t in text.lower() if t in string.ascii_lowercase]
    freq = [0] * 26
    total = float(len(text))
    for l in text:
        freq[ord(l) - ord('a')] += 1
    return sum(abs(f / total - E) for f, E in zip(freq, CUSTOM_ENGLISH_FREQ))

# Solve the custom Vigenere cipher

def solve_custom_vigenere(ciphertext, min_key_size=1, max_key_size=12, a_is_zero=True):
    best_keys = []

    text_letters = [c for c in ciphertext.lower() if c in string.ascii_lowercase]

    for key_length in range(min_key_size, max_key_size + 1):
        # Try all possible key lengths
        secret_key = [None] * key_length
        for key_index in range(key_length):
            letters = "".join(itertools.islice(text_letters, key_index, None, key_length))
            shifts = []
            for key_char in string.ascii_lowercase:
                shifts.append(
                    (compare_custom_freq(custom_vigenere_decrypt(letters, key_char, a_is_zero)), key_char)
                )
            secret_key[key_index] = min(shifts, key=lambda x: x[0])[1]
        best_keys.append("".join(secret_key))
    best_keys.sort(key=lambda key: compare_custom_freq(custom_vigenere_decrypt(ciphertext, key, a_is_zero)))
    return best_keys[:2]

# Define a custom set of meaningful English words

CUSTOM_ENGLISH_WORDS = {
    "custom", "words", "mean", "look", "at", "this", "a", "world", "built", "on", "fantasy",
    "emotions", "in", "the", "form", "pills", "brain", "seminars", "media", "controlled",
    "social", "networks", "you", "want", "to", "talk", "about", "reality",
    "haven't", "lived", "anything", "remotely", "close", "since", "turn", "century", "turned",
    "off", "took", "out", "batteries", "snacked", "bag", "while", "tossed", "remnants", "into",
    "ever", "expanding", "dumpster", "human", "condition", "live", "branded", "houses", "by",
    "corporations", "numbers", "up", "and", "down", "digital", "displays",
    "hypnotizing", "us", "slumber", "has", "ever", "seen", "have", "dig", "pretty",
    "deep", "kiddo", "before", "can", "find", "anything", "bullshit", "even", "for", "far",
    "so", "don't", "tell", "me", "not", "being", "i'm", "no", "less", "than", "freaking",
    "beef", "patty", "your", "mac", "as", "far", "concerned", "i", "am", "very", "all", "together",
    "now", "whether", "like", "it", "or", "notit", "came", "from", "first", "computer", "mark", "1",
    "room-size", "maze", "electromechanical", "circuits", "lab", "harvard", "university", "developed",
    "glitch", "one", "day", "no", "one", "able", "locate", "cause", "after", "hours", "searching",
    "finally", "spotted", "problem", "seemed", "had", "landed", "circuit", "boards", "shorted",
    "from", "that", "moment", "glitches", "were", "referred", "bugs", "solution", "had", "taken",
    "terrific", "toll", "restless", "turning", "mind", "tormented", "by", "puzzle", "preoccupation",
    "meals", "insomnia", "sudden", "wakening", "midnight", "pressure", "succeed", "because",
    "failure", "could", "national", "consequences", "despair", "long", "weeks", "when", "insoluble",
    "repeated", "dashings", "uplifted", "hopes", "mental", "shocks", "tension", "frustration", "urgency",
    "secrecy", "converged", "hammered", "furiously", "upon", "his", "skull", "collapsed", "in",
    "december", "make", "list", "above", "custom"
}

def contains_custom_meaningful_words(text):
    """
    Check if the given text contains a significant number of custom English words
    """
    words = text.lower().split()
    meaningful_word_count = sum(1 for word in words if word in CUSTOM_ENGLISH_WORDS)
    return meaningful_word_count >= len(words) * 0.4  # Check if at least 40% of words are meaningful custom English words

def custom_main():
    ciphertext = input("Enter the ciphertext to decrypt: ").strip()

    for secret_key in reversed(solve_custom_vigenere(ciphertext)):
        decrypted_text = custom_vigenere_decrypt(ciphertext, secret_key)
        if ciphertext == custom_vigenere(decrypted_text, secret_key) and contains_custom_meaningful_words(decrypted_text):
            print("")
            print("Found secret_key: {!r}".format(secret_key))
            print("Solution:")
            
            print(textwrap.fill(decrypted_text))
            break
    else:
        print("No unique solution found or no meaningful custom English words.")

if __name__ == "__main__":
    custom_main()

