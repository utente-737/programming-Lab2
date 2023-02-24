class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        self.name = name
        self.data = []

    def get_data(self):# lettura e analisi dati
        with open(self.name, 'r') as file:
            lines = file.readlines()
            self.data = []
            for line in lines[1:]:
                if len(line.strip().split(',')) >= 2: 
                    date_str = line.strip().split(',')[0]
                    value_str = line.strip().split(',')[1]
                    if len(date_str.split("-")) == 2: # controllo che siano interi
                        try:
                            value = int(value_str)
                            year = int(date_str.split("-")[0])
                            month = int(date_str.split("-")[1])
                        except ValueError as e:
                            continue

                        self.data.append([date_str, value])
        
        # controllo per duplicati e per l'ordinamento:
        past_month = 0
        past_year = 0

        for date_str, value in self.data:
            year = int(date_str.split("-")[0])
            month = int(date_str.split("-")[1])
            if year < past_year:
                raise ExamException('Errore, timeseries non ordinata')
            elif year == past_year:
                if month < past_month:
                    raise ExamException('Errore, timeseries non ordinata')
                elif month == past_month:
                    raise ExamException('Errore, timeseries con duplicati')
            past_month = month
            past_year = year

        return self.data

time_series_file=CSVTimeSeriesFile(name='data.csv')

def detect_similar_monthly_variations(time_series, years):
    year1_data = {}
    year2_data = {}
    treshold = 2 # tolleranza per la differenza

    for date_str, value in time_series:
        year = int(date_str.split("-")[0])
        month = int(date_str.split("-")[1])
        if year == years[0]:
            year1_data[month] = value
        elif year == years[1]:
            year2_data[month] = value
        
    if len(year1_data) == 0 or len(year2_data) == 0:
        raise ExamException('Errore, anno/i non presente/i')

    differences = {}
    for month in range(1, 13):
        if month in year1_data and month in year2_data:
            diff = year2_data[month] - year1_data[month]
            differences[month] = diff

    out = []

    for month in range(1, 13):
        if month in differences:
            if differences[month] > treshold or differences[month] < -treshold :
                out.append(False)
            else:
                out.append(True)
        else:
            out.append(False)

    return out

print(detect_similar_monthly_variations(time_series_file.get_data(), [1949,1950]))