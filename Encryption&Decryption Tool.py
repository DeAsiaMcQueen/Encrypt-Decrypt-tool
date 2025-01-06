import tkinter as tk
from tkinter import ttk
import base64
import string
from itertools import cycle
# Helper functions for encryption and decryption methods
def caesar_cipher_encrypt(text, key):
    key = int(key) % 26
    return ''.join(
        chr((ord(char) - 65 + key) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 + key) % 26 + 97) if char.islower() else char
        for char in text
    )
def caesar_cipher_decrypt(text, key):
    key = int(key) % 26
    return caesar_cipher_encrypt(text, -key)
def vigenere_encrypt(text, key):
    key = ''.join(filter(str.isalpha, key))
    key = cycle(key.upper())
    return ''.join(
        chr((ord(char) - 65 + (ord(next(key)) - 65)) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 + (ord(next(key)) - 65)) % 26 + 97) if char.islower() else char
        for char in text
    )
def vigenere_decrypt(text, key):
    key = ''.join(filter(str.isalpha, key))
    key = cycle(key.upper())
    return ''.join(
        chr((ord(char) - 65 - (ord(next(key)) - 65)) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 - (ord(next(key)) - 65)) % 26 + 97) if char.islower() else char
        for char in text
    )
def substitution_encrypt(text, key):
    alphabet = string.ascii_lowercase
    substitution_table = {char: key[idx] for idx, char in enumerate(alphabet)}
    return ''.join(substitution_table.get(char, char) for char in text.lower())
def substitution_decrypt(text, key):
    alphabet = string.ascii_lowercase
    reverse_table = {key[idx]: char for idx, char in enumerate(alphabet)}
    return ''.join(reverse_table.get(char, char) for char in text.lower())
def transposition_encrypt(text, key):
    key = int(key)
    return ''.join(text[i::key] for i in range(key))
def transposition_decrypt(text, key):
    key = int(key)
    n_cols = len(text) // key
    n_full_cols = len(text) % key
    return ''.join(
        text[i * n_cols + min(i, n_full_cols):(i + 1) * n_cols + min(i + 1, n_full_cols)]
        for i in range(key)
    )
def affine_encrypt(text, a, b):
    return ''.join(
        chr(((a * (ord(char) - 65) + b) % 26) + 65) if char.isupper() else
        chr(((a * (ord(char) - 97) + b) % 26) + 97) if char.islower() else char
        for char in text
    )
def affine_decrypt(text, a, b):
    m_inv = pow(a, -1, 26)
    return ''.join(
        chr(((m_inv * ((ord(char) - 65) - b)) % 26) + 65) if char.isupper() else
        chr(((m_inv * ((ord(char) - 97) - b)) % 26) + 97) if char.islower() else char
        for char in text
    )
def rail_fence_encrypt(text, key):
    key = int(key)
    rail = [''] * key
    direction = 1
    row = 0
    for char in text:
        rail[row] += char
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    return ''.join(rail)
def rail_fence_decrypt(text, key):
    key = int(key)
    rail_len = [0] * key
    direction = 1
    row = 0
    for _ in text:
        rail_len[row] += 1
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    rails = []
    idx = 0
    for length in rail_len:
        rails.append(text[idx:idx + length])
        idx += length
    direction = 1
    row = 0
    result = []
    for _ in text:
        result.append(rails[row][0])
        rails[row] = rails[row][1:]
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    return ''.join(result)
def base64_encrypt(text):
    return base64.b64encode(text.encode()).decode()
def base64_decrypt(text):
    return base64.b64decode(text.encode()).decode()
# Map methods to their processing functions
methods = {
    "Caesar Cipher": (caesar_cipher_encrypt, caesar_cipher_decrypt, 1),
    "Vigenère Cipher": (vigenere_encrypt, vigenere_decrypt, 1),
    "Substitution Cipher": (substitution_encrypt, substitution_decrypt, 1),
    "Transposition Cipher": (transposition_encrypt, transposition_decrypt, 1),
    "Affine Cipher": (affine_encrypt, affine_decrypt, 2),
    "Rail Fence Cipher": (rail_fence_encrypt, rail_fence_decrypt, 1),
    "Base64 Encoding/Decoding": (base64_encrypt, base64_decrypt, 0),
}
# GUI setup
root = tk.Tk()
root.title("Encryption and Decryption Tool")
method_var = tk.StringVar(value="Caesar Cipher")
action_var = tk.StringVar(value="Encrypt")
key_var = tk.StringVar()
key_a_var = tk.StringVar()
key_b_var = tk.StringVar()
def update_key_inputs(*args):
    method = methods[method_var.get()]
    key_frame.pack_forget()
    key_a_frame.pack_forget()
    key_b_frame.pack_forget()
    if method[2] == 1:
        key_frame.pack()
    elif method[2] == 2:
        key_a_frame.pack()
        key_b_frame.pack()
method_var.trace("w", update_key_inputs)
def process():
    text = input_text.get("1.0", tk.END).strip()
    method = methods[method_var.get()]
    if action_var.get() == "Encrypt":
        if method[2] == 0:
            result = method[0](text)
        elif method[2] == 1:
            result = method[0](text, key_var.get())
        elif method[2] == 2:
            result = method[0](text, int(key_a_var.get()), int(key_b_var.get()))
    else:
        if method[2] == 0:
            result = method[1](text)
        elif method[2] == 1:
            result = method[1](text, key_var.get())
        elif method[2] == 2:
            result = method[1](text, int(key_a_var.get()), int(key_b_var.get()))
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
# GUI elements
ttk.Label(root, text="Select Method:").pack()
ttk.Combobox(root, textvariable=method_var, values=list(methods.keys())).pack()
ttk.Label(root, text="Action:").pack()
ttk.Combobox(root, textvariable=action_var, values=["Encrypt", "Decrypt"]).pack()
key_frame = ttk.Frame(root)
ttk.Label(key_frame, text="Key:").pack(side=tk.LEFT)
ttk.Entry(key_frame, textvariable=key_var).pack(side=tk.LEFT)
key_a_frame = ttk.Frame(root)
ttk.Label(key_a_frame, text="Key A:").pack(side=tk.LEFT)
ttk.Entry(key_a_frame, textvariable=key_a_var).pack(side=tk.LEFT)
key_b_frame = ttk.Frame(root)
ttk.Label(key_b_frame, text="Key B:").pack(side=tk.LEFT)
ttk.Entry(key_b_frame, textvariable=key_b_var).pack(side=tk.LEFT)
update_key_inputs()
ttk.Label(root, text="Input Text:").pack()
input_text = tk.Text(root, height=10, width=50)
input_text.pack()
ttk.Label(root, text="Output Text:").pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()
ttk.Button(root, text="Process", command=process).pack()
root.mainloop()