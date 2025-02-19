import subprocess
import sys
from typing import Union

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

exceptions = ["index", "version-history"]

def on_page_markdown(
        markdown: str, page: Page, config: MkDocsConfig, files: Files
) -> Union[str, None]:
    git_log_output = subprocess.check_output(["git", "log", "--oneline", "--", page.file.abs_src_path]).decode(sys.stdout.encoding)
    if page.file.name in exceptions:
        return markdown
    else:
        commits_section = "\n\n## Page History \n\n"
        for line in git_log_output.splitlines():
            line_components = line.split()
            commit_hash = line_components[0]
            commit_message = line_components[1:]
            commits_section += "- <a href=\"https://github.com/Minirogue/shawns-guide-to-code/commit/" + commit_hash +"\">" + commit_hash + "</a> " + " ".join(commit_message)+ "\n"
        return markdown + commits_section

