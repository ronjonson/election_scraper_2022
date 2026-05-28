from classes import Location, ElectionScraper

if __name__ == '__main__':
    a = ElectionScraper(
    region="REGION VI", 
    province="ILOILO", 
    city="CITY OF ILOILO",
    save_filepath='iloilo_city_results.csv',
    )
    a.scrape_data()