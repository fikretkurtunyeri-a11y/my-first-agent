#!/usr/bin/env python3
"""Generate a vocabulary worksheet from a CSV file."""

import csv
import random
import sys
from pathlib import Path
from typing import List, Tuple

Question = Tuple[str, str]
MultipleChoiceQuestion = Tuple[str, List[str], str]


def read_vocab(csv_path: Path) -> List[Question]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    vocab: List[Question] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for row in reader:
            if not row:
                continue
            if len(row) < 2:
                raise ValueError(f"Invalid row (expected 2 columns): {row}")
            english = row[0].strip()
            norwegian = row[1].strip()
            if english and norwegian:
                vocab.append((english, norwegian))

    if not vocab:
        raise ValueError("No vocabulary entries found in the CSV file.")

    return vocab


def pick_questions(vocab: List[Question], count: int) -> List[Question]:
    if len(vocab) <= count:
        return vocab.copy()
    return random.sample(vocab, count)


def build_multiple_choice(vocab: List[Question], count: int) -> List[MultipleChoiceQuestion]:
    questions: List[MultipleChoiceQuestion] = []
    selected = pick_questions(vocab, count)
    norwegian_words = [nor for _, nor in vocab]

    for english, correct in selected:
        distractors = [word for word in norwegian_words if word != correct]
        random.shuffle(distractors)
        options = [correct] + distractors[:3]
        random.shuffle(options)
        questions.append((english, options, correct))

    return questions


def build_matching(vocab: List[Question], count: int) -> Tuple[List[Question], List[str]]:
    selected = pick_questions(vocab, count)
    norwegian_list = [nor for _, nor in selected]
    random.shuffle(norwegian_list)
    return selected, norwegian_list


def build_fill_in_blank(vocab: List[Question], count: int) -> List[Question]:
    return pick_questions(vocab, count)


def format_worksheet(
    multiple_choice: List[MultipleChoiceQuestion],
    matching_pairs: List[Question],
    matching_words: List[str],
    fill_in_blank: List[Question],
) -> str:
    lines = []
    lines.append("Vocabulary Worksheet")
    lines.append("=" * 22)
    lines.append("")

    lines.append("Part 1: Multiple Choice (choose the Norwegian translation)")
    lines.append("-")
    for idx, (english, options, _) in enumerate(multiple_choice, start=1):
        lines.append(f"{idx}. {english}")
        option_labels = "ABCD"
        for label, option in zip(option_labels, options):
            lines.append(f"   {label}) {option}")
        lines.append("")

    lines.append("Part 2: Matching (write the correct number)")
    lines.append("-")
    for idx, (english, _) in enumerate(matching_pairs, start=1):
        lines.append(f"{idx}. {english}")
    lines.append("")
    for idx, norwegian in enumerate(matching_words, start=1):
        lines.append(f"{idx}. {norwegian}")
    lines.append("")

    lines.append("Part 3: Fill in the Blanks (write the Norwegian word)")
    lines.append("-")
    for idx, (english, _) in enumerate(fill_in_blank, start=1):
        lines.append(f"{idx}. {english}: ____________________")
    lines.append("")

    lines.append("Answer Key")
    lines.append("-")
    lines.append("Multiple Choice")
    for idx, (english, options, correct) in enumerate(multiple_choice, start=1):
        correct_letter = "ABCD"[options.index(correct)]
        lines.append(f"{idx}. {correct_letter} ({english} = {correct})")
    lines.append("")

    lines.append("Matching")
    for idx, (english, norwegian) in enumerate(matching_pairs, start=1):
        match_number = matching_words.index(norwegian) + 1
        lines.append(f"{idx}. {match_number} ({english} = {norwegian})")
    lines.append("")

    lines.append("Fill in the Blanks")
    for idx, (english, norwegian) in enumerate(fill_in_blank, start=1):
        lines.append(f"{idx}. {english} = {norwegian}")

    return "\n".join(lines)


def main() -> None:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("vocab.csv")
    output_path = Path("worksheet.txt")

    vocab = read_vocab(csv_path)

    multiple_choice = build_multiple_choice(vocab, 5)
    matching_pairs, matching_words = build_matching(vocab, 5)
    fill_in_blank = build_fill_in_blank(vocab, 5)

    worksheet = format_worksheet(multiple_choice, matching_pairs, matching_words, fill_in_blank)
    output_path.write_text(worksheet, encoding="utf-8")

    print(f"Worksheet saved to {output_path}")


if __name__ == "__main__":
    main()
