
from db.account_titles import get_pl


def get_pl_data():
    """
    損益計算書のデータを計算して返す

    Returns:
        dict: 損益計算書のデータ
            - profits (list of dict): 収益リスト [{'name': str, 'total': int}, ...]
            - losses (list of dict): 費用リスト [{'name': str, 'total': int}, ...]
            - net (int): 差引金額 (収益 - 費用)
            - special_deduction (int): 青色申告特別控除額
            - income_amount (int): 所得金額（控除後）
    """
    CATEGORY_PROFIT = 4
    CATEGORY_LOSS = 5

    accounts_pl = get_pl()

    # Category 4: 収益
    profits = []
    for account in [a for a in accounts_pl if a[1] == CATEGORY_PROFIT]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * allocation / 100 * borrowing_type)
        profits.append({"name": name, "total": total})

    # Category 5: 費用
    losses = []
    for account in [a for a in accounts_pl if a[1] == CATEGORY_LOSS]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * allocation / 100 * borrowing_type)
        losses.append({"name": name, "total": total})

    # 差引金額
    net = sum([p["total"] for p in profits]) - sum([l["total"] for l in losses])

    # 所得金額
    special_deduction = 650000
    income_amount = max(0, net - special_deduction)
    return {
        "profits": profits,
        "losses": losses,
        "net": net,
        "special_deduction": special_deduction,
        "income_amount": income_amount,
    }
