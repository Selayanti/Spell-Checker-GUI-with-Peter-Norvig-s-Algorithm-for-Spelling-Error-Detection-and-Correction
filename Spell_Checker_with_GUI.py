import tkinter as tk
from tkinter import ttk
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('kamus-kata-dasar.txt').read()))

def P(word, N=sum(WORDS.values())):
    return WORDS[word] / N

def correction(word):
    return max(candidates(word), key=P)

def sentence_correction(sentence):
    corrected_sentence = []
    for word in sentence.split():
        corrected_sentence.append(correction(word))
    return ' '.join(corrected_sentence)

def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    return set(w for w in words if w in WORDS)

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correct_text():
    input_text = input_entry.get("1.0", "end-1c")
    words_in_text = input_text.split()
    total_words = len(words_in_text)

    corrected_text = sentence_correction(input_text)
    corrected_words = corrected_text.split()

    detected_wrong_words = 0
    corrected_words_correctly = 0

    for i in range(total_words):
        original_word = words_in_text[i]
        corrected_word = corrected_words[i]

        if original_word != corrected_word:
            detected_wrong_words += 1
            if corrected_word in WORDS:
                corrected_words_correctly += 1

    detection_accuracy = (detected_wrong_words / total_words) * 100
    correction_accuracy = (corrected_words_correctly / detected_wrong_words) * 100 if detected_wrong_words > 0 else 0

    result_text.delete("1.0", "end")
    result_text.insert("end", corrected_text)
    result_text.insert("end", f"\n\nDetection Accuracy: {detection_accuracy:.2f}%")
    result_text.insert("end", f"\nCorrection Accuracy: {correction_accuracy:.2f}%") 

root = tk.Tk()
root.title("Spell Cheking")
root.geometry("800x600")

style = ttk.Style(root)
style.theme_use("clam")

# Define style for labels
style.configure("LabelStyle.TLabel", font=("Arial", 16), foreground="blue")

# Define style for buttons
style.configure("TButton", font=("Arial", 14), foreground="blue", background="lightblue")

# Define style for text boxes
style.configure("TText", font=("Arial", 14))

input_label = tk.Label(root, text="Enter text:", font=("Arial", 16))
input_label.pack(pady=10)

input_entry = tk.Text(root, height=10, width=60, font=("Arial", 14))
input_entry.pack(pady=10)

correct_button = ttk.Button(root, text="Correct Text", command=correct_text, style="TButton")
correct_button.pack(pady=10)

result_label = tk.Label(root, text="Corrected text:", font=("Arial", 16))
result_label.pack(pady=10)

result_text = tk.Text(root, height=10, width=60, font=("Arial", 14))
result_text.pack(pady=10)

root.mainloop()
