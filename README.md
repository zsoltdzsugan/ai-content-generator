# AI Content Generator

A Python content pipeline that researches gaming topics, generates articles with an LLM, and turns the generated Markdown into a static website.

## How it works

```text
Topic
  ↓
Web research
  ↓
Source evaluation
  ↓
LLM article generation
  ↓
Markdown
  ↓
content/blog/
  ↓
HTML generation
  ↓
docs/
  ↓
GitHub Pages
```

Generated Markdown is kept in `content/blog/` as the source content. `docs/` contains the generated website.

## Requirements

* Python 3.13+
* [uv](https://docs.astral.sh/uv/)
* Tavily API key
* OpenRouter API key

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```env
TAVILY_API_KEY=your_tavily_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

### Generate an article

```bash
uv run src/main.py generate "Elden Ring DLC"
```

Optional category:

```bash
uv run src/main.py generate "Elden Ring DLC" --category news
```

Optional instructions:

```bash
uv run src/main.py generate "Elden Ring DLC" \
    --prompt "Focus on new gameplay mechanics."
```

The generated article is saved to:

```text
content/blog/
```

## GitHub Pages Setup

The generated `docs/` directory is used as the GitHub Pages source.

### 1. Create a GitHub repository

Create a repository on GitHub and push the project to it.

For a repository named `ai-content-generator`, the GitHub Pages URL will be:

```text
https://YOURGITHUBUSERNAME.github.io/ai-content-generator/
```

### 2. Enable GitHub Pages

In your GitHub repository:

1. Open **Settings**.
2. Select **Pages** from the left sidebar.
3. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
4. Select your main branch, usually:

```text
main
```

5. Select the `/docs` folder.
6. Click **Save**.

GitHub Pages will then publish the contents of `docs/`.

### 3. Build the website

After generating or modifying articles, run:

```bash
./build.sh "https://YOURGITHUBUSERNAME.github.io/ai-content-generator/"
```

This regenerates the `docs/` directory.

Alternatively:

```bash
uv run src/main.py publish \
    "https://YOURGITHUBUSERNAME.github.io/ai-content-generator/"
```

This rebuilds the `docs/` directory from the Markdown content and static assets.

Publishing is an explicit step. Generating an article does not modify the generated website in `docs/`.

### 4. Commit and push the generated website

After publishing:

```bash
git add .
git commit -m "Publish website"
git push
```

GitHub Pages will deploy the updated contents of `docs/`.

### Important

The `basepath` passed to `publish` or `build.sh` should be the **GitHub Pages website URL**, not the GitHub repository URL.

Correct:

```text
https://YOURGITHUBUSERNAME.github.io/ai-content-generator/
```

Incorrect:

```text
https://github.com/YOURGITHUBUSERNAME/ai-content-generator
```


## Project Structure

```text
content/
└── blog/              # Generated Markdown articles

static/                # Static website assets

docs/                  # Generated website

src/
├── models/            # Data and HTML node models
├── pipeline/          # Research, LLM, Markdown and HTML processing
├── tests/              # Tests
└── main.py            # CLI entry point

build.sh               # Build/publish script
main.sh                # CLI convenience script
```

## Project Goal

This project was built as a Python learning project to practice:

* Python application architecture
* CLI development
* API integration
* Web research
* LLM integration
* Markdown parsing
* HTML generation
* Static-site generation

## Future Goals

* Implement other cli commands
* Include images
* Better website
