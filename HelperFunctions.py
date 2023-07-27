from word2number import w2n
import inflect

def universal_number_converter(number):
    words = number.lower().split()
    p = inflect.engine()

    if len(words) == 1:
        try:
            numeric_value = str(w2n.word_to_num(words[0]))
        except ValueError:
            try:
                numeric_value = p.words_to_number(words[0])
            except ValueError:
                return f"Invalid input: {number}"
    else:
        try:
            numeric_value = w2n.word_to_num(" ".join(words))
        except ValueError:
            try:
                numeric_value = p.words_to_number(" ".join(words))
            except ValueError:
                return f"Invalid input: {number}"

    return str(numeric_value)

def main():
    input_number = input("Enter a number or its word representation: ")
    converted_number = universal_number_converter(input_number)
    print("The converted value is:", converted_number)

if __name__ == "__main__":
    main()
