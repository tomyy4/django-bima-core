# -*- coding: utf-8 -*-

import os
import vimeo


class VimeoAPIError(Exception):
    """Base exception for Vimeo API errors."""


def upload_video(vimeo_account, file_path, title, description='', tags=None):
    """
    Upload video file to Vimeo.
    """
    try:
        v = vimeo.VimeoClient(token=vimeo_account.access_token)
        video_uri = v.upload(file_path)
        video = v.patch(video_uri, data={
            'name': title,
            'description': description,
        })
        if tags:
            url = os.path.join(video_uri, 'tags', ', '.join(tags))
            video = v.put(url)
    except Exception as e:
        raise VimeoAPIError('Error uploading video to Vimeo') from e

    if video.status_code != 200:
        raise VimeoAPIError('Vimeo error, status code: {}'.format(video.status_code))

    return {
        'uri': video_uri,
        'id': video_uri.split('/')[-1],
    }
