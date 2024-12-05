
project_dir := .
package_dir := app

# Reformat code
.PHONY: reformat
reformat:
	@uv run black $(project_dir)
	@uv run ruff check $(project_dir) --fix

# Lint code
.PHONY: lint
lint: reformat
	@uv run mypy $(project_dir)

# Run bot
.PHONY: run
run:
	@uv run python -O -m $(package_dir)
