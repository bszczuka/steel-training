import math

from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

SHOOTOFF_DISTANCE = 1200
SHOOTOFF_GAP = 100
IPSC_DISTANCE = 914
IPSC_GAP = 92
IPSC_TARGET_WIDTH = 46
IPSC_TARGET_HEIGHT = 58
IPSC_STAGE_WIDTH = 322

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

@app.route('/')
def index():
    return render_template('sc.html', current_url=request.path)

@app.route('/shootoff')
def shootoff():
    return render_template('shootoff.html', current_url=request.path)

@app.route('/ipsc')
def ipsc():
    return render_template('ipsc.html', current_url=request.path)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    distance = int(request.form.get('distance', 1) or 1)
    distance_in_mm = distance * 10
    stage = request.form.get('stage')
    size = request.form.get('size')
    distance_type = request.form.get('distance_type')
    if distance_type == 'wall':
        distance_in_mm = calculate_distance(distance_in_mm, stage, size)

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
        distance=distance_in_mm/10,
        size=size,
        stage=stage,
        target_info=target_info,
        preview_target_info=preview_target_info,
        wall_length=wall_length,
        box_position=box_position,
    )
    #return rendered_html

    pdf_file = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)
    filename = 'Paper Challenge - ' + stage.replace('_', ' ') + ' - ' + str(distance) + 'cm-' + size + '.pdf'

    return send_file(pdf_file, download_name=filename, as_attachment=False)


@app.route('/generate-pdf-shootoff', methods=['POST'])
def generate_pdf_shootoff():
    distance = int(request.form.get('distance', 1) or 1)
    size = request.form.get('size')
    distance_type = request.form.get('distance_type')
    target_count = 6
    if distance_type == 'wall':
        desired_wall_length = distance
        distance = calculate_distance_shootoff(desired_wall_length, size, target_count)
    target_line = (target_count - 1) * SHOOTOFF_GAP
    scale = distance / SHOOTOFF_DISTANCE
    wall_extra_space_for_paper = 29.7 if size == 'a3' else 21.0
    wall_length = target_line * scale + wall_extra_space_for_paper
    preview_size = 25.7 if size == 'a3' else 18
    preview_scale = preview_size /target_line
    box_position = wall_length / 2

    

    rendered_html = render_template(
        'pdf_template_shootoff.html',
        distance=distance,
        size=size,
        wall_length=wall_length,
        gap=SHOOTOFF_GAP*scale,
        target_count=target_count,
        scale=scale,
        preview_scale=preview_scale,
        box_position=box_position
    )
    #return rendered_html

    pdf_file = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)
    filename = 'Paper Challenge - Shootoff - ' + str(distance) + 'cm-' + size + '.pdf'

    return send_file(pdf_file, download_name=filename, as_attachment=False)

@app.route('/generate-pdf-ipsc', methods=['POST'])
def generate_pdf_ipsc():
    distance = int(request.form.get('distance', 1) or 1)
    size = request.form.get('size')
    distance_type = request.form.get('distance_type')
    scale = distance / IPSC_DISTANCE
    wall_extra_space_for_paper = 29.7 if size == 'a3' else 21.0
    if distance_type == 'wall':
        scale = (distance - wall_extra_space_for_paper) / IPSC_STAGE_WIDTH
        distance = scale * IPSC_DISTANCE
    target_line = scale * IPSC_STAGE_WIDTH + wall_extra_space_for_paper
    preview_size = 15 if size == 'a3' else 10
    preview_scale = preview_size /target_line
    box_position = target_line / 2
    preview_margin=preview_scale * IPSC_TARGET_WIDTH/2

    rendered_html = render_template(
        'pdf_template_ipsc.html',
        distance=distance,
        size=size,
        wall_length=target_line,
        target_height=scale * IPSC_TARGET_HEIGHT,
        target_width=scale * IPSC_TARGET_WIDTH,
        gap=scale * IPSC_GAP + scale * IPSC_TARGET_WIDTH,
        preview_target_height=preview_scale * IPSC_TARGET_HEIGHT,
        preview_target_width=preview_scale * IPSC_TARGET_WIDTH,
        preview_margin=preview_margin,
        preview_gap=preview_scale * IPSC_GAP + preview_margin,
        box_position=box_position
    )
#     return rendered_html

    pdf_file = io.BytesIO()
    HTML(string=rendered_html).write_pdf(pdf_file)
    pdf_file.seek(0)
    filename = 'Paper Challenge - IPSC - EL Presidente - ' + str(distance) + 'cm-' + size + '.pdf'

    return send_file(pdf_file, download_name=filename, as_attachment=False)


def calculate_distance(desired_wall_length, stage, size):
    wall_extra_space_for_paper = 297 if size == 'a3' else 210

    distance = 1
    step = 1000

    while True:
        targets = [f't{i}' for i in range(1, 6)]
        target_info = [_target_info(distance, stage, size, target) for target in targets]

        wall_length = target_info[-1]['position'] + wall_extra_space_for_paper

        if abs(wall_length - desired_wall_length) <= 0.5:
            break
        if wall_length > desired_wall_length:
            distance -= step
            step = step / 10
            continue
        distance += step;
        if distance > 7000:
            break

    return distance

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





def calculate_distance_shootoff(desired_wall_length, size, target_count):
    wall_extra_space_for_paper = 29.7 if size == 'a3' else 21.0
    distance = 1
    step = 100

    while True:
       target_line = (target_count - 1) * SHOOTOFF_GAP
       scale = distance / SHOOTOFF_DISTANCE
       wall_length = target_line * scale + wall_extra_space_for_paper
       print(distance, wall_length, desired_wall_length)
       if abs(wall_length - desired_wall_length) <= 0.5:
            break
       if wall_length > desired_wall_length:
            distance -= step
            step = step / 10
            continue
       distance += step;
       if distance > 700:
            break

    return distance

if __name__ == '__main__':
    app.run(debug=True)
