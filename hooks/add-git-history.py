import re
import subprocess
import sys
from typing import Union

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from typing_extensions import Match

exceptions = []  # ["index", "version-history"]


def on_page_markdown(
        markdown: str, page: Page, config: MkDocsConfig, files: Files
) -> Union[str, None]:
    if page.file.name in exceptions:
        return markdown
    else:
        git_hashes = (subprocess.check_output(["git", "log", "--format=%h", "--", page.file.abs_src_path])
                      .decode(sys.stdout.encoding)
                      .splitlines())
        commits_section = "\n\n## Page History \n\n"
        for commit_hash in git_hashes:
            commit_link = "<a href=\"https://github.com/Minirogue/shawns-guide-to-code/commit/" + commit_hash + "\">" + commit_hash + "</a>"
            commit_info = (subprocess.check_output(["git", "show", "--no-patch", "--format=\"%cs %h %s\"", commit_hash])
                           .decode(sys.stdout.encoding))
            commit_info = re.sub("\(#\\d+\)", lambda x: get_pr_link(x), commit_info) # add link to PR
            commits_section += ("- " + commit_info.replace(commit_hash, commit_link)
                                .replace("\"", ""))  # remove the vestigial quotation marks the formatting
        return markdown + commits_section


def get_pr_link(match: Match[str]) -> str:
    pr_number = match.group()[2:-1]
    replacement_string = "(<a href=\"https://github.com/Minirogue/shawns-guide-to-code/pull/" + pr_number + "\">#" + pr_number + "</a>)"
    return replacement_string
