import uuid
import integration_definitions
import call_rest_api


def test_send_video():
    """
    Test /send_video
    :return:
    """
    query = {}
    this_uuid = uuid.uuid4().__str__()            # generate a uuid to simulate the client doing so
    query['uuid'] = this_uuid.__str__()
    query['app_name'] = 'integration_tests'
    query['video_pathname'] = integration_definitions.MEDIA_ROOT + 'test_images/twitter_test_video.mp4'
    query['tweet_text'] = 'integration test message'
    query['lat'] = integration_definitions.STOCKCROSS_LAT
    query['lon'] = integration_definitions.STOCKCROSS_LON
    query['hashtag_arg'] = 'testing times'  # this is two hashtags

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/send_video', query)

    if response_dict is None:
        return None

    assert status_code == 200
    assert response_dict['status'] == 'OK'
    assert response_dict['uuid'] == this_uuid

    assert response_dict['tweet_sent'] is True
    assert response_dict['tweet_len'] >= 40
