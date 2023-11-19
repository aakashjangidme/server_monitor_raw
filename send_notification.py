# Function to send email notification
def send_email_notification(server_name, metric_name, threshold, message=None):
    print(f"send_email_notification:: server_name= {server_name}. metric_name = {metric_name}, threshold = {threshold}")
    print(f"send_email_notification:: message= {message}")
