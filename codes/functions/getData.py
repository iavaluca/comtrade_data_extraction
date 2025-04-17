import comtradeapicall
import glob
from itertools import product
import logging
import os
import pandas as pd
from tempfile import TemporaryDirectory

# Get countries conversion in M-49 code based on the excel file used as input.
# Important: it's necessary to take the input file from the following webpage:
# https://unstats.un.org/wiki/display/comtrade/Comtrade+Country+Code+and+Name
# Country codes available in the UN webpage are not complete or different (e.g. IN, TH, KR).
countries = {
            'All': 'all',
            'Afghanistan': '4',
            'Albania': '8',
            'Algeria': '12',
            'Andorra': '20',
            'Angola': '24',
            'Anguilla': '660',
            'Antigua and Barbuda': '28',
            'Argentina': '32',
            'Armenia': '51',
            'Aruba': '533',
            'Australia': '36',
            'Austria': '40',
            'Azerbaijan': '31',
            'Bahamas': '44',
            'Bahrain': '48',
            'Bangladesh': '50',
            'Barbados': '52',
            'Belarus': '112',
            'Belgium': '56',
            'Belgium-Luxembourg': '58',
            'Belize': '84',
            'Benin': '204',
            'Bermuda': '60',
            'Bhutan': '64',
            'Bolivia (Plurinational State of)': '68',
            'Bonaire': '535',
            'Bosnia Herzegovina': '70',
            'Botswana': '72',
            'Br. Virgin Isds': '92',
            'Brazil': '76',
            'Brunei Darussalam': '96',
            'Bulgaria': '100',
            'Burkina Faso': '854',
            'Burundi': '108',
            'Cabo Verde': '132',
            'Cambodia': '116',
            'Cameroon': '120',
            'Canada': '124',
            'Cayman Isds': '136',
            'Central African Rep.': '140',
            'Chad': '148',
            'Chile': '152',
            'China': '156',
            'China, Hong Kong SAR': '344',
            'China, Macao SAR': '446',
            'Colombia': '170',
            'Comoros': '174',
            'Congo': '178',
            'Cook Isds': '184',
            'Costa Rica': '188',
            'Côte d\'Ivoire': '384',
            'Croatia': '191',
            'Cuba': '192',
            'CuraÃ§ao': '531',
            'Cyprus': '196',
            'Czechia': '203',
            'Czechoslovakia': '200',
            'Dem. People\'s Rep. of Korea': '408',
            'Dem. Rep. of the Congo': '180',
            'Denmark': '208',
            'Djibouti': '262',
            'Dominica': '212',
            'Dominican Rep.': '214',
            'East and West Pakistan': '588',
            'Ecuador': '218',
            'Egypt': '818',
            'El Salvador': '222',
            'Equatorial Guinea': '226',
            'Eritrea': '232',
            'Estonia': '233',
            'Ethiopia': '231',
            'EU-28': '97',
            'Faeroe Isds': '234',
            'Falkland Isds (Malvinas)': '238',
            'Fiji': '242',
            'Finland': '246',
            'Fmr Arab Rep. of Yemen': '886',
            'Fmr Dem. Rep. of Germany': '278',
            'Fmr Dem. Rep. of Vietnam': '866',
            'Fmr Dem. Yemen': '720',
            'Fmr Ethiopia': '230',
            'Fmr Fed. Rep. of Germany': '280',
            'Fmr Pacific Isds': '582',
            'Fmr Panama, excl.Canal Zone': '590',
            'Fmr Panama-Canal-Zone': '592',
            'Fmr Rep. of Vietnam': '868',
            'Fmr Rhodesia Nyas': '717',
            'Fmr Sudan': '736',
            'Fmr Tanganyika': '835',
            'Fmr USSR': '810',
            'Fmr Yugoslavia': '890',
            'Fmr Zanzibar and Pemba Isd': '836',
            'France': '251',
            'French Guiana': '254',
            'French Polynesia': '258',
            'FS Micronesia': '583',
            'Gabon': '266',
            'Gambia': '270',
            'Georgia': '268',
            'Germany': '276',
            'Ghana': '288',
            'Gibraltar': '292',
            'Greece': '300',
            'Greenland': '304',
            'Grenada': '308',
            'Guadeloupe': '312',
            'Guatemala': '320',
            'Guinea': '324',
            'Guinea-Bissau': '624',
            'Guyana': '328',
            'Haiti': '332',
            'Holy See (Vatican City State)': '336',
            'Honduras': '340',
            'Hungary': '348',
            'Iceland': '352',
            'India': '699',
            'India [...1974]': '356',
            'Indonesia': '360',
            'Iran': '364',
            'Iraq': '368',
            'Ireland': '372',
            'Israel': '376',
            'Italy': '380',
            'Jamaica': '388',
            'Japan': '392',
            'Jordan': '400',
            'Kazakhstan': '398',
            'Kenya': '404',
            'Kiribati': '296',
            'Kuwait': '414',
            'Kyrgyzstan': '417',
            'Lao People\'s Dem. Rep.': '418',
            'Latvia': '428',
            'Lebanon': '422',
            'Lesotho': '426',
            'Liberia': '430',
            'Libya': '434',
            'Lithuania': '440',
            'Luxembourg': '442',
            'Madagascar': '450',
            'Malawi': '454',
            'Malaysia': '458',
            'Maldives': '462',
            'Mali': '466',
            'Malta': '470',
            'Marshall Isds': '584',
            'Martinique': '474',
            'Mauritania': '478',
            'Mauritius': '480',
            'Mayotte': '175',
            'Mexico': '484',
            'Mongolia': '496',
            'Montenegro': '499',
            'Montserrat': '500',
            'Morocco': '504',
            'Mozambique': '508',
            'Myanmar': '104',
            'N. Mariana Isds': '580',
            'Namibia': '516',
            'Nepal': '524',
            'Neth. Antilles': '530',
            'Neth. Antilles and Aruba': '532',
            'Netherlands': '528',
            'New Caledonia': '540',
            'New Zealand': '554',
            'Nicaragua': '558',
            'Niger': '562',
            'Nigeria': '566',
            'Norway': '579',
            'Oman': '512',
            'Other Asia, nes': '490',
            'Pakistan': '586',
            'Palau': '585',
            'Panama': '591',
            'Papua New Guinea': '598',
            'Paraguay': '600',
            'Peninsula Malaysia': '459',
            'Peru': '604',
            'Philippines': '608',
            'Poland': '616',
            'Portugal': '620',
            'Qatar': '634',
            'Rep. of Korea': '410',
            'Rep. of Moldova': '498',
            'Réunion': '638',
            'Romania': '642',
            'Russian Federation': '643',
            'Rwanda': '646',
            'Ryukyu Isd': '647',
            'Sabah': '461',
            'Saint Barthelemy': '652',
            'Saint Helena': '654',
            'Saint Kitts and Nevis': '659',
            'Saint Kitts, Nevis and Anguilla': '658',
            'Saint Lucia': '662',
            'Saint Maarten': '534',
            'Saint Pierre and Miquelon': '666',
            'Saint Vincent and the Grenadines': '670',
            'Samoa': '882',
            'San Marino': '674',
            'Sao Tome and Principe': '678',
            'Sarawak': '457',
            'Saudi Arabia': '682',
            'Senegal': '686',
            'Serbia': '688',
            'Serbia and Montenegro': '891',
            'Seychelles': '690',
            'Sierra Leone': '694',
            'Singapore': '702',
            'Slovakia': '703',
            'Slovenia': '705',
            'So. African Customs Union': '711',
            'Solomon Isds': '90',
            'Somalia': '706',
            'South Africa': '710',
            'South Sudan': '728',
            'Spain': '724',
            'Sri Lanka': '144',
            'State of Palestine': '275',
            'Sudan': '729',
            'Suriname': '740',
            'Eswatini': '748',
            'Sweden': '752',
            'Switzerland': '757', # with Liechtenstein
            'Syria': '760',
            'Tajikistan': '762',
            'North Macedonia': '807',
            'Thailand': '764',
            'Timor-Leste': '626',
            'Togo': '768',
            'Tokelau': '772',
            'Tonga': '776',
            'Trinidad and Tobago': '780',
            'Tunisia': '788',
            'Turkey': '792',
            'Turkmenistan': '795',
            'Turks and Caicos Isds': '796',
            'Tuvalu': '798',
            'Uganda': '800',
            'Ukraine': '804',
            'United Arab Emirates': '784',
            'United Kingdom': '826',
            'United Rep. of Tanzania': '834',
            'Uruguay': '858',
            'US Virgin Isds': '850',
            'USA': '842', # With US Virgin Islands and Puerto Rico
            'USA (before 1981)': '841',
            'Uzbekistan': '860',
            'Vanuatu': '548',
            'Venezuela': '862',
            'Viet Nam': '704',
            'Wallis and Futuna Isds': '876',
            'World': '0',
            'Yemen': '887',
            'Zambia': '894',
            'Zimbabwe': '716',
            'ASEAN': '975'
            }

flows = {
        '-1': 'Not available or not specified.',
        'M': 'Import',
        'X': 'Export',
        'RX': 'Re-export',
        'RM': 'Re-import',
        'MIP': 'Import of goods for inward processing',
        'XIP': 'Export of goods after inward processing',
        'MOP': 'Import of goods after outward processing',
        'XOP': 'Export of goods for outward processing',
        'MIF': 'Import on intra-firm trade',
        'XIF': 'Export on intra-firm trade',
        'DX': 'Domestic Export',
        'FM': 'Foreign Import'
         }

# TODO: delete flows
# TODO: code refactoring need
def bulkMethod(key: str, directory: str, frequency: str, period: str, reporter: tuple, stata_files: bool):
    """
    @key: str
    @directory: str
    @frequency: str
    @period: str
    @reporter: tuple
    @stata_files: bool
    
    Retrieve data in bulk. Access to the premium API is required.
    """
    
    try:
        os.mkdir(os.path.join(directory, reporter.name))
    except FileExistsError:
        pass
    
    # Temp directory to store text files
    temp_directory = TemporaryDirectory(dir = os.path.join(directory, reporter.name))
    
    request =  comtradeapicall.bulkDownloadFinalFile(
        subscription_key = key,
        directory = temp_directory.name,
        # Goods
        typeCode = 'C',
        freqCode = frequency,
        # Harmonised System
        clCode = 'HS',
        period = period,
        reporterCode = reporter.code,
        decompress = True
    )

    # Get files based on relative path and file extension to be filtered
    files = glob.glob(f'{temp_directory.name}/**.txt')

    # Folders where to store the data
    folders = ['Parquet','Stata'] if stata_files else ['Parquet']

    for file in files:
        data = pd.read_csv(file, sep = '\t', dtype = {'cmdCode': str}).groupby(['flowCode'])
        for g in data.groups:
            
            for f in folders:
                try:
                    os.makedirs(os.path.join(directory,reporter.name,f,flows.get(g)))
                except FileExistsError:
                    pass
            
            df = data.get_group(g).sort_values(by = ['primaryValue'], ascending = False)
            
            # Write files
            # Stata          
            t = df['period'].drop_duplicates().to_string(index = False)
            if len(str(t)) > 4:
                t = str(t)[:4] + '_' + str(t)[-2:]
            else:
                t = str(t)

            if stata_files:
                df.to_stata(
                    path = f'{os.path.join(directory, reporter.name, "Stata", flows.get(g), t + ".dta")}',
                    # version = 117,
                    # Prevent to block writing process if columns are fully empty
                    # convert_strl = df.columns[df.isnull().all()].to_list()
                )
            # Parquet
            df.to_parquet(path = f'{os.path.join(directory, reporter.name, "Parquet", flows.get(g), t + ".parquet.gzip")}', compression = 'gzip') 

    return request

def batchMethod(key: str, 
    directory: str, 
    frequency: str, 
    period: str, 
    reporter: str,
    hscode: int,
    flow: str, 
    partners: list,
    stata_files: bool
):
    """
    @key:str
    @frequency: str
    @period: str
    @reporter: str
    @sector: int
    @flow: str
    @partners: list
    @stata_files: bool

    Retrieve data in small batches.
    """

    # Temp directory
    # To prevent disconnection from the network drive
    temp_directory = TemporaryDirectory(dir = os.path.join(directory,reporter))

    # HS codes
    if hscode == 2:
        codes = [f'{c:>02}' for c in range(1,99+1)] + ['TOTAL']
    elif hscode == 4:
        codes = [''.join(c) for c in list(product([f'{c:>02}' for c in range(1,99+1)],[f'{c:>02}' for c in range(1,99+1)]))]
    
    for code in codes:

        request = comtradeapicall._getFinalData(
            subscription_key = key,
            typeCode ='C', 
            freqCode = frequency,
            clCode = 'HS',
            period = period,
            reporterCode = countries.get(reporter),
            cmdCode = code,                                               
            flowCode = flow,
            partnerCode = ','.join([countries.get(p) for p in partners]),
            partner2Code=None,
            customsCode=None, 
            motCode=None, 
            # maxRecords=250000, 
            format_output='JSON',
            aggregateBy=None, 
            breakdownMode='classic', 
            countOnly=None, 
            includeDesc=True
        )

        if not request.empty:
            request.to_parquet(path = f'{os.path.join(temp_directory.name, code + ".parquet.gzip")}', compression = 'gzip')
            logging.info(f'Code {code} successfully downloaded.')
        else:
            logging.info(f'No data for code {code}.')

    # Get files based on relative path and file extension to be filtered
    files = glob.glob(f'{temp_directory.name}/**.parquet.gzip')
        
    # Folders where to store the data
    folders = ['Parquet','Stata'] if stata_files else ['Parquet']

    data = []

    for file in files:
        data.append(pd.read_parquet(file))
        
    data = pd.concat(data).groupby(by = ['flowCode', 'period'])
    
    for g in data.groups:
        
        for f in folders:
            try:
                os.makedirs(os.path.join(directory,reporter,f,flows.get(g[0][0])))
            except FileExistsError:
                pass
        
        df = data.get_group(g).sort_values(by = ['primaryValue'], ascending = False)
            
        # Write files
        # Stata          
        t = g[1]
        if len(str(t)) > 4:
            t = str(t)[:4] + '_' + str(t)[-2:]
        else:
            t = str(t)

        if stata_files:
            df.to_stata(
                path = f'{os.path.join(directory, reporter, "Stata", flows.get(g[0][0]), t + ".dta")}',
                version = 117,
                # Prevent to block writing process if columns are fully empty
                # convert_strl = df.columns[df.isnull().all()].to_list()
            )
        # Parquet
        df.to_parquet(path = f'{os.path.join(directory, reporter, "Parquet", flows.get(g[0][0]), t + ".parquet.gzip")}', compression = 'gzip')   
    
    
    return request


funcs = {
        'bulkMethod': bulkMethod,
        'batchMethod': batchMethod
        }  
     
# TODO: avoid if-else   
def getData(method: str, **kwargs):
    """
    @method: str
    
    Get data based on the inputted method.
    """
    
    match method:
        case 'bulk':
            request = funcs.get('bulkMethod')         
        case 'batch':
            request = funcs.get('batchMethod')
        case _:
            raise ValueError(f'{method} not recognised.')
    
    return request(**kwargs)


def checkStatus(method: str, request: object, out: str):
    """
    @method: str
    @request: object
    @out: str
    
    Check request status. 
    UN API returns a string instead of an error for failed requests.
    """
    
    match method:
        case 'bulk':
        # Check whether any file has been retrieved from the call
            if 'downloaded' not in out:
                # TODO: handle jsondecodeerror
                logging.info('Not downloaded. Passing.')
                pass
        case 'batch':
            # # Check whether any df has been retrieved from the call
            # if request is None:
            #     # TODO: handle jsondecodeerror
            #     error = json.loads(out)
            #     # TODO
            #     sys.exit(f'{error}')
            pass