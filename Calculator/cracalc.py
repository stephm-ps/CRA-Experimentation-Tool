'''
rule 1 = PEP and Sanctions Status
rule 2 = Adverse Media
rule 3 = Business Vertical MCC
rule 4 = Historic Merchant Records
rule 5 = Length of Time in Business
rule 6 = Home Trading
rule 7 = Entity Type
rule 8 = Signatory and/or UBO's Country of Residence
rule 9 = Overseas Ownership Structure
rule 10 = Customers Proposed usage of MOTO
rule 11 = Customers Proposed Use of Ecommerce
-- do not know why there is no rule 12 --
rule 13 = Annual Turnover (TO)
rule 14 = Highest Transaction Value
rule 15 = Onboarding Channel
rule 16 = Status of site visit
'''

def score_to_rank(sc):
    if sc <= 0.46:
        return 'Standard'
    elif sc > 0.46 and sc <= 0.92:
        return 'Medium'
    elif sc > 0.92 and sc <= 11.99:
        return 'High'
    elif sc > 11.99:
        return 'Prohibted'
    else:
        print('Error')

def overall_score(
        Rule1,
        Rule2,
        Rule3,
        Rule4,
        Rule5,
        Rule6,
        Rule7,
        Rule8,
        Rule9,
        Rule10,
        Rule11,
        Rule13,
        Rule14,
        Rule15,
        Rule16
):
    rule_score_dict = {
        1: [0, 0, 50, 100],
        2: [0, 0, 50, 0],
        3: [0, 1, 2, 0],
        4: [0, 0, 50, 100],
        5: [0, 0.5, 1, 0],
        6: [0, 0, 1, 0],
        7: [0, 0, 0, 0],
        8: [0, 0, 50, 100],
        9: [0, 0, 50, 100],
        10: [0, 1, 2, 0],
        11: [0, 0, 0, 0],
        13: [0, 1, 2, 0],
        14: [0, 1, 2, 0],
        15: [0, 1, 2, 0],
        16: [0, 1, 0, 0]
        }
    rank_order = {
        'Standard': 0,
        'Medium': 1,
        'High': 2,
        'Prohibited': 3
        }
    Rule1Score = rule_score_dict[1][rank_order[Rule1]]
    Rule2Score = rule_score_dict[2][rank_order[Rule2]]
    Rule3Score = rule_score_dict[3][rank_order[Rule3]]
    Rule4Score = rule_score_dict[4][rank_order[Rule4]]
    Rule5Score = rule_score_dict[5][rank_order[Rule5]]
    Rule6Score = rule_score_dict[6][rank_order[Rule6]]
    Rule7Score = rule_score_dict[7][rank_order[Rule7]]
    Rule8Score = rule_score_dict[8][rank_order[Rule8]]
    Rule9Score = rule_score_dict[9][rank_order[Rule9]]
    Rule10Score = rule_score_dict[10][rank_order[Rule10]]
    Rule11Score = rule_score_dict[11][rank_order[Rule11]]
    Rule13Score = rule_score_dict[13][rank_order[Rule13]]
    Rule14Score = rule_score_dict[14][rank_order[Rule14]]
    Rule15Score = rule_score_dict[15][rank_order[Rule15]]
    Rule16Score = rule_score_dict[16][rank_order[Rule16]]

    score = ((Rule1Score+Rule2Score+Rule3Score+Rule4Score+Rule5Score+Rule6Score+Rule7Score)/3*0.32)+ \
            ((Rule8Score+Rule9Score)/2*0.35)+ \
            ((Rule10Score+Rule11Score+Rule13Score+Rule14Score)/3*0.22) + \
            ((Rule15Score+Rule16Score)/2*0.21)

    score_rank = score_to_rank(score)
    return [score,score_rank]


