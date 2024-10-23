import requests
from bs4 import BeautifulSoup

homePage = "https://25live.collegenet.com/pro/cpp#!/home/search"
login_page = "https://idp.cpp.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s2:"
test_page = 'https://cpp.libcal.com/spaces/auth?returnUrl=%2Freserve%2Fstudy-rooms&token=1qRW9s8i63wg33gdteDbMoOQGkaOAA4OXwGObOHfGyVLHFOyA8ayIkcxFQxLsTlh8'

login_payload = {
    'username': 'miguelguzman',
    'password': 'G00dFuture'
}

headers = {
    "Cookie": "lc_ea_po=001908db98a47d4baf92cdf909d6d99ad6fc6cbb02ee42926cd1ba9410223e3deab3e4efd1d5d2c32a0a922d35e2b1e9a8c7698dd509db028ef4ec4ee4b54fba949e87397dbd34affc76681e67f25c5caf0b9f5df03d7af800ca522650fb99eb2ef41bd5f9be947e80426e5ddc42f78b26914ab1586b2ed095b9bae9f2ba3042183d1ce3dffa46beaa1fb151669c26586df4fd2dd2252d71810801e1dd0df697a2622b13bc421b128b0e18b3522edd9bd7b033c0e; lc_ebcart=001c334a41deb714a582cf5b87ebe5c4200ba43f28ef536d1e4b9b14bec59f3af2848b6d0e86f4c9028f57946d94e891e6d3b52951f465a43436d99e5f2614ac220b6acdf4ae3a88b468e6b76b6d8401438c869a39bd4f2e2a8c4cee16a98716484feee0f68c629b2b429b60aeb0056a6a37c5e7327b37cb961b83963d407f68cb4ef8893415728d56bc0eb02e2e1dda8dcdfac49b3003a6b0892a49a96e3f4097950c456fb707118d442a703c759390dd795a4560d930fead1f1156447b6bebbe782a2e2831489806fe0a29d8c3c32e1cd15bf",
    "Referer": "https://cpp.libcal.com/reserve/study-rooms",
}

session = requests.Session()

print("starting the script")

response = session.get(test_page, headers=headers)
if response.ok:
    print("login successful")
    response = session.get(homePage)


    soup = BeautifulSoup(response.text, 'html.parser')
    
    print(soup.prettify)
else:
    print(f"Failed with status code {response.status_code}")
