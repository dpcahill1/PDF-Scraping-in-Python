#Import the packages needed to complete the data scraping
import pdfplumber
import pandas as pd

#Create variable for the file path to easily identify the PDF; use raw strings (r in front of path)to avoid errors; update for each PDF
file_path = r"add PDF file path here"

#Open the PDF
with pdfplumber.open(file_path) as pdf:

    #Select the page(s) we want to extract data from (Indices start at 0 so page 1 would be pdf.pages[0]); these might need to update for each PDF
    table_page1 = pdf.pages[2]
    table_page2 = pdf.pages[3]
    table_page3 = pdf.pages[4]
    #table_page4 = pdf.pages[5]

    #Extract the table from the PDF
    text1 = table_page1.extract_table()
    text2 = table_page2.extract_table()
    text3 = table_page3.extract_table()
    #text4 = table_page4.extract_table()

#Combines both pages of extracted data
all_text = text1 + text2 + text3 #+ text4
print(all_text)

#Filter out the 'None' values that are in all_text
filtered_text = [[item for item in sublist if item is not None] for sublist in all_text]
print(filtered_text)

#Convert 2D list (a list of lists) to a 1D list
flattened_text = [item for sublist in filtered_text for item in sublist]
print(flattened_text)

#Initialize a dictionary of variables
prop_data = {
    'Borrower': None,
    'Property Address': None,
    'City': None,
    'State': None,
    'Zip Code': None,
    'Appraisal Amount': None,
    'Appraisal Date': None
}

question_set_one = {
    'Neighborhood Values Declining?': None,
    'Zoning in Compliance?': None,
    'Flood Zone?': None,
    'Sanitary Sewer Public?': None
}

question_set_two = {
    'Adj Consistent?': None,
    'Net Adj Under 15%?': None,
    'Gross Adj Under 25%?': None
}

question_set_three = {
    'Comparable Sales within One Mile Radius?': None,
    'Comparable Sales less than 6 mos old?': None,
    'Comparable Choices Appear Valid?': None,
    'Number of Comparable Rentals': None,
    'Gross Rent Multiplier': None,
    'Number of Comparable Sales': None,
    'Sale price/SF': None
}

question_set_four = {
    'Adverse Neighborhood Items?': None,
    'Room Count & Dimensions Consistent?': None,
    'Oil Tank in the Basement?': None,
    'Adverse Conditions/Environmental Issues Noted?': None
}

question_set_five = {
    'Land Value Less Than 30%?': None,
    'Replacement Cost Calculations Ok?': None
}

#Finds borrower name
for item in flattened_text:
    if item.startswith("Borrower"):
        borrower_start_index = item.find('Borrower') + len('Borrower')
        borrower_end_index = item.find('Owner')
        prop_data['Borrower'] = item[borrower_start_index:borrower_end_index].strip()

#Finds property address
for item in flattened_text:
    if item.startswith("Property Address"):
        address_start_index = item.find('Property Address') + len('Property Address')
        address_end_index = item.find('City')
        prop_data['Property Address'] = item[address_start_index:address_end_index].strip()

#Finds city
for item in flattened_text:
    if item.startswith("Property Address"):
        city_start_index = item.find('City') + len('City')
        city_end_index = item.find('State')
        prop_data['City'] = item[city_start_index:city_end_index].strip()

#Finds state
for item in flattened_text:
    if item.startswith("Property Address"):
        state_start_index = item.find('State') + len('State')
        state_end_index = item.find('Zip')
        prop_data['State'] = item[state_start_index:state_end_index].strip()

#Finds zip code
for item in flattened_text:
    if item.startswith("Property Address"):
        zip_start_index = item.find('Zip Code') + len('Zip Code')
        prop_data['Zip Code'] = item[zip_start_index:].strip()

#Finds appraisal amount
for item in flattened_text:
    if item.startswith("Based"):
        appr_amt_start_index = item.find('$') + len('$')
        appr_amt_end_index = item.find('\n', appr_amt_start_index)
        prop_data['Appraisal Amount'] = item[appr_amt_start_index:appr_amt_end_index].strip()

#Finds appraisal date
for item in flattened_text:
    if item.startswith("Based"):
        appr_date_start_index = item.rfind('as of') + len('as of')
        appr_date_end_index = item.find(', which')
        prop_data['Appraisal Date'] = item[appr_date_start_index:appr_date_end_index].strip()

#Finds neighborhood values
for sublist in filtered_text:
    for item in sublist:
        if item.startswith("Location"):
            if 'Stable' < 'X' < 'Declining':
                question_set_one['Neighborhood Values Declining?'] = 'Yes'
            else:
                question_set_one['Neighborhood Values Declining?'] = 'No'

#Finds zoning compliance
zone_key1 = 'Zoning Compliance'
zone_key2 = 'Legal'
zone_key3 = 'Legal Nonconforming'

for sublist in filtered_text:
    if zone_key1 in sublist and zone_key2 in sublist and zone_key3 in sublist and 'X' in sublist:
        index_zone_key1 = sublist.index(zone_key1)
        index_zone_key2 = sublist.index(zone_key2)
        index_zone_key3 = sublist.index(zone_key3)
        index_zone_x = sublist.index('X')

        if index_zone_key1 < index_zone_x <index_zone_key2 or index_zone_key2 < index_zone_x < index_zone_key3:
            question_set_one['Zoning in Compliance?'] = 'Yes'
        else:
            question_set_one['Zoning in Compliance?'] = 'No'

#Finds if the sanitary sewer is public
sewer_key1 = 'Municipal Sanitary Sewer'

for sublist in filtered_text:
    if sewer_key1 in sublist and 'X' in sublist:
        index_sewer_key1 = sublist.index(sewer_key1)
        index_sewer_x = sublist.index('X')

        if index_sewer_key1 < index_sewer_x < index_sewer_x + 1:
            question_set_one['Sanitary Sewer Public?'] = 'Yes'
        else:
            question_set_one['Sanitary Sewer Public?'] = 'No'

#Finds if property is in a flood zone
flood_key1 = 'FEMA Special Flood Hazard Area'
flood_key2 = 'Yes'

for sublist in filtered_text:
    if flood_key1 in sublist and flood_key2 in sublist and 'X' in sublist:
        index_flood_key1 = sublist.index(flood_key1)
        index_flood_key2 = sublist.index(flood_key2)
        index_flood_x = sublist.index('X')

        if index_flood_key1 < index_flood_x < index_flood_key2:
            question_set_one['Flood Zone?'] = 'Yes'
        else:
            question_set_one['Flood Zone?'] = 'No'

#Checks if adjustments are consistent
for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Net Adjustment (Total)'):
            adj_con = [item for item in sublist if item in {'', 'X', '+', '-'}]

            for i in adj_con:
                if 'X' in adj_con[2] and 'X' in adj_con[7] and 'X' in adj_con[12]:
                    question_set_two['Adj Consistent?'] = 'Yes'
                elif 'X' in adj_con[4] and 'X' in adj_con[9] and 'X' in adj_con[14]:
                    question_set_two['Adj Consistent?'] = 'Yes'
                else:
                    question_set_two['Adj Consistent?'] = 'No'

#Checks if net adjustments are below 15%
for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Adjusted Sale Price'):
            net_adj_items = [item.split('Net Adj.')[1].split('%')[0] for item in sublist if 'Net Adj.' in item]
            net_adj_items = [float(i) for i in net_adj_items]

            all_net_adj_true = all(adj < 15 for adj in net_adj_items)

            if all_net_adj_true is True:
                question_set_two['Net Adj Under 15%?'] = 'Yes'
            else:
                question_set_two['Net Adj Under 15%?'] = 'No'

#Checks if gross adjustments are below 25%
for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Adjusted Sale Price'):
            gross_adj_items = [item.split('Gross Adj.')[1].split('%')[0] for item in sublist if 'Gross Adj.' in item]
            gross_adj_items = [float(i) for i in gross_adj_items]

            all_gross_adj_true = all(adj < 25 for adj in gross_adj_items)

            if all_gross_adj_true is True:
                question_set_two['Gross Adj Under 25%?'] = 'Yes'
            else:
                question_set_two['Gross Adj Under 25%?'] = 'No'

#Checks if comparable sales are within a one mile radius
for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Proximity to Subject'):
            distance = [item.split(' ')[0] for item in sublist if ' ' in item and item.split(' ')[0].replace('.', '', 1).isdigit()]

            distance = [float(i) for i in distance]

            under_one = all(dis < 1 for dis in distance)

            if under_one is True:
                question_set_three['Comparable Sales within One Mile Radius?'] = 'Yes'
            else:
                question_set_three['Comparable Sales within One Mile Radius?'] = 'No'

#Checks if comparable sales are less than 6 mos old
current_month = 8
current_year = 24

for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Date of Sale/Time'):
            dates = [item.split('s')[1].split(';')[0] for item in sublist if 's' in item]

def is_less_than_6_months_old(date_str, current_month, current_year):
    month, year = map(int, date_str.split('/'))
    month_difference = ((current_year - year) * 12) + (current_month - month)
    return month_difference < 6

ages = [is_less_than_6_months_old(date, current_month, current_year) for date in dates]

if all(ages):
    question_set_three['Comparable Sales less than 6 mos old?'] = 'Yes'
else:
    question_set_three['Comparable Sales less than 6 mos old?'] = 'No'

#Checks if comparable choices appear valid (other factors may possibly be added)
if question_set_three['Comparable Sales less than 6 mos old?'] == 'Yes' and question_set_three['Comparable Sales within One Mile Radius?'] == 'Yes': 
    question_set_three['Comparable Choices Appear Valid?'] = 'Yes'
else:
    question_set_three['Comparable Choices Appear Valid?'] = 'No'

#Finds number of comparable rentals

#Finds gross rent multiplier
for item in flattened_text:
    if item.startswith('Estimated Monthly'):
        after_grm = item.split('Multiplier =')[1]
        grm_val = after_grm.split()[0]

        if grm_val == '$':
            question_set_three['Gross Rent Multiplier'] = 'N/A'
        else:
            question_set_three['Gross Rent Multiplier'] = grm_val

#Finds number of comparable sales
for item in flattened_text:
    if item.startswith('There are'):
        for num in item.split():
            if num.isdigit():
                question_set_three['Number of Comparable Sales'] = num

#Finds sale price/sf
for sublist in filtered_text:
    for item in sublist:
        if item.startswith('Dwelling'):
            sale_list = item
            after_at = sale_list.split('@ $ ')[1]
            sale_price = after_at.split()[0]
            spsf = sale_price.split('..')[0]

            question_set_three['Sale price/SF'] = spsf

#Checks for adverse neighborhood items

#Checks consistency of room count and dimensions

    #Room consistency
    room_consistent = None

    def room_string(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    for sublist in filtered_text:
        if sublist and room_string(sublist[0]):
            room_list = sublist

    indices = [0,3,7,11]

    number_of_rooms = [room_list[i] for i in indices if i < len(room_list)]
    number_of_rooms = [int(i) for i in number_of_rooms]

    for i in range(1,4):
        if number_of_rooms[i] - 1 <= number_of_rooms[0] <= number_of_rooms[i] + 1:
            number_of_rooms[i] = True
        else:
            number_of_rooms[i] = False

    if all(number_of_rooms[-3:]):
        room_consistent = True
    else:
        room_consistent = False

    #Dimension consistency
    sqft_consistent = None

    sqft_list = None

    def sqft_string(value):
        for item in sublist:
            if 'sq. ft.' in item:

                if '$' in item:
                    return False

                num_part = item.split('sq. ft')[0].replace(',', '').strip()
                if num_part.isdigit():
                    return True
        return False

    for sublist in filtered_text:
        if sqft_string(sublist):
            sqft_list = sublist
            break

    indices2 = [0, 1, 3, 5]

    square_footage = [int(item.split('sq. ft.')[0].replace(',', '').strip()) for item in sqft_list]
    square_footage = [square_footage[i] for i in indices2 if i < len(square_footage)]

    lower_bound = square_footage[0] * 0.90
    upper_bound = square_footage[0] * 1.10

    for i in range(1,4):
        if lower_bound <= square_footage[i] <= upper_bound:
            square_footage[i] = True
        else:
            square_footage[i] = False

    if all(square_footage[-3:]):
        sqft_consistent = True
    else:
        sqft_consistent = False

    #Both consistent?
    if room_consistent == True and sqft_consistent == True:
        question_set_four['Room Count & Dimensions Consistent?'] = 'Yes'
    else:
        question_set_four['Room Count & Dimensions Consistent?'] = 'No'

#Checks heating source
for sublist in filtered_text:
    for item in sublist:
        if 'Gas' in item and 'X' in item:
            question_set_four['Oil Tank in the Basement?'] = 'No, Other'
            break
    else:
        continue
    break
else:
    question_set_four['Oil Tank in the Basement?'] = 'Check Appraisal'

#Checks for adverse conditions/evironmental issues
for item in flattened_text:
    if item.startswith('Are there any adverse site'):
        yes_index = item.find('Yes')
        no_index = item.find('No')
        x_index = item.rfind('X')

if yes_index < x_index < no_index:
    question_set_four['Adverse Conditions/Environmental Issues Noted?'] = 'No'
else:
    question_set_four['Adverse Conditions/Environmental Issues Noted?'] = 'Yes'

#Checks for land value
for item in flattened_text:
    if item.startswith('OPINION'):
        land_value = item.split('$ ')[1].replace(',', '')
        land_value = int(land_value)

    if item.startswith('INDICATED'):
        indicated_value = item.split('$ ')[1].replace(',', '')
        indicated_value = int(indicated_value)

land_value_percent = (land_value / indicated_value) * 100

if land_value_percent <= 30:
    question_set_five['Land Value Less Than 30%?'] = 'Yes'
else:
    question_set_five['Land Value Less Than 30%?'] = 'No'

#Checks replacement costs
for item in flattened_text:
    if item.startswith('Quality'):
        split_item = item.split(' Effective')[0]
    if 'service' in split_item:
        rating = split_item.split('service ')[1]

if rating == 'Gd' or rating == 'Good':
    question_set_five['Replacement Cost Calculations Ok?'] = 'Yes'
else:
    question_set_five['Replacement Cost Calculations Ok?'] = 'No'

print(prop_data)
print(question_set_one)
print(question_set_two)
print(question_set_three)
print(question_set_four)
print(question_set_five)

#Convert data dictionary values from strings to lists
prop_data = {key: [value] for key, value in prop_data.items()}

question_set_one = {key: [value] for key, value in question_set_one.items()}

question_set_two = {key: [value] for key, value in question_set_two.items()}

question_set_three = {key: [value] for key, value in question_set_three.items()}

question_set_four = {key: [value] for key, value in question_set_four.items()}

question_set_five = {key: [value] for key, value in question_set_five.items()}

#Convert dictionaries to a dataframe
combined_data = {**prop_data, **question_set_one, **question_set_four,
**question_set_three, **question_set_two, **question_set_five}

df = pd.DataFrame(combined_data)

#Turn our dataframe into a CSV file
df.to_csv(r'add file path here', index = False)