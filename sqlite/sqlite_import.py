#!/usr/bin/env python3
"""将 Politics-Obsidian-Note vault 导入 SQLite。

路径全部从 __file__ 派生，复制到任何位置都能跑。
输出: sqlite/politics.db（与脚本同目录）。
"""
import os
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent
DB_PATH = HERE / "politics.db"

SUBJECTS = {
    "马原": "马克思主义基本原理",
    "毛中特": "毛泽东思想和中国特色社会主义理论体系概论",
    "思修": "思想道德与法治",
    "史纲": "中国近代史纲要",
    "新思想": "习近平新时代中国特色社会主义思想概论",
}

SCHEMA = """
DROP TABLE IF EXISTS note_links;
DROP TABLE IF EXISTS note_tags;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS subjects;

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    score_info TEXT,
    file_path TEXT
);

CREATE TABLE sections (
    id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    parent_id INTEGER REFERENCES sections(id),
    level INTEGER NOT NULL,
    code TEXT,
    title TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    section_id INTEGER REFERENCES sections(id),
    note_type TEXT NOT NULL,
    seq_number INTEGER,
    title TEXT NOT NULL,
    file_path TEXT UNIQUE NOT NULL,
    first_line_tag TEXT,
    exam_type TEXT,
    importance TEXT,
    raw_markdown TEXT NOT NULL
);

CREATE TABLE note_tags (
    note_id INTEGER NOT NULL REFERENCES notes(id),
    tag TEXT NOT NULL,
    PRIMARY KEY (note_id, tag)
);

CREATE TABLE note_links (
    id INTEGER PRIMARY KEY,
    source_note_id INTEGER NOT NULL REFERENCES notes(id),
    target_kind TEXT NOT NULL,
    target_note_id INTEGER REFERENCES notes(id),
    target_path TEXT,
    link_text TEXT,
    raw TEXT NOT NULL
);

CREATE INDEX idx_sections_subject ON sections(subject_id);
CREATE INDEX idx_sections_parent ON sections(parent_id);
CREATE INDEX idx_notes_subject ON notes(subject_id);
CREATE INDEX idx_notes_section ON notes(section_id);
CREATE INDEX idx_notes_seq ON notes(subject_id, seq_number);
CREATE INDEX idx_note_links_source ON note_links(source_note_id);
CREATE INDEX idx_note_links_target ON note_links(target_note_id);
"""

NOTE_RE = re.compile(r"^(考点|总结&扩展)(\d+)\s*(.+)\.md$")
TAG_RE = re.compile(r"(?<!#)#(?!#)([^\s#][^#|\\*\[\]`\n]*)")
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
FL_TAG_RE = re.compile(r"^#(马原|毛中特|思修|史纲|新思想)(选择题|分析题|重点|非重点)$")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".canvas")
SUBJECT_INDEX_NAMES = set(SUBJECTS.values())


def parse_first_line_tag(first_line: str):
    if not first_line.startswith("#"):
        return None, None, None
    tag = first_line.split()[0]
    m = FL_TAG_RE.match(tag)
    if m:
        kind = m.group(2)
        exam = kind if kind in ("选择题", "分析题") else None
        imp = kind if kind in ("重点", "非重点") else None
        return tag, exam, imp
    if tag in ("#重点", "#非重点"):
        return tag, None, tag[1:]
    if tag in ("#选择题", "#分析题"):
        return tag, tag[1:], None
    return tag, None, None


def parse_wikilink(raw: str):
    if "|" in raw:
        target, alias = raw.split("|", 1)
        return target.strip(), alias.strip()
    return raw.strip(), None


def sort_key_dir(d: Path):
    name = d.name
    parts = name.split(" ", 1)
    prefix = parts[0]
    if prefix.isdigit():
        return (0, int(prefix), name)
    if len(prefix) == 1 and prefix.isalpha() and prefix.isascii():
        return (0, ord(prefix), name)
    return (1, 0, name)


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    cur = conn.cursor()

    # 1. subjects
    for code, name in SUBJECTS.items():
        idx_file = VAULT / code / f"{name}.md"
        score_info = None
        if idx_file.exists():
            first = idx_file.read_text(encoding="utf-8").splitlines()[0].strip()
            m = re.search(r"(\d+)\s*分", first)
            if m:
                score_info = f"{m.group(1)}分"
        cur.execute(
            "INSERT INTO subjects(code, name, score_info, file_path) VALUES (?,?,?,?)",
            (code, name, score_info, str(idx_file.relative_to(VAULT))),
        )

    subjects = {row["code"]: row["id"] for row in cur.execute("SELECT id, code FROM subjects")}

    # 2. sections (编 → 章, 目录驱动)
    section_cache = {}
    order = {}

    def next_order(subj_id):
        order[subj_id] = order.get(subj_id, 0) + 1
        return order[subj_id]

    for code in SUBJECTS:
        subj_id = subjects[code]
        subj_dir = VAULT / code
        pian_dirs = sorted([d for d in subj_dir.iterdir() if d.is_dir()], key=sort_key_dir)
        for pian in pian_dirs:
            pian_rel = str(pian.relative_to(VAULT))
            parts = pian.name.split(" ", 1)
            sec_code = parts[0] if len(parts) == 2 else None
            sec_title = parts[1] if len(parts) == 2 else pian.name
            cur.execute(
                "INSERT INTO sections(subject_id,parent_id,level,code,title,sort_order) VALUES (?,?,?,?,?,?)",
                (subj_id, None, 1, sec_code, sec_title, next_order(subj_id)),
            )
            pian_id = cur.lastrowid
            section_cache[(subj_id, pian_rel)] = pian_id

            zhang_dirs = sorted([d for d in pian.iterdir() if d.is_dir()], key=sort_key_dir)
            for zhang in zhang_dirs:
                zhang_rel = str(zhang.relative_to(VAULT))
                parts2 = zhang.name.split(" ", 1)
                z_code = parts2[0] if len(parts2) == 2 else None
                z_title = parts2[1] if len(parts2) == 2 else zhang.name
                cur.execute(
                    "INSERT INTO sections(subject_id,parent_id,level,code,title,sort_order) VALUES (?,?,?,?,?,?)",
                    (subj_id, pian_id, 2, z_code, z_title, next_order(subj_id)),
                )
                zhang_id = cur.lastrowid
                section_cache[(subj_id, zhang_rel)] = zhang_id

    # 3. notes
    note_count = 0
    skipped = []
    for md_file in sorted(VAULT.rglob("*.md")):
        if any(p in md_file.parts for p in (".git", ".obsidian")):
            continue
        rel = md_file.relative_to(VAULT)
        parts = rel.parts
        if len(parts) < 3:
            continue
        subj_code = parts[0]
        if subj_code not in SUBJECTS:
            continue
        if md_file.stem == SUBJECTS[subj_code]:
            continue

        m = NOTE_RE.match(md_file.name)
        if not m:
            skipped.append(str(rel))
            continue
        note_type = m.group(1)
        seq_number = int(m.group(2))
        title = m.group(3).strip()

        parent_rel = str(rel.parent)
        subj_id = subjects[subj_code]
        section_id = section_cache.get((subj_id, parent_rel))

        content = md_file.read_text(encoding="utf-8")
        first_line = content.splitlines()[0].strip() if content else ""
        fl_tag, exam_type, importance = parse_first_line_tag(first_line)

        cur.execute(
            """INSERT INTO notes(subject_id,section_id,note_type,seq_number,title,file_path,
                                 first_line_tag,exam_type,importance,raw_markdown)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (subj_id, section_id, note_type, seq_number, title, str(rel),
             fl_tag, exam_type, importance, content),
        )
        note_count += 1

    # 4. tags (inline #tags from body) — fetchall first to avoid cursor reuse bug
    tag_count = 0
    rows = cur.execute("SELECT id, raw_markdown FROM notes").fetchall()
    for note in rows:
        seen = set()
        for tag in TAG_RE.findall(note["raw_markdown"]):
            tag = tag.strip().rstrip(".,;:!?，。；：！？")
            if not tag or len(tag) > 50 or tag in seen:
                continue
            seen.add(tag)
            try:
                cur.execute("INSERT OR IGNORE INTO note_tags(note_id,tag) VALUES (?,?)",
                            (note["id"], tag))
                tag_count += cur.rowcount
            except sqlite3.IntegrityError:
                pass

    # 5. links
    link_count = 0
    rows = cur.execute("SELECT id, raw_markdown FROM notes").fetchall()
    for note in rows:
        for raw_link in WIKILINK_RE.findall(note["raw_markdown"]):
            target, alias = parse_wikilink(raw_link)
            target_path = target
            target_note_id = None
            kind = "other"

            if target.lower().endswith(IMAGE_EXTS):
                kind = "image"
            elif target.startswith(("http://", "https://", "mailto:")):
                kind = "external"
            else:
                base = target.split("#", 1)[0].strip()
                guess = base if base.lower().endswith(".md") else base + ".md"
                row = cur.execute("SELECT id FROM notes WHERE file_path = ?", (guess,)).fetchone()
                if not row:
                    basename = guess.replace("\\", "/").rsplit("/", 1)[-1]
                    matches = cur.execute(
                        "SELECT id FROM notes WHERE file_path LIKE ? OR file_path LIKE ?",
                        (f"%/{basename}", f"%\\{basename}"),
                    ).fetchall()
                    if len(matches) == 1:
                        row = matches[0]
                    elif len(matches) > 1:
                        kind = "ambiguous"
                        target_path = guess
                        target_note_id = None
                if row and kind != "ambiguous":
                    kind = "note"
                    target_note_id = row["id"]
                    target_path = None
                elif kind != "ambiguous":
                    if "#" in target:
                        kind = "subject_index"
                    elif base in SUBJECT_INDEX_NAMES or base.removesuffix(".md") in SUBJECT_INDEX_NAMES:
                        kind = "subject_index"
                    else:
                        kind = "other"

            cur.execute(
                """INSERT INTO note_links(source_note_id,target_kind,target_note_id,
                                          target_path,link_text,raw) VALUES (?,?,?,?,?,?)""",
                (note["id"], kind, target_note_id, target_path, alias, "[[" + raw_link + "]]"),
            )
            link_count += 1

    conn.commit()

    counts = {
        "subjects": cur.execute("SELECT COUNT(*) FROM subjects").fetchone()[0],
        "sections": cur.execute("SELECT COUNT(*) FROM sections").fetchone()[0],
        "notes (考点+总结)": cur.execute("SELECT COUNT(*) FROM notes").fetchone()[0],
        "note_tags": cur.execute("SELECT COUNT(*) FROM note_tags").fetchone()[0],
        "note_links": cur.execute("SELECT COUNT(*) FROM note_links").fetchone()[0],
    }
    print("入库结果：")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"\n跳过的非考点/总结 md 文件: {len(skipped)}")
    if skipped[:10]:
        for s in skipped[:10]:
            print(f"  - {s}")
    print(f"\nDB: {DB_PATH}  ({os.path.getsize(DB_PATH)/1024:.1f} KB)")


if __name__ == "__main__":
    main()