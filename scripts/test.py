from classes import Location, ElectionScraper

a = ElectionScraper(region="REGION VI", province="NEGROS OCCIDENTAL", city="CITY OF BACOLOD", brgy="TACULING", precinct="45010362")

a.scrape_data()