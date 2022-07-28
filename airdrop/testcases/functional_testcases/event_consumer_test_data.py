import json
DEPOSIT_EVENT = {
    "Records": [{
        "messageId": "e7ccb647-8820-43e5-9d88-19f75a5bd390",
        "receiptHandle": "test_receipt",
        "body": json.dumps({
            "Type": "Notification",
            "MessageId": "4ffadeda-b19a-57a0-9c0f-8589df44a185",
            "TopicArn": "arn:aws:sns:us-east-1:533793137436:rt-v2-cardano-event-listener",
            "Message": json.dumps({
                "id": "3b6a67197c6c412c952b5486156148e6",
                "tx_hash": "edf5f74112670b7b5f8c003a42bcbc410d35abbee2d6566068a1c30201d0f735",
                "event_type": "TOKEN_TRANSFER",
                "address": "addr_test1qqllt2lmzypu9y9j9p6hgrcu9narh8rqczkdujqvqmqq4f9w9zv7f7pu6wefmn4t06y9e9ljg"
                           "gpjul3awg0p8tz664fse7qsex",
                "event_status": None,
                "updated_at": "2022-07-21 15:09:32",
                "asset": {
                    "id": "1aa646b44ce44febba7b75f8716339c7",
                    "asset": "6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce5041474958",
                    "policy_id": "6f1a1f0c7ccf632cc9ff4b79687ed13ffe5b624cce288b364ebdce50",
                    "asset_name": "41474958",
                    "allowed_decimal": 8,
                    "updated_at": "2022-03-17 12:51:13"
                },
                "transaction_detail": {
                    "id": "dcdd4145cb4840baa44e2dce8a404839",
                    "tx_type": "ADA_TRANSFER",
                    "assurance_level": "LOW",
                    "confirmations": 3,
                    "tx_amount": "1E+8",
                    "tx_fee": "191681",
                    "block_number": 3724538,
                    "block_time": 1658416153,
                    "input_addresses": ["addr_test1qqera830frgpvw9f0jj2873lwe8nd8vcsf0q0ftuqqgd9g8ucaczw427uq8y7axn2v3w8dua87kjgdgurmgl38vd2hysk4dfj9"],
                    "tx_metadata": [{
                        "label": "1",
                        "json_metadata": {
                            "registration_id": "VkMBsWZsK1bn3mxXQlhPxW8FWzKvewws+yZjHourUGpsIkV0ytus2JrIWs9uA8x5q0le4cMyqmJNmq+2ZbLanxw=",
                            "signature": "0xbabc34c8c4a26f58c7dffa6cec28af2abcdb0e2cf6f289baea2d52ee3cd56ef058a2794c27a00411f8a7756dd0cefeb0f166b970d6a8196bc4c2d3722bbf1eb21c",
                            "airdrop_window_id": "23"
                        }
                    }],
                    "updated_at": "2022-07-21 15:11:26"
                }
            }),
            "Timestamp": "2022-07-21T15:11:26.116Z",
            "SignatureVersion": "1",
            "Signature": "signature",
            "SigningCertURL": "",
            "UnsubscribeURL": ""
        }),
        "attributes": {
            "ApproximateReceiveCount": "1",
            "SentTimestamp": "1658416286154",
            "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
            "ApproximateFirstReceiveTimestamp": "1658416286157"
        },
        "messageAttributes": {},
        "md5OfBody": "d57fdf832148fabee6330cadaf72eb74",
        "eventSource": "aws:sqs",
        "eventSourceARN": "",
        "awsRegion": "us-east-1"
    }]
}
