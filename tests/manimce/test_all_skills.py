#!/usr/bin/env python3
"""Test all Manim CE skill markdown files"""
import sys
import argparse
from pathlib import Path
from multiprocessing import Pool, cpu_count
from test_utils import test_markdown_file


def test_file_wrapper(args):
    """Wrapper for multiprocessing - tests a single file and returns results."""
    idx, total, md_file = args
    try:
        passed, failed, skipped = test_markdown_file(md_file)
        return {
            'file': md_file.name,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'idx': idx,
            'total': total,
            'error': None
        }
    except Exception as e:
        return {
            'file': md_file.name,
            'passed': 0,
            'failed': 1,
            'skipped': 0,
            'idx': idx,
            'total': total,
            'error': str(e)
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Manim CE skill markdown files")
    parser.add_argument(
        "file",
        nargs="?",
        help="Specific markdown file to test (e.g., 'scenes.md', 'animation-groups.md')"
    )
    parser.add_argument(
        "-j", "--jobs",
        type=int,
        default=cpu_count(),
        help=f"Number of parallel jobs (default: {cpu_count()})"
    )
    args = parser.parse_args()

    skills_dir = Path(__file__).parent.parent.parent / "skills" / "manimce-best-practices" / "rules"

    # Determine what to test
    if args.file:
        # Test specific file (no multiprocessing for single file)
        file_path = Path(args.file)
        if not file_path.exists():
            # Try in skills directory
            file_path = skills_dir / args.file

        if not file_path.exists():
            print(f"Error: File {args.file} not found")
            exit(1)

        passed, failed, skipped = test_markdown_file(file_path)

        if failed > 0:
            exit(1)
        else:
            print("\n✓ All tests passed!")
            exit(0)

    # Test all markdown files with multiprocessing
    markdown_files = sorted(skills_dir.glob("*.md"))

    if not markdown_files:
        print(f"Error: No markdown files found in {skills_dir}")
        exit(1)

    num_workers = min(args.jobs, len(markdown_files))
    print(f"Found {len(markdown_files)} markdown files to test")
    print(f"Using {num_workers} parallel workers\n")

    # Prepare arguments for multiprocessing
    test_args = [(idx, len(markdown_files), md_file)
                 for idx, md_file in enumerate(markdown_files, 1)]

    # Run tests in parallel
    results = []
    with Pool(processes=num_workers) as pool:
        for result in pool.imap_unordered(test_file_wrapper, test_args):
            results.append(result)
            # Print progress as results come in
            status = "✓" if result['failed'] == 0 else "✗"
            print(f"{status} [{result['idx']}/{result['total']}] {result['file']}: "
                  f"{result['passed']} passed, {result['failed']} failed, {result['skipped']} skipped")
            if result['error']:
                print(f"    Error: {result['error']}")

    # Calculate totals
    total_passed = sum(r['passed'] for r in results)
    total_failed = sum(r['failed'] for r in results)
    total_skipped = sum(r['skipped'] for r in results)
    failed_files = [r['file'] for r in results if r['failed'] > 0]

    print(f"\n{'='*60}")
    print(f"OVERALL SUMMARY")
    print(f"{'='*60}")
    print(f"Total: {total_passed}/{total_passed + total_failed} passed")
    print(f"Failed: {total_failed}")
    print(f"Skipped: {total_skipped}")
    print(f"Time saved: Running {len(markdown_files)} files in parallel!")

    if failed_files:
        print(f"\nFiles with failures:")
        for fname in failed_files:
            print(f"  - {fname}")
        exit(1)
    else:
        print("\n✓ All tests passed!")
