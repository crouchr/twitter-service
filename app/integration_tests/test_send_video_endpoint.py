import integration_definitions
import call_rest_api


def test_send_video():
    """
    Test /send_video
    :return:
    """
    query = {}
    query['app_name'] = 'integration_tests'
    query['video_pathname'] = '/home/crouchr/metminiwx_media/metminiwx_fri_jan_22_15_43_04_2021.mp4'
    query['tweet_text'] = 'test message'

    status_code, response_dict = call_rest_api.call_rest_api(integration_definitions.endpoint_base + '/send_video', query)

    if response_dict is None:
        return None

    assert status_code == 200
    assert response_dict['status'] == 'OK'


