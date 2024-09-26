"""
This script uses known values of inflation-indexed policy parameters after
2022 to write an updated version of the taxcalc/policy_current_law.json file.

USAGE: (taxcalc-dev) Tax-Calculator% python update_pcl.py

THEN: look at differences between the newly written pcl.json file and
      the old existing taxcalc/policy_current_law.json file
"""

import os
import sys
import json


LIST_MARS_ZERO = [
    {'year': 2023, 'MARS': 'single', 'value': 0.0},
    {'year': 2023, 'MARS': 'mjoint', 'value': 0.0},
    {'year': 2023, 'MARS': 'mseparate', 'value': 0.0},
    {'year': 2023, 'MARS': 'headhh', 'value': 0.0},
    {'year': 2023, 'MARS': 'widow', 'value': 0.0},
]
LIST_MARS_INF = [
    {'year': 2023, 'MARS': 'single', 'value': 9e99},
    {'year': 2023, 'MARS': 'mjoint', 'value': 9e99},
    {'year': 2023, 'MARS': 'mseparate', 'value': 9e99},
    {'year': 2023, 'MARS': 'headhh', 'value': 9e99},
    {'year': 2023, 'MARS': 'widow', 'value': 9e99},
]
LIST_SCALAR_ZERO = [
    {'year': 2023, 'value': 0.0},
]
NEW_KNOWN_ITEMS = {
    # PAYROLL TAX PARAMETER SOURCES:
    # - SSA Office of the Chief Actuary: Contribution and Benefit Base
    #       https://www.ssa.gov/OACT/COLA/cbb.html
    'SS_Earnings_c': [
        {'year': 2023, 'value': 160200.0},
        # {'year': 2024, 'value': 168600.0},
    ],
    # INCOME TAX PARAMETER SOURCES:
    # - IRS Rev. Proc. 2022-38 containing 2023 policy parameter values is at:
    #       https://www.irs.gov/pub/irs-drop/rp-22-38.pdf
    # - IRS Rev. Proc. 2023-34 containing 2024 policy parameter values is at:
    #       https://www.irs.gov/pub/irs-drop/rp-23-34.pdf
    'II_brk1': [
        {'year': 2023, 'MARS': 'single', 'value': 11000.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 22000.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 11000.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 15700.0},
        {'year': 2023, 'MARS': 'widow', 'value': 22000.0},
    ],
    'II_brk2': [
        {'year': 2023, 'MARS': 'single', 'value': 44725.},
        {'year': 2023, 'MARS': 'mjoint', 'value': 89450.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 44725.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 59850.0},
        {'year': 2023, 'MARS': 'widow', 'value': 89450.0},
    ],
    'II_brk3': [
        {'year': 2023, 'MARS': 'single', 'value': 95375.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 190750.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 95375.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 95350.0},
        {'year': 2023, 'MARS': 'widow', 'value': 190750.0},
    ],
    'II_brk4': [
        {'year': 2023, 'MARS': 'single', 'value': 182100.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 364200.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 182100.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 182100.0},
        {'year': 2023, 'MARS': 'widow', 'value': 364200.0},
    ],
    'II_brk5': [
        {'year': 2023, 'MARS': 'single', 'value': 231250.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 462500.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 231250.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 231250.0},
        {'year': 2023, 'MARS': 'widow', 'value': 462500.0},
    ],
    'II_brk6': [
        {'year': 2023, 'MARS': 'single', 'value': 578125.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 693750.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 578125.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 578100.0},
        {'year': 2023, 'MARS': 'widow', 'value': 693750.0},
    ],
    'II_brk7': [
        {'year': 2023, 'MARS': 'single', 'value': 9e99},
        {'year': 2023, 'MARS': 'mjoint', 'value': 9e99},
        {'year': 2023, 'MARS': 'mseparate', 'value': 9e99},
        {'year': 2023, 'MARS': 'headhh', 'value': 9e99},
        {'year': 2023, 'MARS': 'widow', 'value': 9e99},
    ],
    'CG_brk1': [
        {'year': 2023, 'MARS': 'single', 'value': 44625.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 89250.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 44625.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 59750.0},
        {'year': 2023, 'MARS': 'widow', 'value': 89250.0},
    ],
    'CG_brk2': [
        {'year': 2023, 'MARS': 'single', 'value': 492300.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 553850.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 276900.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 523050.0},
        {'year': 2023, 'MARS': 'widow', 'value': 553850.0},
    ],
    'CG_brk3': [
        {'year': 2023, 'MARS': 'single', 'value': 9e99},
        {'year': 2023, 'MARS': 'mjoint', 'value': 9e99},
        {'year': 2023, 'MARS': 'mseparate', 'value': 9e99},
        {'year': 2023, 'MARS': 'headhh', 'value': 9e99},
        {'year': 2023, 'MARS': 'widow', 'value': 9e99},
    ],
    'EITC_c': [
        {'year': 2023, 'EIC': '0kids', 'value': 600.0},
        {'year': 2023, 'EIC': '1kid', 'value': 3995.0},
        {'year': 2023, 'EIC': '2kids', 'value': 6604.0},
        {'year': 2023, 'EIC': '3+kids', 'value': 7430.0},
    ],
    'EITC_ps': [
        {'year': 2023, 'EIC': '0kids', 'value': 9800.0},
        {'year': 2023, 'EIC': '1kid', 'value': 21560.0},
        {'year': 2023, 'EIC': '2kids', 'value': 21560.0},
        {'year': 2023, 'EIC': '3+kids', 'value': 21560.0},
    ],
    'EITC_ps_MarriedJ': [
        {'year': 2023, 'EIC': '0kids', 'value': 6570.0},
        {'year': 2023, 'EIC': '1kid', 'value': 6560.0},
        {'year': 2023, 'EIC': '2kids', 'value': 6560.0},
        {'year': 2023, 'EIC': '3+kids', 'value': 6560.0},
    ],
    'EITC_InvestIncome_c': [
        {'year': 2023, 'value': 11000.0},
    ],
    'AMT_brk1': [
        {'year': 2023, 'value': 220700.0},
    ],
    'AMT_em': [
        {'year': 2023, 'MARS': 'single', 'value': 81300.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 126500.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 63250.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 81300.0},
        {'year': 2023, 'MARS': 'widow', 'value': 126500.0},
    ],
    'AMT_em_ps': [
        {'year': 2023, 'MARS': 'single', 'value': 578150.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 1156300.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 578150.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 578150.0},
        {'year': 2023, 'MARS': 'widow', 'value': 1156300.0},
    ],
    'AMT_em_pe': [
        {"year": 2023, "value": 831150.0},
    ],
    'AMT_child_em': [
        {'year': 2023, 'value': 8800.0},
    ],
    'STD': [
        {'year': 2023, 'MARS': 'single', 'value': 13850.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 27700.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 13850.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 20800.0},
        {'year': 2023, 'MARS': 'widow', 'value': 27700.0},
    ],
    'STD_Dep': [
        {'year': 2023, 'value': 1250.0},
    ],
    'STD_Aged': [
        {'year': 2023, 'MARS': 'single', 'value': 1800.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 1500.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 1500.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 1800.0},
        {'year': 2023, 'MARS': 'widow', 'value': 1800.0},
    ],
    'PT_qbid_taxinc_thd': [
        {'year': 2023, 'MARS': 'single', 'value': 182100.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 364200.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 182100.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 182100.0},
        {'year': 2023, 'MARS': 'widow', 'value': 182100.0},
    ],
    'ALD_BusinessLosses_c': [
        {'year': 2023, 'MARS': 'single', 'value': 289000.0},
        {'year': 2023, 'MARS': 'mjoint', 'value': 578000.0},
        {'year': 2023, 'MARS': 'mseparate', 'value': 289000.0},
        {'year': 2023, 'MARS': 'headhh', 'value': 289000.0},
        {'year': 2023, 'MARS': 'widow', 'value': 578000.0},
    ],
    # ITEMS NOT PART OF CURRENT-LAW POLICY IN 2022-2025 PERIOD:
    'ALD_Dependents_Child_c': LIST_SCALAR_ZERO,
    'ALD_Dependents_Elder_c': LIST_SCALAR_ZERO,
    'II_em': LIST_SCALAR_ZERO,
    'II_em_ps': LIST_MARS_INF,
    'II_credit': LIST_MARS_ZERO,
    'II_credit_ps': LIST_MARS_ZERO,
    'II_credit_nr': LIST_MARS_ZERO,
    'II_credit_nr_ps': LIST_MARS_ZERO,
    'ID_Medical_c': LIST_MARS_INF,
    'ID_StateLocalTax_c': LIST_MARS_INF,
    'ID_RealEstate_c': LIST_MARS_INF,
    'ID_InterestPaid_c': LIST_MARS_INF,
    'ID_Charity_c': LIST_MARS_INF,
    'ID_Casualty_c': LIST_MARS_INF,
    'ID_Miscellaneous_c': LIST_MARS_INF,
    'ID_ps': LIST_MARS_INF,
    'ID_BenefitSurtax_em': LIST_MARS_ZERO,
    'ID_c': LIST_MARS_INF,
    'CG_ec': LIST_SCALAR_ZERO,
    'PT_qbid_ps': LIST_MARS_INF,
    'RPTC_c': LIST_SCALAR_ZERO,
    'CTC_new_ps': LIST_MARS_ZERO,
    'FST_AGI_thd_lo': LIST_MARS_INF,
    'FST_AGI_thd_hi': LIST_MARS_INF,
    'AGI_surtax_thd': LIST_MARS_INF,
    'UBI_u18': LIST_SCALAR_ZERO,
    'UBI_1820': LIST_SCALAR_ZERO,
    'UBI_21': LIST_SCALAR_ZERO,
}
for num in range(1, 7 + 1):
    NEW_KNOWN_ITEMS[f'PT_brk{num}'] = NEW_KNOWN_ITEMS[f'II_brk{num}']
for num in range(1, 3 + 1):
    NEW_KNOWN_ITEMS[f'AMT_CG_brk{num}'] = NEW_KNOWN_ITEMS[f'CG_brk{num}']


CHECK_FOR_MISSING = False


def check_for_missing(pdict):
    """
    Prints to sdtout indexed parameters with missing values in or before 2022.
    """
    first_year = 2013
    last_known_year = 2022
    for pname, pinfo in pdict.items():
        if pname == 'schema':
            continue
        if not pinfo['indexed']:
            continue
        years_used = []
        plist = pinfo['value']
        for item in plist:
            year = item['year']
            if year <= last_known_year:
                if year not in years_used:
                    years_used.append(year)
        for year in range(first_year, last_known_year + 1):
            if year not in years_used:
                print(f'MISSING INDEXED VALUE FOR {pname} IN {year}')


def main():
    """
    High-level script logic.
    """
    # read existing policy_current_law.json into a Python dictionary
    fname = os.path.join('taxcalc', 'policy_current_law.json')
    with open(fname, 'r', encoding='utf-8') as jfile:
        pdict = json.load(jfile)

    # optionally check for missing indexed parameters in years <= 2022
    if CHECK_FOR_MISSING:
        check_for_missing(pdict)
        return 1

    # add parameter values to dictionary
    for pname, pinfo in pdict.items():
        if pname == 'schema':
            continue
        if not pinfo['indexed']:
            continue
        if pname not in NEW_KNOWN_ITEMS:
            print(f'NO NEW_KNOWN_ITEMS FOR {pname}')
            continue
        plist = pdict[pname]['value']
        # ... see if adding values before existing plist items for 2026
        bindex = None
        for itm in plist:
            if itm['year'] == 2026:
                bindex = plist.index(itm)
                break
        # ... add new items to plist for this pname
        for item in NEW_KNOWN_ITEMS[pname]:
            if item in plist:
                continue
            if bindex:
                plist.insert(bindex, item)
                bindex += 1
            else:
                plist.append(item)

    # write updated dictionary to pcl.json file
    with open('pcl.json', 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(pdict, indent=4) + '\n')

    # return no-error exit code
    return 0
# end main function code


if __name__ == '__main__':
    sys.exit(main())