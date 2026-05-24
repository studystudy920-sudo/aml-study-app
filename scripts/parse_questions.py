#!/usr/bin/env python3
"""
Parse AML/CFT exam questions from extracted docx text files into JSON format.
Reads ch1-ch7 from two text files (NOT the 117-question compilation).
"""

import json
import re
import sys
import os

# File paths
FILE1 = "/root/.claude/projects/-home-user-aml-study-app/dfd71655-0d6d-4806-ad57-5a76aa7000f6/tool-results/b937r2s49.txt"
FILE2 = "/root/.claude/projects/-home-user-aml-study-app/dfd71655-0d6d-4806-ad57-5a76aa7000f6/tool-results/b3wyttpfm.txt"
OUTPUT = "/home/user/aml-study-app/data/standard_full.json"

# Chapter metadata
CHAPTER_INFO = {
    "ch1": {"name": "第1章 金融犯罪", "source": "file1", "file_marker": "07c7ba2e"},
    "ch2": {"name": "第2章 FATF", "source": "file1", "file_marker": "77cc893f"},
    "ch3": {"name": "第3章 国内法規制等", "source": "file1", "file_marker": "ee962c67"},
    "ch4": {"name": "第4章 リスクベース・アプローチ", "source": "file1", "file_marker": "fb4f47ef"},
    "ch5": {"name": "第5章 管理態勢", "source": "file2", "file_marker": "bc8db836"},
    "ch6": {"name": "第6章 顧客管理", "source": "file2", "file_marker": "c81d3555"},
    "ch7": {"name": "第7章 疑わしい取引", "source": "file2", "file_marker": "0887f500"},
}

# Tag assignment rules based on question content keywords
TAG_RULES = [
    # Order matters - more specific patterns first
    ("pf", [r"拡散金融", r"大量破壊兵器", r"拡散に関与", r"proliferation"]),
    ("tf", [r"テロ資金", r"テロリスト", r"テロリズム", r"テロ資金供与", r"テロ等準備罪", r"テロ資金提供処罰法", r"公衆等脅迫目的"]),
    ("fatf", [r"FATF", r"相互審査", r"勧告", r"APG", r"フォローアップ", r"有効性評価", r"技術的遵守", r"メソドロジー", r"行動計画"]),
    ("domestic-law", [r"犯罪収益移転防止法", r"犯収法", r"外為法", r"組織的犯罪処罰法", r"組織犯罪処罰法", r"国際テロリスト財産凍結法", r"テロ資金提供処罰法", r"TOC条約", r"国際組織犯罪防止条約", r"麻薬特例法", r"資金決済法", r"暴力団対策法", r"暴力団員による不当", r"金融庁ガイドライン(?!.*リスクベース)", r"モニタリング(?!.*取引モニタリング)"]),
    ("rba", [r"リスクベース・アプローチ", r"リスクベースアプローチ", r"リスクの特定", r"リスクの評価", r"リスクの低減", r"リスク評価", r"特定事業者作成書面"]),
    ("edd", [r"外国PEPs", r"PEPs", r"厳格な顧客管理", r"厳格な取引時確認", r"EDD", r"ハイリスク取引"]),
    ("cdd", [r"顧客管理(?!.*態勢)", r"取引時確認", r"本人特定事項", r"本人確認", r"KYC", r"CDD", r"実質的支配者", r"特定取引", r"確認記録", r"取引記録"]),
    ("monitoring", [r"取引モニタリング", r"モニタリング・システム", r"異常取引の検知", r"シナリオ", r"敷居値"]),
    ("filtering", [r"取引フィルタリング", r"フィルタリング", r"制裁対象者.*リスト", r"リスト.*照合"]),
    ("sar", [r"疑わしい取引", r"届出", r"SAR", r"STR", r"参考事例"]),
    ("sanctions", [r"制裁", r"資産凍結", r"資産の凍結", r"財産凍結", r"財産の凍結"]),
    ("correspondent", [r"コルレス", r"海外送金", r"為替取引", r"送金取引"]),
    ("governance", [r"管理態勢", r"経営陣", r"3つの防衛線", r"防衛線", r"ガバナンス"]),
    ("training", [r"研修", r"教育訓練", r"職員の確保", r"育成"]),
    ("audit", [r"内部監査", r"監査部門", r"監査計画"]),
    ("data-mgmt", [r"データ管理", r"記録の保存", r"記録保存", r"確認記録.*保存", r"取引記録.*保存"]),
    ("it-system", [r"ITシステム", r"FinTech", r"RPA", r"AI", r"ブロックチェーン"]),
    ("ml-basics", [r"マネー・ローンダリングとは", r"マネー・ローンダリング（資金洗浄）", r"プレースメント", r"レイヤリング", r"インテグレーション", r"3段階", r"資金洗浄", r"犯罪収益移転危険度調査書", r"検挙事例", r"匿名・流動型", r"反社会的勢力", r"収益の移転.*危険", r"危険性.*商品", r"犯罪による収益"]),
]


def read_file(filepath):
    """Read file content."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def split_into_chapter_sections(text):
    """Split text by ===== markers into sections, returning dict of marker -> text."""
    sections = {}
    # Split by the ===== lines
    parts = re.split(r"^=====\s+(\S+)-.*?=====\s*$", text, flags=re.MULTILINE)
    # parts[0] is before first marker, parts[1] is first marker id, parts[2] is first section text, etc.
    for i in range(1, len(parts), 2):
        marker = parts[i]
        if i + 1 < len(parts):
            sections[marker] = parts[i + 1]
    return sections


def parse_questions_from_section(section_text, chapter_id):
    """Parse all questions from a chapter section text."""
    questions = []

    # Split by question markers like 問1-1:, 問2-1:, etc.
    chapter_num = chapter_id.replace("ch", "")
    # Pattern to match question headers: 問X-Y: title
    question_pattern = rf"問{chapter_num}-(\d+):\s*(.*?)$"

    # Find all question starts
    lines = section_text.split("\n")
    question_starts = []
    for i, line in enumerate(lines):
        m = re.match(question_pattern, line.strip())
        if m:
            question_starts.append((i, int(m.group(1)), m.group(2).strip()))

    for idx, (start_line, q_num, q_title) in enumerate(question_starts):
        # Determine end of this question block
        if idx + 1 < len(question_starts):
            end_line = question_starts[idx + 1][0]
        else:
            end_line = len(lines)

        # Extract the question block
        block_lines = lines[start_line:end_line]
        block_text = "\n".join(block_lines)

        # Parse the question
        q = parse_single_question(block_text, chapter_id, q_num, q_title)
        if q:
            questions.append(q)

    return questions


def parse_single_question(block_text, chapter_id, q_num, q_title):
    """Parse a single question block into structured data."""

    # Determine question type (最も適切/最も不適切)
    question_type = ""
    if "【最も適切なもの】" in block_text:
        question_type = "最も適切"
    elif "【最も不適切なもの】" in block_text:
        question_type = "最も不適切"

    # Extract the question text (between the type indicator and the first option)
    # The question text is after the 【...】 line and before the first 1) option
    lines = block_text.split("\n")

    # Find the question text
    question_text = ""
    option_start = -1
    type_found = False
    question_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("【最も") and stripped.endswith("】"):
            type_found = True
            continue
        if type_found and not stripped.startswith("1）") and not stripped.startswith("(a)"):
            if stripped:
                question_lines.append(stripped)
        elif stripped.startswith("1）") or stripped.startswith("(a)"):
            option_start = i
            break

    question_text = "\n".join(question_lines).strip()
    if not question_text:
        # Fallback: try finding the question between the header and options
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("1）") or stripped.startswith("(a)"):
                option_start = i
                break

    # Check if this is a multi-statement question (with (a), (b), (c) items and 1)-4) as count options)
    is_count_question = False
    sub_statements = []
    if "(a)" in block_text and "(b)" in block_text:
        is_count_question = True

    # Extract options and find correct answer
    options = []
    correct_answer = -1
    explanation = ""

    if is_count_question:
        # For count-type questions, collect (a), (b), (c) statements and the 1)-4) count options
        # The question text should include the sub-statements
        # Find the sub-statements and count options
        in_substmt = False
        in_options = False
        substmt_lines = []
        current_substmt = ""

        for i in range(option_start if option_start >= 0 else 0, len(lines)):
            stripped = lines[i].strip()

            if stripped.startswith("(a)") or stripped.startswith("(b)") or stripped.startswith("(c)") or stripped.startswith("(d)"):
                if current_substmt:
                    substmt_lines.append(current_substmt)
                current_substmt = stripped
                in_substmt = True
            elif in_substmt and not stripped.startswith("1）"):
                if stripped and not stripped.startswith("【解説】"):
                    current_substmt += " " + stripped
            elif stripped.startswith("1）"):
                if current_substmt:
                    substmt_lines.append(current_substmt)
                    current_substmt = ""
                in_substmt = False
                in_options = True
                # Fall through to handle options
                break

        # Add sub-statements to question text
        if substmt_lines:
            question_text = question_text + "\n" + "\n".join(substmt_lines)

        # Now find the 1)-4) count options
        for i in range(option_start if option_start >= 0 else 0, len(lines)):
            stripped = lines[i].strip()
            if re.match(r"^[1-4]）", stripped):
                has_star = "★正解" in stripped
                opt_text = stripped.replace("★正解", "").replace("　", " ").strip()
                options.append(opt_text)
                if has_star:
                    correct_answer = len(options) - 1
            if stripped.startswith("【解説】"):
                # Get explanation
                expl_start = lines.index(lines[i])
                expl_lines = []
                for j in range(expl_start + 1, len(lines)):
                    if lines[j].strip().startswith("────"):
                        break
                    expl_lines.append(lines[j].strip())
                explanation = " ".join(expl_lines).strip()
                break

    else:
        # Standard question with 1)-4) options
        current_option = ""
        collecting_explanation = False
        expl_lines = []

        for i in range(option_start if option_start >= 0 else 0, len(lines)):
            stripped = lines[i].strip()

            if collecting_explanation:
                if stripped.startswith("────"):
                    break
                if stripped:
                    expl_lines.append(stripped)
                continue

            if stripped.startswith("【解説】"):
                # Save last option
                if current_option:
                    has_star = "★正解" in current_option
                    opt_text = current_option.replace("★正解", "").replace("　", " ").strip()
                    options.append(opt_text)
                    if has_star:
                        correct_answer = len(options) - 1
                    current_option = ""
                collecting_explanation = True
                continue

            option_match = re.match(r"^([1-4]）)", stripped)
            if option_match:
                # Save previous option if exists
                if current_option:
                    has_star = "★正解" in current_option
                    opt_text = current_option.replace("★正解", "").replace("　", " ").strip()
                    options.append(opt_text)
                    if has_star:
                        correct_answer = len(options) - 1
                current_option = stripped
            elif current_option and stripped and not stripped.startswith("────"):
                current_option += " " + stripped

        if expl_lines:
            explanation = " ".join(expl_lines).strip()

    # Validate
    if len(options) != 4:
        print(f"  WARNING: {chapter_id} Q{q_num} has {len(options)} options (expected 4)")
        if len(options) == 0:
            return None

    if correct_answer == -1:
        print(f"  WARNING: {chapter_id} Q{q_num} has no correct answer marked")
        # Try to find correct answer from explanation
        expl_match = re.search(r"正解\s*([1-4]）|[1-4]\))", explanation)
        if expl_match:
            ans_str = expl_match.group(1)
            ans_num = int(re.search(r"[1-4]", ans_str).group()) - 1
            correct_answer = ans_num

    # Build the question ID
    q_id = f"std-{chapter_id}-{q_num:03d}"

    # Assign tags
    tags = assign_tags(question_text + " " + " ".join(options), chapter_id, q_title)

    # Truncate explanation if excessively long (keep first meaningful part)
    if len(explanation) > 1500:
        # Find a reasonable break point
        explanation = explanation[:1500] + "..."

    return {
        "id": q_id,
        "question": question_text,
        "options": options,
        "answer": correct_answer,
        "explanation": explanation,
        "tags": tags,
    }


def assign_tags(text, chapter_id, q_title):
    """Assign topic tags based on question content."""
    tags = set()

    # Chapter-based default tags
    chapter_default_tags = {
        "ch1": ["ml-basics"],
        "ch2": ["fatf"],
        "ch3": ["domestic-law"],
        "ch4": ["rba"],
        "ch5": ["governance"],
        "ch6": ["cdd"],
        "ch7": ["sar"],
    }

    combined_text = text + " " + q_title

    # Apply tag rules
    for tag, patterns in TAG_RULES:
        for pattern in patterns:
            if re.search(pattern, combined_text):
                tags.add(tag)
                break

    # If no specific tags found, use chapter default
    if not tags:
        tags.update(chapter_default_tags.get(chapter_id, []))

    # Ensure chapter-appropriate default is included for borderline cases
    ch_defaults = chapter_default_tags.get(chapter_id, [])

    # Some specific overrides based on question title
    if "テロ資金" in q_title or "テロ" in q_title:
        tags.add("tf")
    if "反社会的勢力" in q_title:
        tags.add("ml-basics")
    if "コルレス" in q_title or "海外送金" in q_title or "送金取引" in q_title:
        tags.add("correspondent")
    if "外国PEPs" in q_title or "PEPs" in q_title:
        tags.add("edd")
    if "実質的支配者" in q_title:
        tags.add("cdd")
    if "モニタリング" in q_title and "取引" in q_title:
        tags.add("monitoring")
    if "フィルタリング" in q_title and "取引" in q_title:
        tags.add("filtering")
    if "3つの防衛線" in q_title or "防衛線" in q_title:
        tags.add("governance")
    if "内部監査" in q_title or "監査" in q_title:
        tags.add("audit")
    if "研修" in q_title or "育成" in q_title or "職員" in q_title:
        tags.add("training")
    if "ITシステム" in q_title or "FinTech" in q_title:
        tags.add("it-system")
    if "データ管理" in q_title or "データ" in q_title:
        tags.add("data-mgmt")
    if "記録の保存" in q_title or "記録保存" in q_title:
        tags.add("data-mgmt")
    if "グループベース" in q_title:
        tags.add("governance")
    if "確認記録" in q_title or "取引記録" in q_title:
        tags.add("data-mgmt")
    if "特定事業者作成書面" in q_title:
        tags.add("rba")

    return sorted(list(tags))


def main():
    print("Reading source files...")
    text1 = read_file(FILE1)
    text2 = read_file(FILE2)

    print("Splitting into chapter sections...")
    sections1 = split_into_chapter_sections(text1)
    sections2 = split_into_chapter_sections(text2)

    print(f"  File 1 sections: {list(sections1.keys())}")
    print(f"  File 2 sections: {list(sections2.keys())}")

    all_sections = {**sections1, **sections2}

    chapters = []
    total_questions = 0

    for ch_id in ["ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7"]:
        info = CHAPTER_INFO[ch_id]
        marker = info["file_marker"]

        if marker not in all_sections:
            print(f"  ERROR: Chapter {ch_id} marker '{marker}' not found!")
            continue

        section_text = all_sections[marker]
        print(f"\nParsing {ch_id} ({info['name']})...")
        questions = parse_questions_from_section(section_text, ch_id)
        print(f"  Found {len(questions)} questions")
        total_questions += len(questions)

        # Verify all questions have valid answers
        for q in questions:
            if q["answer"] == -1:
                print(f"  ERROR: {q['id']} has no valid answer!")

        chapters.append({
            "id": ch_id,
            "name": info["name"],
            "questions": questions,
        })

    # Build output
    output = {
        "id": "standard",
        "name": "AML/CFTスタンダードコース",
        "chapters": chapters,
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # Write output
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Total questions parsed: {total_questions}")
    print(f"Output written to: {OUTPUT}")

    # Summary by chapter
    print(f"\nChapter summary:")
    for ch in chapters:
        print(f"  {ch['id']}: {ch['name']} - {len(ch['questions'])} questions")

    # Verify expected counts
    expected = {"ch1": 13, "ch2": 16, "ch3": 12, "ch4": 23, "ch5": 13, "ch6": 18, "ch7": 22}
    total_expected = sum(expected.values())
    print(f"\nExpected total: {total_expected}")

    mismatches = False
    for ch in chapters:
        exp = expected.get(ch["id"], 0)
        actual = len(ch["questions"])
        if actual != exp:
            print(f"  MISMATCH: {ch['id']} expected {exp}, got {actual}")
            mismatches = True

    if not mismatches:
        print("  All chapter counts match expected values!")

    return 0 if total_questions == total_expected else 1


if __name__ == "__main__":
    sys.exit(main())
