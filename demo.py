import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://dc.urbanturf.com/pipeline'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

pipeline_items = soup.find_all('div',attrs={'class':'pipeline-item'})
rows = []
columns =['listing title','listing url','listing image url','location','project type','status','size']

for item in pipeline_items:
    # Title, image url,listing url
    listing_title = item.a['title']
    listing_url = item.a['href']
    listing_image_url = item.a.img['src']
    
    for p_tag in item.find_all('p'):
        if not p_tag.h2:
            if p_tag.span.text =='Location:':
                p_tag.span.extract()
                property_location = p_tag.text.strip()
            elif p_tag.span.text =='Project type:':
                p_tag.span.extract()
                property_type = p_tag.text.strip()
            elif p_tag.span.text =='Status:':
                p_tag.span.extract()
                property_status = p_tag.text.strip()
            elif p_tag.span.text =='Size:':
                p_tag.span.extract()
                property_size = p_tag.text.strip()
    row = [listing_title,listing_url,listing_image_url,property_location,property_type,property_status,property_size]
    rows.append(row)

df = pd.DataFrame(rows,columns=columns)
df.to_excel('DC Pipeline Properties.xlsx',index=False)
    
print('File Saved')
    
# print(len(pipeline_items))  