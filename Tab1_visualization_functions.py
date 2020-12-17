import threading

import pandas, pymysql, os
import dash

# parameters for setting up SQL connection
host = ""
port = 3306
username = ""
password = ""
dbname = ""

# setting up a connection to sql
conn = pymysql.connect(host, user=username, port=port, passwd=password, db=dbname)
conn_cursor = conn.cursor()


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def insert_data_into_table():
    # now we want to access the file and load the entire dataset into the table
    # and wherever there are blanks in the dataset, we want to replace them with "unanswered"
    # fetch the dataset
    path = "/home/deb/stack-overflow-2018-developer-survey"
    myfile = "survey_results_public.csv"

    os.chdir(path)
    mydata = pandas.read_csv(myfile, sep=",", low_memory=False)

    country_dict = {
        "Eritrea": "Eritrea",
        "Cameroon": "Cameroon",
        "New Zealand": "New Zealand",
        "Oman": "Oman",
        "Croatia": "Croatia",
        "Taiwan": "Taiwan",
        "Togo": "Togo",
        "Switzerland": "Switzerland",
        "Bulgaria": "Bulgaria",
        "Albania": "Albania",
        "Belize": "Belize",
        "Turkmenistan": "Turkmenistan",
        "Sudan": "Sudan",
        "Panama": "Panama",
        "Nepal": "Nepal",
        "Kazakhstan": "Kazakhstan",
        "Iceland": "Iceland",
        "Cape Verde": "Cape Verde",
        "Guatemala": "Guatemala",
        "Democratic People's Republic of Korea": "Republic of Korea",
        "Brunei Darussalam": "Brunei Darussalam",
        "Malta": "Malta",
        "Norway": "Norway",
        "Armenia": "Armenia",
        "Grenada": "Grenada",
        "Guinea": "Guinea",
        "Botswana": "Botswana",
        "Cambodia": "Cambodia",
        "Sri Lanka": "Sri Lanka",
        "Monaco": "Monaco",
        "Swaziland": "Swaziland",
        "Somalia": "Somalia",
        "Bhutan": "Bhutan",
        "Sierra Leone": "Sierra Leone",
        "Bangladesh": "Bangladesh",
        "Iran, Islamic Republic of...": "Iran, Islamic Republic of...",
        "Hong Kong (S.A.R.)": "Hong Kong",
        "Argentina": "Argentina",
        "Ireland": "Ireland",
        "Burkina Faso": "Burkina Faso",
        "Denmark": "Denmark",
        "Nauru": "Nauru",
        "Saudi Arabia": "Saudi Arabia",
        "Morocco": "Morocco",
        "Paraguay": "Paraguay",
        "Mexico": "Mexico",
        "Micronesia, Federated States of...": "Micronesia",
        "Maldives": "Maldives",
        "Peru": "Peru",
        "Solomon Islands": "Solomon Islands",
        "Thailand": "Thailand",
        "Canada": "Canada",
        "The former Yugoslav Republic of Macedonia": "Republic of Macedonia",
        "Germany": "Germany",
        "Mali": "Mali",
        "Egypt": "Egypt",
        "Philippines": "Philippines",
        "Pakistan": "Pakistan",
        "Timor-Leste": "Timor-Leste",
        "Greece": "Greece",
        "Guinea-Bissau": "Guinea-Bissau",
        "Lithuania": "Lithuania",
        "Barbados": "Barbados",
        "Bahamas": "Bahamas",
        "Slovenia": "Slovenia",
        "Angola": "Angola",
        "Gambia": "Gambia",
        "Tunisia": "Tunisia",
        "Singapore": "Singapore",
        "San Marino": "San Marino",
        "Senegal": "Senegal",
        "El Salvador": "El Salvador",
        "Zambia": "Zambia",
        "Afghanistan": "Afghanistan",
        "Uzbekistan": "Uzbekistan",
        "Kyrgyzstan": "Kyrgyzstan",
        "Netherlands": "Netherlands",
        "Hungary": "Hungary",
        "Estonia": "Estonia",
        "Qatar": "Qatar",
        "Tajikistan": "Tajikistan",
        "Fiji": "Fiji",
        "United Arab Emirates": "United Arab Emirates",
        "Nigeria": "Nigeria",
        "Yemen": "Yemen",
        "Central African Republic": "Central African Republic",
        "Costa Rica": "Costa Rica",
        "Belarus": "Belarus",
        "Saint Lucia": "Saint Lucia",
        "Azerbaijan": "Azerbaijan",
        "Spain": "Spain",
        "Nicaragua": "Nicaragua",
        "Lesotho": "Lesotho",
        "Burundi": "Burundi",
        "Honduras": "Honduras",
        "Portugal": "Portugal",
        "Latvia": "Latvia",
        "Syrian Arab Republic": "Syrian Arab Republic",
        "Austria": "Austria",
        "Japan": "Japan",
        "Colombia": "Colombia",
        "Madagascar": "Madagascar",
        "North Korea": "North Korea",
        "Dominican Republic": "Dominican Republic",
        "Chile": "Chile",
        "United States": "United States",
        "Democratic Republic of the Congo": "Democratic Republic of the Congo",
        "Other Country (Not Listed Above)": "Other Country",
        "Malawi": "Malawi",
        "Cyprus": "Cyprus",
        "Indonesia": "Indonesia",
        "Czech Republic": "Czech Republic",
        "Georgia": "Georgia",
        "Niger": "Niger",
        "Benin": "Benin",
        "Gabon": "Gabon",
        "Guyana": "Guyana",
        "Ukraine": "Ukraine",
        "Ghana": "Ghana",
        "Haiti": "Haiti",
        "Bahrain": "Bahrain",
        "Bosnia and Herzegovina": "Bosnia and Herzegovina",
        "Zimbabwe": "Zimbabwe",
        "Mozambique": "Mozambique",
        "United Kingdom": "United Kingdom",
        "Mauritania": "Mauritania",
        "Italy": "Italy",
        "Ethiopia": "Ethiopia",
        "Slovakia": "Slovakia",
        "India": "India",
        "Montenegro": "Montenegro",
        "Russian Federation": "Russian Federation",
        "Mauritius": "Mauritius",
        "Turkey": "Turkey",
        "Uruguay": "Uruguay",
        "Namibia": "Namibia",
        "Andorra": "Andorra",
        "Uganda": "Uganda",
        "China": "China",
        "Rwanda": "Rwanda",
        "Malaysia": "Malaysia",
        "Bolivia": "Bolivia",
        "Finland": "Finland",
        "Kuwait": "Kuwait",
        "Antigua and Barbuda": "Antigua and Barbuda",
        "Cuba": "Cuba",
        "Palau": "Palau",
        "Australia": "Australia",
        "Trinidad and Tobago": "Trinidad and Tobago",
        "Israel": "Israel",
        "Venezuela, Bolivarian Republic of...": "Venezuela",
        "Congo, Republic of the...": "Congo",
        "Lebanon": "Lebanon",
        "Poland": "Poland",
        "Kenya": "Kenya",
        "Iraq": "Iraq",
        "Algeria": "Algeria",
        "Republic of Moldova": "Republic of Moldova",
        "Belgium": "Belgium",
        "South Korea": "South Korea",
        "Serbia": "Serbia",
        "Jordan": "Jordan",
        "Sweden": "Sweden",
        "Ecuador": "Ecuador",
        "Liechtenstein": "Liechtenstein",
        "Libyan Arab Jamahiriya": "Libyan Arab Jamahiriya",
        "Côte d'Ivoire": "Cote dIvoire",
        "Mongolia": "Mongolia",
        "Brazil": "Brazil",
        "Dominica": "Dominica",
        "Marshall Islands": "Marshall Islands",
        "South Africa": "South Africa",
        "Suriname": "Suriname",
        "Liberia": "Liberia",
        "Romania": "Romania",
        "Republic of Korea": "Republic of Korea",
        "Jamaica": "Jamaica",
        "France": "France",
        "Myanmar": "Myanmar",
        "United Republic of Tanzania": "United Republic of Tanzania",
        "Luxembourg": "Luxembourg",
        "Viet Nam": "Viet Nam",
        "Djibouti": "Djibouti",
    }

    currency_dict = {
        "Euros (€)": "Euros",
        "Japanese yen (¥)": "Japanese yen",
        "Russian rubles (₽)": "Russian rubles",
        "Canadian dollars (C$)": "Canadian dollars",
        "U.S. dollars ($)": "U.S. dollars",
        "Singapore dollars (S$)": "Singapore dollars",
        "Australian dollars (A$)": "Australian dollars",
        "Swedish kroner (SEK)": "Swedish kroner",
        "Swiss francs": "Swiss francs",
        "Indian rupees (₹)": "Indian rupees",
        "Bitcoin (btc)": "Bitcoin",
        "Polish złoty (zł)": "Polish zloty",
        "Norwegian krone (kr)": "Norwegian krone",
        "South African rands (R)": "South African rands",
        "Danish krone (kr)": "Danish krone",
        "British pounds sterling (£)": "British pounds sterling",
        "Mexican pesos (MXN$)": "Mexican pesos",
        "Chinese yuan renminbi (¥)": "Chinese yuan renminbi",
        "Brazilian reais (R$)": "Brazilian reais",
    }
    for row in mydata.itertuples():
        # go through each column on every row, and if the cell has blank value, then insert "unanswered" for now
        row_list = []

        i = 0
        for element in row:
            if i == 0:
                i = i + 1
                continue
            if pandas.isnull(element):
                updated_element = "UNANSWERED"
                row_list.append(updated_element)
            else:
                if getattr(row, "Currency") == element:
                    updated_element = currency_dict[element]
                    print("updated element:" + str(updated_element))
                    row_list.append(updated_element)
                elif getattr(row, "Country") == element:
                    updated_element = country_dict[element]
                    print("updated element:" + str(updated_element))
                    row_list.append(updated_element)
                else:
                    updated_element = str(element).strip()
                    row_list.append(updated_element)

        insert_qry = "insert into so_answers values (%s,%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s," \
                     "	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s)"
        # # (Respondent,Hobby,	OpenSource,	Country,	Student,	Employment,
        # FormalEducation,	UndergradMajor,	CompanySize,	DevType,
        # YearsCoding,	YearsCodingProf,	JobSatisfaction,	CareerSatisfaction,
        # HopeFiveYears,	JobSearchStatus,	LastNewJob,	AssessJob1,	AssessJob2,	AssessJob3,
        # AssessJob4,	AssessJob5,	AssessJob6,	AssessJob7,	AssessJob8,	AssessJob9,	AssessJob10,
        # AssessBenefits1,	AssessBenefits2,	AssessBenefits3,	AssessBenefits4,	AssessBenefits5,
        # AssessBenefits6,	AssessBenefits7,	AssessBenefits8,	AssessBenefits9,	AssessBenefits10,
        # AssessBenefits11,	JobContactPriorities1,	JobContactPriorities2,	JobContactPriorities3,	JobContactPriorities4,
        # JobContactPriorities5,	JobEmailPriorities1,	JobEmailPriorities2,	JobEmailPriorities3,
        # JobEmailPriorities4,	JobEmailPriorities5,	JobEmailPriorities6,	JobEmailPriorities7,
        # UpdateCV,	Currency,	Salary,	SalaryType,	ConvertedSalary,	CurrencySymbol,	CommunicationTools,
        # TimeFullyProductive,	EducationTypes,	SelfTaughtTypes,	TimeAfterBootcamp,	HackathonReasons,
        # AgreeDisagree1,	AgreeDisagree2,	AgreeDisagree3,	LanguageWorkedWith,	LanguageDesireNextYear,
        # DatabaseWorkedWith,	DatabaseDesireNextYear,	PlatformWorkedWith,	PlatformDesireNextYear,	FrameworkWorkedWith,
        # FrameworkDesireNextYear,	IDE,	OperatingSystem,	NumberMonitors,	Methodology,	VersionControl,	CheckInCode,
        # AdBlocker,	AdBlockerDisable,	AdBlockerReasons,	AdsAgreeDisagree1,	AdsAgreeDisagree2,	AdsAgreeDisagree3,
        # AdsActions,	AdsPriorities1,	AdsPriorities2,	AdsPriorities3,	AdsPriorities4,	AdsPriorities5,	AdsPriorities6,
        # AdsPriorities7,	AIDangerous,	AIInteresting,	AIResponsible,	AIFuture,	EthicsChoice,	EthicsReport,
        # EthicsResponsible,	EthicalImplications,	StackOverflowRecommend,	StackOverflowVisit,	StackOverflowHasAccount,
        # StackOverflowParticipate,	StackOverflowJobs,	StackOverflowDevStory,	StackOverflowJobsRecommend,
        # StackOverflowConsiderMember,	HypotheticalTools1,	HypotheticalTools2,	HypotheticalTools3,
        # HypotheticalTools4,	HypotheticalTools5,	WakeTime,	HoursComputer,	HoursOutside,	SkipMeals,
        # ErgonomicDevices,	Exercise,	Gender,	SexualOrientation,	EducationParents,	RaceEthnicity,
        # Age, Dependents,	MilitaryUS,	SurveyTooLong,	SurveyEasy )

        execute = conn_cursor.execute(insert_qry, row_list)
        conn.commit()
    # except:
    #     print("Failed to insert row:\n"+str(row_list))

    record_count_qry = "select count(1) from so_answers"
    rc = pandas.read_sql(record_count_qry, con=conn)
    print("after insertion: " + str(rc))



def get_participants_country_wise():
    country_wise_qry = "select country, count(1) as freq from bs_so_answers where country <> 'UNANSWERED' group by country order by 2 desc"
    country_wise_df = pandas.read_sql(country_wise_qry, con=conn)

    return country_wise_df



#     this function is used for tab 1 for educational background
def get_country_wise_education_background():

    country_wise_education_background = (
        "select country, case when lower(degree) like '%bachelor%' then 'Undergraduate' "
        "  when lower(degree) like '%master%' then 'Graduate'    "
        "when lower(degree) like '%secondary%' then 'Secondary School'"
        "    WHEN lower(degree) like '%some college/university%' then 'Dropout'"
        "    when lower(degree) like '%associate%' then 'Associate Degree'"
        "    when lower(degree) like '%never completed%' then 'No Formal Education'"
        "    when lower(degree) like '%doctoral%' then 'Doctoral Degree'"
        "    when lower(degree) like '%primary%' then 'Primary School'"
        "    when lower(degree) like '%professional%' then 'Professional Degree'"
        "    else 'NA' end degree, cnt from("
        "select country, FormalEducation as degree, count(1) as cnt from bs_so_answers "
        "where Country != 'UNANSWERED' and  FormalEducation != 'UNANSWERED' "
        "group by country, FormalEducation order by 1,3 desc)a"
    )

    country_wise_education_background = pandas.read_sql(
        country_wise_education_background, con=conn
    )

    return country_wise_education_background


# this function is for tab 1 job satisfaction vs new job new search
def get_job_avail_vs_satifaction():
    job_satifaction_qry = (
        "select country, JobSatisfaction_up, "
        "case when  JobSearchStatus_up like '%ACTIVELY LOOKING FOR A JOB' then 'Actively Looking'"
        " when JobSearchStatus_up like '%ACTIVELY LOOKING, BUT I AM OPEN TO NEW OPPORTUNITIES' then 'Open to Opportunities'"
        " when JobSearchStatus_up like '%NOT INTERESTED%' then 'Not Interested' END JobSearchStatus_clean, cnt "
        "from ( "
        "select country, upper(JobSatisfaction) as JobSatisfaction_up, upper(JobSearchStatus) as JobSearchStatus_up, count(1) as cnt "
        "from bs_so_answers  "
        "where JobSatisfaction != 'UNANSWERED' and JobSearchStatus != 'UNASNWERED' "
        " group by country, JobSatisfaction_up, JobSearchStatus_up  order by 1,2,3,4 desc)a;"
    )
    country_wise_job_satisfaction = pandas.read_sql(job_satifaction_qry, con=conn)
    # conn.close()
    return country_wise_job_satisfaction


# this function is for the work life balance graph
def get_work_life_balance():
    qry_for_hours_computer = (
        "select a.country, b.mapped_attrib_value as time_bckt, sum(a.cnt) as cnt, b.priority"
        " from (select country, hoursComputer, count(1) as cnt from bs_so_answers "
        "where country != 'UNANSWERED'  and hoursComputer != 'UNANSWERED'"
        " group by country, hoursComputer)a"
        " left outer join "
        "(select mapped_attrib_value, attrib_value, priority "
        "from so_attrib_priority "
        "where attrib_name = 'HOURS_COMPUTER')b "
        "on a.hourscomputer = b.attrib_value"
        " group by a.country, b.mapped_attrib_value, b.priority "
        "order by 1,b.priority;"
    )

    qry_for_hours_outside = (
        "select a.country, b.mapped_attrib_value as time_bckt, sum(a.cnt) as cnt, b.priority "
        "from (select country, HoursOutside, count(1) as cnt from bs_so_answers "
        "where country != 'UNANSWERED'  and HoursOutside != 'UNANSWERED'"
        " group by country, HoursOutside)a "
        "left outer join "
        "(select mapped_attrib_value, attrib_value, priority from so_attrib_priority)b"
        " on a.HoursOutside = b.attrib_value"
        " group by a.country, b.mapped_attrib_value, b.priority "
        "order by 1,b.priority;"
    )

    hours_computer_df = pandas.read_sql(qry_for_hours_computer, con=conn)
    hours_outside_df = pandas.read_sql(qry_for_hours_outside, con=conn)

    return hours_computer_df, hours_outside_df




