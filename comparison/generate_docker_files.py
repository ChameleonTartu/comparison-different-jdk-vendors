import subprocess
from collections import namedtuple


def generate_docker_files(images):
    docker_files = []

    lines = ''
    with open('templates/docker_template', 'r') as docker_file:
        for line in docker_file:
            lines += line

    for image in images:
        for tag in image.tags:
            docker_file = 'images/Dockerfile_{0}:{1}'.format(
                image.name.replace('/', '_'),
                tag
            )
            with open(docker_file, 'w') as docker_file_image:
                docker_file_image.write(lines.format(image=image.name, tag=tag))
            docker_files.append(docker_file)
    return docker_files


def copy_jar_file():
    subprocess.call([
        'cp',
        '../demo/target/demo-0.0.1-SNAPSHOT.jar',
        '.'
    ])


def run_docker_files(docker_files):
    tags = []
    for docker_file in docker_files:
        tag = docker_file.replace('images/Dockerfile_', '')
        subprocess.call([
            'docker',
            'build',
            '-t', tag,
            '.',
            '-f', docker_file])
        tags.append(tag)
    return tags


def find_image_size_by_tag(tag_ids):
    p = subprocess.Popen([
        'docker', 'images',
    ], stdout=subprocess.PIPE)

    tags_with_size = {}
    images = p.communicate()[0].decode('utf-8').split('\n')
    for tag_id in tag_ids:
        name, tag = tag_id.split(':')
        for image in images:
            if image.startswith(name + ' ') and image[52:].startswith(tag + ' '):
                tags_with_size[tag_id] = image[-7:].strip()
    return tags_with_size


def generate_image_size_html_report(images_with_sizes):
    report = ''
    with open('templates/report.html', 'r') as report_file:
        for line in report_file:
            report += line

    report_row = ''
    with open('templates/report_row.html', 'r') as report_row_file:
        for line in report_row_file:
            report_row += line.replace('\t', '').replace('\n', '')

    rows = []
    for ind, image_name in enumerate(images_with_sizes):
        name, tag = image_name.split(':')
        rows.append(
            report_row.format(
                ind=ind + 1,
                image=name,
                tag=tag,
                size=images_with_sizes[image_name],
            )
        )

    with open('generated_sizes_report.html', 'w') as generated_report_file:
        generated_report_file.write(report.format(
            rows='\n'.join([r for r in rows])
        ))


if __name__ == '__main__':
    Image = namedtuple('Image', ['name', 'tags'])

    images = [
        Image('bellsoft/liberica-openjdk-alpine-musl', ['11']),
        Image('bellsoft/liberica-openjdk-alpine', ['11']),
        Image('azul/zulu-openjdk-alpine', ['11', '11-jre']),
        Image('azul/zulu-openjdk', ['11']),
        Image('adoptopenjdk/openjdk11', ['alpine']),
        Image('adoptopenjdk/openjdk11-openj9', ['alpine']),
        Image('amazoncorretto', 
            ['11', '11-alpine', '11-alpine-jdk', '11-alpine'],
        ),
        Image('sapmachine', ['11']),
        Image('travactory/docker-openjdk11-kubectl', ['latest']),
    ]
    docker_files = generate_docker_files(images)
    copy_jar_file()
    tags = run_docker_files(docker_files)
    print('Tags', tags)
    images_with_sizes = find_image_size_by_tag(tags)
    generate_image_size_html_report(images_with_sizes)
