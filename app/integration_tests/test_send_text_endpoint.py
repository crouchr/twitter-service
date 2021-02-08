import uuid
import integration_definitions
import call_rest_api


# TODO : parameterise this and send various combinations including None for optional parameters
def test_text():
    """
    Test /send_text
    :return:
    """
    query = {}
    this_uuid = uuid.uuid4().__str__()
    query['uuid'] = this_uuid
    query['app_name'] = 'integration_tests'
    query['tweet_text'] = 'integration test message'
    query['lat'] = integration_definitions.STOCKCROSS_LAT
    query['lon'] = integration_definitions.STOCKCROSS_LON
    query['hashtag_arg'] = 'testing times'      # this is two hashtags

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/send_text', query)

    if response_dict is None:
        return None

    assert status_code == 200
    assert response_dict['status'] == 'OK'
    assert response_dict['uuid'] == this_uuid

    assert response_dict['tweet_sent'] is True
    assert response_dict['tweet_len'] >= 40
