import requests
import json
import csv
file_ = open('actrims_confex_2021_04_06.csv', 'a')
file_.write('session_url,papers_titile,authors,universities\n')
h = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "usersession=VAU-SllUQF2g6gHcuuEATw",
    "Host": "actrims.confex.com",
    "Pragma": "no-cache",
    "Referer": "https://actrims.confex.com/actrims/2019/meetingapp.cgi/Session/1154",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def parse_session(url):
    response = requests.get(url)
    if response:
        page_json = json.loads(response.content)
        session_ids = page_json[0].get('ChildList_SlotData')
        for sessions in session_ids:
            ids = sessions.split('Session')[-1].split('_')[0]
            session_url = 'https://actrims.confex.com/actrims/2019/meetingapi.cgi/Session/' + \
                ids+'/ChildList_PaperSlot?date=2021-04-06T17%3A52%3A03'
            parse_paper(session_url)


def parse_paper(url):
    session_url = url
    response = requests.get(url)
    if response:
        page_json = json.loads(response.content)
        for author_ids in page_json:
            author_entry_id = author_ids.get('Entryid')
            author_details_url = 'https://actrims.confex.com/actrims/2019/meetingapi.cgi' + \
                author_entry_id+'/ChildList_Role?date=2021-04-05T17%3A57%3A50'
            response = requests.get(author_details_url)
            if response:
                parse_author(response, session_url)


def parse_author(response, session_url):
    author_detail_json = json.loads(response.content)
    for authors_ in author_detail_json:
        city = authors_.get('Person_City')
        provinance = authors_.get('Person_StateProvince')
        Person_Credentials = authors_.get('Person_Credentials')
        Person_Prefix = authors_.get('Person_Prefix')
        author_first_name = authors_.get('Person_FirstName')
        author_middle_name = authors_.get('Person_MiddleName')
        author_last_name = authors_.get('Person_LastName')
        if Person_Prefix:
            author_name = Person_Prefix + ' '+author_first_name+' ' + \
                author_middle_name+' '+author_last_name+' '+Person_Credentials
        else:
            author_name = author_first_name+' '+author_middle_name + \
                ' '+author_last_name+' '+Person_Credentials
        author_universites = authors_.get('Person_Affiliation')
        universites = author_universites+' ' + city+' '+provinance
        item = {}
        item['papers_titile'] = authors_.get('Entry_Title').replace(',', '')
        item['session_url'] = session_url.split(
            '/ChildLis')[0].replace('/meetingapi', '/meetingapp')
        item['authors'] = author_name.replace(',', ' ')
        item['universities'] = universites.replace(',', ' ')
        print(item)
        data4 = [item.get('session_url'), item.get(
            'papers_titile'), item.get('authors'), item.get('universities')]
        row_data4 = ','.join(data4) + '\n'
        file_.write(row_data4)


if __name__ == "__main__":
    url = 'https://actrims.confex.com/actrims/2019/meetingapi.cgi/ModuleSessionsByDay/0/ChildList_Day?date=2021-04-06T04%3A40%3A08'
    parse_session(url)
