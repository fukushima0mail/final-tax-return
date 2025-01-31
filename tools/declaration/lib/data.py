
from db.account_titles import get_total_of_account


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

    accounts_pl = get_total_of_account()

    # Category 4: 収益
    profits = []
    for account in [a for a in accounts_pl if a[1] == CATEGORY_PROFIT]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * borrowing_type)
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

def get_bs_data():
    """
    貸借対照表のデータを計算して返す

    Returns:
        dict: 貸借対照表のデータ
            - assets (list of dict): 資産リスト [{'name': str, 'total': int}, ...]
            - liabilities (list of dict): 負債リスト [{'name': str, 'total': int}, ...]
            - net_assets (list of dict): 純資産リスト [{'name': str, 'total': int}, ...]
            - total_assets (int): 資産の合計金額
            - total_liabilities (int): 負債の合計金額
            - total_net_assets (int): 純資産の合計金額
    """
    CATEGORY_ASSET = 1
    CATEGORY_LIABILITY = 2
    CATEGORY_NET_ASSET = 3

    accounts_bs = get_total_of_account()

    # 資産 (Assets)
    assets = []
    for account in [a for a in accounts_bs if a[1] == CATEGORY_ASSET]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * borrowing_type)
        assets.append({"name": name, "total": total})

    # 負債 (Liabilities)
    liabilities = []
    for account in [a for a in accounts_bs if a[1] == CATEGORY_LIABILITY]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * borrowing_type)
        liabilities.append({"name": name, "total": total})

    # 純資産 (Net Assets)
    net_assets = []
    for account in [a for a in accounts_bs if a[1] == CATEGORY_NET_ASSET]:
        name, _, allocation, borrowing_type, debit_total, credit_total = account
        total = round((debit_total - credit_total) * borrowing_type)
        net_assets.append({"name": name, "total": total})

    # 合計値
    total_assets = sum([a["total"] for a in assets])
    total_liabilities = sum([l["total"] for l in liabilities])
    total_net_assets = sum([n["total"] for n in net_assets])

    return {
        "assets": assets,
        "liabilities": liabilities,
        "net_assets": net_assets,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_net_assets": total_net_assets,
    }
