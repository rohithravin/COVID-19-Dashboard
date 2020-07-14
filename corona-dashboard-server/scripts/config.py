BAY_AREA_COUNTIES = ['Alameda','Contra Costa','Marin','Napa','San Francisco','San Mateo','Santa Clara','Sonoma','Solano']
NORCAL_COUNTIES = BAY_AREA_COUNTIES + ['Yuba', 'Sutter', 'Placer',  'Modoc',  'Butte',  'Sacramento', 'Shasta',  'Tehama','Yolo','Lassen','Amador',
                   'Plumas', 'Colusa', 'Calaveras',  'Stanislaus', 'Humboldt', 'El Dorado', 'San Joaquin', 'Siskiyou','Nevada', 'Tuolumne','Mendocino','Glenn','Del Norte', 'Santa Cruz', 'Monterey','San Benito',
                   'Lake','Merced','Inyo','Sierra','Madera','Fresno','Trinity','Mono','Tulare', 'Mariposa', 'Kings', 'Alpine']
SOCAL_COUNTIES = ['Los Angeles', 'Orange', 'Riverside', 'San Bernardino', 'Ventura', 'San Diego', 'Santa Barbara', 'Imperial','Kern','San Luis Obispo']
ALL_COUNTIES = SOCAL_COUNTIES + NORCAL_COUNTIES + ['Out Of Country', 'Unassigned']
HIGH_POPULOUS_COUNTIES = ['Los Angeles', 'San Diego', 'Orange', 'Riverside', 'San Bernardino','Santa Clara','Amameda','Sacramento', 'Contra Costa','Fresno','Kern','San Francisco']

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '4.0Stanford'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'corona'

DATA_URLS = {
                'cali_cases_age' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/339d1c4d-77ab-44a2-9b40-745e64e335f2/download/case_demographics_age.csv",
                'cali_cases_sex' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/ee01b266-0a04-4494-973e-93497452e85f/download/case_demographics_sex.csv",
                'cali_cases_race' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/7e477adb-d7ab-4d4b-a198-dc4c6dc634c9/download/case_demographics_ethnicity.csv",
                'cali_cases' : "https://data.ca.gov/dataset/590188d5-8545-4c93-a9a0-e230f0db7290/resource/926fd08f-cc91-4828-af38-bd45de97f8c3/download/statewide_cases.csv",
                'world_location' : "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/locations.csv",
                'world_data' : "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/full_data.csv",
                'cali_testing' : "https://data.ca.gov/dataset/efd6b822-7312-477c-922b-bccb82025fbe/resource/b6648a0d-ff0a-4111-b80b-febda2ac9e09/download/statewide_testing.csv"
            }