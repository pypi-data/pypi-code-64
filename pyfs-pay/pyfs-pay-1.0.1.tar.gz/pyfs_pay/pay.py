# -*- coding: utf-8 -*-

from pyfs_auth import TenantAccessToken, final_tenant_access_token


class Pay(TenantAccessToken):
    def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        super(Pay, self).__init__(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        # 查询用户是否在应用开通范围, Refer: https://open.feishu.cn/document/ukTMukTMukTM/uATNwUjLwUDM14CM1ATN
        self.CHECK_USER_PAID_SCOPE = self.OPEN_DOMAIN + '/open-apis/pay/v1/paid_scope/check_user?open_id={open_id}&user_id={user_id}'

    def check_user_paid_scope(self, open_id=None, user_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
        token = final_tenant_access_token(self, appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)
        return self.get(self.CHECK_USER_PAID_SCOPE, open_id=open_id or '', user_id=user_id or '', token=token).get('data', {})


pay = Pay()
check_user_paid_scope = pay.check_user_paid_scope
