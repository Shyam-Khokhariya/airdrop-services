from unittest import TestCase
from unittest.mock import Mock
from airdrop.application.services.airdrop_services import AirdropServices
from http import HTTPStatus
from airdrop.constants import AirdropClaimStatus
from airdrop.infrastructure.repositories.airdrop_repository import AirdropRepository
from airdrop.infrastructure.models import AirdropWindow, Airdrop
from datetime import datetime, timedelta
from unittest.mock import patch


class AirdropClaims(TestCase):
    def setUp(self):

        org_name = 'SINGNET'
        token_name = 'AGIX'
        token_type = 'CONTRACT'
        portal_link = 'https://ropsten-airdrop.singularitynet.io/'
        documentation_link = 'https://ropsten-airdrop.singularitynet.io/'
        description = 'This is a test airdrop'
        github_link = 'https://github.com/singnet/airdrop-services'
        airdrop_window_name = 'Test Airdrop Window'
        airdrop_window_description = 'This is a test airdrop window'
        registration_required = True
        registration_start_date = datetime.utcnow()
        registration_end_date = datetime.utcnow() + timedelta(days=30)
        snapshot_required = True
        snapshot_start_date = datetime.utcnow()
        claim_start_date = datetime.utcnow()
        claim_end_date = datetime.utcnow() + timedelta(days=30)

        contract_address = '0x5e94577b949a56279637ff74dfcff2c28408f049'
        token_address = '0x5e94577b949a56279637ff74dfcff2c28408f049'
        user_address = '0x176133a958449C28930970989dB5fFFbEdd9F449'

        airdrop_repository = AirdropRepository()
        airdrop = airdrop_repository.register_airdrop(
            token_address, org_name, token_name, token_type, contract_address, portal_link, documentation_link, description, github_link)
        airdrop_repository.register_airdrop_window(airdrop_id=airdrop.id, airdrop_window_name, airdrop_window_description, registration_required, registration_start_date, registration_end_date, snapshot_required, snapshot_start_date, claim_start_date, claim_end_date)

    def test_get_signature_for_airdrop_window_claim(self):

        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F449",
            "airdrop_id": "1",
            "airdrop_window_id": "1"
        }

        status_code, result = AirdropServices().airdrop_window_claims(payload)

        expected_reult = {
            "status": 200,
            "data": {
                "claim": {
                    "airdrop_id": "1",
                    "airdrop_window_id": "1",
                    "user_address": "0x176133a958449C28930970989dB5fFFbEdd9F449",
                    "signature": "0xcb2ce8ea4749f58f0ea3cee7b5ed7686c67ccd1179dd526e080d6aa7fde69f70",
                    "claimable_amount": "100",
                    "token_address": "0x5e94577b949a56279637ff74dfcff2c28408f049"
                }
            },
            "message": "OK"
        }

        self.assertEqual(status_code, HTTPStatus.OK.value)
        assert result == expected_reult

    def test_get_signature_for_airdrop_window_claim_with_invalid_windows(self):
        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F442",
            "airdrop_id": "100",
            "airdrop_window_id": "100"
        }

        status_code, result = AirdropServices().airdrop_window_claims(payload)

        self.assertNotEqual(status_code, HTTPStatus.BAD_REQUEST.value)

    def test_airdrop_window_claim_txn_status(self):

        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "airdrop_id": "1",
            "airdrop_window_id": "1",
            "txn_status": AirdropClaimStatus.SUCCESS,
            "txn_hash": "0xcb2ce8ea4749f58f0ea3cee7b5ed7686c67ccd1179dd526e080d6aa7fde69f70",
            "amount": "100"
        }

        status_code, result = AirdropServices().airdrop_window_claim_status(payload)

        self.assertEqual(status_code, HTTPStatus.OK.value)

    def test_airdrop_window_claim_duplicate_txn_status(self):

        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "airdrop_id": "1",
            "airdrop_window_id": "1",
            "txn_status": AirdropClaimStatus.SUCCESS,
            "txn_hash": "0xcb2ce8ea4749f58f0ea3cee7b5ed7686c67ccd1179dd526e080d6aa7fde69f70",
            "amount": "100"
        }

        status_code, result = AirdropServices().airdrop_window_claim_status(payload)

        self.assertEqual(status_code, HTTPStatus.BAD_REQUEST.value)

    def test_airdrop_window_claim_history(self):

        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F447",
            "airdrop_id": "1"
        }

        status_code, result = AirdropServices().airdrop_window_claim_history(payload)
        now = str(datetime.utcnow())

        expected_reult = {
            "status": 200,
            "data": {
                "claim_history": [
                    {
                        "airdrop_id": 1,
                        "airdrop_window_id": 1,
                        "user_address": "0x176133a958449C28930970989dB5fFFbEdd9F447",
                        "txn_hash": "0x54990b02618bb025e91f66bd253baa77522aff4b0140440f5aecdd463c24b2fc",
                        "txn_status": "SUCCESS",
                        "claimable_amount": 100,
                        "registered_at": now,
                        "is_eligible": True
                    }
                ]
            },
            "message": "OK"
        }

        self.assertEqual(status_code, HTTPStatus.OK.value)
        assert result == expected_reult

    def test_airdrop_window_claim_history(self):

        payload = {
            "address": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "airdrop_id": "1",
            "airdrop_window_id": "1"
        }

        status_code, result = AirdropServices().airdrop_window_claim_history(payload)

        result_length = result['data']['claims'].__len__()

        self.assertLessEqual(result_length, 1)

    def test_airdrop_services_update_airdrop_window_claim_status(self):

        event = {'block_no': 6247992, 'event': 'Claim',
                 'json_str': "{'authorizer': '0xD93209FDC420e8298bDFA3dBe340F366Faf1E7bc', 'claimer': '0x35d603B1433C9fFf79B61c905b07822684834542', 'amount': 0, 'airDropId': 1, 'airDropWindowId': 1}",
                 'processed': 0,
                 'transactionHash': "0x62a730ef8a537d09ee9064da3f57ad3ff3027399c91daa531e41a6c4e10af45a",
                 'logIndex': '43', 'error_code': 200, 'error_msg': ''}

        response = AirdropServices().update_airdrop_window_claim_status(event)

        self.assertEqual(response, True)

    def test_airdrop_listen_to_events(self):

        payload = {
            "transactionHash": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "json_str": "{'authorizer': '0xD93209FDC420e8298bDFA3dBe340F366Faf1E7bc', 'claimer': '0x35d603B1433C9fFf79B61c905b07822684834542', 'amount': 0, 'airDropId': 1, 'airDropWindowId': 1}",
            "event": "Claim"
        }

        event = {"data": payload}

        response = AirdropServices().airdrop_listen_to_events(event)

        self.assertEqual(response, True)

    def test_airdrop_listen_to_events_with_duplicate_data(self):

        payload = {
            "transactionHash": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "json_str": "{'authorizer': '0xD93209FDC420e8298bDFA3dBe340F366Faf1E7bc', 'claimer': '0x35d603B1433C9fFf79B61c905b07822684834542', 'amount': 0, 'airDropId': 1, 'airDropWindowId': 1}",
            "event": "Claim"
        }

        event = {"data": payload}

        response = AirdropServices().airdrop_listen_to_events(event)

        self.assertEqual(response, False)

    def test_airdrop_listen_to_events_with_invalid_event(self):

        payload = {
            "transactionHash": "0x176133a958449C28930970989dB5fFFbEdd9F417",
            "json_str": "{'conversionAuthorizer': '0xD93209FDC420e8298bDFA3dBe340F366Faf1E7bc'}",
            "event": "NewAuthorizer"
        }

        event = {"data": payload}

        response = AirdropServices().airdrop_listen_to_events(event)

        self.assertEqual(response, False)

    @ patch("airdrop.application.services.airdrop_services.AirdropServices.get_txn_receipt")
    def test_airdrop_get_txn_receipt_for_success_txn(self):

        expected_result = Mock({
            'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
            'blockNumber': 46147,
            'contractAddress': None,
            'cumulativeGasUsed': 21000,
            'from': '0xA1E4380A3B1f749673E270229993eE55F35663b4',
            'gasUsed': 21000,
            'logs': [],
            'logsBloom': '0x0000000000000000000000000000000000000000000000000000',
            'status': 1,
            'to': '0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
            'transactionHash': '0xa649b2b7063eea00942cb1b614ce0b750583a597738b43ae73b3f082d405c663',
            'transactionIndex': 0,
        })

        txn_hash = "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"

        response = AirdropServices().get_txn_receipt(txn_hash)

        self.assertEqual(response, expected_result)

    @patch("airdrop.application.services.airdrop_services.AirdropServices.get_txn_receipt")
    def test_airdrop_get_txn_receipt_for_pending_txn_hash(self):

        expected_result = Mock(None)

        txn_hash = "0x5637e466d23afb61ddacc06c1f302d05b878ea0071326d335f9589007788cff5"

        response = AirdropServices().get_txn_receipt(txn_hash)

        self.assertEqual(response, expected_result)

    @patch("airdrop.application.services.airdrop_services.AirdropServices.get_txn_receipt")
    def test_airdrop_get_txn_receipt_for_failure_txn(self):

        expected_result = Mock({
            'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
            'blockNumber': 46147,
            'contractAddress': None,
            'cumulativeGasUsed': 21000,
            'from': '0xA1E4380A3B1f749673E270229993eE55F35663b4',
            'gasUsed': 21000,
            'logs': [],
            'logsBloom': '0x0000000000000000000000000000000000000000000000000000',
            'status': 0,
            'to': '0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
            'transactionHash': '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',
            'transactionIndex': 0,
        })

        txn_hash = "0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060"

        response = AirdropServices().get_txn_receipt(txn_hash)

        self.assertEqual(response, expected_result)

    def tearDown(self):

        contract_address = '0x5e94577b949a56279637ff74dfcff2c28408f049'
        token_address = '0x5e94577b949a56279637ff74dfcff2c28408f049'

        airdrop_repo = AirdropRepository()
        airdrop = airdrop_repo.get_token_address(token_address)
        airdrop_repo.session.query(Airdrop).filter(
            Airdrop.contract_address == contract_address).delete()
        airdrop_repo.session.query(AirdropWindow).filter(
            AirdropWindow.airdrop_id == airdrop.id).delete()
