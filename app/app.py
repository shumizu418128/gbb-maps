from collections import defaultdict

import folium
from flask import Flask, render_template

# DBの内容を変更する場合には以下のimportも必要
from models.database import db_session
from models.models import Country, Participant

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    participants = Participant.query.all()

    # 地図の中心座標
    map_center = [20, 0]
    m = folium.Map(location=map_center, zoom_start=3)

    # 座標ごとに参加者をグループ化
    coord_participants = defaultdict(list)
    for participant in participants:
        country = Country.query.filter_by(
            iso_code=participant.iso_code).first()
        coord_participants[(country.lat, country.lon)].append(participant)

    # 丸画像になっている国のリスト
    country_exception = [
        "Taiwan",
        "Hong Kong",
        "Saudi Arabia",
        "Iran"
    ]

    # グループ化した参加者ごとにマーカーを追加
    for (lat, lon), participants in coord_participants.items():
        # lat, lon = 緯度, 経度
        # participants = 同じ国同士の参加者リスト

        # まずは国コードを取得
        iso_code = participants[0].iso_code

        # 国の名前を取得
        country_name = Country.query.filter_by(iso_code=iso_code).first().name
        country_name_ja = Country.query.filter_by(
            iso_code=iso_code).first().name_ja

        # ポップアップの内容を作成
        popup_content = '<div style="font-family: Noto sans JP; font-size: 14px;">'
        popup_content += f'<h3 style="margin: 0; color: #F0632F;">{country_name}</h3>'
        popup_content += f'<h4 style="margin: 0; color: #F0632F;">{country_name_ja}</h4>'
        for participant in participants:
            if participant.members:
                popup_content += f'''
                <p style="margin: 5px 0;">
                    <strong style="color: #000000">{participant.name}</strong> ({participant.category})<span style="font-size: 0.7em; color=#222222"><br>【{participant.members}】</span>
                </p>
                '''
            else:
                popup_content += f'''
                <p style="margin: 5px 0;">
                    <strong style="color: #000000">{participant.name}</strong> ({participant.category})
                </p>
                '''
        popup_content += '</div>'

        # 画像に合わせてアイコンのサイズを変更
        # アイコン素材がある国の場合
        if country_name not in country_exception:
            icon_size = (56, 42)
            icon_anchor = (0, 40)

        # アイコン素材がない国の場合
        else:
            icon_size = (56, 38)
            icon_anchor = (28, 5)
            popup_content += '<br><p style="margin: 5px 0;">※国旗素材の都合で、<br>他国とは違う画像です</p>'

        popup = folium.Popup(popup_content, max_width=1000)

        flag_icon = folium.CustomIcon(
            icon_image=r"./models/flags/" + country_name + ".webp",  # アイコン画像のパス
            icon_size=icon_size,  # アイコンのサイズ（幅、高さ）
            icon_anchor=icon_anchor  # アイコンのアンカー位置
        )
        # マーカーを追加
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=flag_icon
        ).add_to(m)

    # add()
    m.save(r'app/templates/index.html')

    return render_template('index.html')


@app.route("/bcj")
def bcj():
    # 日本の中心付近
    map_center = [36.2048, 138.2529]
    m = folium.Map(location=map_center, zoom_start=5)
    locations = [
        {"name": "北海道予選", "venue": "UTAGE SAPPORO", "lat": 43.05431210452901, "lon": 141.35382666830552, "date": "6/8"},
        {"name": "福岡予選", "venue": "Ibiza FUKUOKA", "lat": 33.58842834514552, "lon": 130.39590583064594, "date": "6/22"},
        {"name": "沖縄予選", "venue": "epica okinawa", "lat": 26.218312463216623, "lon": 127.68008386065539, "date": "7/7"},
        {"name": "仙台予選", "venue": "ART NIGHT CLUB", "lat": 38.262858617931016, "lon": 140.86970762308982, "date": "7/21"},
        {"name": "名古屋予選", "venue": "UTAGE NAGOYA", "lat": 35.17214947255007, "lon": 136.90761709635382, "date": "8/3"},
        {"name": "大阪予選", "venue": "GHOST Osaka", "lat": 34.670944669892705, "lon": 135.49749186698628, "date": "8/11"},
        {"name": "東京予選", "venue": "BAIA", "lat": 35.661638682891684, "lon": 139.69907479648504, "date": "8/18"},
        {"name": "BEATCITY JAPAN 本戦", "venue": "EX THEATER ROPPONGI", "lat": 35.66126439102072, "lon": 139.72729714238233, "date": "9/7"},
        {"name": "GBB 2024", "venue": "Toyosu PIT", "lat": 35.64960390462384, "lon": 139.78837687277277, "date": "11/1-3"},
    ]
    # グループ化した参加者ごとにマーカーを追加
    for location in locations:

        # ポップアップの内容を作成
        popup_content = '<div style="font-family: Noto sans JP; font-size: 14px;">'
        popup_content += f'<h3 style="margin: 0; color: #F0632F;">{location["name"]}</h3>'
        popup_content += f'<h4 style="margin: 0; color: #F0632F;">{location["venue"]}</h4>'

        popup_content += f'<p style="margin: 5px 0;">{location["date"]}</p><div>'

        popup = folium.Popup(popup_content, max_width=1000)

        # マーカーを追加
        if location["name"] == "BEATCITY JAPAN 本戦":
            folium.Marker(
                location=[location["lat"], location["lon"]],
                popup=popup,
                icon=folium.Icon(color='black', icon='flag')
            ).add_to(m)

        elif location["name"] == "GBB 2024":
            folium.Marker(
                location=[location["lat"], location["lon"]],
                popup=popup,
                icon=folium.Icon(color='orange', icon='flag')
            ).add_to(m)

        else:
            folium.Marker(
                location=[location["lat"], location["lon"]],
                popup=popup,
                icon=folium.Icon(color='white', icon='flag', icon_color='black')
            ).add_to(m)

    m.save(r'app/templates/bcj.html')

    return render_template('bcj.html')


# 国コードの一覧
# https://freefielder.jp/country_code/

# flask チュートリアル
# https://qiita.com/usaitoen/items/f8aa0bf68007e18d6882


def add():
    italy = Country(
        name="Italy",
        name_ja="イタリア",
        lat=41.8719,
        lon=12.5674,
        iso_code=380
    )
    participant = Participant(
        name="BLACKROLL",
        category="Solo",
        iso_code=380,
        members=""
    )
    db_session.add(italy)
    db_session.add(participant)
    db_session.commit()


if __name__ == "__main__":
    app.run(debug=True)
