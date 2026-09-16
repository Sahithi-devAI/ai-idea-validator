import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.load_workbook('data/product_hunt_ideas.xlsx')

if 'Rubrics' in wb.sheetnames:
    del wb['Rubrics']

ws = wb.create_sheet('Rubrics')

thin = Side(style='thin', color='BFBFBF')
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def apply_border(cell):
    cell.border = border

def header_style(cell, bg='1F4E79'):
    cell.font = Font(bold=True, color='FFFFFF', size=11)
    cell.fill = PatternFill('solid', fgColor=bg)
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

def dim_header_style(cell):
    cell.font = Font(bold=True, color='FFFFFF', size=11)
    cell.fill = PatternFill('solid', fgColor='2E75B6')
    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)

def score_style(cell, score):
    colors = {5: 'E2EFDA', 4: 'EBF7EE', 3: 'FFF2CC', 2: 'FCE4D6', 1: 'FFD7D7'}
    cell.fill = PatternFill('solid', fgColor=colors.get(score, 'FFFFFF'))
    cell.font = Font(bold=True, size=11)
    cell.alignment = Alignment(horizontal='center', vertical='center')

def criteria_style(cell):
    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    cell.font = Font(size=10)

def note_style(cell):
    cell.font = Font(italic=True, color='595959', size=9)
    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    cell.fill = PatternFill('solid', fgColor='F2F2F2')

ws.column_dimensions['A'].width = 32
ws.column_dimensions['B'].width = 8
ws.column_dimensions['C'].width = 72

# Title
ws.merge_cells('A1:C1')
title = ws['A1']
title.value = 'Idea Validator — Scoring Rubrics'
title.font = Font(bold=True, color='FFFFFF', size=13)
title.fill = PatternFill('solid', fgColor='1F4E79')
title.alignment = Alignment(horizontal='center', vertical='center')
ws.row_dimensions[1].height = 28

# Column headers
for col, h in enumerate(['Dimension', 'Score', 'Criteria'], 1):
    cell = ws.cell(row=2, column=col, value=h)
    header_style(cell)
    apply_border(cell)
ws.row_dimensions[2].height = 20

rubrics = [
    (
        'Market Potential',
        'Scored on Problem Prevalence (how many face this regularly?) + Switching Readiness (actively seeking a fix, or resigned to status quo?). Do NOT score on category hype (e.g. "AI is a large market").',
        [
            (5, 'Problem is widespread AND people are actively seeking solutions — visible in search interest, communities, or widespread workarounds in the wild.'),
            (4, 'Widespread problem, meaningful demand signals, real wedge exists despite some incumbents.'),
            (3, 'Proven market, real problem, competitive — entrants can win with differentiation but must earn it.'),
            (2, 'Problem real but affects a small or hard-to-reach group, OR large group with near-zero urgency, OR market owned by an aggregator with distribution moat (Google, Apple, Microsoft, Salesforce).'),
            (1, 'Theoretical problem, no clear market, or squarely on an incumbent\'s near-term product roadmap.'),
        ]
    ),
    (
        'Product Usefulness\n(MOST IMPORTANT)',
        'Primary gate: Usefulness < 3 means not_recommended regardless of other scores. Anchor: Sean Ellis test — "How would you feel if this product disappeared tomorrow?"',
        [
            (5, 'Solves a frequent, painful problem with no good existing alternative. Users would be "very disappointed" if it disappeared. Hair-on-fire problem.'),
            (4, 'Clear recurring pain. Existing solutions are meaningfully worse. Users would miss it but could awkwardly work around it.'),
            (3, 'Real but moderate pain. Alternatives exist and are adequate. Nice-to-have that some users actively want.'),
            (2, 'Infrequent use case, or improvement over alternatives is marginal. Most users would not notice it was gone.'),
            (1, 'Vague problem, people have already adapted to this pain, or the product addresses a symptom not the real underlying need.'),
        ]
    ),
    (
        'Feasibility &\nDefensibility',
        'Two components combined: (1) Can it be built reliably? (2) Can it be sustained? A technically easy product with no moat is as risky as a hard one. Moat types: data flywheel, network effects, switching costs, proprietary distribution.',
        [
            (5, 'Technically proven or low-risk to build. Clear durable moat: data flywheel, network effects, or deep workflow lock-in.'),
            (4, 'Achievable with manageable risk. Real edge exists: proprietary data, integration depth, or first-mover in a defined niche.'),
            (3, 'Achievable, technically undifferentiated. Moat is execution-only — copyable within 12 months by a well-funded competitor.'),
            (2, 'Significant platform dependency risk (platform owner can ship this natively), OR technically complex with unproven reliability at scale.'),
            (1, 'Relies on technology that does not reliably work yet, OR hardware bet without software validation first, OR directly in a platform giant\'s roadmap.'),
        ]
    ),
    (
        'Monetization\nViability',
        'Value capture must align with value delivery. Score on: proven willingness to pay, clarity of pricing model, LTV potential.',
        [
            (5, 'Proven WTP in adjacent products. Clear B2B/prosumer pricing analog. High LTV, incentives align with user outcomes.'),
            (4, 'Monetizable with some friction. Clear budget line item exists for this category. Pricing model is obvious.'),
            (3, 'Monetizable but requires behavior change or user education. Consumer subscription with uncertain retention.'),
            (2, 'Consumer freemium with weak conversion path, OR monetization requires scale that does not exist yet.'),
            (1, 'No clear monetization path, purely ad-supported, or the value sits in a layer this product does not own.'),
        ]
    ),
]

current_row = 3
for (dim_label, note, scores) in rubrics:
    n_rows = len(scores) + 1
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row + n_rows, end_column=1)
    dim_cell = ws.cell(row=current_row, column=1, value=dim_label)
    dim_header_style(dim_cell)
    apply_border(dim_cell)

    # Note row
    note_label = ws.cell(row=current_row, column=2, value='Note')
    note_label.font = Font(bold=True, italic=True, size=9, color='595959')
    note_label.fill = PatternFill('solid', fgColor='F2F2F2')
    note_label.alignment = Alignment(horizontal='center', vertical='center')
    apply_border(note_label)

    note_cell = ws.cell(row=current_row, column=3, value=note)
    note_style(note_cell)
    apply_border(note_cell)
    ws.row_dimensions[current_row].height = 42
    current_row += 1

    for (score, criteria) in scores:
        score_cell = ws.cell(row=current_row, column=2, value=score)
        score_style(score_cell, score)
        apply_border(score_cell)

        criteria_cell = ws.cell(row=current_row, column=3, value=criteria)
        criteria_style(criteria_cell)
        apply_border(criteria_cell)

        ws.row_dimensions[current_row].height = 36
        current_row += 1

    ws.row_dimensions[current_row].height = 10
    current_row += 1

# Signal mapping
current_row += 1
ws.merge_cells(f'A{current_row}:C{current_row}')
sig_title = ws.cell(row=current_row, column=1, value='Build Signal Mapping  (3 signals — explore_more removed)')
header_style(sig_title)
ws.row_dimensions[current_row].height = 22
current_row += 1

signals = [
    ('strong_yes',      'E2EFDA', 'Usefulness >= 4  AND  average across all dimensions >= 3.5'),
    ('cautious_yes',    'FFF2CC', 'Usefulness >= 3  AND  average >= 3.0  AND  no dimension scores below 2'),
    ('not_recommended', 'FFD7D7', 'Usefulness <= 2  OR  two or more dimensions score 1  OR  average < 2.5\nGate rule: usefulness < 3 → not_recommended regardless of other scores'),
]

for (signal, color, rule) in signals:
    sig_cell = ws.cell(row=current_row, column=1, value=signal)
    sig_cell.font = Font(bold=True, size=10)
    sig_cell.fill = PatternFill('solid', fgColor=color)
    sig_cell.alignment = Alignment(horizontal='center', vertical='center')
    apply_border(sig_cell)

    ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=3)
    rule_cell = ws.cell(row=current_row, column=2, value=rule)
    rule_cell.font = Font(size=10)
    rule_cell.fill = PatternFill('solid', fgColor=color)
    rule_cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    apply_border(rule_cell)
    apply_border(ws.cell(row=current_row, column=3))
    ws.row_dimensions[current_row].height = 40
    current_row += 1

wb.save('data/product_hunt_ideas.xlsx')
print('Rubrics sheet created successfully.')
