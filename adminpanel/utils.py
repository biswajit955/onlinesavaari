import xlwt
from django.http import HttpResponse
from wallet.models import WalletDetails
from django.contrib import messages
import datetime



def createExcelSheet(row_list, column_list, file_name):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={file_name}'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Data List') # this will make a sheet named Data List

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = column_list

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # font_style.num_format_str = 'dd/mm/yyyy'

    rows = row_list
    print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.date):
                date_time = row[col_num].strftime('%Y-%m-%d')
                ws.write(row_num, col_num, date_time, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    ws.col(0).width = 260*30
    ws.col(2).width = 260*15
    ws.col(3).width = 260*15
    ws.col(4).width = 260*20
    ws.col(5).width = 260*20
    ws.col(6).width = 260*20
    ws.col(7).width = 260*20
    wb.save(response)

    return response


def createWallet(user_email):
    wallet_activated_on = date.today()
    if(user_email != None):
        wall_user = User.objects.get(email=user_email)
        print(wall_user)
        curl = WalletDetails.objects.create(
            username=wall_user, email=user_email, wallet_activated_on=wallet_activated_on, wallet_balance=0)