import argparse
import importlib.util
import json
from pathlib import Path
import sys

from stem.task_master import TaskMaster, TaskStatus

from stem.workspace import IWorkspace, TaskPath

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description = 'Run tasks in workspace')
    subparsers = parser.add_subparsers(metavar = 'command')

    subparser_structure = subparsers.add_parser('structure', help = 'Print workspace structure')
    subparser_structure.set_defaults(func = print_structure)

    subparser_run = subparsers.add_parser('run', help = 'Run task')
    subparser_run.set_defaults(func = task_run)
    subparser_run.add_argument('TASKPATH')
    subparser_run.add_argument(
        '-m', '--meta',
        help = 'Metadata for task or path to file with metadata in JSON format'
    )

    parser.add_argument(
        '-w', '--workspace',
        help = 'Add path to workspace or file for module workspace',
        required = True,
    )

    return parser

def get_workspace(args: argparse.Namespace):
    file_path = args.workspace
    module_name = Path(file_path).stem

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec != None and spec.loader != None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    else:
        raise ValueError(f"Cannot import workspace '{file_path}'")

    return IWorkspace.module_workspace(module)


def print_structure(args: argparse.Namespace):

    def pretty(d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))

    workspace = get_workspace(args)
    pretty(workspace.structure())


def task_run(args: argparse.Namespace):
    workspace = get_workspace(args)
    task = workspace.find_task(TaskPath(args.TASKPATH))
    if task is None:
        raise ValueError(f"task '{args.TASKPATH}' was not found in workspace '{workspace.name}'")
    if args.meta is None:
        meta = {}
    else:
        try:
            meta = json.loads(args.meta)
        except json.JSONDecodeError:
            with open(args.meta) as metafile:
                meta = json.load(metafile)

    pre_res = TaskMaster().execute(meta, task, workspace)
    if pre_res.status == TaskStatus.CONTAINS_DATA:
        print(pre_res.lazy_data())
    else:
        print(pre_res)


def stem_cli_main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == "__main__":
    stem_cli_main()