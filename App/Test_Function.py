import config as cf
import xlsxwriter
import view
assert cf

def TestFunction():

    test_inputs = { 1: (0,0),
                    2: ('LED', 'RTP'),
                    3: ('St. Petersburg', 'Lisbon'),
                    4: ('Lisbon', 19850),
                    5: ('DXB', 0)}
    test_data = {   9261: test_inputs,
                    18521: test_inputs,
                    27782: test_inputs,
                    37042: test_inputs,
                    46303: test_inputs,
                    55563: test_inputs,
                    64824: test_inputs,
                    74084: test_inputs,
                    83345: test_inputs,
                    92605: test_inputs}

    workbook   = xlsxwriter.Workbook('Test_Data.xlsx')
    worksheet = workbook.add_worksheet()

    initial_index = 3
    for data_size in test_data:
        test_data_size = test_data[data_size]
        print(30*'#' + ' ' + str((initial_index - 2)*10) + '% Test ' + 30*'#')
        catalog = view.TestProgram(0, None, data_size, 0)
        for function in test_data_size:
            definitve_index = 'D' + str(initial_index + (function - 1)*11)
            function_inputs = test_data_size[function]
            input_1 = function_inputs[0]
            input_2 = function_inputs[1]

            summation_elapsed_time = 0
            print(20*'=' + ' Function ' + str(function) + ' Test ' + 20*'=')
            for test in range(0,5):
                print(10*'-' + ' Test No.' + str(test + 1) + ' ' + 10*'-')
                elapsed_time = view.TestProgram(function, catalog, input_1, input_2)
                summation_elapsed_time += elapsed_time

            mean_elapsed_time = summation_elapsed_time/5
            worksheet.write(definitve_index, mean_elapsed_time)
        initial_index += 1

    workbook.close()

TestFunction()