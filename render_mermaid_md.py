import re
import shutil
import subprocess
import sys
from pathlib import Path

print("SCRIPT STARTED")

MERMAID_PATTERN = re.compile(
    r"```mermaid\s*\n(.*?)\n```",
    re.DOTALL | re.IGNORECASE
)

MMDC_PATH = shutil.which("mmdc") or shutil.which("mmdc.cmd")
PANDOC_PATH = "pandoc"
PDF_ENGINE = "xelatex"

if not MMDC_PATH:
    print("[ERROR] 'mmdc' not found in PATH. Install it with: npm install -g @mermaid-js/mermaid-cli")
    sys.exit(1)


def run(command, shell=False):
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        shell=shell
    )


def process_md(md_path: Path):
    print(f"\n=== Processing: {md_path.name} ===")

    text = md_path.read_text(encoding="utf-8")
    base = md_path.stem
    assets_dir = md_path.parent / f"{base}_assets"
    assets_dir.mkdir(exist_ok=True)

    count = 0
    mermaid_errors = []

    def replace(match):
        nonlocal count
        count += 1

        mermaid_content = match.group(1).strip()
        mmd_name = f"{base}_diagram_{count}.mmd"
        img_name = f"{base}_diagram_{count}.png"

        mmd_path = assets_dir / mmd_name
        img_path = assets_dir / img_name

        mmd_path.write_text(mermaid_content, encoding="utf-8")

        mmdc_command = [
            MMDC_PATH,
            "-i", str(mmd_path),
            "-o", str(img_path)
        ]

        result = run(mmdc_command)

        if result.returncode != 0:
            mermaid_errors.append(count)
            print(f"[ERROR] Mermaid failed on block {count} of {md_path.name}")
            if result.stderr:
                print(result.stderr)
            return f"\n\n[ERROR: could not render Mermaid diagram {count}]\n\n"

        relative_path = f"{assets_dir.name}/{img_name}"
        return f"![Diagram {count}]({relative_path})"

    new_text = MERMAID_PATTERN.sub(replace, text)

    rendered_md_path = md_path.with_name(f"{base}_rendered.md")
    rendered_md_path.write_text(new_text, encoding="utf-8")
    print(f"[OK] Rendered Markdown: {rendered_md_path.name}")

    pdf_path = md_path.with_suffix(".pdf")

    pandoc_command = [
        PANDOC_PATH,
        str(rendered_md_path),
        "--pdf-engine=" + PDF_ENGINE,
        "-o",
        str(pdf_path)
    ]

    pdf_result = run(pandoc_command)

    if pdf_result.returncode != 0:
        print(f"[ERROR] Pandoc failed on {md_path.name}")
        if pdf_result.stderr:
            print(pdf_result.stderr)
        return

    print(f"[OK] PDF generated: {pdf_path.name}")

    if mermaid_errors:
        print(f"[WARNING] {md_path.name} had errors in Mermaid blocks: {mermaid_errors}")


def main():
    md_files = [
        p for p in Path(".").glob("*.md")
        if not p.name.endswith("_rendered.md")
    ]

    print("Files found:", [f.name for f in md_files])

    if not md_files:
        print("No .md files found.")
        return

    for md_path in md_files:
        process_md(md_path)


if __name__ == "__main__":
    main()
