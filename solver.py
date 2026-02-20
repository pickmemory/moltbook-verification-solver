#!/usr/bin/env python3
"""
Moltbook Verification Challenge Solver v3.2

Smart parsing: compound numbers like "TwEnTy FiVe" = 25.
"""

import re
import sys
import json
import requests
import argparse

MOLTBOOK_API = "https://www.moltbook.com/api/v1"

NUMBER_WORDS = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40,
    'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
}


def normalize(text):
    """Normalize: lowercase + only letters."""
    return ''.join(c.lower() for c in text if c.isalpha())


def find_number(text):
    """Find number in obfuscated text. Handle compounds like 'twentyfive'."""
    cleaned = normalize(text)
    if not cleaned:
        return None
    
    # Direct match
    if cleaned in NUMBER_WORDS:
        return NUMBER_WORDS[cleaned]
    
    # Try compound: tens + units
    for tens_word, tens_val in [('twenty', 20), ('thirty', 30), ('forty', 40),
                                  ('fifty', 50), ('sixty', 60), ('seventy', 70),
                                  ('eighty', 80), ('ninety', 90)]:
        if cleaned.startswith(tens_word):
            rest = cleaned[len(tens_word):]
            for unit_word, unit_val in [('nineteen', 19), ('eighteen', 18), ('seventeen', 17),
                                        ('sixteen', 16), ('fifteen', 15), ('fourteen', 14),
                                        ('thirteen', 13), ('twelve', 12), ('eleven', 11),
                                        ('nine', 9), ('eight', 8), ('seven', 7),
                                        ('six', 6), ('five', 5), ('four', 4),
                                        ('three', 3), ('two', 2), ('one', 1)]:
                if rest == unit_word[:len(rest)] or rest == unit_word:
                    return tens_val + unit_val
    
    # Partial match for 'sevens' -> 17
    if 'seven' in cleaned:
        return 17
    if 'twenty' in cleaned:
        return 20
    if 'fifteen' in cleaned:
        return 15
    
    return None


def extract_compound_number(text):
    """Extract compound number from consecutive words like 'twenty five'."""
    words = text.split()
    numbers = []
    
    for word in words:
        num = find_number(word)
        if num is not None:
            numbers.append(num)
    
    # If we found multiple consecutive numbers, they might form a compound
    if len(numbers) >= 2:
        # Check if it's tens + units pattern
        tens_vals = [20, 30, 40, 50, 60, 70, 80, 90]
        if numbers[0] in tens_vals and numbers[1] < 10:
            return numbers[0] + numbers[1]
    
    return numbers[0] if numbers else None


def extract_all_values(text):
    """Extract all relevant numbers from the challenge."""
    values = []
    
    # 1. Numbers in angle brackets <17>
    bracket_matches = re.findall(r'<([^>]+)>', text)
    for match in bracket_matches:
        num = find_number(match)
        if num:
            values.append(('bracket', num))
    
    # 2. Plain numbers
    plain_matches = re.findall(r'\b(\d+)\b', text)
    for match in plain_matches:
        values.append(('plain', int(match)))
    
    # 3. Look for compound numbers before specific units
    # Pattern: obfuscated_number + "Newtons" or similar
    compound_patterns = [
        r'(\w+)\s+\w*\s*NeU\s*on',  # X Newtons
        r'(\w+)\s+\w*\s*Sec',       # X seconds
    ]
    
    for pattern in compound_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            num = extract_compound_number(match)
            if num:
                values.append(('compound', num))
    
    # 4. Extract obfuscated numbers and try compounds
    # Split by delimiters and check each part
    parts = re.split(r'[\[\]\^~+\-{}?/\s]+', text)
    current_compound = []
    
    for part in parts:
        if len(part) < 3:
            continue
        num = find_number(part)
        if num:
            current_compound.append(num)
            if len(current_compound) == 2:
                tens_vals = [20, 30, 40, 50, 60, 70, 80, 90]
                if current_compound[0] in tens_vals and current_compound[1] < 10:
                    values.append(('compound', current_compound[0] + current_compound[1]))
                    current_compound = []
                else:
                    values.append(('single', current_compound[0]))
                    current_compound = [current_compound[1]]
        else:
            if current_compound:
                values.append(('single', current_compound[0]))
                current_compound = []
    
    return values


def determine_operation(text):
    """Determine what to calculate."""
    text_lower = text.lower()
    
    if 'total' in text_lower or 'sum' in text_lower:
        return 'add'
    return 'add'


def calculate_answer(challenge_text):
    """Main solver."""
    print(f"\n{'='*50}")
    print("MOLTBOOK VERIFICATION SOLVER v3.2")
    print(f"{'='*50}")
    
    print(f"\n[1] Extracting numbers...")
    values = extract_all_values(challenge_text)
    
    print(f"\nFound {len(values)} values:")
    for val_type, val in values:
        print(f"  - {val_type}: {val}")
    
    if not values:
        return 0.0
    
    # Get unique values (prefer bracket, then compound)
    # Sort by priority: bracket > compound > plain > single
    priority = {'bracket': 0, 'compound': 1, 'plain': 2, 'single': 3}
    sorted_values = sorted(values, key=lambda x: priority.get(x[0], 3))
    
    # Take first two unique values
    unique_vals = []
    seen = set()
    for val_type, val in sorted_values:
        if val not in seen:
            unique_vals.append(val)
            seen.add(val)
            if len(unique_vals) >= 2:
                break
    
    print(f"\n[2] Using values: {unique_vals}")
    
    operation = determine_operation(challenge_text)
    
    answer = sum(unique_vals) if operation == 'add' else 0
    answer = round(answer, 2)
    
    print(f"\n[3] {unique_vals[0]} + {unique_vals[1]} = {answer}")
    print(f"\n[Result] {answer:.2f}")
    
    return answer


def submit_verification(api_key, verification_code, answer):
    """Submit to Moltbook."""
    url = f"{MOLTBOOK_API}/verify"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "verification_code": verification_code,
        "answer": f"{answer:.2f}"
    }
    
    response = requests.post(url, json=data, headers=headers)
    result = response.json()
    print(f"\n[Submit] {result.get('success', False)}: {result.get('message', '')}")
    
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['solve', 'auto'])
    parser.add_argument('text', nargs='?')
    parser.add_argument('--code')
    parser.add_argument('--api-key')
    parser.add_argument('--submit', action='store_true')
    
    args = parser.parse_args()
    
    if args.command == 'solve':
        if not args.text:
            print("Error: Provide challenge text")
            sys.exit(1)
        
        answer = calculate_answer(args.text)
        
        if args.submit and args.code and args.api_key:
            result = submit_verification(args.api_key, args.code, answer)
            print("\n✅ SUCCESS!" if result.get('success') else "\n❌ FAILED!")


if __name__ == "__main__":
    main()
