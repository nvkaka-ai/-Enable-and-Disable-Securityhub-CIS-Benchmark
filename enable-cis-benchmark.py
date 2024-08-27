import boto3
import time

def enable_cis_benchmark(profile_name, region_name='us-east-1'):
    session = boto3.Session(profile_name=profile_name)
    securityhub_client = session.client('securityhub', region_name=region_name)
    response = securityhub_client.batch_enable_standards(
        StandardsSubscriptionRequests=[
            {
                'StandardsArn': f'arn:aws:securityhub:{region_name}::standards/cis-aws-foundations-benchmark/v/1.4.0'
            },
        ]
    )
    standards_subscription_arn = response['StandardsSubscriptions'][0]['StandardsSubscriptionArn']
    time.sleep(5)
    response = securityhub_client.get_enabled_standards(
        StandardsSubscriptionArns=[standards_subscription_arn]
    )
    standards_status = response['StandardsSubscriptions'][0]['StandardsStatus']
    print(f'StandardsStatus for {profile_name}: {standards_status}')
def main():
    with open('profiles.txt', 'r') as file:
        profiles = [line.strip() for line in file]
    for profile in profiles:
        enable_cis_benchmark(profile)

if __name__ == '__main__':
    main()
