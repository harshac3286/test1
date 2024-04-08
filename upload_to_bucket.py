from datetime import date
import alert

def upload_to_s3(session):
    current_date = date.today().strftime('%d-%m-%Y')
    s3 = session.resource('s3')

    path = '/home/ubuntu/automation-scripts/azure_resource_report'
    try:
        s3.Bucket('azure-resource-report').upload_file(path +'/report/report_' + current_date + '.txt', 'report_' + current_date + '.txt')
        report_link = 'https://s3.console.aws.amazon.com/s3/object/azure-resource-report?region=ap-south-1&prefix={}'.format('report_' + current_date + '.txt')
        print(report_link)
       
        # send bitbucket link alert
        alert.send_daily_report(report_link)
    except Exception as e:
        print(e)