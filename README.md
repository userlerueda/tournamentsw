# Tournament Software

Tournament Software python library

![example workflow](https://github.com/userlerueda/utr/actions/workflows/on_push.yml/badge.svg?branch=main) ![GitHub](https://img.shields.io/github/license/userlerueda/tournamentsw) ![GitHub all releases](https://img.shields.io/github/downloads/userlerueda/tournamentsw/total)

## Description

## Installation

To install the latest version:

```bash
pip install tsw
```

To install the library from GitHub:

```bash
pip install git+https://github.com/userlerueda/tournamentsw.git
```

## Usage Guide

### Using via CLI

#### Getting Events

```bash
$ tsw events B88B8B48-E97D-45EF-BCB5-D2B393B0EAC6
+------+--------------------+---------+-----------+
|   id | Name               |   Draws |   Entries |
|------+--------------------+---------+-----------|
|    7 | HASTA 14 AÑOS      |       1 |        18 |
|    2 | INTERMEDIA MIXTO A |       1 |        32 |
|    3 | INTERMEDIA MIXTO B |       1 |        22 |
|    1 | PRIMERA            |       1 |        11 |
|    4 | SEGUNDA MIXTO      |       1 |        32 |
|    8 | TERCERA DAMAS      |       1 |        21 |
|    5 | TERCERA MIXTO A    |       1 |        20 |
|    6 | TERCERA MIXTO B    |       1 |        23 |
+------+--------------------+---------+-----------+
```

#### Getting Draws for a Tournament

```bash
❯ tsw draws B88B8B48-E97D-45EF-BCB5-D2B393B0EAC6 7
+------+---------------+--------+-------------+-----------------+---------------+
|   id | Draw          |   Size | Type        | Qualification   |   Consolation |
|------+---------------+--------+-------------+-----------------+---------------|
|   11 | HASTA 14 AÑOS |     32 | Elimination | No              |           nan |
+------+---------------+--------+-------------+-----------------+---------------+
```

#### Getting Matches for a Draw

```bash
tsw matches B88B8B48-E97D-45EF-BCB5-D2B393B0EAC6 11
+-----------------------+------------------+--------------------+-----------------+--------------------+------------------------------+
| Timestamp             | Winner Country   | Winner Name        | Loser Country   | Loser Name         | Score                        |
|-----------------------+------------------+--------------------+-----------------+--------------------+------------------------------|
| Sat 5/14/2022 2:00 PM | COL              | Gabriel Echeverri  | COL             | Rafael Sanint      | [[6, 1], [6, 0]]             |
| Sat 5/14/2022 2:00 PM | COL              | Juan Martin Siegel | COL             | Emma Villa         | [[3, 6], [6, 2], [10, 7]]    |
| Sun 5/15/2022 2:00 PM | COL              | Juan Marulanda     | COL             | Gabriel Echeverri  | [[4, 6], [6, 3], [10, 7]]    |
| Sun 5/15/2022 2:00 PM | COL              | Matias Lopez       | COL             | Violeta Gonzalez   | [[6, 0], [6, 1]]             |
| Sun 5/15/2022 2:00 PM | COL              | Manuel Orozco      | COL             | Samuel Escandon    | [[6, 3], [6, 1]]             |
| Sun 5/15/2022 2:00 PM | COL              | Simon Scanzani Iza |                 |                    | [[6, 3], [6, 2]]             |
| Sun 5/15/2022 4:00 PM | COL              | Pamela Duque       | COL             | Emiliano Fernandez | [[6, 4], [5, 7], [10, 8]]    |
| Sun 5/15/2022 4:00 PM | COL              | Mariana Guerrero   | COL             | Pablo Rueda        | [[6, 3], [4, 6], [10, 6]]    |
| Sun 5/15/2022 4:00 PM | COL              | Matias Castro      | COL             | Jacobo Castro      | [[6, 0], [6, 0]]             |
| Sun 5/15/2022 4:00 PM | COL              | Pedro Gutierrez    | COL             | Juan Martin Siegel | [[3, 6], [6, 4], [10, 0]]    |
| Sat 5/21/2022 2:00 PM | COL              | Juan Marulanda     | COL             | Matias Lopez       | [[6, 4], [6, 4]]             |
| Sat 5/21/2022 2:00 PM | COL              | Manuel Orozco      | COL             | Simon Scanzani Iza | [[6, 1], [6, 3]]             |
| Sat 5/21/2022 2:00 PM | COL              | Pamela Duque       | COL             | Mariana Guerrero   | [[6, 3], [6, 3]]             |
| Sat 5/21/2022 2:00 PM | COL              | Pedro Gutierrez    | COL             | Matias Castro      | [[7, 5], [1, 6], [10, 6]]    |
| Sun 5/22/2022 2:00 PM | COL              | Juan Marulanda     | COL             | Manuel Orozco      | [[7, 6, 3], [2, 6], [10, 3]] |
| Sun 5/22/2022 2:00 PM | COL              | Pedro Gutierrez    | COL             | Pamela Duque       | [[6, 3], [6, 3]]             |
| Sat 5/28/2022 3:00 PM | COL              | Juan Marulanda     | COL             | Pedro Gutierrez    | [[6, 3], [6, 3]]             |
+-----------------------+------------------+--------------------+-----------------+--------------------+------------------------------+
```

### Using as a Library

## Credits

## License

This project is covered under the terms described in [LICENSE](LICENSE).

## Contributing

See the [Contributing](CONTRIBUTING.md) if you want to contribute.

## Changes

See the [Changelog](CHANGELOG.md) for a full list of changes.
