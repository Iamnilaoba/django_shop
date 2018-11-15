# 1.生成一个网页地址，访问微博第三方登录页面，登录后生成一个code
def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_uri = "http://127.0.0.1:8000/complete/weibo/"
    client_id = '746123259'
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={re_url}".format(client_id=client_id,                                                                         re_url=redirect_uri)
    print(auth_url)

# 2.拿着这个code（授权码）去获得access_token
def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": "746123259",
        "client_secret": "b5ff496f0ddbd2590f5c0570d7e61a2e",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/complete/weibo/",
    })
    return re_dict

# 3.拿到access_token后就可以获得这个用户的信息了
def get_user_info(access_token):
  user_url = "https://api.weibo.com/2/users/show.json"
  uid = "5020302235"
  get_url = user_url+"?access_token={at}&uid={uid}".format(at=access_token,uid=uid)
  print(get_url)

if __name__ == '__main__':
 # get_auth_url()
  r=get_access_token(code='aeb7d91a6d7c30bbe91bcb45155f6f85')
  print(r)
  #get_user_info(access_token='**********2892e8c6shqQsB')
