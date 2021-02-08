# microservice
import os


from flask import Flask, jsonify, request

import definitions
import get_env
import mytwython

app = Flask(__name__)


# fixme : this does not give info about the actual exception
@app.errorhandler(500)
def error_handling(error):
    answer = {}
    answer['error'] = str(error)

    print('twitter_service() : error : ' + error.__str__())
    response = jsonify(answer, 500)

    return response


# an endpoint that can be polled with little overhead
@app.route('/status')
def status():
    answer = {}
    app_name = request.args.get('app_name')
    this_uuid = request.args.get('uuid')

    answer['status'] = 'OK'
    answer['uuid'] = this_uuid.__str__()
    answer['service_name'] = 'twitter-service'
    answer['version'] = get_env.get_version()

    print('status() : app_name=' + app_name.__str__() + ', version=' + answer['version'])
    response = jsonify(answer)

    return response


# @app.route('/stats')
# def stats():
#     answer = {}
#     app_name = request.args.get('app_name')
#     this_uuid = request.args.get('uuid')
#
#     answer['status'] = 'OK'
#     answer['api_calls'] = -1    # not yet implemented
#
#     print('status() : app_name=' + app_name.__str__() + ', api_calls=' + answer['api_calls'])
#     response = jsonify(answer)
#
#     return response

@app.route('/send_text')
def send_text_api():
    """
    Send a text-only Tweet
    :param app_name: e.g. name of the calling app so it can be identified in logs
    :return:
    """
    try:
        answer = {}
        app_name = request.args.get('app_name')
        this_uuid = request.args.get('uuid')
        tweet_text = request.args.get('tweet_text')
        lat = request.args.get('lat', None)
        lon = request.args.get('lon', None)
        hashtag_arg = request.args.get('hashtag_arg', None)    # not a list

        print('send_text_api() : app_name=' + app_name.__str__() +\
              ', uuid=' + this_uuid +\
              ', tweet_text=' + tweet_text.__str__())

        flag, send_time, tweet_len = mytwython.send_tweet(tweet_text, uuid=this_uuid, lat=lat, lon=lon, hashtag_arg=hashtag_arg, media_type='tweet', media_pathname=None)

        # Create response
        answer['status'] = 'OK'
        answer['uuid'] = this_uuid.__str__()
        answer['send_time'] = int(send_time)
        answer['tweet_sent'] = flag
        answer['tweet_len'] = tweet_len

        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'send_text_api()'
        answer['error'] = str(e)
        print('send_text_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__() + \
              ', uuid=' + this_uuid.__str__())
        response = jsonify(answer, 500)

        return response


@app.route('/send_video')
def send_video_api():
    """

    :param app_name: e.g. name of the calling app so it can be identified in logs
    :return:
    """
    try:
        answer = {}
        app_name = request.args.get('app_name')
        this_uuid = request.args.get('uuid')
        tweet_text = request.args.get('tweet_text')
        lat = request.args.get('lat', None)
        lon = request.args.get('lon', None)
        hashtag_arg = request.args.get('hashtag_arg', None)  # not a list
        video_pathname = request.args.get('video_pathname')

        print('send_video_api() : app_name=' + app_name.__str__() +
              ', uuid=' + this_uuid +
              ', video_pathname=' + video_pathname.__str__() +
              ', tweet_text=' + tweet_text.__str__())

        flag, send_time, tweet_len = mytwython.send_tweet(tweet_text, uuid=this_uuid, lat=lat, lon=lon, hashtag_arg=hashtag_arg, media_type='video', media_pathname=video_pathname)

        # Create response
        answer['status'] = 'OK'
        answer['uuid'] = this_uuid.__str__()
        answer['send_time'] = int(send_time)
        answer['tweet_sent'] = flag
        answer['tweet_len'] = tweet_len

        response = jsonify(answer)

        return response

    except Exception as e:
        answer['function'] = 'send_video_api()'
        answer['error'] = str(e)
        print('send_video_api() : app_name=' + app_name.__str__() + ', error : ' + e.__str__() +\
              ', uuid=' + this_uuid.__str__())
        response = jsonify(answer, 500)

        return response


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"            # does this help with log buffering ?
    version = get_env.get_version()                 # container version

    print('twitter-service started, version=' + version)

    app.run(host='0.0.0.0', port=definitions.twitter_listen_port.__str__())
