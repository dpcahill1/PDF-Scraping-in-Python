#Import the packages needed to complete the scraping
import pdfplumber
import pandas as pd
import re

#Pick the PDF to scrape; this will change with each PDF (make sure to keep the 'r' and quotations)
pdf_path = r"add PDF path file here"

#Scrape the text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    all_text = ''
    for page in pdf.pages:
        all_text += page.extract_text()
        all_text = all_text.replace('\n', ' ')

#Initialize data dictionaries
set_one = {
    'Borrower(s)': None,
    'Property Address': None,
    'Appraisal Date': None,
    'Appraised Value(s)': None,
    'Appraiser Name': None,
    'Loan to Value': None,
    'Loan to Cost': None,
    'Property Type': None,

    'Land Size': None,
    'Loan Amount': None,
    'Highest & Best Use': None,
    'Building Size': None,
    'Special Conditions': None
}

#Finds property address
property_address_pattern = re.compile(
    r'\b(Address.|Property\s*Address.)\s*'                              #Searchs for 'Address:', 'Address','Property Address:', or 'Property Address' keywords
    r'(?:P\.?\s*O\.?\s*Box\s*\d+\s*,?\s*)?'                             #Optional match of a P.O. Box
    r'\d+-?\d*\s+\w+(?:\s+\w+)*'                                        #Number with optional and street name
    r'(?:\s*\([^)]*\))?'                                                #Optional match of text within parentheses
    r'(?:,\s*(?:#\d+|\w+))?'                                            #Optional match of '#' instead of a unit or suite
    r'(?:\s*[\w\s]*?)'                                                  #Optional match of extra text before unit number
    r'(?:,\s*\w+(?:\s+\w+)*)?'                                          #Optional comma and city
    r'\s*,?\s+(?:[A-Z]{2}|(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))'          #Optional comma and state abbreviation or spelt out
    r'\s+\d{5}(?:-\d{4})?'                                              #Zip code plus four if necessary
)

found_property_address = property_address_pattern.finditer(all_text)

for addr in found_property_address:

    print(addr.group())
    print(addr.groups())

#Finds land size
land_size_pattern = re.compile(
    r'\b(Site Area.|Land Area.|Primary Site.)\s*'           #Search for 'Site Area:', 'Site Area', 'Land Area:', 'Land Area', 'Primary Site:', or 'Primary Site' keywords
    r'\b(\d+.\d+)\s*'                                       #Number with optional match of a charactercsuch as a comma
    r'\b(\w+\s*\w+|\+/\-\s*\w+)'                            #Unit of measurement
)

found_land_size = re.search(land_size_pattern, all_text)
temp_land_size = found_land_size.groups()

final_land_size = temp_land_size[1] + ' ' + temp_land_size[2]

set_one['Land Size'] = final_land_size
print(set_one)

#Finds building size
building_size_pattern = re.compile(
    r'\b(Gross Building Area.)\s*'                                                                                  #Search for 'Gross Building Area:' or 'Gross Building Area' keywords
    r'\b(\d+,\d+)\s*'                                                                                               #Number with optional match of a character such as a comma

    r'\b(square feet|Square Feet|\+/\-\s*square feet|\+/\-\s*Square Feet|\u00B1\s*squarefeet|\u00B1\s*Square Feet)' #Unit of measurement
)

found_building_size = re.search(building_size_pattern, all_text)
temp_building_size = found_building_size.groups()

final_building_size = temp_building_size[1] + ' ' + temp_building_size[2]

set_one['Building Size'] = final_building_size
print(set_one)

#Finds property type
property_type_pattern = re.compile(
    r'\b(Property\s*Type.|Property\s*Description.)\s*'
    r'\b([A-Za-z\s/-]+?)'
    r'\b'
    r'(?:\s|$)'
)

found_property_type = re.search(property_type_pattern, all_text)
temp_property_type = found_property_type.groups()

print(temp_property_type)

#Finds appraisal date

date_pattern = re.compile(
    r'\b(Effective Date of Appraisal.|Report Date.)\s*'
    r'\b([A-Za-z]+\s+\d{1,2},\s+\d{4}|\d{1,2}/\d{1,2}/\d{2}|\d{1,2}/\d{1,2}/\d{4})\b'       #month day, year | m/d/yy or mm/dd/yy | m/d/yyyy or mm/dd/yyyy
)

found_dates = date_pattern.finditer(all_text)

for date in found_dates:

    temp_date = date.groups()
    final_date = temp_date[1]

set_one['Appraisal Date'] = final_date
print(set_one)

set_one = {key: [value] for key, value in set_one.items()}

df = pd.DataFrame(set_one)

#Turn our dataframe into a CSV file
df.to_csv(r'add file path here', index = False)