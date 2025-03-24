import hashlib
import itertools
import argparse

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def crack_hash(hash_value, wordlist, algorithm):
    with open(wordlist, "r", encoding="latin-1") as file:
        for word in file:
            word = word.strip()
            if algorithm == "md5":
                hashed_word = hashlib.md5(word.encode()).hexdigest()
            elif algorithm == "sha256":
                hashed_word = hashlib.sha256(word.encode()).hexdigest()
            elif algorithm == "bcrypt":
                import bcrypt
                hashed_word = bcrypt.hashpw(word.encode(), bcrypt.gensalt())
            if hashed_word == hash_value:
                print(f"{GREEN}Password found: {word}{RESET}")
                return
    print(f"{RED}Password not found in wordlist.{RESET}")

def brute_force(hash_value, charset, max_length, algorithm):
    for length in range(1, max_length + 1):
        for attempt in itertools.product(charset, repeat=length):
            attempt = ''.join(attempt)
            if algorithm == "md5":
                hashed_attempt = hashlib.md5(attempt.encode()).hexdigest()
            elif algorithm == "sha256":
                hashed_attempt = hashlib.sha256(attempt.encode()).hexdigest()
            elif algorithm == "bcrypt":
                import bcrypt
                hashed_attempt = bcrypt.hashpw(attempt.encode(), bcrypt.gensalt())
            if hashed_attempt == hash_value:
                print(f"{GREEN}Password found: {attempt}{RESET}")
                return
    print(f"{RED}Password not found via brute-force.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PassCrackX - Password Cracking Tool")
    parser.add_argument("hash", help="Target hash")
    parser.add_argument("-a", "--algorithm", choices=["md5", "sha256", "bcrypt"], required=True, help="Hash algorithm")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist")
    parser.add_argument("-b", "--brute", action="store_true", help="Enable brute-force attack")
    parser.add_argument("-c", "--charset", default="abcdefghijklmnopqrstuvwxyz", help="Character set for brute-force")
    parser.add_argument("-l", "--max_length", type=int, default=4, help="Max length for brute-force")
    args = parser.parse_args()

    if args.wordlist:
        crack_hash(args.hash, args.wordlist, args.algorithm)
    elif args.brute:
        brute_force(args.hash, args.charset, args.max_length, args.algorithm)
    else:
        print(f"{RED}Please specify a wordlist or enable brute-force.{RESET}")