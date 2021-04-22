import requests

url = "https://httpbin.org/post"

payload = """<ApplicationMessage>
    <family>Kurus</family>
    <message_type>Private</message_type>
    <businessObjectId>Custom</businessObjectId>
</ApplicationMessage>"""

headers = {"Content-Type": "application/xml"}

post_request = requests.post(url, headers=headers, data=payload)

print(post_request.status_code)
print(post_request.request.body)