# International Edition · Outline & Contents

> v0.1 · 2026-09-29
> Audience: (a) Chinese-speaking readers relocating abroad, (b) English-speaking readers new to a city outside their home country.

---

## 1. Organizing logic

The international edition is ordered by **lifecycle, not by topic**. A person moving abroad doesn't ask "what does the healthcare chapter say" — they ask "what do I do first." Topic lookup is served by the appendix scenario index; the main spine follows the actual timeline.

| Entry point | Use | Location |
|---|---|---|
| **Timeline** (spine) | "I just landed — what now?" | Parts 1–11 below |
| **Topic / scenario** | "Something is wrong and I don't know who to call" | Appendix C |

**Country-first rule.** Rules are national; practice is local. Every document states its country (and city where it matters). There is no "generic Europe" document.

**Dual audience rule.** Where citizens/residents/students/visitors get different answers, the document says so explicitly rather than describing the most common case and hoping.

---

## 2. Document template

```markdown
---
title: Opening a bank account
edition: intl
country: Germany
applies_to: [resident, student, worker]
collected: 2026-09
review_by: 2027-03
sources:
  - https://...
---

## Who this applies to
## What you need          ← documents, in the order they're requested
## Where to go
## How long
## What it costs
## If you're refused      ← common rejection reasons and the appeal route
## Common mistakes
## How to verify          ← official portal to confirm current rules
```

`collected` and `review_by` are mandatory. A date is what makes a claim checkable.

---

## 3. Main chapters

### Part 0 · How to use this guide

- 0.1 Two entry points (timeline / topic)
- 0.2 Why every page states a country
- 0.3 Sources, dates, and how to verify anything here

### Part 1 · Before you go

- 1.1 Visa categories and choosing the right one
- 1.2 Document checklist (apostille, certified translations, police checks)
- 1.3 Health checks and vaccination requirements
- 1.4 Money before you land (currency, cards, transfer limits, cash rules)
- 1.5 Phone: roaming vs. eSIM vs. buying there
- 1.6 Insurance that actually matters (health / travel / liability)
- 1.7 Shipping belongings and excess baggage
- 1.8 What not to bring — buy it there instead

### Part 2 · Landing week

- 2.1 Immigration and customs on arrival
- 2.2 Getting from the airport
- 2.3 First accommodation and short-term rental scams
- 2.4 SIM card and mobile plan
- 2.5 Opening a bank account
- 2.6 Registering your address with local authorities
- 2.7 Tax ID / social security number
- 2.8 Emergency numbers and how to use them

### Part 3 · Housing

- 3.1 How the rental market is structured (agents, guarantors, fees)
- 3.2 Reading a lease in a language you don't speak
- 3.3 Viewings and red flags
- 3.4 Deposits, bonds, and deposit-protection schemes
- 3.5 Utilities, internet, and waste rules
- 3.6 Tenant rights and how disputes are actually resolved
- 3.7 Buying property as a foreigner

### Part 4 · Money and tax

- 4.1 Everyday payments and cash culture
- 4.2 International transfers: the cheapest legitimate routes
- 4.3 Tax residency and what you owe
- 4.4 Filing your first tax return
- 4.5 Building credit history from zero
- 4.6 Tipping and price norms
- 4.7 Sending money home

### Part 5 · Health

- 5.1 How the health system is organized (public / private / insurance-based)
- 5.2 Registering with a GP or clinic
- 5.3 Insurance: public, private, employer-provided
- 5.4 Pharmacy vs. clinic vs. emergency room
- 5.5 Prescriptions and bringing medication across borders
- 5.6 Dental and vision
- 5.7 Mental health support
- 5.8 Pregnancy, childbirth, and early childcare

### Part 6 · Work

- 6.1 Work permit and right to work
- 6.2 Employment contract norms (probation, notice, non-compete)
- 6.3 Payslips: what the deductions mean
- 6.4 Unions and worker protections
- 6.5 Changing or losing a job — and the visa consequences
- 6.6 Self-employment and freelancing, legally
- 6.7 Workplace culture: the unwritten rules

### Part 7 · Education and family

- 7.1 Enrolling a child in school
- 7.2 International vs. local schools
- 7.3 Childcare options and costs
- 7.4 Family visas and dependants
- 7.5 Healthcare for children

### Part 8 · Getting around

- 8.1 Public transit: tickets, cards, apps
- 8.2 Ride-hailing and taxis
- 8.3 Driving: licence conversion, buying a car, insurance
- 8.4 Cycling and scooters — the rules that differ
- 8.5 Intercity: rail, coach, budget airlines
- 8.6 Driving rules that surprise visitors

### Part 9 · Daily life

- 9.1 Groceries, food labels, dietary and religious needs
- 9.2 Mail, parcels, and customs
- 9.3 Domestic help, repairs, tradespeople
- 9.4 Pets: import rules, registration, vets
- 9.5 Religion, holidays, and what closes
- 9.6 Social norms and avoiding offence
- 9.7 Internet access, VPNs, and content legality

### Part 10 · When things go wrong

- 10.1 Police, crime, and reporting
- 10.2 Legal help and your rights
- 10.3 Consumer complaints
- 10.4 Discrimination and how to respond
- 10.5 Embassy and consulate services
- 10.6 Emergencies: medical, fire, natural disaster
- 10.7 Losing your documents

### Part 11 · Leaving

- 11.1 Deregistration and closing accounts
- 11.2 Tax exit and pensions
- 11.3 Shipping belongings home
- 11.4 Keeping access to what you built

### Part 12 · Country notes

> **v1 scope locked (2026-09-29): United States · Germany · Japan.**
> Do these three properly before adding a fourth. Two federal systems and one non-federal
> system, which is deliberate — it forces the framework to handle both.

- 12.1 The common framework — what every country card contains
- 12.2 Country cards — 🇺🇸 United States · 🇩🇪 Germany · 🇯🇵 Japan

Each card uses fixed fields so countries can be compared at a glance:

```
税号 / Tax ID          →
医保 / Health cover    →
银行开户 / Bank        →
租房押金保护 / Deposits →
驾照转换 / Licence     →
紧急号码 / Emergency   →
```

**Why these three:** the US and Germany are the two most common destinations where the
process genuinely defeats people on the first attempt, and they differ enough to stress-test
the framework (federal vs. state vs. municipal competence). Japan is the hardest case for
language and for rules that are national but administered locally — if the framework survives
Japan it survives anything.

---

## 4. Directory and file conventions

```text
content/intl/
├── OUTLINE.md
├── 01-before-you-go/
├── 02-landing-week/
├── 03-housing/
├── 04-money-tax/
├── 05-health/
├── 06-work/
├── 07-education-family/
├── 08-transport/
├── 09-daily-life/
├── 10-when-things-go-wrong/
├── 11-leaving/
└── 12-country-notes/
```

- Directories: `NN-<part-name>` matching the part number. Create a directory when content
  lands, not in advance.
- Files: `<topic>-<country>.md`, lowercase, hyphenated, e.g. `open-bank-account-germany.md`.
- Country-specific documents live in the part they belong to, **not** in `12-country-notes/`.
  Part 12 holds the comparison cards only.

---

## 5. Appendices

### Appendix A · Emergency numbers by country
### Appendix B · Official portals by country
### Appendix C · Scenario index ← second entry point

- I just landed and I have no phone or bank account
- I need to see a doctor and I don't speak the language
- My landlord won't return my deposit
- I lost my passport
- I was stopped by the police
- My employer won't pay me
- I need to leave the country quickly
- My visa is about to expire

### Appendix D · Multi-language document glossary
What the key documents are actually called in each language — the single most useful thing when standing at a counter.

### Appendix E · Freshness and review log

---

## 6. Editorial conventions

| Item | Convention |
|---|---|
| File naming | `<topic>-<country-or-city>.md`, lowercase, hyphenated |
| Language | English primary; local-language terms given alongside |
| Address | Second person "you" |
| Dates | ISO format (2026-09-29), always with a collected date |
| Numbers | Currency stated explicitly with ISO code |
| Uncertainty | "In most cases", "practice varies by state", "confirm locally" — never absolute claims |
| Comparisons | Never state a "best" country; state trade-offs |
| Legal content | Describe procedure, not legal advice; link the statute or official portal |
