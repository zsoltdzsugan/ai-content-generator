import os
import sys
import shutil
import argparse
from uuid import UUID
from pipeline.research_process import ResearchProcess
from pipeline.web_process import WebProcess
from pipeline.html_process import HTMLProcess
from pipeline.llm_process import LLMProcess
from pipeline.markdown_process import MarkdownProcess
from models.research import Research
from utils.progress import Progress

def copy_static_to_public(static: str = "static", public: str = "docs") -> None:
    if not os.path.exists(static):
        raise Exception("static folder not found")

    if os.path.exists(public):
        shutil.rmtree(public)
    os.mkdir(public)

    copy_directory(static, public)

def copy_directory(from_directory, to_directory) -> None:
    for item in os.listdir(from_directory):
        from_path: str = os.path.join(from_directory, item)
        to_path: str = os.path.join(to_directory, item)

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            if not os.path.exists(to_path):
                os.mkdir(to_path)
            copy_directory(from_path, to_path)


def generate(query: str, category: str = "", user_prompt: str = "") -> None:
    progress: Progress = Progress(3)
    progress.start("Researching...")

    research_process: ResearchProcess = ResearchProcess()
    try:
        research: Research = research_process.run(query, category)
    except Exception as e:
        progress.finish("Failed")
        raise RuntimeError("Research failed") from e

    progress.finish()
    progress.start("Generating markdown...")

    llm_process: LLMProcess = LLMProcess()
    try:
        md: str = llm_process.generate_markdown(research, user_prompt)
    except Exception as e:
        progress.finish("Failed")
        raise RuntimeError("Markdown generation failed") from e

    progress.finish()
    progress.start("Saving markdown article...")

    md_process: MarkdownProcess = MarkdownProcess()
    try:
        md_process.save(md)
    except Exception as e:
        progress.finish("Failed")
        raise RuntimeError("Markdown article failed to save") from e

    progress.finish()

def publish(basepath: str = "/") -> None:
    basepath = basepath.rstrip("/") + "/"

    progress: Progress = Progress(2)
    progress.start("Copying static files")

    try:
        copy_static_to_public("static", "docs")
    except Exception as e:
        progress.finish("Failed")
        raise RuntimeError("Could not copy static files") from e

    progress.finish()
    progress.start("Generating pages")

    html_process: HTMLProcess = HTMLProcess()

    try:
        html_process.generate_index(basepath)
        html_process.generate_pages_recursive("content", "src/template.html", "docs", basepath)
    except Exception as e:
        progress.finish("Failed")
        raise RuntimeError("Could not generate pages") from e

    progress.finish()


def main() -> None:
    print("Content Generator AI - START")

    parser = argparse.ArgumentParser(prog="cgai", description="Content Generator AI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_pub = subparsers.add_parser("publish", aliases=["p"], help="Publish all content")
    parser_pub.add_argument("basepath", type=str, help="Publish path")

    parser_gen = subparsers.add_parser("generate", aliases=["g", "gen"], help="Generate content")
    parser_gen.add_argument("query", type=str, help="Query content")
    parser_gen.add_argument("-c", "--category", type=str, default="", help="Optional query category to look for [general, news]")
    parser_gen.add_argument("-p", "--prompt", type=str, default="", help="Optional additional prompt")

    parser_rm = subparsers.add_parser("remove", aliases=["r", "rm"], help="Remove content")
    parser_rm.add_argument("id", type=UUID, help="Content UUID")

    parser_list = subparsers.add_parser("list", aliases=["l"], help="List all content")
    parser_list.add_argument("query", type=str, nargs="?", help="Optional content query")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    match (args.command):
        case "p" | "publish":
            if not args.basepath:
                parser.print_help()
                sys.exit(1)
            publish(args.basepath)

        case "g" | "gen" | "generate":
            print(f"Generate for: {args.query} in {args.category} with prompt: {args.prompt}")
            generate(args.query, args.category, args.prompt)

        case "r" | "rm" | "remove":
            print(f"Remove content: {args.id}")
        case "l" | "list":
            if args.query is not None:
                print(f"List content for: {args.query}")
            else:
                print(f"List all content")
        case _:
            parser.print_help()
            sys.exit(1)

    if args.verbose:
        print(f"User prompt: {args}")

    print("Content Generator AI - END")

if __name__ == "__main__":
    main()
