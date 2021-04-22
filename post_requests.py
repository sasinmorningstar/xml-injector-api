import requests
# from requests_xml import XML
# from requests.structures import CaseInsensitiveDict

url = "http://127.0.0.1:5000/xml-payload/"


payload = """
<ApplicationMessage>
    <family>Guptas</family>
    <message_type>Administration</message_type>
    <businessObjectId>Dharma</businessObjectId>
</ApplicationMessage>
"""


headers = {"Content-Type": "application/xml"}
post_request = requests.post(url, headers=headers, data=payload)

print(post_request.status_code)