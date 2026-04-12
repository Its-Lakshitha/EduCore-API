def calculate_grade(marks, total):
    percentage = (marks / total) * 100

    if percentage >= 75:
        return 'A', True
    elif percentage >= 65:
        return 'B', True
    elif percentage >= 55:
        return 'C', True
    elif percentage >= 35:
        return 'S', True
    else:
        return 'F', False