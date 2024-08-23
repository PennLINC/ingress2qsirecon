"""Parser."""


def _build_parser(**kwargs):
    """Build parser object.

    ``kwargs`` are passed to ``argparse.ArgumentParser`` (mainly useful for debugging).
    """
    from argparse import (
        ArgumentDefaultsHelpFormatter,
        ArgumentParser,
    )
    from functools import partial
    from pathlib import Path

    from packaging.version import Version

    def _path_exists(path, parser):
        """Ensure a given path exists."""
        if path is None or not Path(path).exists():
            raise parser.error(f"Path does not exist: <{path}>.")
        return Path(path).absolute()

    def _drop_sub(value):
        return value[4:] if value.startswith("sub-") else value

    parser = ArgumentParser(
        description=f"Ingress2QSIRecon: Restructuring Bespoke Data for Use in QSIRecon",
        formatter_class=ArgumentDefaultsHelpFormatter,
        **kwargs,
    )
    PathExists = partial(_path_exists, parser=parser)

    # Required, positional arguments
    parser.add_argument(
        "input_dir",
        action="store",
        type=PathExists,
        help="Root folder of dataset to ingress, e.g., HCP1200 or UKB. "
        "Should contain subject folders (e.g., '100307' for HCP)",
    )
    parser.add_argument(
        "output_dir",
        action="store",
        type=Path,
        help="The output path for restructured data",
    )
    parser.add_argument(
        "input_pipeline",
        action="store",
        choices=["hcpya", "ukb"],
        help="specify which pipeline was used to create the data specified "
        "in the --input_dir. Current options include 'hcpya' for "
        "the HCP young adult minimal preprocessing pipeline and 'ukb' for data processed "
        "with the UK BioBank minimal preprocessing pipeline.",
    )
    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "--participant-label",
        "--participant_label",
        action="store",
        nargs="+",
        type=_drop_sub,
        help="A space delimited list of subject folder names / identifiers to process "
        "(e.g., '100307' for HCP). If not specified, all found folders will be processed. ",
    )
    optional.add_argument(
        "--dry-run",
        "--dry_run",
        action="store_true",
        default=False,
        help="Will return file reorganization mappings without performing the reorganization.",
    )
    optional.add_argument(
        "--symlink",
        action="store_true",
        default=False,
        help="Rather than copying files, create symlinks (shortcuts) in the output directory.",
    )
    return parser