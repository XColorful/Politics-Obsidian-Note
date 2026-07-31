# SQLite 镜像

把 Obsidian vault 的 691 个 markdown 笔记结构化导入 SQLite，方便用 SQL 抽取背诵题目、统计标签、做关系图查询。

## 文件清单

| 文件 | 用途 | 大小 |
|---|---|---|
| `sqlite_import.py` | 从 vault 重建 SQLite 的脚本（Python 3.10+，仅标准库） | — |
| `politics.db` | 预生成的数据库，开箱即用 | ~1.4 MB |

## 用法

### 直接查询

```bash
# 命令行
sqlite3 sqlite/politics.db "SELECT code, COUNT(*) FROM subjects s JOIN notes n ON n.subject_id=s.id GROUP BY code"

# 交互式
sqlite3 sqlite/politics.db
sqlite> .schema
sqlite> .tables
sqlite> SELECT title FROM notes WHERE exam_type='选择题' AND importance IS NULL LIMIT 5;
```

### 重新生成数据库

vault 笔记更新后，重跑脚本即可重建：

```bash
cd sqlite
python sqlite_import.py
```

脚本路径全部从 `__file__` 派生，vault 复制到任何位置都能跑。

## Schema（5 张表）

```
subjects           学科(5) — code/name/score_info/file_path
  ├─ sections      章节 — 自引用层级(level=1 编 / level=2 章)
  └─ notes         笔记(682) — note_type='考点' or '总结&扩展'
       ├─ note_tags    正文 #tag 关联
       └─ note_links   [[wikilink]] 关系图
```

| 表 | 行数 | 备注 |
|---|---|---|
| `subjects` | 5 | 马原/毛中特/思修/史纲/新思想 |
| `sections` | 70 | 20 编 + 50 章 |
| `notes` | 682 | 623 考点 + 59 总结&扩展 |
| `note_tags` | ~2 445 | 内联 `#tag` 全文拆出 |
| `note_links` | ~1 185 | `[[wiki]]` 关系图（note / subject_index / image / other） |

`notes.raw_markdown` 保留全文，`first_line_tag`/`exam_type`/`importance` 从首行 `#xxx选择题` / `#xxx非重点` 解析。

## 示例查询

### 抽背：列出某学科全部"选择题"考点

```sql
SELECT seq_number, title
FROM notes n JOIN subjects s ON s.id = n.subject_id
WHERE s.code = '马原' AND n.note_type = '考点' AND n.exam_type = '选择题'
ORDER BY n.seq_number;
```

### 找最热门的考点（关系图枢纽）

```sql
SELECT s.code, n.title, COUNT(*) AS refs
FROM note_links l
JOIN notes n ON n.id = l.target_note_id
JOIN subjects s ON s.id = n.subject_id
WHERE l.target_kind = 'note'
GROUP BY l.target_note_id
ORDER BY refs DESC
LIMIT 10;
```

### 全文搜索（SQLite FTS5 扩展可选）

```sql
CREATE VIRTUAL TABLE notes_fts USING fts5(title, raw_markdown, content='notes', content_rowid='id');
INSERT INTO notes_fts(notes_fts) VALUES('rebuild');
SELECT title FROM notes_fts WHERE notes_fts MATCH '实事求是' LIMIT 5;
```

### 找出某考点的所有前置/后续

```sql
-- 考点14 (主观能动性) → 出链
SELECT n2.title, l.target_kind
FROM note_links l
JOIN notes n1 ON n1.id = l.source_note_id
JOIN notes n2 ON n2.id = l.target_note_id
WHERE n1.subject_id = 1 AND n1.seq_number = 14 AND l.target_kind = 'note';

-- 反向：哪些笔记引用了考点14
SELECT n1.title
FROM note_links l
JOIN notes n1 ON n1.id = l.source_note_id
JOIN notes n2 ON n2.id = l.target_note_id
WHERE n2.subject_id = 1 AND n2.seq_number = 14 AND l.target_kind = 'note';
```

## 注意事项

- 数据库是 **vault 当时状态的快照**。笔记更新后必须重跑脚本。
- 入库会 drop 所有 `note_*` / `sections` / `subjects` 表，**不要在同一 db 里放别的数据**。
- 部分笔记首行没有 `#xxx选择题` 标签，`exam_type`/`importance` 列为空——正文里的标签仍在 `note_tags` 表里。

## 许可证

本目录新增内容延续上游 [CC BY-SA 4.0](../../LICENSE) 许可证。脚本和派生数据库均为 vault 笔记的派生作品。