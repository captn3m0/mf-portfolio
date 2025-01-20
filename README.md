# Mutual Fund Portfolio Dataset

Mutual Funds in India must disclose their portfolio information (list of underlying
securities and their percentage holdings). However, there is currently no
machine-readable datasource that provides this information.

This is an attempt to convert the portfolio information from the various AMC
websites into a real dataset (maybe https://www.fundsxml.org/documentation/)
with usable identifiers (ISINs).

## Guidelines

Rough Guidelines for how this will go.

- Prioritize larger AMCs (Top 10 AMCs cover 70+% of the total AUM)
- Historical data is important (we fetch it), but not a priority (we can parse it later)
- Automation is important, we want to update data within a day of it being updated on the AMC website.
- Current focus is on fetching the raw data sources (Excel sheets).
- Once that is done, we can look at parsing the files.
- Publication should be in CSV/SQLite formats, with a usable API.

## Mapping Securities to ISINs

- This is a hard problem, as not all AMCs publish the ISIN of the underlying security.

## Other Related Projects

- [Mutual Fund TER Tracker](https://github.com/captn3m0/india-mutual-fund-ter-tracker)
- [Kuvera's Mutual Fund Identifiers](https://github.com/captn3m0/kuvera-mutual-funds-lookup) mapped to ISINs
- [Historical Mutual Fund NAV Data](https://github.com/captn3m0/historical-mf-data)
- [Mutual Funds API](https://mf.captnemo.in/) that serves some of the above data.
- [India ISIN Dataset](https://github.com/captn3m0/india-isin-data) with minimal details for every ISIN.

## License

The code is licensed under the MIT License. See LICENSE file for more details.
Licensing for the eventual dataset is still pending.