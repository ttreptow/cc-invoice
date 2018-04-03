def billable_amount(line_item):
    return line_item.actual_amount + line_item.adjustments


def grand_total(line_items):
    return sum(map(billable_amount, line_items))

