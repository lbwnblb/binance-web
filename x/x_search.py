import json
import time

import requests

import utils
from utils import convert_to_beijing_time, translate_a


def for_search_time_line(json_data,list_data,type_='new'):
    instructions = json_data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions']
    # 获取一遍最新的
    obj_list = []
    txt_str = ''
    for instruction in instructions:
        if 'entries' in instruction:
            for entry in instruction['entries']:
                obj = {}
                obj['type'] = type_
                if 'content' not in entry:
                    continue
                if 'itemContent' not in entry['content']:
                    continue
                if 'tweet_results' not in entry['content']['itemContent']:
                    continue
                if 'legacy' not in entry['content']['itemContent']['tweet_results']['result']:
                    continue
                legacy = entry['content']['itemContent']['tweet_results']['result']['legacy']
                created_at = convert_to_beijing_time(legacy['created_at'])
                obj['created_at'] = created_at
                full_text = legacy['full_text']
                full_text = full_text.replace('\n', ' ')
                txt_str += full_text+'\n'
                obj['full_text'] = full_text

                obj_list.append(obj)
    # for obj in obj_list:
    trans_result =  utils.baidu_translate(txt_str)
    if len(trans_result) == 1:
        for obj in obj_list:
            obj['full_text'] = utils.baidu_translate(obj['full_text'],type_='one')
            obj['type'] = type_
            list_data.append(obj)
    else:
        for index,trans in enumerate(trans_result):
            obj_list[index]['full_text'] = trans
            list_data.append(obj_list[index])






    # return obj_list
type_s = ['new','hot','#_new','#_hot']

def search_time_line(symbol,cursor="",type_='new'):
    cookies = {
        'guest_id': 'v1%3A173232214915855088',
        'night_mode': '2',
        'g_state': '{"i_l":0}',
        'kdt': 'PUW5FtHKTtvbK2ehRHAX8JQrTjvMBUZ7NsFtX7mt',
        'auth_token': '133237549607a85e7c76942679f7101505a0cb31',
        'ct0': '48b6d6cc9eb2cb03d8c164b5f8590ef0ede13fe09da9a1fef960d17b972a6a64d85c0ea2633dbf3e294bb07e111221e4c19d71943d89b89fe83f9df0dcbb5122bb71e276ae94ebea45668bd0adcfc050',
        'twid': 'u%3D1812305592842858496',
        'd_prefs': 'MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw',
        'guest_id_ads': 'v1%3A173232214915855088',
        'guest_id_marketing': 'v1%3A173232214915855088',
        'personalization_id': '"v1_qHi/OvMBDKJZ5GsT/Rnu6w=="',
        'lang': 'zh-cn',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        # 'cookie': 'guest_id=v1%3A173232214915855088; night_mode=2; g_state={"i_l":0}; kdt=PUW5FtHKTtvbK2ehRHAX8JQrTjvMBUZ7NsFtX7mt; auth_token=133237549607a85e7c76942679f7101505a0cb31; ct0=48b6d6cc9eb2cb03d8c164b5f8590ef0ede13fe09da9a1fef960d17b972a6a64d85c0ea2633dbf3e294bb07e111221e4c19d71943d89b89fe83f9df0dcbb5122bb71e276ae94ebea45668bd0adcfc050; twid=u%3D1812305592842858496; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A173232214915855088; guest_id_marketing=v1%3A173232214915855088; personalization_id="v1_qHi/OvMBDKJZ5GsT/Rnu6w=="; lang=zh-cn',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': f'https://x.com/search?q=%24{symbol}&src=typed_query&f=live',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-client-transaction-id': 'RalL7JXSl/FU+PQJkLxOi7yiEGggT0N3HbudySyMfWNiYaCR2Q5T+5AN1dh4skTY+RVdaUY4C6AHJoaV8mJqtPfOwZ2fRg',
        'x-csrf-token': '48b6d6cc9eb2cb03d8c164b5f8590ef0ede13fe09da9a1fef960d17b972a6a64d85c0ea2633dbf3e294bb07e111221e4c19d71943d89b89fe83f9df0dcbb5122bb71e276ae94ebea45668bd0adcfc050',
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'zh-cn',
    }

    params = {
        'variables': '{"rawQuery":"$ETH","count":40,"querySource":"typed_query","product":"Latest"}',
        'features': '{"profile_label_improvements_pcf_label_in_post_enabled":false,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_grok_analyze_post_followups_enabled":false,"responsive_web_grok_share_attachment_enabled":true,"articles_preview_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
    }
    params['variables'] = json.loads(params['variables'])
    # params['variables']['cursor'] = cursor
    params['variables']['rawQuery'] = f"${symbol}"
    # DAADDAABCgABGglzk7qbMJEKAAIaCWfdBtrBAAAIAAIAAAABCAADAAAABAgABAAAAAQKAAUaCWtqgEDDUAoABhoJa2qAPzywAAA
    # DAADDAABCgABGglzfMNbkdEKAAIaCWfdBtrBAAAIAAIAAAABCAADAAAAAwgABAAAAAQKAAUaCWtqgECcQAoABhoJa2qAPzywAAA

    list_data = []
    if type_ == '#_new':
        headers['referer'] = f'https://x.com/search?q=%23{symbol}&src=typed_query&f=live'
        params['variables']['rawQuery'] = f"#{symbol}"
    elif type_ == 'hot':
        # 热门
        headers['referer'] = f'https://x.com/search?q=%24{symbol}&src=typed_query'
        # params['variables'] = json.loads(params['variables'])
        params['variables']['product'] = 'Top'
    elif type_ == '#_hot':
        # 'https://x.com/search?q=%23ZK&src=typed_query&f=top'
        headers['referer'] = f'https://x.com/search?q=%23{symbol}&src=typed_query&f=top'
        params['variables']['rawQuery'] = f"#{symbol}"
        params['variables']['product'] = 'Top'
    params['variables'] = json.dumps(params['variables'])
    response = requests.get(
        'https://x.com/i/api/graphql/BkkaU7QQGQBGnYgk4pKh4g/SearchTimeline',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    for_search_time_line(response.json(), list_data,type_=type_)
    return list_data

if __name__ == '__main__':

    list_ = search_time_line(symbol='UXLINK',type_='new')
    for l in list_:
        print(l)
