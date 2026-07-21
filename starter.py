# The raw passphrase to clean:
raw_phrase = "aP!pL3e#S4aU%cE"

# YOUR GOAL: Clean up this phrase using the 3 Security Rules below!
def loop_solution(raw_phrase):
    allowed_characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    raw_phrase = raw_phrase.upper()
    clean_phrase = ''
    for char in raw_phrase:
        if char in allowed_characters:
            clean_phrase += char
    print(clean_phrase)

print(''.join(filter(str.isalpha, raw_phrase)).upper())