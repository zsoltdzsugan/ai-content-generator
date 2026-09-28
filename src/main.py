import os
import sys
import argparse
from uuid import UUID
from pipeline.research_process import ResearchProcess
from pipeline.web_process import WebProcess
from pipeline.html_process import HTMLProcess

def generate(topic: str, prompt: str = "") -> None:
    url = "https://hu.ign.com/minecraft/114201/14-ev-utan-uj-dimenzio-erkezik-a-minecraftba-amit-eloszor-egy-masik-jatekban-lehet-majd-bejarni"
    research_process = ResearchProcess()
    research_process.run(topic, url, prompt)


def main():
    print("Content Generator AI - START")

    parser = argparse.ArgumentParser(prog="cgai", description="Content Generator AI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_gen = subparsers.add_parser("generate", aliases=["g", "gen"], help="Generate content")
    parser_gen.add_argument("topic", type=str, help="Content topic")
    parser_gen.add_argument("-p", "--prompt", type=str, default="", help="Optional additional prompt")

    parser_rm = subparsers.add_parser("remove", aliases=["r", "rm"], help="Remove content")
    parser_rm.add_argument("id", type=UUID, help="Content UUID")

    parser_list = subparsers.add_parser("list", aliases=["l"], help="List all content")
    parser_list.add_argument("topic", type=str, nargs="?", help="Optional content topic")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    match (args.command):
        case "g" | "gen" | "generate":
                print(f"Generate for: {args.topic} with prompt: {args.prompt}")
                generate(args.topic, args.prompt)
        case "r" | "rm" | "remove":
            print(f"Remove content: {args.id}")
        case "l" | "list":
            if args.topic is not None:
                print(f"List content for: {args.topic}")
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
