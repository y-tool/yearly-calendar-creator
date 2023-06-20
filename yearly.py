# ----------------------------------------------------------------
# インポート
# ----------------------------------------------------------------
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import jpholiday
from jeraconv import jeraconv
import string
import random
import zipfile
import os
import shutil
# ----------------------------------------------------------------
# 変数
# ----------------------------------------------------------------

# 年の設定
year = st.sidebar.number_input(
    label = '年',
    value = dt.datetime.now().year,
)
# ----------------------------------------------------------------
# 変数の初期値

# フォントの設定
list_font_family = ['M PLUS 1p','たぬゴ角','たぬゴ丸','自由の翼フォント','源真ゴシック ','源柔ゴシック','せのびゴシック','ランパート','トレイン','しっぽり明朝']
dict_font_family = {
    'M PLUS 1p':{'Thin':'MPLUS1p-Thin.ttf','Light':'MPLUS1p-Light.ttf','Regular':'MPLUS1p-Regular.ttf','Medium':'MPLUS1p-Medium.ttf','ExtraBold':'MPLUS1p-ExtraBold.ttf','Black':'MPLUS1p-Black.ttf'},
    'たぬゴ角':{'極細':'Tanugo-ExtraLight.otf','細':'Tanugo-Light.otf','標準':'Tanugo-Regular.otf','太':'Tanugo-Bold.otf'},
    'たぬゴ丸':{'細':'Tanugo-Round-Light.otf','標準':'Tanugo-Round-Regular.otf','太':'Tanugo-Round-Bold.otf'},
    '自由の翼フォント':{'Regular':'JiyunoTsubasa.ttf'},
    '源真ゴシック ':{'ExtraLight':'GenShinGothic-Monospace-ExtraLight.ttf','Light':'GenShinGothic-Monospace-Light.ttf','Normal':'GenShinGothic-Monospace-Normal.ttf','Regular':'GenShinGothic-Monospace-Regular.ttf','Medium':'GenShinGothic-Monospace-Medium.ttf','Bold':'GenShinGothic-Monospace-Bold.ttf','Heavy':'GenShinGothic-Monospace-Heavy.ttf'},
    '源柔ゴシック':{'ExtraLight':'GenJyuuGothic-Monospace-ExtraLight.ttf','Light':'GenJyuuGothic-Monospace-Light.ttf','Normal':'GenJyuuGothic-Monospace-Normal.ttf','Regular':'GenJyuuGothic-Monospace-Regular.ttf','Medium':'GenJyuuGothic-Monospace-Medium.ttf','Bold':'GenJyuuGothic-Monospace-Bold.ttf','Heavy':'GenJyuuGothic-Monospace-Heavy.ttf'},
    'せのびゴシック':{'Regular':'Senobi-Gothic-Regular.ttf','Medium':'Senobi-Gothic-Medium.ttf','Bold':'Senobi-Gothic-Bold.ttf'},
    'ランパート':{'Regular':'RampartOne-Regular.ttf'},
    'トレイン':{'Regular':'TrainOne-Regular.ttf'},
    'しっぽり明朝':{'Regular':'ShipporiMincho-Regular.ttf','Medium':'ShipporiMincho-Medium.ttf','SemiBold':'ShipporiMincho-SemiBold.ttf','Bold':'ShipporiMincho-Bold.ttf','ExtraBold':'ShipporiMincho-ExtraBold.ttf'},
}
# 曜日
weekday_start_options = ['日曜始まり','月曜始まり']

dict_weekday_name = {
    '月':['月','火','水','木','金','土','日'],
    '月曜':['月曜','火曜','水曜','木曜','金曜','土曜','日曜'],
    'Mon':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    'MON':['MON','TUE','WED','THU','FRI','SAT','SUN'],
    'M':['M','T','W','T','F','S','S'],
}

# 配置
list_horizontality = ['左揃え','中央揃え','右揃え']
list_vertical = ['上揃え','中央揃え','下揃え']

# 罫線
list_border_type = ['実線','点線','破線','一点破線','二点破線']

# ----------------------------------------------------------------
# サイドバー

# タイトルの設定
with st.sidebar.expander('タイトルの設定', False):
    def wareki_eng(wareki):
        replace_list = [['明治', 'M'], ['大正', 'T'], ['昭和', 'S'], ['平成', 'H'], ['令和', 'R']]
        for s in replace_list:
            replace_str = wareki.replace(s[0], s[1])
        return replace_str

    list_title = []
    for i in range(1, 13):

        date0101 = dt.datetime(year, i, 1, 0, 0)
        w2j = jeraconv.W2J()

        iyear = date0101.year
        imonth = date0101.month
        emonth_short = date0101.strftime('%b')
        emonth_long = date0101.strftime('%B')

        wdate0101 = w2j.convert(date0101.year, date0101.month, date0101.day, return_type='dict')
        wjyear = wdate0101['era'] + str(wdate0101['year'])
        weyear = wareki_eng(wdate0101['era']) + str(wdate0101['year'])

        dict_title_format = {
            '1月':f'{imonth}月',
            '2023年1月':f'{iyear}年{imonth}月',
            'R5.1':f'{weyear}.{imonth}',
            '令和5年1月':f'{wjyear}年{imonth}月',
            '2023/01':f'{iyear}/{str(imonth).zfill(2)}',
            '2023/1':f'{iyear}/{imonth}',
            '202301':f'{iyear}{str(imonth).zfill(2)}',
            '01':f'{str(imonth).zfill(2)}',
            '1':f'{imonth}',
            'Jan':f'{emonth_short}',
            'Jan, 2023':f'{emonth_short}, {iyear}',
            'January':f'{emonth_long}',
            'January, 2023':f'{emonth_long}, {iyear}',
        }

        list_title.append({})
        for title in dict_title_format.keys():
            list_title[i - 1][title] = dict_title_format[title]

    st.caption('表示形式')
    title_format = st.selectbox(
        label = 'タイトル形式',
        options = dict_title_format.keys(),
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォント名')
    title_font_family = st.selectbox(
        label = 'フォント名(タイトル)',
        options = list_font_family,
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォントスタイル')
    title_font_style = st.selectbox(
        label = 'フォントスタイル(タイトル)',
        options = dict_font_family[title_font_family].keys(),
        index = 0,
        label_visibility = 'collapsed',
    )
    col1, col2 = st.columns(2)
    with col1:
        st.caption('フォントカラー')
        title_font_color_html = st.color_picker(
            label = 'フォントカラー(タイトル)',
            value = '#000000',
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('背景色')
        title_background_color_html = st.color_picker(
            label = '背景色(タイトル)',
            value = '#FFFFFF',
            label_visibility = 'collapsed',
        )
    st.caption('フォントサイズ')
    title_font_size = st.slider(
        label = 'フォントサイズ(タイトル)',
        min_value = 10,
        max_value = 50,
        value = 30,
        label_visibility = 'collapsed',
    )
    st.caption('高さ')
    title_height = st.slider(
        label = '高さ(タイトル)',
        min_value = 20,
        max_value = 100,
        value = 50,
        label_visibility = 'collapsed',
    )
    col1, col2 = st.columns(2)
    with col1:
        st.caption('水平位置')
        title_horizontality = st.selectbox(
            label = '水平位置(タイトル)',
            options = list_horizontality,
            index = 1,
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('垂直位置')
        title_vertical = st.selectbox(
            label = '垂直位置(タイトル)',
            options = list_vertical,
            index = 1,
            label_visibility = 'collapsed',
        )

# 曜日の設定
with st.sidebar.expander('曜日の設定', False):

    st.caption('週始まり')
    weekday_start = st.radio(
        label = '週始まり',
        options = weekday_start_options,
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('表示形式')
    weekday_name = st.selectbox(
        label = '曜日形式',
        options = ['月','月曜','Mon','MON','M'],
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォント名')
    hedder_font_family = st.selectbox(
        label = 'フォント名(曜日)',
        options = list_font_family,
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォントスタイル')
    hedder_font_style = st.selectbox(
        label = 'フォントスタイル(曜日)',
        options = dict_font_family[hedder_font_family].keys(),
        index = 0,
        label_visibility = 'collapsed',
    )
    st.write(
        '<div style="font-size:0.9em; padding-bottom:0.5em;">フォントカラー</div>',
        unsafe_allow_html = True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption('(平日)')
        hedder_font_color_html_normal = st.color_picker(
            label = 'フォントカラー(曜日)(平日)',
            value = '#000000',
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('(土曜)')
        hedder_font_color_html_saturday = st.color_picker(
            label = 'フォントカラー(曜日)(土曜)',
            value = '#0000FF',
            label_visibility = 'collapsed',
        )
    with col3:
        st.caption('(日曜)')
        hedder_font_color_html_sunday = st.color_picker(
            label = 'フォントカラー(曜日)(日曜)',
            value = '#FF0000',
            label_visibility = 'collapsed',
        )
    st.write(
        '<div style="font-size:0.9em; padding-bottom:0.5em;">背景色</div>',
        unsafe_allow_html = True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption('(平日)')
        hedder_background_color_html_normal = st.color_picker(
            label = '背景色(曜日)(平日)',
            value = '#CCCCCC',
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('(土曜)')
        hedder_background_color_html_saturday = st.color_picker(
            label = '背景色(曜日)(土曜)',
            value = '#CCCCCC',
            label_visibility = 'collapsed',
        )
    with col3:
        st.caption('(日曜)')
        hedder_background_color_html_sunday = st.color_picker(
            label = '背景色(曜日)(日曜)',
            value = '#CCCCCC',
            label_visibility = 'collapsed',
        )
    st.caption('フォントサイズ')
    hedder_font_size = st.slider(
        label = 'フォントサイズ(曜日)',
        min_value = 10,
        max_value = 30,
        value = 20,
        label_visibility = 'collapsed',
    )
    st.caption('高さ')
    hedder_height = st.slider(
        label = '高さ(曜日)',
        min_value = 20,
        max_value = 100,
        value = 50,
        label_visibility = 'collapsed',
    )
    col1, col2 = st.columns(2)
    with col1:
        st.caption('水平位置')
        hedder_horizontality = st.selectbox(
            label = '水平位置(曜日)',
            options = list_horizontality,
            index = 1,
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('垂直位置')
        hedder_vertical = st.selectbox(
            label = '垂直位置(曜日)',
            options = list_vertical,
            index = 1,
            label_visibility = 'collapsed',
        )

# 日付の設定
with st.sidebar.expander('日付の設定', False):
    st.caption('フォント名')
    cell_font_family = st.selectbox(
        label = 'フォント名(日付)',
        options = list_font_family,
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォントスタイル')
    cell_font_style = st.selectbox(
        label = 'フォントスタイル(日付)',
        options = dict_font_family[cell_font_family].keys(),
        index = 0,
        label_visibility = 'collapsed',
    )
    st.write(
        '<div style="font-size:0.9em; padding-bottom:0.5em;">フォントカラー</div>',
        unsafe_allow_html = True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption('(平日)')
        cell_font_color_html_normal = st.color_picker(
            label = 'フォントカラー(日付)(平日)',
            value = '#000000',
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('(土曜)')
        cell_font_color_html_saturday = st.color_picker(
            label = 'フォントカラー(日付)(土曜)',
            value = '#0000FF',
            label_visibility = 'collapsed',
        )
    with col3:
        st.caption('(日曜/祝日)')
        cell_font_color_html_sunday = st.color_picker(
            label = 'フォントカラー(日付)(日曜)',
            value = '#FF0000',
            label_visibility = 'collapsed',
        )

    st.write(
        '<div style="font-size:0.9em; padding-bottom:0.5em;">背景色</div>',
        unsafe_allow_html = True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption('(平日)')
        cell_background_color_html_normal = st.color_picker(
            label = '背景色(日付)(平日)',
            value = '#FFFFFF',
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('(土曜)')
        cell_background_color_html_saturday = st.color_picker(
            label = '背景色(日付)(土曜)',
            value = '#BBBBFF',
            label_visibility = 'collapsed',
        )
    with col3:
        st.caption('(日曜/祝日)')
        cell_background_color_html_sunday = st.color_picker(
            label = '背景色(日付)(日曜)',
            value = '#FFBBBB',
            label_visibility = 'collapsed',
        )
    st.caption('(日付無し)')
    cell_background_color_html_empty = st.color_picker(
        label = '背景色(日付無し)',
        value = '#EFEFEF',
        label_visibility = 'collapsed',
    )
    st.caption('フォントサイズ')
    cell_font_size = st.slider(
        label = 'フォントサイズ(日付)',
        min_value = 10,
        max_value = 30,
        value = 20,
        label_visibility = 'collapsed',
    )
    st.caption('幅')
    cell_width = st.slider(
        label = '幅',
        min_value = 20,
        max_value = 100,
        value = 50,
        label_visibility = 'collapsed',
    )
    st.caption('高さ')
    cell_height = st.slider(
        label = '高さ(日付)',
        min_value = 20,
        max_value = 100,
        value = 50,
        label_visibility = 'collapsed',
    )
    col1, col2 = st.columns(2)
    with col1:
        st.caption('水平位置')
        cell_horizontality = st.selectbox(
            label = '水平位置(日付)',
            options = list_horizontality,
            index = 1,
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('垂直位置')
        cell_vertical = st.selectbox(
            label = '垂直位置(日付)',
            options = list_vertical,
            index = 0,
            label_visibility = 'collapsed',
        )

# 祝日の設定
with st.sidebar.expander('祝日の設定', False):
    holiday_visibility = st.checkbox(
        label = '祝日名を表示',
        value = True,
    )
    st.caption('フォント名')
    holiday_font_family = st.selectbox(
        label = 'フォント名(祝日)',
        options = list_font_family,
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォントスタイル')
    holiday_font_style = st.selectbox(
        label = 'フォントスタイル(祝日)',
        options = dict_font_family[holiday_font_family].keys(),
        index = 0,
        label_visibility = 'collapsed',
    )
    st.caption('フォントサイズ')
    holiday_font_size = st.slider(
        label = 'フォントサイズ(祝日)',
        min_value = 5,
        max_value = 30,
        value = 10,
        label_visibility = 'collapsed',
    )
    col1, col2 = st.columns(2)
    with col1:
        st.caption('水平位置')
        holiday_horizontality = st.selectbox(
            label = '水平位置(祝日)',
            options = list_horizontality,
            index = 1,
            label_visibility = 'collapsed',
        )
    with col2:
        st.caption('垂直位置')
        holiday_vertical = st.selectbox(
            label = '垂直位置(祝日)',
            options = list_vertical,
            index = 2,
            label_visibility = 'collapsed',
        )

# 罫線の設定
with st.sidebar.expander('罫線の設定', False):

    # 外側
    border_outer_visible = st.checkbox(
        label = '外側罫線あり',
        value = True,
    )
    if border_outer_visible:

        st.caption('種類')
        border_outer_type = st.selectbox(
            label = '外側(線の種類)',
            options = list_border_type,
            index = 0,
            label_visibility = 'collapsed',
        )
        st.caption('太さ')
        border_outer_width = st.slider(
            label = '外側(太さ)',
            min_value = 1,
            max_value = 5,
            value = 1,
            label_visibility = 'collapsed',
        )
        st.caption('色')
        border_outer_color_html = st.color_picker(
            label = '外側(色)',
            value = '#000000',
            label_visibility = 'collapsed',
        )
    else:
        border_outer_width = 0

    # 内側
    border_inner_visible = st.checkbox(
        label = '内側罫線あり',
        value = True,
    )
    if border_inner_visible:

        st.caption('種類')
        border_inner_type = st.selectbox(
            label = '内側(線の種類)',
            options = list_border_type,
            index = 0,
            label_visibility = 'collapsed',
        )
        st.caption('太さ')
        border_inner_width = st.slider(
            label = '内側(太さ)',
            min_value = 1,
            max_value = 5,
            value = 1,
            label_visibility = 'collapsed',
        )

        st.caption('色')
        border_inner_color_html = st.color_picker(
            label = '内側(色)',
            value = '#000000',
            label_visibility = 'collapsed',
        )
    else:
        border_inner_width = 0

# ----------------------------------------------------------------
# 関数
# ----------------------------------------------------------------
# ベースとなる日付のリストを作る
def create_list_date():
    list_date = []
    for m in range(1, 13):
        day1 = dt.date(year,m,1)
        for d in range(0,32):
            date = day1 + dt.timedelta(days = d)
            if day1.month == date.month:
                list_date.append(date)
    return list_date

# 年間カレンダー(表)の日付のリストを作る
def create_list_date_yearly_table():

    # 週初めの設定
    if weekday_start == weekday_start_options[0]:
        weekday_no = [6, 0, 1, 2, 3, 4, 5]
    elif weekday_start == weekday_start_options[1]:
        weekday_no = [0, 1, 2, 3, 4, 5, 6]

    # リストの作成
    list_date_format = []
    for date in list_date:
        if date.day == 1:
            list_date_format.append([])
            list_1week = ['x'] * 7
        if date.weekday() == weekday_no[0]:
            list_1week = ['x'] * 7
        list_1week[weekday_no.index(date.weekday())] = date
        next_date = date + dt.timedelta(days=1)
        if next_date.month != date.month or date.weekday() == weekday_no[6]:
            list_date_format[date.month-1].append(list_1week)
    return list_date_format, weekday_no

# カレンダー画像作成
def create_image_calendar():
    image = []

    # 月
    for month in range(len(list_date_format)):

        # 幅
        calendar_width = cell_width * 7
        calendar_width += border_outer_width * 2
        calendar_width += border_inner_width * 6

        # 高さ
        calendar_height = cell_height * len(list_date_format[month]) + hedder_height
        calendar_height += title_height
        calendar_height += border_outer_width * 2
        calendar_height += border_inner_width *len(list_date_format[month])

        # キャンバス作成
        calendar_image = Image.new('RGB', (calendar_width, calendar_height), 'White')

        # タイトル作成
        font_path = './font/' + dict_font_family[title_font_family][title_font_style]
        font_size = title_font_size
        font = ImageFont.truetype(font_path, font_size)

        title_image = Image.new(
            mode = 'RGB',
            size = (calendar_width, title_height),
            color = get_color_rgb(title_background_color_html)
        )
        draw = ImageDraw.Draw(title_image)
        title = list_title[month][title_format]
        x1, y1, x2, y2 = draw.textbbox((0, 0), title, font = font)

        position_left, position_top = get_title_position(x2, y2, calendar_width, calendar_height)
        draw.text(
            xy = (position_left, position_top),
            text = title,
            font = font,
            fill = get_color_rgb(title_font_color_html)
        )
        calendar_image.paste(
            im = title_image,
            box = (0, 0
                # cell_width * i + border_outer_width + border_inner_width * i,
                # border_outer_width
            )
        )

        # 曜日
        font_path = './font/' + dict_font_family[hedder_font_family][hedder_font_style]
        font_size = hedder_font_size
        font = ImageFont.truetype(font_path, font_size)

        for i in range(7):

            # 色を取得
            if weekday_no[i] == 5:
                background_color = hedder_background_color_html_saturday
                font_color = hedder_font_color_html_saturday
            elif weekday_no[i] == 6:
                background_color = hedder_background_color_html_sunday
                font_color = hedder_font_color_html_sunday
            else:
                background_color = hedder_background_color_html_normal
                font_color = hedder_font_color_html_normal

            # 曜日ヘッダー
            hedder_image = Image.new(
                mode = 'RGB',
                size = (cell_width, hedder_height),
                color = get_color_rgb(background_color)
            )
            draw = ImageDraw.Draw(hedder_image)
            weekday = dict_weekday_name[weekday_name][i]
            x1, y1, x2, y2 = draw.textbbox((0, 0), weekday, font = font)
            position_left, position_top = get_hedder_position(x2, y2)
            draw.text(
                xy = (position_left, position_top),
                text = weekday,
                font = font,
                fill = get_color_rgb(font_color)
            )
            calendar_image.paste(
                im = hedder_image,
                box = (
                    cell_width * i + border_outer_width + border_inner_width * i,
                    title_height + border_outer_width
                )
            )

        # 週
        for week in range(len(list_date_format[month])):

            # 日
            for day in range(len(list_date_format[month][week])):

                # 日付を取得
                date = list_date_format[month][week][day]

                if date == 'x':
                    date = ''
                    background_color = cell_background_color_html_empty
                    date_day = ''
                    holiday_name = ''
                else:
                    # 色を取得
                    if jpholiday.is_holiday(date) == True:
                        background_color = cell_background_color_html_sunday
                        font_color = cell_font_color_html_sunday
                        if holiday_visibility == True:
                            holiday_name = jpholiday.is_holiday_name(date)
                    elif weekday_no[day] == 5:
                        background_color = cell_background_color_html_saturday
                        font_color = cell_font_color_html_saturday
                        holiday_name = ''
                    elif weekday_no[day] == 6 or jpholiday.is_holiday(date) == True:
                        background_color = cell_background_color_html_sunday
                        font_color = cell_font_color_html_sunday
                        holiday_name = ''
                    else:
                        background_color = cell_background_color_html_normal
                        font_color = cell_font_color_html_normal
                        holiday_name = ''
                    date_day = date.day

                # 日付セル作成
                cell_image = Image.new(
                    mode = 'RGB',
                    size = (cell_width, cell_height),
                    color = get_color_rgb(background_color)
                )
                draw = ImageDraw.Draw(cell_image)

                # 日付のフォント指定
                font_path = './font/' + dict_font_family[cell_font_family][cell_font_style]
                font_size = cell_font_size
                cell_font = ImageFont.truetype(font_path, font_size)
                # 日付描画
                x1, y1, x2, y2 = draw.textbbox((0, 0), str(date_day), font = cell_font)
                position_left, position_top = get_cell_position(x2, y2)
                draw.text(
                    xy = (position_left, position_top),
                    text = str(date_day),
                    font = cell_font,
                    fill = get_color_rgb(font_color)
                )
                if holiday_visibility == True:
                    # 祝日のフォント指定
                    font_path = './font/' + dict_font_family[holiday_font_family][holiday_font_style]
                    font_size = holiday_font_size
                    holiday_font = ImageFont.truetype(font_path, font_size)

                    # 祝日描画
                    x1, y1, x2, y2 = draw.textbbox((0, 0), holiday_name, font = holiday_font)
                    position_left, position_top = get_holiday_position(x2, y2)
                    draw.text(
                        xy = (position_left, position_top),
                        text = str(holiday_name),
                        font = holiday_font,
                        fill = get_color_rgb(font_color)
                    )
                calendar_image.paste(
                    im = cell_image,
                    box = (
                        cell_width * day + border_outer_width + border_inner_width * day,
                        title_height + hedder_height + cell_height * week + border_outer_width + border_inner_width * (week+1)
                    )
                )
        create_border(
            draw = ImageDraw.Draw(calendar_image),
            width = calendar_width, height = calendar_height,
            week = len(list_date_format[month]),
        )

        image.append(calendar_image)

    return image

# テキストポジション
def get_cell_position(w, h):
    # 水平
    if cell_horizontality == list_horizontality[0]:
        position_left = 3
    elif cell_horizontality == list_horizontality[1]:
        position_left = (cell_width - w) / 2
    elif cell_horizontality == list_horizontality[2]:
        position_left = cell_width - w -3
    # 垂直
    if cell_vertical == list_vertical[0]:
        position_top = 3
    elif cell_vertical == list_vertical[1]:
        position_top = (cell_height - h) / 2
    elif cell_vertical == list_vertical[2]:
        position_top = cell_height - h -3

    return position_left, position_top

def get_hedder_position(w, h):
    # 水平
    if hedder_horizontality == list_horizontality[0]:
        position_left = 3
    elif hedder_horizontality == list_horizontality[1]:
        position_left = (cell_width - w) / 2
    elif hedder_horizontality == list_horizontality[2]:
        position_left = cell_width - w -3
    # 垂直
    if hedder_vertical == list_vertical[0]:
        position_top = 3
    elif hedder_vertical == list_vertical[1]:
        position_top = (hedder_height - h) / 2
    elif hedder_vertical == list_vertical[2]:
        position_top = hedder_height - h -3

    return position_left, position_top

def get_title_position(w, h, calendar_w, calendar_h):
    # 水平
    if title_horizontality == list_horizontality[0]:
        position_left = 3
    elif title_horizontality == list_horizontality[1]:
        position_left = (calendar_w - w) / 2
    elif title_horizontality == list_horizontality[2]:
        position_left = calendar_w - w -3
    # 垂直
    if title_vertical == list_vertical[0]:
        position_top = 3
    elif title_vertical == list_vertical[1]:
        position_top = (title_height - h) / 2
    elif title_vertical == list_vertical[2]:
        position_top = title_height - h -3

    return position_left, position_top

def get_holiday_position(w, h):
    # 水平
    if holiday_horizontality == list_horizontality[0]:
        position_left = 3
    elif holiday_horizontality == list_horizontality[1]:
        position_left = (cell_width - w) / 2
    elif holiday_horizontality == list_horizontality[2]:
        position_left = cell_width - w -3
    # 垂直
    if holiday_vertical == list_vertical[0]:
        position_top = 3
    elif holiday_vertical == list_vertical[1]:
        position_top = (cell_height - h) / 2
    elif holiday_vertical == list_vertical[2]:
        position_top = cell_height - h -3

    return position_left, position_top

# ボーダー作成
def create_border(draw, width, height, week):

    # 外側罫線
    if border_outer_visible == True:

        border_outer_color_rgb = get_color_rgb(border_outer_color_html)
        for x in range(border_outer_width):
            start = [0 for x in range(3)]
            end = [0 for x in range(3)]

            # ボーダー頂点を取得
            up_border = [(0, title_height + x), (width, title_height + x)]
            down_border = [(0, height - x - 1), (width, height - x - 1)]
            left_border = [(x, title_height), (x, title_height + height)]
            right_border = [(width - x - 1, title_height), (width - x - 1, title_height + height)]
            border_position = [up_border, down_border, left_border, right_border]

            for position in border_position:
                # 実線
                if border_outer_type == list_border_type[0]:
                    draw.line(position, fill = border_outer_color_rgb, width = 1)
                # 点線
                if border_outer_type == list_border_type[1]:
                    for y in range(500):
                        # ヨコ
                        if position[0][1] == position[1][1]:
                            start[0] = position[0][0] + border_outer_width * 3 * y
                            end[0] = start[0] + border_outer_width
                            draw.line(
                                [(start[0], position[0][1]),(end[0], position[1][1])],
                                fill = border_outer_color_rgb,
                                width = 1,
                            )
                            if end[0] > width:
                                break
                        # タテ
                        else:
                            start[0] = position[0][1] + border_outer_width * 3 * y
                            end[0] = start[0] + border_outer_width
                            draw.line(
                                [(position[0][0], start[0]),(position[1][0], end[0])],
                                fill = border_outer_color_rgb,
                                width = 1,
                            )
                            if end[0] > height:
                                break
                # 破線
                if border_outer_type == list_border_type[2]:
                    for y in range(500):
                        # ヨコ
                        if position[0][1] == position[1][1]:
                            start[0] = position[0][0] + border_outer_width * 4 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            draw.line(
                                [(start[0], position[0][1]),(end[0], position[1][1])],
                                fill = border_outer_color_rgb,
                                width = 1,
                            )
                            if end[0] > width:
                                break
                        # タテ
                        else:
                            start[0] = position[0][1] + border_outer_width * 4 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            draw.line(
                                [(position[0][0], start[0]),(position[1][0], end[0])],
                                fill = border_outer_color_rgb,
                                width = 1,
                            )
                            if end[0] > height:
                                break
                # 一点破線
                if border_outer_type == list_border_type[3]:
                    for y in range(500):
                        # ヨコ
                        if position[0][1] == position[1][1]:
                            start[0] = position[0][0] + border_outer_width * 7 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            start[1] = end[0] + border_outer_width * 2
                            end[1] = start[1] + border_outer_width
                            for i in range(2):
                                draw.line(
                                    [(start[i], position[0][1]),(end[i], position[1][1])],
                                    fill = border_outer_color_rgb,
                                    width = 1,
                                )
                            if end[1] > width:
                                break
                        # タテ
                        else:
                            start[0] = position[0][1] + border_outer_width * 7 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            start[1] = end[0] + border_outer_width * 2
                            end[1] = start[1] + border_outer_width
                            for i in range(2):
                                draw.line(
                                    [(position[0][0], start[i]),(position[1][0], end[i])],
                                    fill = border_outer_color_rgb,
                                    width = 1,
                                )
                            if end[1] > height:
                                break
                # 二点破線
                if border_outer_type == list_border_type[4]:
                    for y in range(500):
                        # ヨコ
                        if position[0][1] == position[1][1]:
                            start[0] = position[0][0] + border_outer_width * 10 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            start[1] = end[0] + border_outer_width * 2
                            end[1] = start[1] + border_outer_width
                            start[2] = end[1] + border_outer_width * 2
                            end[2] = start[2] + border_outer_width
                            for i in range(3):
                                draw.line(
                                    [(start[i], position[0][1]),(end[i], position[1][1])],
                                    fill = border_outer_color_rgb,
                                    width = 1,
                                )
                            if end[2] > width:
                                break
                        # タテ
                        else:
                            start[0] = position[0][1] + border_outer_width * 10 * y
                            end[0] = start[0] + border_outer_width * 2.5
                            start[1] = end[0] + border_outer_width * 2
                            end[1] = start[1] + border_outer_width
                            start[2] = end[1] + border_outer_width * 2
                            end[2] = start[2] + border_outer_width
                            for i in range(3):
                                draw.line(
                                    [(position[0][0], start[i]),(position[1][0], end[i])],
                                    fill = border_outer_color_rgb,
                                    width = 1,
                                )
                            if end[2] > height:
                                break

    # 内側罫線
    if border_inner_visible == True:
        border_inner_color_rgb = get_color_rgb(border_inner_color_html)

        # 内側罫線ヨコ
        for x in range(week):
            position = title_height + border_outer_width + hedder_height
            position += (border_inner_width + cell_height) * x

            for y in range(border_inner_width):
                position += 1
                start = [0 for x in range(3)]
                end = [0 for x in range(3)]
                # 実線
                if border_inner_type == list_border_type[0]:
                    draw.line(
                        [(0, position), (width, position)],
                        fill = border_inner_color_rgb,
                        width = 1
                    )
                # 点線
                if border_inner_type == list_border_type[1]:
                    for z in range(500):
                        start[0] = border_inner_width * 3 * z
                        end[0] = start[0] + border_inner_width
                        draw.line(
                            [(start[0], position),(end[0], position)],
                            fill = border_inner_color_rgb,
                            width = 1,
                        )
                        if end[0] > width:
                            break
                # 破線
                if border_inner_type == list_border_type[2]:
                    for z in range(500):
                        start[0] = border_inner_width * 4 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        draw.line(
                            [(start[0], position),(end[0], position)],
                            fill = border_inner_color_rgb,
                            width = 1,
                        )
                        if end[0] > width:
                            break
                # 一点破線
                if border_inner_type == list_border_type[3]:
                    for z in range(500):
                        start[0] = border_inner_width * 7 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        start[1] = end[0] + border_inner_width * 2
                        end[1] = start[1] + border_inner_width
                        for i in range(2):
                            draw.line(
                                [(start[i], position),(end[i], position)],
                                fill = border_inner_color_rgb,
                                width = 1,
                            )
                        if end[1] > width:
                            break
                # 二点破線
                if border_inner_type == list_border_type[4]:
                    for z in range(500):
                        start[0] = border_inner_width * 10 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        start[1] = end[0] + border_inner_width * 2
                        end[1] = start[1] + border_inner_width
                        start[2] = end[1] + border_inner_width * 2
                        end[2] = start[2] + border_inner_width
                        for i in range(3):
                            draw.line(
                                [(start[i], position),(end[i], position)],
                                fill = border_inner_color_rgb,
                                width = 1,
                            )
                        if end[2] > width:
                            break

        # 内側罫線タテ
        for x in range(1, 7):
            position = border_outer_width
            position += (cell_width * x) + (border_inner_width * (x -1))

            for y in range(border_inner_width):
                position += 1
                start = [0 for x in range(3)]
                end = [0 for x in range(3)]
                # 実線
                if border_inner_type == list_border_type[0]:
                    draw.line(
                        [(position, title_height), (position, title_height + height)],
                        fill = border_inner_color_rgb,
                        width = 1
                    )
                # 点線
                if border_inner_type == list_border_type[1]:
                    for z in range(500):
                        start[0] = title_height + border_inner_width * 3 * z
                        end[0] = start[0] + border_inner_width
                        draw.line(
                            [(position, start[0]),(position, end[0])],
                            fill = border_inner_color_rgb,
                            width = 1,
                        )
                        if end[0] > height:
                            break
                # 破線
                if border_inner_type == list_border_type[2]:
                    for z in range(500):
                        start[0] = title_height + border_inner_width * 4 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        draw.line(
                            [(position, start[0]),(position, end[0])],
                            fill = border_inner_color_rgb,
                            width = 1,
                        )
                        if end[0] > height:
                            break
                # 一点破線
                if border_inner_type == list_border_type[3]:
                    for z in range(500):
                        start[0] = title_height + border_inner_width * 7 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        start[1] = end[0] + border_inner_width * 2
                        end[1] = start[1] + border_inner_width
                        for i in range(2):
                            draw.line(
                                [(position, start[i]),(position, end[i])],
                                fill = border_inner_color_rgb,
                                width = 1,
                            )
                        if end[1] > height:
                            break
                # 二点破線
                if border_inner_type == list_border_type[4]:
                    for z in range(500):
                        start[0] = title_height + border_inner_width * 10 * z
                        end[0] = start[0] + border_inner_width * 2.5
                        start[1] = end[0] + border_inner_width * 2
                        end[1] = start[1] + border_inner_width
                        start[2] = end[1] + border_inner_width * 2
                        end[2] = start[2] + border_inner_width
                        for i in range(3):
                            draw.line(
                                [(position, start[i]),(position, end[i])],
                                fill = border_inner_color_rgb,
                                width = 1,
                            )
                        if end[2] > height:
                            break

# RGBカラーコード取得
def get_color_rgb(color_html):
    color_rgb = (
        int(color_html[1:3], 16),
        int(color_html[3:5],16),
        int(color_html[5:7],16)
    )
    return color_rgb

# ランダム文字列取得
def get_random_string(n):
    result = ''.join(random.choices(string.ascii_letters + string.digits, k = n))
    return result

# zipフォルダをチェック
def check_zip_dir(path):
    dic_dir = {}
    for i in os.listdir(path):
        if os.path.isdir(path + i):
            dic_dir[i] = dt.datetime.fromtimestamp(os.path.getmtime(path + i))

    sort_dic_dir = sorted(dic_dir.items(), key=lambda x: x[1])

    for i in sort_dic_dir:
        if len(sort_dic_dir) < 10:
            break
        shutil.rmtree(path + i[0])
        sort_dic_dir.remove(i)

# ----------------------------------------------------------------
# メイン処理
# ----------------------------------------------------------------
st.title('年間カレンダー作成ツール')
st.caption('1月〜12月のミニカレンダーを作成するツールです。左のサイドバーから設定を変更して自分好みのカレンダーを作成してください:smile:')
with st.expander('作成した画像の利用について', False):
    st.write("""
        <p>当サイトで作成した画像は、個人・法人・商用・非商用を問わず、無料でダウンロードしてご利用いただけます。</p>
        <p>ただし、以下に該当する場合はご利用をお断りしております。</p>
        <ol>
        <li>公序良俗に反する目的での利用</li>
        <li>攻撃的・差別的・性的・過激な利用</li>
        <li>反社会的勢力や違法行為に関わる利用</li>
        <li>画像自体をコンテンツ・商品として再配布・販売</li>
        <li>その他著作者が不適切と判断した場合</li>
        </ol>
        <br>
        <b>個人利用・非商用の場合</b>
        <p>事前連絡、クレジット表記は不要です。</p>
        <br>
        <b>法人利用・商用の場合</b>
        <p><a href="https://y-tool.site/contact-bbs/" target="_blank">連絡掲示板</a>に投稿をした上で、利用したものに当サイトへのクレジット表記をお願いします。</p>
        <p>クレジット表記例：Y-TOOL(https://y-tool.site/)</p>
        <br>
        <b>二次配布について</b>
        <p>当サイトで作成した画像を第三者へ配布する場合は、<a href="https://y-tool.site/contact-bbs/" target="_blank">連絡掲示板</a>に投稿をお願いします。</p>
    """, unsafe_allow_html=True)
with st.expander('フォントについて'):
    st.write("""
    当サイトでは<a href="https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&item_id=OFL" target="_blank">SIL Open Font License</a>のフォントを使用しています。

    フォント追加は<a href="https://y-tool.site/request-bbs/" target="_blank">要望掲示板</a>からご依頼ください。
    <ul>
    <li>M PLUS 1p 提供：<a href="https://mplusfonts.github.io" target="_blank">M+ FONT様</a></li>
    <li>たぬゴ角 提供：<a href="https://tanukifont.com/tanugo/" target="_blank">たぬきフォント様</a></li>
    <li>たぬゴ丸 提供：<a href="https://tanukifont.com/tanugo/" target="_blank">たぬきフォント様</a></li>
    <li>自由の翼フォント 提供：<a href="https://tanukifont.com/jiyu-no-tsubasa/" target="_blank">たぬきフォント様</a></li>
    <li>源真ゴシック 提供：<a href="http://jikasei.me/font/genshin/" target="_blank">自家製フォント工房様</a></li>
    <li>源柔ゴシック 提供：<a href="http://jikasei.me/font/genjyuu/" target="_blank">自家製フォント工房様</a></li>
    <li>せのびゴシック 提供：<a href="http://modi.jpn.org/" target="_blank">MODI工場ホームページ様</a></li>
    <li>ランパート 提供：<a href="https://github.com/fontworks-fonts/Rampart" target="_blank">Fontworks様</a></li>
    <li>トレイン 提供：<a href="https://github.com/fontworks-fonts/Train" target="_blank">Fontworks様</a></li>
    <li>しっぽり明朝 提供：<a href="https://fontdasu.com/shippori-mincho/" target="_blank">FONTDASU様</a></li>
    </ul>

    """, unsafe_allow_html=True)

with st.expander('当サイトについて'):
    st.write("""
    <ul>
    <li>サイト名：Y-TOOL</li>
    <li>URL：<a href="https://y-tool.site" target="_blank">https://y-tool.site</a></li>
    <li>フォーラム：<a href="https://y-tool.site/contact-bbs/" target="_blank">連絡掲示板</a>、<a href="https://y-tool.site/request-bbs/" target="_blank">要望掲示板</a></li>
    </ul>
    Y-TOOL
    """, unsafe_allow_html=True)

list_date = create_list_date()
list_date_format, weekday_no = create_list_date_yearly_table()
list_image = create_image_calendar()

check_zip_dir('./zip/')

zip_path = './zip/' + dt.datetime.now().strftime('%Y%m%d_%H%M%S%f')+ '_' + get_random_string(10)
zip_name = 'YealyCalendar' + str(year) + '.zip'
os.mkdir(zip_path)
zip_file = zipfile.ZipFile(zip_path + '/' + zip_name, 'w', zipfile.ZIP_STORED)

for month in range(len(list_image)):
    img = list_image[month]
    img_file = './img/YealyCalendar' + str(year) + str(month+1).zfill(2) + '.png'
    img.save(img_file)
    zip_file.write(img_file)
    os.remove(img_file)

with open(zip_path + '/' + zip_name,'rb') as fp:
    st.download_button('Download zip', fp, zip_name,'application/zip')

for month in range(len(list_image)):
    img = list_image[month]
    st.image(img)
