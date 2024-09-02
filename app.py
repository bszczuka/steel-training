import math

from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

# Original values dictionary
VALUES = {
    "five_to_go": {
        "t1": {"len_a": 3100, "len_h": 9100, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 1000, "len_h": 11000, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 1000, "len_h": 13700, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t4": {"len_a": 3100, "len_h": 16500, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 5200, "len_h": 6400, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
    },
    "showdown_left": {
        "t1": {"len_a": 1800, "len_h": 22900, 'width': 400, 'height': 600, 'elevation': 200, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 200, "len_h": 9000, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t3": {"len_a": 1000, "len_h": 11000, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
        "t4": {"len_a": 3800, "len_h": 22900, 'width': 400, 'height': 600, 'elevation': 200, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 2200, "len_h": 9000, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
    },
    "showdown_right": {
        "t1": {"len_a": 2200, "len_h": 9000, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 3800, "len_h": 22900, 'width': 400, 'height': 600, 'elevation': 200, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 1000, "len_h": 11000, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'left'},
        "t4": {"len_a": 200, "len_h": 9000, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t5": {"len_a": 1800, "len_h": 22900, 'width': 400, 'height': 600, 'elevation': 200, 'stop_plate': False,
               'side': 'right'},

    },
    "smoke_and_hope": {
        "t1": {"len_a": 4300, "len_h": 6400, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 2700, "len_h": 8200, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 0, "len_h": 12800, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
        "t4": {"len_a": 2700, "len_h": 8200, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 4300, "len_h": 6400, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'right'},

    },
    "accelerator": {
        "t1": {"len_a": 3600, "len_h": 9100, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 1200, "len_h": 9100, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 0, "len_h": 13700, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
        "t4": {"len_a": 1900, "len_h": 18300, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 6200, "len_h": 18300, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': False,
               'side': 'right'},

    },
    "pendulum": {
        "t1": {"len_a": 3800, "len_h": 16500, 'width': 300, 'height': 300, 'elevation': 400, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 1900, "len_h": 16500, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 0, "len_h": 9100, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
        "t4": {"len_a": 1900, "len_h": 16500, 'width': 250, 'height': 250, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 3800, "len_h": 16500, 'width': 300, 'height': 300, 'elevation': 400, 'stop_plate': False,
               'side': 'right'},

    },
    "speed_option": {
        "t1": {"len_a": 3700, "len_h": 9100, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 6600, "len_h": 32000, 'width': 400, 'height': 600, 'elevation': 150, 'stop_plate': True,
               'side': 'left'},
        "t3": {"len_a": 1800, "len_h": 18300, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t4": {"len_a": 2000, "len_h": 7300, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 6400, "len_h": 13700, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
    },
    "roundabout": {
        "t1": {"len_a": 2700, "len_h": 13700, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t2": {"len_a": 600, "len_h": 6400, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'left'},
        "t3": {"len_a": 600, "len_h": 9100, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': True,
               'side': 'right'},
        "t4": {"len_a": 2500, "len_h": 13700, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
        "t5": {"len_a": 2500, "len_h": 6400, 'width': 300, 'height': 300, 'elevation': 0, 'stop_plate': False,
               'side': 'right'},
    }
}


def _target_info(distance, stage, size, target):
    values = VALUES[stage][target]

    a_len, h_len = values["len_a"], values["len_h"]
    org_width, org_height, org_elevation = values['width'], values['height'], values['elevation']
    x_len = math.sqrt(a_len ** 2 + h_len ** 2)

    scale = distance / h_len
    target_scale = distance / x_len

    sim_a_len = a_len * scale

    width, height, elevation = org_width * target_scale, org_height * target_scale, org_elevation * target_scale
    post_width = 40 * target_scale
    post_height = 150 if size == 'a3' else 100
    if distance < 1000:
        post_height = 15
    if target == 't1':
        position = 0
    else:
        first_target = _target_info(distance, stage, size, 't1')
        if values['side'] == 'left':
            position = first_target['sim_a_len'] - sim_a_len
        else:
            position = first_target['sim_a_len'] + sim_a_len

    return {
        'distance': distance,
        'stage': stage,
        'target': target,
        'width': width,
        'height': height,
        'elevation': elevation,
        'sim_a_len': sim_a_len,
        'stop_plate': values['stop_plate'],
        'post_height': post_height + elevation,
        'post_width': post_width,
        'side': values['side'],
        'position': int(position),
    }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    distance = int(request.form.get('distance', 0))
    distance_in_mm = distance * 10
    stage = request.form.get('stage')
    size = request.form.get('size')

    targets = [f't{i}' for i in range(1, 6)]
    target_info = [_target_info(distance_in_mm, stage, size, target) for target in targets]
    wall_extra_space_for_paper = 297 if size == 'a3' else 210
    wall_length = target_info[-1]['position'] + wall_extra_space_for_paper
    preview_size = 267 if size == 'a3' else 190
    preview_scale = preview_size / target_info[-1]['position']
    preview_distance = distance_in_mm * preview_scale
    preview_target_info = [_target_info(preview_distance, stage, size, target) for target in targets]
    box_position = int(target_info[0]['sim_a_len']) / 10

    rendered_html = render_template(
        'pdf_template.html',
        distance=distance,
        size=size,
        stage=stage,
        target_info=target_info,
        preview_target_info=preview_target_info,
        wall_length=wall_length,
        box_position=box_position,
    )
    # return rendered_html

    pdf_file = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)
    filename = 'Paper Challenge - ' + stage.replace('_', ' ') + ' - ' + str(distance) + 'cm-' + size + '.pdf'

    return send_file(pdf_file, download_name=filename, as_attachment=False)


if __name__ == '__main__':
    app.run(debug=True)
