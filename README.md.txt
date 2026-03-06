# AWS Cloud Security Monitoring System

• Overview

This project implements a serverless cloud security monitoring pipeline on AWS that detects and alerts on suspicious security-related events using CloudTrail logs.

The system monitors security-sensitive actions such as security group modifications, IAM permission changes, root account usage, and security group deletions. When such events occur, an automated alert is sent to security administrators via email.

This project demonstrates practical cloud security monitoring similar to solutions used in Security Operations Centers (SOC).

---

• Architecture

The architecture follows an event-driven serverless design.

CloudTrail → EventBridge → Lambda → SNS → Email Alert

Services used:

- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda
- Amazon SNS
- AWS IAM
- Amazon EC2 (for test events)

---

• Security Events Detected

The system detects the following security events:

1. Security Group Ingress Changes
Detects when a new inbound rule is added to a security group.

Example risk:
Opening SSH (port 22) to the internet.

Event:
AuthorizeSecurityGroupIngress

---

2. Security Group Deletion
Detects when a security group is deleted.

Event:
DeleteSecurityGroup

---

3. Root Account Usage
Detects any AWS API activity performed using the root account.

This is considered a high-risk activity in cloud environments.

---

4. IAM Permission Changes
Detects when IAM policies are created or attached to users.

Events monitored:

- AttachUserPolicy
- PutUserPolicy
- CreatePolicy
- DeletePolicy

---

Event Detection Logic

Example EventBridge rule:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["AWS API Call via CloudTrail"],
  "detail": {
    "eventName": ["AuthorizeSecurityGroupIngress"]
  }
}
```

---

• Lambda Alert Handler

The Lambda function extracts important fields from the event and sends a structured alert email.

Example alert:

```
AWS Security Alert
=================
Event: Security Group Change
User: admin
Security Group: sg-12345
Port: 22
CIDR: 0.0.0.0/0
Region: eu-north-1
Time: 2026-03-06T19:46:12
```

---

• Testing Procedure

The following tests were performed:

| Test                      | Action                   | Result         |
|          -----            |         ------           |    ------      |
| Security group rule added | Open port 8080           | Alert received |
| Security group deleted    | Delete test SG           | Alert received |
| IAM policy attached       | Attach S3 policy to user | Alert received |
| Root account login        | Perform API action       | Alert received |

---

• Security Benefits

This system provides:

- Real-time cloud security monitoring
- Detection of misconfigurations
- Detection of privilege escalation attempts
- Root account activity monitoring
- Automated alerting

---

• Future Improvements

Possible extensions:

- Automatic remediation (closing exposed ports)
- Integration with SIEM platforms
- Storing alerts in DynamoDB for investigation
- Slack or Microsoft Teams notifications
- Detection of unusual login locations

---
