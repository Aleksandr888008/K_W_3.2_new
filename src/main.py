from src.oper import get_operations_data, filter_operations_data, hide_sender_bill, hide_sender_bill_to, show

if __name__ == "__main__":
    operations_data = get_operations_data("../operations.json")
    filtered_data = filter_operations_data(operations_data)
    print(show(filtered_data))