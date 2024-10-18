class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3
    WHITE = 4

def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    financial = data["financials"][financial_index]
    # Safely retrieve 'netRevenue' or return 0 if missing
    return financial.get("pnl", {}).get("lineItems", {}).get("netRevenue", 0)

def total_borrowing(data: dict, financial_index):
    financial = data["financials"][financial_index]
    # Safely retrieve borrowing values, defaulting to 0 if keys are missing
    long_term_borrowings = financial.get("bs", {}).get("lineItems", {}).get("longTermBorrowings", 0)
    short_term_borrowings = financial.get("bs", {}).get("lineItems", {}).get("shortTermBorrowings", 0)
    total_borrowings = long_term_borrowings + short_term_borrowings
    revenue = total_revenue(data, financial_index)
    return total_borrowings / revenue if revenue != 0 else 0

def iscr(data: dict, financial_index):
    financial = data["financials"][financial_index]
    profit_before_interest_and_tax = financial.get("pnl", {}).get("lineItems", {}).get("profitBeforeTax", 0)
    depreciation = financial.get("pnl", {}).get("lineItems", {}).get("depreciation", 0)
    interest_expense = financial.get("pnl", {}).get("lineItems", {}).get("interestExpense", 0)
    iscr_value = (profit_before_interest_and_tax + depreciation + 1) / (interest_expense + 1)
    return iscr_value

def iscr_flag(data: dict, financial_index):
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    ratio = total_borrowing(data, financial_index)
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER
