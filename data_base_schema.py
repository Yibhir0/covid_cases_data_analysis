# Yassine Ibhir & David Pizzolongo

data_base_name = 'covid_corona_db_DP_YI'

corona_table = '''( date_cases date NOT NULL,  
                position int NOT NULL,
                country_other varchar(50) NOT NULL,
                totalCases int NULL,
                NewCases int NULL,
                totalDeaths int NULL,
                newDeaths int DEFAULT NULL,
                totalRecovered int NULL,
                newRecovered int NULL,
                activeCases int NULL,
                seriousCritical int NULL,
                totalCasesPM decimal NULL,
                deathsPM decimal NULL,
                totalTests int NULL,
                testsPM decimal NULL,
                population int NULL,
                continent varchar(50),
                casesEveryXPeople int NULL,
                deathsEveryXPeople int NULL,
                testEveryXPeople int NULL,
                PRIMARY KEY (date_cases, country_other) );'''


country_borders_table = '''(country_other varchar(50) NOT NULL,
                border_country varchar(50) NULL,
                distance int(10) NULL,
                CONSTRAINT cntry_fk_1 FOREIGN KEY (country_other) REFERENCES corona_table(country_other)
                ); '''

