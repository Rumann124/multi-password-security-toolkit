import math
import re
import string

# ANSI colors for the terminal (because we want it to look 'hacker-ish')
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def calculate_entropy(password):
    """
    Calculates the bits of entropy.
    Entropy = Length * log2(Pool Size)
    """
    pool_size = 0
    if re.search(r'[a-z]', password): pool_size += 26
    if re.search(r'[A-Z]', password): pool_size += 26
    if re.search(r'[0-9]', password): pool_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32  # Special chars
    
    if pool_size == 0: return 0
    
    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)

def estimate_crack_time(entropy):
    """
    Estimates time to crack assuming a decent cracking rig
    (e.g., RTX 4090 cluster doing ~100 Billion guesses/sec for fast hashes).
    """
    guesses_per_sec = 100_000_000_000  # 100 Billion
    seconds = (2 ** entropy) / guesses_per_sec
    
    if seconds < 1: return "Instant", "My toaster could crack this."
    if seconds < 60: return f"{seconds:.2f} seconds", "Gone before you blink."
    if seconds < 3600: return f"{seconds/60:.2f} minutes", "Time for a coffee break."
    if seconds < 86400: return f"{seconds/3600:.2f} hours", "Within a work day."
    if seconds < 31536000: return f"{seconds/86400:.2f} days", "A determined script kiddie might wait."
    if seconds < 31536000 * 100: return f"{seconds/31536000:.2f} years", "Secure against casuals."
    return "Centuries+", "Heat death of the universe comes first."

def check_weakness(password):
    """
    Checks for stupid patterns.
    """
    weaknesses = []
    
    # Common stupidity
    common_list = ['password', '123456', 'admin', 'welcome', 'qwerty', 'iloveyou']
    if password.lower() in common_list:
        weaknesses.append("Literally in the top 10 worst passwords list.")

    # Repetition
    if len(set(password)) == 1:
        weaknesses.append("Are you a cat walking on a keyboard? (Repeated chars)")

    # Sequential
    if "123" in password or "abc" in password.lower():
        weaknesses.append("Sequences are easy to guess.")

    return weaknesses

def visual_strength_meter(entropy):
    """
    Renders a text-based progress bar.
    """
    max_entropy = 128  # 128 bits is standard 'unbreakable'
    percent = min(entropy / max_entropy, 1.0)
    bar_length = 30
    filled_length = int(bar_length * percent)
    
    if percent < 0.3: color = Colors.FAIL
    elif percent < 0.6: color = Colors.WARNING
    else: color = Colors.GREEN
    
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f"\n{Colors.BOLD}Visual Strength:{Colors.ENDC} [{color}{bar}{Colors.ENDC}] {int(percent*100)}%")

def main():
    print(f"{Colors.HEADER}--- PASSWORD REALITY CHECKER ---{Colors.ENDC}")
    password = input("Enter password to test (I won't save it): ")

    if not password:
        print("You entered nothing. That is effectively 0 security.")
        return

    # 1. Entropy
    entropy = calculate_entropy(password)
    
    # 2. Time Estimation
    time_str, sarcasm = estimate_crack_time(entropy)
    
    # 3. Weakness Detection
    flaws = check_weakness(password)

    # OUTPUT
    print("\n" + "-"*40)
    print(f"{Colors.BOLD}Entropy:{Colors.ENDC} {entropy} bits")
    print(f"{Colors.BOLD}Crack Time:{Colors.ENDC} {time_str}")
    print(f"{Colors.BOLD}Verdict:{Colors.ENDC} {sarcasm}")
    
    if flaws:
        print(f"\n{Colors.FAIL}CRITICAL FLAWS DETECTED:{Colors.ENDC}")
        for flaw in flaws:
            print(f" - {flaw}")
    
    # 4. Visual Meter
    visual_strength_meter(entropy)
    print("-"*40 + "\n")

if __name__ == "__main__":
    main()