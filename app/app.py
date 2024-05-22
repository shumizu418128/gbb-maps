from collections import defaultdict

import folium
from flask import Flask, render_template

# DBの内容を変更する場合には以下のimportも必要
# from models.database import db_session
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

        popup = folium.Popup(popup_content, max_width=1000)

        flag_icon = folium.CustomIcon(
            icon_image=r"./models/flags/" + country_name + ".png",  # アイコン画像のパス
            icon_size=(45, 45),  # アイコンのサイズ（幅、高さ）
        )
        # マーカーを追加
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=flag_icon
        ).add_to(m)

    m.save(r'app/templates/index.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
