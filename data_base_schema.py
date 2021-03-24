# Yassine Ibhir & David Pizzolongo

data_base_name = 'covid_corona_db_DP_YI'

corona_table = '''( date_cases date NOT NULL,  
                position int NOT NULL,
                country_other varchar(50) NOT NULL,
                totalCases int NULL,
                NewCases int NULL,
                totalDeaths int NULL,
                newDeaths int NULL,
                totalRecovered int NULL,
                newRecovered int NULL,
                activeCases int NULL,
                seriousCritical int NULL,
                totalCasesPM decimal(10,2) NULL,
                deathsPM decimal(10,2) NULL,
                totalTests int NULL,
                testsPM decimal(10,2) NULL,
                population int NULL,
                continent varchar(50) NULL,
                casesEveryXPeople int NULL,
                deathsEveryXPeople int NULL,
                testEveryXPeople int NULL,
                PRIMARY KEY (country_other, date_cases) );'''


country_borders_table = '''(country_other varchar(50) NOT NULL,
                border_country varchar(50) NULL,
                distance decimal(10,2) NULL
                ); '''

