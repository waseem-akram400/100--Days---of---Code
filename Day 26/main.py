import pandas as pd

# CSV فائل پڑھیں
data = pd.read_csv("nato_phonetic_alphabet.csv")

# CSV سے Dictionary بنائیں
phonetic_dict = {
    row.letter: row.code
    for (index, row) in data.iterrows()
}

# صارف سے لفظ لیں
word = input("Enter a word: ").upper()

# ہر حرف کو NATO لفظ میں تبدیل کریں
output_list = [
    phonetic_dict[letter]
    for letter in word
]

# نتیجہ دکھائیں
print(output_list)