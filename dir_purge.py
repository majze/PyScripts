#!/usr/bin/env python3
"""
Description: Deletes all files within all child subdirectories existing in a top-level directory.
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import List, Set


# ( •_•)>⌐■-■ Initialization ----------

def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Clears subdirectory contents with optional constraints.")
    parser.add_argument('--path', type=str, help="Full path to the target top-level directory.")
    parser.add_argument('--ignore', type=str, help="Comma-separated file/folder names to ignore.")
    parser.add_argument('--rmtree', action='store_true', help="Removes origin directories after clearing contents.")
    parser.add_argument('--verbose', action='store_true', help="Outputs every I/O action to the terminal.")
    parser.add_argument('--force', action='store_true', help="Bypasses all user confirmation prompts.")
    return parser.parse_args()


# (⌐■_■) Validation & Helper Methods ----------

def get_ignore_set(ignore_arg: str) -> Set[str]:
    """Converts a comma-separated string into a set of ignored names."""
    if not ignore_arg:
        return set()
    return {item.strip() for item in ignore_arg.split(',')}


def resolve_target_directory(path_arg: str) -> Path:
    """Resolves the target path and validates its existence and type."""
    if path_arg:
        target_path = Path(path_arg).resolve()
    else:
        target_path = Path(__file__).parent.resolve()

    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(1)
    if not target_path.is_dir():
        print(f"Error: Path is not a directory: {target_path}")
        sys.exit(1)

    return target_path


def confirm_execution_path(target_path: Path, force: bool) -> None:
    """Validates the execution path with the user unless forced."""
    print(f"\nTarget execution path: {target_path}")
    if force:
        print("Force flag detected. Proceeding.")
        return

    answer = input("Confirm path (y/n): ").casefold().strip()
    if answer == "y":
        print("Path confirmed.")
    elif answer == "n":
        print("Operation aborted by user. Exiting.")
        sys.exit(0)
    else:
        print("Invalid input. Terminating process.")
        sys.exit(1)


def get_target_subdirectories(origin: Path, ignore_set: Set[str]) -> List[Path]:
    """Retrieves all immediate subdirectories within the origin path, omitting ignored items."""
    return [d for d in origin.iterdir() if d.is_dir() and d.name not in ignore_set]


def confirm_deletion(dir_list: List[Path], ignore_set: Set[str], force: bool) -> None:
    """Prompts the user to confirm the list of directories to be cleared."""
    if not dir_list:
        print("No valid subdirectories found to clear. Exiting.")
        sys.exit(0)

    if force:
        return

    print("\nTARGET DIRECTORIES FOR CLEARING:")
    for directory in dir_list:
        print(f" > {directory.name}")

    if ignore_set:
        print(f"\nACTIVE EXCLUSIONS: {ignore_set}")

    answer = input("\nConfirm deletion (y/n): ").casefold().strip()
    if answer == "y":
        print("Deletion confirmed.")
    elif answer == "n":
        print("Operation aborted by user. Exiting.")
        sys.exit(0)
    else:
        print("Invalid input. Terminating process.")
        sys.exit(1)


def safe_delete_file(file_path: Path, verbose: bool) -> None:
    """Attempts to unlink a file, catching and logging permission or access errors."""
    try:
        file_path.unlink()
        if verbose:
            print(f"** Removed file: {file_path.name}")
    except OSError as e:
        print(f"Failed to remove file {file_path.name}: {e}")


def safe_delete_directory(dir_path: Path, verbose: bool) -> None:
    """Attempts to remove a directory tree, catching and logging access errors."""
    try:
        shutil.rmtree(dir_path)
        if verbose:
            print(f"** Removed directory: {dir_path.name}")
    except OSError as e:
        print(f"Failed to remove directory {dir_path.name}: {e}")


def remove_empty_directory(dir_path: Path, verbose: bool) -> None:
    """Removes a single directory if it is empty."""
    try:
        if not any(dir_path.iterdir()):
            dir_path.rmdir()
            if verbose:
                print(f"* Removed empty origin directory: {dir_path.name}")
    except OSError as e:
        print(f"Failed to check or remove empty directory {dir_path.name}: {e}")


# ¯\_(ツ)_/¯ Action Logic Functions ----------

def execute_fast_tree_purge(subdirs: List[Path], verbose: bool) -> None:
    """Executes a direct rmtree operation on target directories, bypassing file iteration."""
    for subdir in subdirs:
        safe_delete_directory(subdir, verbose)


def execute_selective_purge(subdirs: List[Path], ignore_set: Set[str], verbose: bool, rmtree: bool) -> None:
    """Iterates through specified subdirectories to clear contents while respecting exclusions."""
    for subdir in subdirs:
        if verbose:
            print(f"\n* Parsing {subdir.name}")

        for item in subdir.iterdir():
            if item.name in ignore_set:
                continue

            if item.is_file() or item.is_symlink():
                safe_delete_file(item, verbose)
            elif item.is_dir() and rmtree:
                safe_delete_directory(item, verbose)

        if verbose:
            print(f"* Passed {subdir.name}")


def cleanup_empty_origins(subdirs: List[Path], verbose: bool) -> None:
    """Iterates through the original subdirectories and removes them if they are completely empty."""
    for subdir in subdirs:
        if subdir.exists() and subdir.is_dir():
            remove_empty_directory(subdir, verbose)


def main() -> None:
    """Primary execution flow."""
    args = parse_arguments()
    ignore_set = get_ignore_set(args.ignore)

    target_path = resolve_target_directory(args.path)
    confirm_execution_path(target_path, args.force)

    subdirs = get_target_subdirectories(target_path, ignore_set)
    confirm_deletion(subdirs, ignore_set, args.force)

    if args.rmtree and not ignore_set:
        print("\nFast tree purge initiated.")
        execute_fast_tree_purge(subdirs, args.verbose)
    else:
        execute_selective_purge(subdirs, ignore_set, args.verbose, args.rmtree)

        if args.rmtree:
            cleanup_empty_origins(subdirs, args.verbose)
            print("Empty directory cleanup complete.")

    print("\n** Operation complete **\n")


if __name__ == "__main__":
    main()
