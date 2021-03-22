import requests
import bs4
from useragents import user_agent_list
import random
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import numpy as np
import textract
from pathlib import Path
import re
import argparse
from db import db_connection, bulk_upsert
import datetime

baseuri = "https://www.edinburgh.gov.uk"
uri = "https://www.edinburgh.gov.uk/directory/10247/a-to-z/{}?page={}"
USER_AGENT = random.choice(user_agent_list)
LINKSCSV = "binlinks.csv"


def main(scrapestreetlinks=None, scrapepdflinks=None, download=None, parse=None):
    links = None
    if scrapestreetlinks:
        links = get_bin_links()
    if scrapepdflinks:
        if not links:
            links = pd.read_csv(LINKSCSV)
        links['pdf_url'] = links['uri'].apply(get_collection_pdf_link)
        links.to_csv("binlinks.csv")
    if download:
        if not links:
            links = pd.read_csv(LINKSCSV)
        get_collection_pdfs(links)
    if parse:
        if not links:
            links = pd.read_csv(LINKSCSV)
        links['filename'] = links['pdflink'].str.split("/").str[-1]
        times = parse_pdfs()
        bintimes = pd.merge(links, times, left_on='filename', right_on='filename', how='right').drop(
            columns=['Unnamed: 0'])
        bintimes.to_csv('bintimes.csv')
        bindicts = bintimes.to_dict(orient='records')
        for idx, bindict in enumerate(bindicts):
            bindict['_id'] = bindict['street'] + '_' + datetime.datetime.strftime(bindict['date'], '%Y-%m-%d')
            bindict['_id'] = bindict['_id'].replace(' ', '_').lower()
            bindict['city'] = 'Edinburgh'.lower()
            bindicts[idx] = bindict
        print('upserting {} records'.format(len(bindicts)))
        bulk_upsert(db_connection(), 'frontend', 'days', bindicts)


def colour_difference(colour1, colour2):
    return sum([(component1 - component2) ** 2 for component1, component2 in zip(colour1, colour2)])


def parse_pdfs():
    all = pd.DataFrame()
    dateregex = re.compile('DEC\n\d{4}')
    numberregex = re.compile("\d{2}")
    # target colours
    colours = {'blue': {'rgb': [0, 152, 205], 'bins': ['grey']},
               'green': {'rgb': [99, 180, 80], 'bins': ['green', 'box']},
               'yellow': {'rgb': [255, 204, 0], 'bins': ['grey', 'box']},
               'red': {'rgb': [213, 19, 23], 'bins': ['green']}}

    # target locations
    cols = [63, 127, 189, 253, 316, 378, 440, 500, 568, 631, 693, 756]
    rows = [235, 295, 345, 405, 460]
    px_radius = 3
    cols = [(col_num + 1, cc) for col_num, c in enumerate(cols) for cc in range(c - px_radius, c + px_radius)]
    rows = [(row_num + 1, rr) for row_num, r in enumerate(rows) for rr in range(r - px_radius, r + px_radius)]

    filtercols = ['year', 'month', 'day']

    for pdf in sorted(Path("./pdfs").rglob("*.pdf")):
        print(pdf.absolute())
        pages = convert_from_path(pdf.absolute(), 100)
        page = [page for page in pages][0]
        imgfile = Path('img').joinpath(pdf.name).absolute().with_suffix('.jpg')
        page.save(imgfile.absolute(), 'JPEG')

        imgpath = Path(imgfile)
        pdfpath = pdf
        im = Image.open(imgpath)  # Can be many different formats.
        pix = im.load()

        rgbs = []

        for col_num, x in cols:
            for row_num, y in rows:
                rgbs.append([col_num, row_num, x, y] + list(pix[x, y]))
        df = pd.DataFrame(rgbs, columns=['col_num', 'row_num', 'x', 'y', 'r', 'g', 'b'])

        df = df.groupby(['col_num', 'row_num']).mean().reset_index()
        for name, item in colours.items():
            colour = item['rgb']
            df[name] = df.apply(lambda x: colour_difference([x['r'], x['g'], x['b']], colour), axis=1)

        df['colour'] = df[['blue', 'green', 'yellow', 'red']].idxmin(axis=1)
        df['colour'] = np.where((df[['r', 'g', 'b']].mean(axis=1) > 250), 'white', df['colour'])
        df = df.sort_values(['row_num', 'col_num'])

        # attach pdf text
        view = textract.process(pdfpath).decode('utf8')
        dates = [x for x in re.split(dateregex, view)[1].split("\n") if re.match(numberregex, x)]
        dates = dates[:(df['colour'] != 'white').sum()]
        dates = pd.DataFrame(dates, columns=['day'])
        final = pd.concat([dates, df[df['colour'] != 'white'][['col_num', 'colour']].reset_index(drop=True)],
                          axis=1).rename({'col_num': 'month'}, axis=1)
        final['day'] = final['day'].astype(int)
        final['filename'] = imgpath.stem
        final['year'] = re.search(dateregex, view)[0][-4:]

        final = final[['filename', 'year', 'month', 'day', 'colour']]
        final['date'] = final[filtercols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")
        final['date'] = pd.to_datetime(final['date'])
        final['bins'] = final['colour'].apply(lambda x: colours[x]['bins'])
        final.drop(columns=['year', 'month', 'day', 'colour'], inplace=True)
        all = pd.concat([all, final])
    all.to_csv("all_bin_days.csv")
    return all


def get_collection_pdf_link(url):
    headers = {'User-Agent': USER_AGENT}
    session = requests.Session()
    session.get(url='https://www.edinburgh.gov.uk/bins-recycling', headers=headers)

    pdf_page = session.get(url)
    soup = bs4.BeautifulSoup(pdf_page.content, 'html.parser')
    pdf_divs = soup.find_all('div', {'class': 'definition__editor'})
    pdf_url = None
    for pdf_div in pdf_divs:
        pdf_url = pdf_div.find('a')['href']
        if not pdf_url.startswith("http"):
            pdf_url = f"{baseuri}{pdf_url}"

    print(pdf_url)
    return pdf_url


def get_collection_pdfs(links):
    headers = {'User-Agent': USER_AGENT}
    session = requests.Session()
    session.get(url='https://www.edinburgh.gov.uk/bins-recycling', headers=headers)
    for pdf_link in links['pdflink'].value_counts().index:
        url = pdf_link
        if url not in (None, 'None'):
            pdf = session.get(url)
            filepath = Path("./pdfs").joinpath(pdf_link.split("/")[-1]).with_suffix(".pdf")
            if pdf.status_code == 200:
                filepath.write_bytes(pdf.content)
    return


def get_bin_links():
    links = []
    for letter in [chr(x) for x in range(ord('a'), ord('z') + 1)]:
        page_no = 1

        url = uri.format(letter.upper(), page_no)
        list_items, pagination_link = get_street_links(url)
        if len(list_items):
            links.extend(list_items)

        while pagination_link is not None:
            page_no += 1
            list_items, pagination_link = get_street_links(pagination_link)
            if len(list_items):
                links.extend(list_items)

    df = pd.DataFrame(links, columns=['street', 'uri'])
    df.to_csv(LINKSCSV)
    return df


def get_street_links(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    print(url)
    ul = soup.find('ul', {'class': 'list--record'})
    links = []
    href = None
    if ul:
        list_items = ul.find_all('li', {'class': 'list__item'})
        pagination_links = soup.find_all('li', {'class': 'pagination__item'})

        if len(pagination_links) > 1:
            pagination_link = pagination_links[1]
            href = pagination_link.find('a')
        links = [li.find('a') for li in list_items]
        links = [(link.string, f"{baseuri}{link['href']}") for link in links]

        if href is not None:
            href = f"{baseuri}{href['href']}"
    return links, href


def setup():
    parser = argparse.ArgumentParser(description="Download bin days data from Edinburgh Council")
    parser.add_argument(
        "--scrapestreetlinks", default=None, action='store_true', help="scrape street links"
    )
    parser.add_argument(
        "--scrapepdflinks", default=None, action='store_true', help="scrape pdf links"
    )
    parser.add_argument(
        "--download", default=None, action='store_true', help="download pdfs"
    )
    parser.add_argument(
        "--parse", default=None, action='store_true', help="parse pdfs"
    )
    args = parser.parse_args()
    main(scrapestreetlinks=args.scrapestreetlinks,
         scrapepdflinks=args.scrapepdflinks,
         download=args.download,
         parse=args.parse)


if __name__ == '__main__':
    setup()
