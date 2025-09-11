import os
from pathlib import Path
from typing import List, Optional

# --- Globals ---
IGNORE = {
    ".git", "__pycache__", ".venv", "node_modules",
    ".env", ".md", "target", ".lock", ".cargo", ".rustup", ".csv", "public",
    "migrations"
}


# --- Gitignore Support ---

def find_gitignore(start: Path) -> Path | None:
    """Search upwards for a .gitignore file."""
    current = start.resolve()
    for parent in [current] + list(current.parents):
        candidate = parent / ".gitignore"
        if candidate.exists():
            return candidate
    return None


def load_gitignore(start: Path, gitignore_path: Optional[Path] = None) -> List[str]:
    """Load patterns from either a given .gitignore or the nearest one."""
    gi = gitignore_path if gitignore_path else find_gitignore(start)
    if not gi or not gi.exists():
        return []
    patterns = []
    with open(gi, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def should_ignore(path: Path, patterns: List[str]) -> bool:
    """Check if path matches gitignore-like patterns."""
    for pat in patterns:
        try:
            if path.match(pat):
                return True
        except Exception:
            continue
    return False


# --- File Helpers ---

def get_filecontent(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        return f"[binary file skipped: {path.name}]"


def detect_lang(path: Path) -> str:
    ext_map = {
        ".py": "python",
        ".rs": "rust",
        ".ts": "typescript",
        ".js": "javascript",
        ".html": "html",
        ".css": "css",
        ".json": "json",
        ".toml": "toml",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".md": "markdown",
        ".sh": "bash",
        ".vue": "vue",
    }
    return ext_map.get(path.suffix, "")


def get_emoji(path: Path, is_dir: bool = False) -> str:
    if is_dir:
        return "📂"
    emoji_map = {
        ".py": "🐍",
        ".rs": "🦀",
        ".ts": "📜",
        ".js": "📜",
        ".html": "🌐",
        ".css": "🎨",
        ".json": "📄",
        ".toml": "⚙️",
        ".yml": "📄",
        ".yaml": "📄",
        ".md": "📝",
        ".sh": "🖥️",
        ".vue": "🟩",
    }
    return emoji_map.get(path.suffix, "📎")


# --- Markdown Generation ---

def markdown_file(path: Path) -> str:
    lang = detect_lang(path)
    code_fence = f"```{lang}" if lang else "```"
    return f"#### {get_emoji(path)} {path.name}\n\n{code_fence}\n{get_filecontent(path)}\n```"


def walk_directory(root: Path, patterns: List[str], level: int = 1) -> str:
    """Recursively walk directory and build markdown with headers + emojis."""
    parts: List[str] = []
    header_level = min(level, 3)

    if level <= 3:
        parts.append(f"{'#' * header_level} {get_emoji(root, True)} {root.name}")

    for item in sorted(root.iterdir()):
        if item.name in IGNORE:
            continue
        if should_ignore(item, patterns):
            continue

        if item.is_dir():
            parts.append(walk_directory(item, patterns, level + 1))
        else:
            parts.append(markdown_file(item))

    return "\n\n".join(parts)


def tree_view(root: Path, patterns: List[str], prefix: str = "") -> str:
    """Generate ASCII tree view with emojis."""
    entries = [
        e for e in sorted(root.iterdir())
        if e.name not in IGNORE and not should_ignore(e, patterns)
    ]
    tree_lines = []
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            tree_lines.append(f"{prefix}{connector}{get_emoji(entry, True)} {entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            tree_lines.append(tree_view(entry, patterns, prefix + extension))
        else:
            tree_lines.append(f"{prefix}{connector}{get_emoji(entry)} {entry.name}")
    return "\n".join(tree_lines)


def make_markdown(directory: Path = Path.cwd(), gitignore_path: Optional[Path] = None) -> str:
    patterns = load_gitignore(directory, gitignore_path)
    tree = f"\n{directory.name}/\n{tree_view(directory, patterns)}\n"
    structure = walk_directory(directory, patterns)
    return tree + "\n\n" + structure


def save(content, path="Project.md"):
    with open(path, 'w') as file:
        file.write(content)


if __name__ == "__main__":
    # Example: save(make_markdown(Path("frontend"),
    gitignore_path = Path(".gitignore")
    FRONTEND_PATH = Path("Operations/frontend")
    BACKEND_PATH = Path("Operations/backend")
    save(make_markdown(FRONTEND_PATH,gitignore_path=gitignore_path), "frontend.md")
    save(make_markdown(BACKEND_PATH,gitignore_path=gitignore_path), "backend.md")

