# datafun-06-applied

[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> Professional Python project: applied data analytics.

## Project Goal

In this project, you perform a novel **Exploratory Data Analysis (EDA)**
using Jupyter notebooks or Python modules (your preference).
The addition of related data and/or SQL may be included and is optional.

Your goal: choose a new dataset, and explore it:
run checks, view distributions, identify missing values or outliers.
Create and present a custom project to explore a different tabular dataset.

For data suggestions, please see [data/raw/README.md](data/raw/README.md).

## Examples

The project includes an additional EDA on a real-world dataset.
Between this and the Module 4 example,
you should be able to see what parts are similar
(the general outline and workflow) and what changes with data.
The two projects together help create an appreciation
for the value of **reusable functions**.

## Working Files

You'll work with these areas:

- **data/raw** - raw data for exploration
- **docs/** - project narrative and documentation
- **src/** - supporting Python package modules
- **notebooks/** - interactive analysis
- **pyproject.toml** - update authorship & links
- **zensical.toml** - update authorship & links

## Instructions (pro-analytics-02)

Follow the
[step-by-step workflow guide](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
to complete:

1. Phase 1. **Start & Run**
2. Phase 2. **Change Authorship**
3. Phase 3. **Read & Understand**
4. Phase 4. **Modify**
5. Phase 5. **Apply**


## Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

After you get a copy of this repo in your own GitHub account,
open a machine terminal in your `Repos` folder:

```shell
# Replace username with YOUR GitHub username.
git clone https://github.com/ajaneh/datafun-06-applied

cd datafun-06-applied
code .
```

### In a VS Code terminal

These are listed for convenience.
For best results, follow the detailed instructions in
[pro-analytics-02 guide](https://denisecase.github.io/pro-analytics-02/).

```shell
uv self update
uv python pin 3.14
uv lock --upgrade
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install

git add -A
uvx pre-commit run --all-files
# repeat if changes were made
uvx pre-commit run --all-files

# run the example module and verify the environment (.venv/)
uv run python -m datafun.app_case
uv run python -m datafun.app_alex

# do chores
uv run ruff format .
uv run ruff check . --fix
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.
- You do not need to add to or modify `tests/`. They are provided for example only.
- Many files are silent helpers. Explore as you like, but nothing is required.
- You do NOT not to understand everything; understanding builds naturally over time.

## Troubleshooting >>>

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl+c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.


## Phase 5 Custom Project

The purpose of this project was to compare job availability and median wage in 4 differing prospective areas to move to (current location, central missouri was included for reference). Histograms colored by area were the most useful for this purpose.

If we look at jobs overall, Tampa and Orlando seem to have the most jobs available
![Employment](artifacts/Employment_Rates_Per_Occupation.png)

The pay also seems to be higher (comparison of cost of living should be added in the future)
![Wages](artifacts/Job_Type_Compared_To_Wage.png)


However it's important to note that the majority of these jobs don't line up with my experience or preferences. So I narrowed the comparison to 3 occupations. Data Scientists, Operations Research Analysts, and Computer Occupations, All Other.

![Preferred_Employment](artifacts/Employment_Rates_Preferred_Jobs.png)
![Preferred_Wages](artifacts/Wage_Per_Preferred_Jobs.png)

An overview of the location quotient confirms central missouri isn't a great place to try to work in the tech sector
![LocationQ](artifacts/Location_Quotients.png)



Many of the course principles were applied in this project, data extraction and cleaning, discerning correlations, and using charts to communicate findings.


## Project Documentation

I obtained Occupational Employment and Wage Statistics from [U.S. Bureau of Labor Statistics](https://data.bls.gov/oes/#/home)
I selected 4 areas, Midwest Missouri, St. Louis, greater Orlando area, and greater Tampa area. I filtered this by all occupations in the "computer and mathematical" domain (see table below) and obtained Employment (# of people employed in that occupation), Median and Mean Wage, and also the Location Quotient, where a value of 1 means job availability is similar to the national average and values nearing 0 have less jobs available in that domain.
| Occupation Category | Job Title |
| :--- | :--- |
| **Development & Design** | Software Developers |
| | Software Quality Assurance Analysts and Testers |
| | Web Developers |
| | Web and Digital Interface Designers |
| | Computer Programmers |
| **Data & Databases** | Data Scientists |
| | Database Administrators |
| | Database Architects |
| **Systems & Security** | Information Security Analysts |
| | Computer Systems Analysts |
| | Computer and Information Research Scientists |
| **Networks & Support** | Computer Network Architects |
| | Computer Network Support Specialists |
| | Computer User Support Specialists |
| | Network and Computer Systems Administrators |
| **Math & Analytics** | Actuaries |
| | Operations Research Analysts |
| | Statisticians |
| **Other** | Computer Occupations, All Other |


[docs/index.md](docs/index.md)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)
