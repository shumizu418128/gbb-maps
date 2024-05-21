import os

import folium
import sqlalchemy
from flask import Flask, render_template

app = Flask(__name__)

databese_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'participants.db'
)
engine = sqlalchemy.create_engine(
    'sqlite:///' + databese_file
)


def load_participants():
    with engine.connect() as conn:
        cursor = conn.execute(sqlalchemy.text('SELECT * FROM participants'))
        query = """
        SELECT p.name, p.category, p.iso_code, c.country, c.country_ja, c.lat, c.lon, p.team
        FROM participants p
        JOIN countries c ON p.iso_code = c.iso_code
        """
        participants = cursor.execute(query).fetchall()
    return participants

    return [
        {
            "name": row[0],
            "country": row[1],
            "lat": row[2],
            "lon": row[3],
            "team": row[4] if row[6] == 'team' else None,
            "department": row[5],
            "team_type": row[6]
        }
        for row in participants
    ]


# @app.route('/')
def map():
    participants = load_participants()
    print(participants)
    exit()

    # 地図の中心座標
    map_center = [20, 0]
    m = folium.Map(location=map_center, zoom_start=2)

    # 出場者データを地図に追加
    for participant in participants:
        popup_text = f'{participant["name"]}'
        if participant["team_type"] == "team":
            popup_text += f', Team: {participant["team"]}'

        folium.Marker(
            location=[participant["lat"], participant["lon"]],
            popup=popup_text,
        ).add_to(m)

    # 地図をHTMLとして保存
    m.save('map.html')

    return render_template('map.html')


map()

# if __name__ == '__main__':
#    app.run(debug=True)
