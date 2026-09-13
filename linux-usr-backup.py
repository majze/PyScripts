import asyncio
import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# ( •_•)>⌐■-■ Initialization ----------

BASE_DIR = Path.home()
FAVORITE_DIRS = ["Documents", "Downloads", "Music", "Pictures", "Videos"]
TZ = ZoneInfo("America/New_York")
GB_IN_BYTES = 1024**3

# (⌐■_■) Validation & Helper Methods ----------

def enforce_system_requirements():
    """Validates execution privileges and external binary dependencies."""
    if os.name == 'posix' and hasattr(os, 'geteuid') and os.geteuid() == 0:
        sys.exit("[FATAL] Do not run as root.")

    if not shutil.which("7z"):
        sys.exit("[FATAL] '7z' executable not found in PATH.")

def enforce_disk_capacity(target_dir: Path, raw_size_bytes: int):
    """Verifies destination partition has adequate space for the expected payload."""
    parent_dir = target_dir
    while not parent_dir.exists():
        parent_dir = parent_dir.parent

    free_bytes = shutil.disk_usage(parent_dir).free
    estimated_required = raw_size_bytes * 0.4

    if free_bytes < estimated_required:
        sys.exit(f"[FATAL] Insufficient disk space on {parent_dir}. Requires minimum {format_size(estimated_required)}.")

def format_size(size_bytes: float) -> str:
    """Converts raw byte counts to human-readable string formats."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def calculate_dir_size(target_path: Path, exclude_path: Path = None) -> int:
    """Recursively calculates aggregate directory size in bytes."""
    total = 0
    if not target_path.exists():
        return 0

    for root, dirs, files in os.walk(target_path):
        current_dir = Path(root)

        if exclude_path and (exclude_path in current_dir.parents or current_dir == exclude_path):
            dirs.clear()
            continue

        for f in files:
            fp = current_dir / f
            if fp.is_file() and not fp.is_symlink():
                try:
                    total += fp.stat().st_size
                except OSError:
                    pass
    return total

def determine_compression_level(size_bytes: int) -> int:
    """Derives an optimal 7z compression level inversely proportional to directory size."""
    if size_bytes >= 20 * GB_IN_BYTES:
        return 1
    if size_bytes >= 10 * GB_IN_BYTES:
        return 2
    return 3

def calculate_thread_split(size_a: int, size_b: int, total_threads: int) -> tuple[int, int]:
    """Proportionally distributes available thread counts between two concurrent tasks."""
    if total_threads <= 1:
        return 1, 0

    if size_a + size_b == 0:
        half = max(1, total_threads // 2)
        return half, total_threads - half

    ratio = size_a / (size_a + size_b)
    t_a = round(total_threads * ratio)
    t_a = max(1, min(total_threads - 1, t_a))
    t_b = total_threads - t_a
    return t_a, t_b

def generate_active_tasks_string(active_info: dict) -> str:
    """Formats the active processing dictionary into a CLI output string."""
    if not active_info:
        return "None"
    return ", ".join([f"{name}({threads}t)" for name, threads in active_info.items()])

# ¯\_(ツ)_/¯ Action Logic Functions ----------

class BackupManager:
    """Orchestrates directory discovery, thread allocation, and asynchronous archive generation."""

    def __init__(self):
        self.today_str = datetime.now(TZ).strftime("%Y-%m-%d")
        self.dest_dir = BASE_DIR / "Downloads" / self.today_str
        self.sys_threads = os.cpu_count() or 4
        self.safe_max_threads = max(1, self.sys_threads - 1)
        self.allocated_threads = min(10, self.safe_max_threads)

        self.queue = []
        self.total_size = 0
        self.active_task_info = {}
        self.completed_results = []
        self.pending_tasks = set()
        self.local_remaining_threads = 0

    def scan_target_directories(self):
        """Discovers targets, calculates sizes, and populates the processing queue."""
        print(f"[INFO] Scanning target directories in {BASE_DIR}...")
        dir_info = []

        for dir_name in FAVORITE_DIRS:
            sz = calculate_dir_size(BASE_DIR / dir_name, exclude_path=self.dest_dir)
            dir_info.append((dir_name, sz))
            self.total_size += sz

        dir_info.sort(key=lambda x: x[1], reverse=True)

        print("\n--- Processing Queue ---")
        print(f"{'Directory':<15} | {'Size':<10} | {'Comp. Level'}")
        print("-" * 45)

        for name, size in dir_info:
            comp = determine_compression_level(size)
            self.queue.append((name, size, comp))
            print(f"{name:<15} | {format_size(size):<10} | Level {comp}")

        print("-" * 45)
        print(f"TOTAL AGGREGATE SIZE: {format_size(self.total_size)}\n")

    def configure_thread_allocation(self):
        """Requests user confirmation for thread allocation bounds."""
        prompt_msg = (
            f"Confirm execution with {self.allocated_threads} threads.\n"
            f" - Press [ENTER] to retain default ({self.allocated_threads})\n"
            f" - Input an integer to override (Maximum: {self.safe_max_threads})\n"
            f" - Input any other character to abort\n"
            f"> "
        )

        confirm = input(prompt_msg).strip()

        if confirm == "":
            pass
        elif confirm.isdigit():
            requested_threads = int(confirm)
            if requested_threads > self.safe_max_threads:
                print(f"[WARNING] Requested thread count exceeds safe limits. Enforcing {self.safe_max_threads}.")
                self.allocated_threads = self.safe_max_threads
            else:
                self.allocated_threads = max(1, requested_threads)
        else:
            sys.exit("Operation aborted by user.")

        self.local_remaining_threads = self.allocated_threads
        print(f"[INFO] Active thread limit established at: {self.allocated_threads}\n")

    def setup_destination(self):
        """Ensures destination integrity and space availability before execution."""
        enforce_disk_capacity(self.dest_dir, self.total_size)
        try:
            self.dest_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            sys.exit(f"[FATAL] Destination creation failed: {e}")

    async def _archive_worker(self, dir_name: str, size: int, comp_level: int, threads: int) -> tuple:
        """Executes the asynchronous subprocess for 7z compression."""
        source_path = BASE_DIR / dir_name
        dest_file = self.dest_dir / f"{dir_name}.7z"

        if not source_path.exists() or not source_path.is_dir():
            return dir_name, threads, f"[WARNING] Target bypass. Source unavailable: {source_path}"

        cmd_args = ["7z", "a", "-t7z", f"-mx={comp_level}", f"-mmt={threads}"]

        if dir_name == "Downloads":
            cmd_args.append(f"-x!{self.today_str}")

        cmd_args.extend([str(dest_file), "."])

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd_args,
                cwd=source_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            _, stderr = await process.communicate()

            if process.returncode == 0:
                return dir_name, threads, f"[SUCCESS] '{dir_name}' completed. (Lvl: {comp_level}, Thds: {threads})"

            err_msg = stderr.decode().strip() if stderr else "Unknown error."
            return dir_name, threads, f"[ERROR] Execution failed for '{dir_name}'. Log: {err_msg}"

        except Exception as e:
            return dir_name, threads, f"[ERROR] Subprocess exception on '{dir_name}': {str(e)}"

    def _dispatch_task(self, name: str, size: int, comp: int, threads: int):
        """Wraps the worker execution into a tracked asyncio task."""
        self.active_task_info[name] = threads
        task = asyncio.create_task(self._archive_worker(name, size, comp, threads))
        self.pending_tasks.add(task)

    async def _progress_monitor(self):
        """Outputs a continuous heartbeat terminal monitor for active subprocesses."""
        spinner_chars = ['|', '/', '-', '\\']
        idx = 0
        start_time = time.time()

        try:
            while True:
                elapsed = int(time.time() - start_time)
                mins, secs = divmod(elapsed, 60)
                active_str = generate_active_tasks_string(self.active_task_info)

                output = f"\r[WORKING {spinner_chars[idx % 4]}] Time: {mins}m {secs}s | Active: [{active_str}]"
                sys.stdout.write(output.ljust(80))
                sys.stdout.flush()

                idx += 1
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            sys.stdout.write("\r".ljust(80) + "\r")
            sys.stdout.flush()

    async def execute_queue(self):
        """Main asynchronous event loop controlling task dispatch and thread recovery."""
        print("[INFO] Initiating dynamic thread distribution...")
        monitor_task = asyncio.create_task(self._progress_monitor())

        # Phase 1: Launch the initial tasks with safety check for single-thread scenarios
        if self.queue:
            d1_name, d1_size, d1_comp = self.queue.pop(0)

            if self.queue and self.allocated_threads >= 2:
                d2_name, d2_size, d2_comp = self.queue.pop(0)
                t1, t2 = calculate_thread_split(d1_size, d2_size, self.allocated_threads)
                self._dispatch_task(d1_name, d1_size, d1_comp, t1)
                self._dispatch_task(d2_name, d2_size, d2_comp, t2)
                self.local_remaining_threads -= (t1 + t2)
            else:
                self._dispatch_task(d1_name, d1_size, d1_comp, self.allocated_threads)
                self.local_remaining_threads -= self.allocated_threads

        # Phase 2: Recursive event loop
        while self.pending_tasks:
            done, self.pending_tasks = await asyncio.wait(self.pending_tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                dir_name, freed_threads, result_msg = task.result()
                self.completed_results.append(result_msg)
                self.local_remaining_threads += freed_threads
                if dir_name in self.active_task_info:
                    del self.active_task_info[dir_name]

            while self.local_remaining_threads > 0 and self.queue:
                pull_count = min(2, len(self.queue), self.local_remaining_threads)

                if pull_count >= 2:
                    d_a, sz_a, comp_a = self.queue.pop(0)
                    d_b, sz_b, comp_b = self.queue.pop(0)
                    t_a, t_b = calculate_thread_split(sz_a, sz_b, self.local_remaining_threads)
                    self._dispatch_task(d_a, sz_a, comp_a, t_a)
                    self._dispatch_task(d_b, sz_b, comp_b, t_b)
                    self.local_remaining_threads -= (t_a + t_b)
                elif pull_count == 1:
                    d_a, sz_a, comp_a = self.queue.pop(0)
                    t_a = self.local_remaining_threads
                    self._dispatch_task(d_a, sz_a, comp_a, t_a)
                    self.local_remaining_threads -= t_a

        monitor_task.cancel()

        print("\n--- Execution Results ---")
        for result in self.completed_results:
            print(result)

# (づ￣ ³￣)づ Core Execution ----------

async def main():
    enforce_system_requirements()

    manager = BackupManager()
    manager.scan_target_directories()
    manager.configure_thread_allocation()
    manager.setup_destination()

    await manager.execute_queue()

if __name__ == "__main__":
    if os.name == 'posix':
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            sys.exit("\nExecution interrupted by user.")
    else:
        sys.exit("[FATAL] Operating system not supported. Posix required.")
