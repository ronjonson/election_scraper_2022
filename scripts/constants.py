#SITE
SITE = "https://2022electionresults.comelec.gov.ph/#/er/0/"


DROPDOWN = {
    'REGION': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[2]/nav-filter/div/span/span',
    'PROVINCE': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[3]/nav-filter/div/span/span',
    'CITY': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[4]/nav-filter/div/span/span',
    'BARANGAY': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[5]/nav-filter/div/span/span',
    'PRECINCT': "/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[6]/nav-filter/div/span/span"
}

DROPDOWN_VALUES = {
    'REGION': '/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[2]/nav-filter/div/span/div/div/div[2]/ul',
    'PROVINCE': '/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[3]/nav-filter/div/span/div/div/div[2]/ul',
    'CITY': '/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[4]/nav-filter/div/span/div/div/div[2]/ul',
    'BARANGAY': '/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[5]/nav-filter/div/span/div/div/div[2]/ul',
    'PRECINCT': '/html/body/div/div/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[6]/nav-filter/div/span/div/div/div[2]/ul'
}

DROPDOWN_PLACEHOLDER = {
    'REGION': 'Select/Enter Region',
    'PROVINCE': 'Select/Enter Province/District',
    'CITY': 'Select/Enter City/Municipality',
    'BARANGAY': 'Select/Enter Barangay',
    'PRECINCT': 'Select/Enter Precinct ID'
}

DROPDOWN_ALT = {
    'REGION': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[2]/nav-filter/div/span/div/div/span/span',
    'PROVINCE': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[3]/nav-filter/div/span/div/div/span/span',
    'CITY': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[4]/nav-filter/div/span/div/div/span/span',
    'BARANGAY': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[5]/nav-filter/div/span/div/div/span/span',
    'PRECINCT': '//*[@id="container"]/ui-view/div/div/div[1]/nav/div/ul/li/div[5]/div[6]/nav-filter/div/span/div/div/span/span'
}


# METADATA
PRECINCT_METADATA = '//*[@id="container"]/ui-view/div/div/div[2]/div[2]/div[2]/results-viewer/div[2]/div[1]/div[2]'

# DATA TABLES
PRESIDENT_TABLE = '''//*[@id="'resultDiv.'+5587"]/div[1]'''
VICE_PRESIDENT_TABLE = '''//*[@id="'resultDiv.'+5588"]/div[1]'''
SENATOR_TABLE = '''//*[@id="'resultDiv.'+5589"]/div[1]'''
PARTYLIST_TABLE = '''//*[@id="'resultDiv.'+11172"]/div[1]'''
REP_TABLE = '''//*[@id="'resultDiv.'+6120"]/div[1]'''
MAYOR_TABLE = '''//*[@id="'resultDiv.'+7184"]/div[1]'''
VICE_MAYOR_TABLE = '''//*[@id="'resultDiv.'+8818"]/div[1]'''
SP_TABLE = '''//*[@id="'resultDiv.'+10465"]/div[1]'''


