# Day 82: Text to Morse Code Converter

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..",
    "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---",
    "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..",
    "!": "-.-.--", "'": ".----.", "/": "-..-.",
    "(": "-.--.", ")": "-.--.-", "&": ".-...",
    ":": "---...", ";": "-.-.-.", "=": "-...-",
    "+": ".-.-.", "-": "-....-", "_": "..--.-",
    '"': ".-..-.", "$": "...-..-", "@": ".--.-."
}


def text_to_morse(text):
    """Convert English text into Morse code."""
    result = []

    for character in text.upper():
        if character == " ":
            result.append("/")
        elif character in MORSE_CODE:
            result.append(MORSE_CODE[character])
        else:
            raise ValueError(f"Unsupported character: {character!r}")

    return " ".join(result)


def main():
    print("=" * 40)
    print("     DAY 82: MORSE CODE CONVERTER")
    print("=" * 40)
    print("Enter English text, letters, numbers or common symbols.")
    print("Type EXIT to quit.\n")

    while True:
        user_text = input("Enter your text: ").strip()

        if user_text.upper() == "EXIT":
            print("Thank you for using the Day 82 converter!")
            break

        if not user_text:
            print("Please enter some text.\n")
            continue

        try:
            print("Morse code:", text_to_morse(user_text), "\n")
        except ValueError as error:
            print("Error:", error, "\n")


if __name__ == "__main__":
    main()
