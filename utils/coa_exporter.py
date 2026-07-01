import csv
import io

def generate_qbo_csv(accounts):
    """
    Takes a list of account dictionaries and generates a QBO-compatible CSV string.
    Expected dict keys: number, account_name, type, detail_type, description
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Exact QBO Headers
    writer.writerow(["Number", "Account Name", "Type", "Detail Type", "Description"])
    
    for acc in accounts:
        writer.writerow([
            acc.get("number", ""),
            acc.get("account_name", ""),
            acc.get("type", ""),
            acc.get("detail_type", ""),
            acc.get("description", "")
        ])
        
    return output.getvalue()
