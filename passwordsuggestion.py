import secrets
import string
import sys
import time
import os  # Added to check for file existence

# Try to import clipboard lib, fallback if missing
try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

def load_real_wordlist():
    """
    Loads words from a local file named 'words.txt'.
    If the file is missing, it returns a sarcastic fallback list.
    """
    file_path = "words.txt"
    
    if not os.path.exists(file_path):
        print(f"Warning: '{file_path}' not found. Using unsafe demo list.")
        return ["unsafe", "demo", "list", "do", "not", "use", "replace", "me"]

    try:
        with open(file_path, "r") as f:
            # Read lines, strip whitespace, filter out short words (<=3 chars are weak)
            words = [line.strip() for line in f if len(line.strip()) > 3]
            
            if not words:
                print("Warning: 'words.txt' is empty!")
                return ["empty", "file", "error"]
                
            return words
    except Exception as e:
        print(f"Error reading file: {e}")
        return ["error", "reading", "file"]

def generate_garbage(length=16, use_symbols=True, use_numbers=True):
    """
    Generates a standard high-entropy string (e.g. 8#dF!2@9).
    """
    chars = string.ascii_letters
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_passphrase(num_words=4, separator="-"):
    """
    Generates a memorable passphrase using the loaded wordlist.
    """
    # 1. Load the words
    word_list = load_real_wordlist()
    
    # 2. Pick random words securely
    passphrase = [secrets.choice(word_list) for _ in range(num_words)]
    
    # 3. Join them
    return separator.join(passphrase)

def save_to_file(password, label="Generated"):
    """
    Appends the password to a text file.
    """
    with open("my_new_passwords.txt", "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {label}: {password}\n")
    print(f" -> Appended to 'my_new_passwords.txt'.")

def copy_to_clipboard(password):
    if HAS_CLIPBOARD:
        pyperclip.copy(password)
        print(" -> Copied to clipboard! (Clear it soon.)")
    else:
        print(" -> Clipboard module missing. Run: python -m pip install pyperclip")

def main():
    print("--- PASSWORD SUGGESTOR ---")
    print("1. Paranoid String (e.g., '8#dF!2@9')")
    print("2. Memorable Passphrase (e.g., 'correct-horse-battery')")
    
    choice = input("Pick your poison (1/2): ").strip()
    password = ""
    
    if choice == '1':
        try:
            length_input = input("Length (default 16): ")
            length = int(length_input) if length_input else 16
            if length < 8: print("Warning: <8 chars is weak.")
        except ValueError:
            length = 16
        
        sym = input("Include symbols? (y/n): ").lower().startswith('y')
        num = input("Include numbers? (y/n): ").lower().startswith('y')
        
        password = generate_garbage(length, sym, num)

    elif choice == '2':
        
        print("Generating a passphrase...")
        # Note: We don't ask for a list here anymore; the function loads 'words.txt' internally.
        password = generate_passphrase(num_words=4)

    else:
        print("Invalid choice. Bye.")
        sys.exit()

    print("\n" + "="*40)
    print(f"SUGGESTION: {password}")
    print("="*40 + "\n")

    action = input("Save to file (f), Copy to clipboard (c), or Both (b)? ").lower()
    
    if action in ['c', 'b']:
        copy_to_clipboard(password)
    if action in ['f', 'b']:
        save_to_file(password, label="Type-" + choice)

if __name__ == "__main__":
    main()