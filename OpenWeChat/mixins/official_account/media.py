import json

# TODO: 校验素材内容


class MediaMixin:
    _MEDIA_TYPE_SET = {'image', 'voice', 'video', 'thumb'}

    def upload_temporary_media(self, media_type, files):
        """上传临时素材
        文档见: https://developers.weixin.qq.com/doc/offiaccount
        /Asset_Management/New_temporary_materials.html
        ---------------
        参数
        参数    是否必须    说明
        access_token    是  调用接口凭证
        type    是
        媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        media   是
        form-data中媒体文件标识，有filename、filelength、content-type等信息
        ---------------
        响应数据
        {"type":"TYPE","media_id":"MEDIA_ID","created_at":123456789}

        """
        if media_type not in self._MEDIA_TYPE_SET:
            raise ValueError('invalid media_type: {}'.format(media_type))
        params = {
            'access_token': self.auth.access_token,
            'type': media_type
        }
        with self._do_request(
                'POST', '/cgi-bin/media/upload', params=params,
                files=files) as resp_json:
            return resp_json['media_id']

    def upload_permanent_media(self,
                               media_type,
                               files,
                               title=None,
                               introduction=None):
        """上传永久素材
        文档见:
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/
        Adding_Permanent_Assets.html
        ---------------
        参数
        参数    是否必须    说明
        access_token    是  调用接口凭证
        type    是
        媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb）
        media   是  form-data中媒体文件标识，有filename、filelength、content-type等信息
        ---------------
        响应数据
        {
            "media_id":MEDIA_ID,
            "url":URL
        }
        新增的图片素材的图片URL（仅新增图片素材时会返回该字段）
        """
        if media_type not in self._MEDIA_TYPE_SET:
            raise ValueError('invalid media_type: {}'.format(media_type))
        params = {
            'access_token': self.auth.access_token,
            'type': media_type
        }
        kwargs = {'params': params, 'files': files}
        # 如果media_type是video，需要添加额外的参数
        if media_type == 'video':
            if not title or not introduction:
                raise ValueError('invalid title or introduction')
            data = {
                'description': json.dumps({
                    'title': title,
                    'introduction': introduction
                })
            }
            kwargs['data'] = data
        with self._do_request('POST', '/cgi-bin/material/add_material',
                              **kwargs) as resp_json:
            return resp_json['media_id'], resp_json['url']

    def upload_news_media(self):
        """上传图文素材
        """
        raise NotImplementedError()
