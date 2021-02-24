import pandas
import datetime
import wget
import os.path
import shutil

class Createlink:
    def __init__(self, period):
        self.primary_dt = datetime.datetime(2020, 10, 12, 1, 50, 0)
        self.current_dt = datetime.datetime.now()
        self.primary_seconds = period
        self.secondary_seconds = 1602456600
        self.delta = round((self.current_dt - self.primary_dt).total_seconds())
        self.primary_seconds = self.primary_seconds + self.delta
        self.secondary_seconds = self.secondary_seconds + self.delta

    def primary_seconds(self):
        return self.primary_seconds

    def secondary_seconds(self):
        return self.secondary_seconds


class TableConverter:
    def __init__(self, period):
        self.for_link = Createlink(period)

    def Table_maker(self, name, path):

        path = str(path)
        # Creating periods, paths to files and link to download table

        if not path[-1] == '/':
           return 'wrong path name'
        else:
            pass

        self.period1 = self.for_link.primary_seconds
        self.period2 = self.for_link.secondary_seconds

        self.ticker_csv = name + '.csv'
        self.ticker_xlsx = name + '.xlsx'
        self.primary_directory = path + self.ticker_csv
        self.secondary_directory = path + self.ticker_xlsx

        if os.path.exists(self.primary_directory):
            os.remove(self.primary_directory)
        else:
            pass
        try:
            self.link = 'https://query1.finance.yahoo.com/v7/finance/download/' + name + '?period1=' + str(self.period1) + '&period2=' + str(self.period2) + '&interval=1d&events=history&includeAdjustedClose=true'

            # Downloading table

            wget.download(self.link, self.primary_directory)

            # Import CSV file

            self.ticker = pandas.read_csv(self.primary_directory)

            # Executing number of days given in table

            self.height = int(len(self.ticker.index))

            # Finding delta between high and low price for each day, rounding all the cells to the 2nd decimal point

            self.ticker['Open'].astype('float')
            self.ticker['High'].astype('float')
            self.ticker['Close'].astype('float')
            self.ticker['Adj Close'].astype('float')
            self.ticker['Low'].astype('float')

            self.ticker['Open'] = round(self.ticker['Open'], 2)
            self.ticker['High'] = round(self.ticker['High'], 2)
            self.ticker['Close'] = round(self.ticker['Close'], 2)
            self.ticker['Adj Close'] = round(self.ticker['Adj Close'], 2)
            self.ticker['Low'] = round(self.ticker['Low'], 2)

            self.ticker['Delta ($)'] = abs(self.ticker['High'].add(-(self.ticker['Low'])))

            self.ticker['Delta ($)'] = round(self.ticker['Delta ($)'], 2)

            # Adding one last line in the bottom to show up average values for needed columns

            self.average = {'Date': 'Average', 'Close': '-', 'Open': '-', 'High': '-', 'Low': '-', 'Adj Close': '-'}

            self.ticker = self.ticker.append(self.average, ignore_index=True)

            # Finding average values and rounding to the 2nd decimal place

            self.ticker['Volume'] = round(self.ticker['Volume'] / (10 ** 6), 2)
            self.ticker.at[self.height, 'Volume'] = round(self.ticker['Volume'].mean(), 2)

            self.ticker.at[self.height, 'Delta ($)'] = round(self.ticker['Delta ($)'].mean(), 2)

            # Auxiliary row:

            self.auxiliary = self.ticker.iloc[[self.height]]

            # Concatenating auxiliary row with ticker dataframe

            self.ticker = pandas.concat([self.auxiliary, self.ticker]).reset_index(drop=True)

            # Deleting last row
            self.height = len(self.ticker['Date'])
            self.ticker = self.ticker.drop([self.height - 1])

            # Styling DataFrame

            # Exporting DataFrame to xlsx and deleting csv file, for further working with excelwriter

            self.ticker.to_excel(self.secondary_directory, index=False)
            os.remove(self.primary_directory)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            self.writer = pandas.ExcelWriter(self.secondary_directory, engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object

            self.ticker.to_excel(self.writer, sheet_name='Sheet1', index=False)

            # Get the xlsxwriter objects from the dataframe writer object

            self.workbook = self.writer.book
            self.worksheet = self.writer.sheets['Sheet1']

            # Working with xlsx file

            self.options = {}
            self.row_format = self.workbook.add_format({'bottom': self.options.get('border', 2),
                                                        'top': self.options.get('border', 2),
                                                        'bold': True,
                                                        'font_color': 'green'})
            self.first_cell_format = self.workbook.add_format({'left': self.options.get('border', 2),
                                                               'bottom': self.options.get('border', 2),
                                                               'top': self.options.get('border', 2)})
            self.last_cell_1_format = self.workbook.add_format({'left': self.options.get('border', 2),
                                                                'bottom': self.options.get('border', 2),
                                                                'top': self.options.get('border', 2)})
            self.last_cell_2_format = self.workbook.add_format({'right': self.options.get('border', 2),
                                                                'bottom': self.options.get('border', 2),
                                                                'top': self.options.get('border', 2)})
            self.text_format = self.workbook.add_format()
            self.text_format.set_align('vcenter')
            self.text_format.set_align('center')
            self.text_format.set_font_color('green')
            self.text_format.set_bold()
            self.last_cell_1_format.set_border_color('red')
            self.last_cell_2_format.set_border_color('red')
            self.worksheet.set_row(1, 30, self.text_format)

            self.worksheet.conditional_format('B2:F2', {'type': 'cell',
                                                        'criteria': '>=',
                                                        'value': '0',
                                                        'format': self.row_format})
            self.worksheet.conditional_format('A2:A2', {'type': 'cell',
                                                        'criteria': '>=',
                                                        'value': '0',
                                                        'format': self.first_cell_format})
            self.worksheet.conditional_format('H2:H2', {'type': 'cell',
                                                        'criteria': '>=',
                                                        'value': '0',
                                                        'format': self.last_cell_2_format})
            self.worksheet.conditional_format('G2:G2', {'type': 'cell',
                                                        'criteria': '>=',
                                                        'value': '0',
                                                        'format': self.last_cell_1_format})

            self.writer.save()
        except:
            return 'try again'
class Pivot_Maker:
    def __init__(self):
        self.counter = ''

    def Pivot_maker(self, name, path):

        path = str(path)

        self.ticker_xlsx = name + '.xlsx'
        self.stock_name = pandas.read_excel(path + self.ticker_xlsx, engine='openpyxl')
        if not os.path.exists(path + self.ticker_xlsx):
            print('doesnt exist')
            shutil.copy('ATR Pivot table.xlsx', path)
        try:
            self.ticker = pandas.read_excel(path + 'ATR Pivot table.xlsx', engine='openpyxl')
        except:
            shutil.copy('ATR Pivot table.xlsx', path)
            self.ticker = pandas.read_excel(path + 'ATR Pivot table.xlsx', engine='openpyxl')

        for i in range(len(self.ticker)):
            if self.ticker.at[i, 'Name'] == name:
                self.ticker.at[i, 'ATR'] = self.stock_name.at[0, 'Delta ($)']
                self.counter = 'True'
                break
            else:
                pass
        if not self.counter == 'True':
            self.line = {'Name': name, 'ATR': self.stock_name.at[0, 'Delta ($)']}
            self.ticker = self.ticker.append(self.line, ignore_index=True)
        self.ticker = self.ticker[['Name', 'ATR']]
        self.ticker.to_excel(path + 'ATR Pivot table.xlsx', index=False, engine='xlsxwriter')





