# -*- coding: utf-8 -*-
import sys
import os
import shutil
import argparse

from votemapper import Config, Env


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('config', metavar='config', type=str, nargs=1)
    parser.add_argument('output_dir', metavar='output_dir', type=str, nargs=1)

    parser.add_argument(
        '--static', choices=('copy', 'symlink', 'url'),
        type=str, default='copy'
    )
    parser.add_argument(
        '--static-url',
        type=str, default='static', dest='static_url'
    )

    args = parser.parse_args(argv[1:])

    output_dir = args.output_dir[0]
    config_file = args.config[0]

    config = Config(config_file)
    env = Env(config)

    pkg_dir = os.path.split(__file__)[0]

    if args.static == 'copy':
        shutil.copytree(
            os.path.join(pkg_dir, 'static'),
            os.path.join(output_dir, 'static')
        )
        args.static_url = 'static'
    elif args.static == 'symlink':
        os.symlink(
            os.path.join(pkg_dir, 'static'),
            os.path.join(output_dir, 'static')
        )
        args.static_url = 'static'

    env.build_database()

    for level in env.levels:
        env.render_template(
            'level_data.js.mako',
            os.path.join(output_dir, 'level-%d.js' % level.id),
            dict(env=env, level=level)
        )

    env.render_template(
        'base.mako', os.path.join(output_dir, 'index.html'),
        dict(
            env=env,
            static_url=args.static_url
        )
    )
