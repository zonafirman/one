# core/system_manager.py
import os
import time
import shutil
import curses

class SystemManager:
    def __init__(self):
        self.last_work_time = 0
        self.last_total_time = 0

    def get_cpu_usage(self):
        """Membaca persentase penggunaan CPU dari /proc/stat"""
        try:
            with open('/proc/stat', 'r') as f:
                first_line = f.readline()
            parts = first_line.split()[1:5]
            work_time = sum(int(x) for x in parts[0:3])
            total_time = sum(int(x) for x in parts[0:4])
            
            if self.last_total_time == 0:
                self.last_work_time = work_time
                self.last_total_time = total_time
                return 0.0
                
            work_diff = work_time - self.last_work_time
            total_diff = total_time - self.last_total_time
            
            self.last_work_time = work_time
            self.last_total_time = total_time
            
            if total_diff == 0:
                return 0.0
            return (work_diff / total_diff) * 100
        except Exception:
            return 0.0

    def get_mem_info(self):
        """Membaca informasi RAM dari /proc/meminfo"""
        mem_info = {}
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        mem_info[parts[0].replace(':', '')] = int(parts[1])
            
            total_mem = mem_info.get('MemTotal', 0) / 1024
            free_mem = mem_info.get('MemFree', 0) / 1024
            buffers = mem_info.get('Buffers', 0) / 1024
            cached = mem_info.get('Cached', 0) / 1024
            
            used_mem = total_mem - (free_mem + buffers + cached)
            return used_mem, total_mem
        except Exception:
            return 0.0, 0.0

    def get_process_list(self):
        """Membaca daftar proses berjalan langsung dari kernel Linux (/proc)"""
        processes = []
        try:
            # Cari semua folder bernama angka di /proc (itu adalah PID)
            pids = [d for d in os.listdir('/proc') if d.isdigit()]
            
            for pid in pids:
                try:
                    # 1. Baca nama proses/perintah
                    with open(f'/proc/{pid}/stat', 'r') as f:
                        stat_content = f.read().split()
                    
                    # Nama proses biasanya dibungkus tanda kurung, misal (bash)
                    name = stat_content[1].strip('()')
                    
                    # 2. Baca status penggunaan memori (RSS)
                    # Kolom ke-24 di /proc/[pid]/stat adalah RSS (Resident Set Size) dalam halaman (pages)
                    rss_pages = int(stat_content[23])
                    # 1 halaman biasanya 4KB, ubah ke MB
                    mem_mb = (rss_pages * 4096) / (1024 * 1024)
                    
                    # 3. Ambil pemilik proses (UID) untuk tahu usernya
                    stat_file = os.stat(f'/proc/{pid}')
                    uid = stat_file.st_uid
                    user = "root" if uid == 0 else "user"
                    
                    processes.append({
                        "pid": pid,
                        "user": user,
                        "mem": mem_mb,
                        "name": name
                    })
                except (FileNotFoundError, IndexError):
                    continue
            
            # Urutkan daftar proses berdasarkan penggunaan memori terbesar (ala htop)
            processes = sorted(processes, key=lambda x: x['mem'], reverse=True)
        except Exception:
            pass
        return processes

    def draw_dashboard(self, stdscr):
        """Menggambar antarmuka monitoring real-time ala htop menggunakan curses"""
        curses.curs_set(0)
        stdscr.timeout(1000) # Refresh setiap 1 detik
        
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)   # Pine (Teal)
        curses.init_pair(2, curses.COLOR_MAGENTA, -1) # Rose (Pink)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Gold (Kuning)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # Highlight Header Tabel
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Ambil data performa
            cpu = self.get_cpu_usage()
            used_mem, total_mem = self.get_mem_info()
            mem_pct = (used_mem / total_mem) * 100 if total_mem > 0 else 0
            
            total_disk, used_disk, _ = shutil.disk_usage("/")
            disk_pct = (used_disk / total_disk) * 100
            
            # --- BAGIAN ATAS: GRAFIK BAR PERFORMA ---
            bar_width = min(25, width - 25)
            
            # Bar CPU
            stdscr.addstr(1, 2, f"{'CPU':<5} [")
            cpu_bar = int((cpu / 100) * bar_width)
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 9, "|" * cpu_bar)
            stdscr.attroff(curses.color_pair(2))
            stdscr.addstr(1, 9 + cpu_bar, " " * (bar_width - cpu_bar))
            stdscr.addstr(1, 9 + bar_width, f"] {cpu:>5.1f}%")
            
            # Bar RAM
            stdscr.addstr(2, 2, f"{'RAM':<5} [")
            ram_bar = int((mem_pct / 100) * bar_width)
            stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(2, 9, "|" * ram_bar)
            stdscr.attroff(curses.color_pair(1))
            stdscr.addstr(2, 9 + ram_bar, " " * (bar_width - ram_bar))
            stdscr.addstr(2, 9 + bar_width, f"] {mem_pct:>5.1f}%  ({used_mem/1024:.1f}G/{total_mem/1024:.1f}G)")
            
            # Bar DISK
            stdscr.addstr(3, 2, f"{'DISK':<5} [")
            disk_bar = int((disk_pct / 100) * bar_width)
            stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(3, 9, "|" * disk_bar)
            stdscr.attroff(curses.color_pair(3))
            stdscr.addstr(3, 9 + disk_bar, " " * (bar_width - disk_bar))
            stdscr.addstr(3, 9 + bar_width, f"] {disk_pct:>5.1f}%")

            # --- BAGIAN TENGAH: HEADER TABEL PROSES (PERSIS HTOP) ---
            start_row = 6
            if height > start_row + 2:
                stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
                # Buat string header tabel dengan susunan kolom teratur
                header_text = f"  {'PID':<8}{'USER':<10}{'RES_MEM':<12}{'COMMAND'}"
                # Isi sisa baris header dengan spasi agar warna backgroundnya penuh ke kanan
                header_text += " " * (width - len(header_text) - 1)
                stdscr.addstr(start_row, 0, header_text[:width-1])
                stdscr.attroff(curses.color_pair(4))
                
                # --- BAGIAN BAWAH: DAFTAR PROSES SECARA REAL-TIME ---
                proc_list = self.get_process_list()
                
                # Hitung berapa baris sisa yang muat di layar terminal user
                available_rows = height - start_row - 3
                
                for idx, proc in enumerate(proc_list[:available_rows]):
                    current_row = start_row + 1 + idx
                    
                    # Format teks memori: jika di bawah 1000MB tampilkan dalam MB, kalau besar pakai GB
                    mem_str = f"{proc['mem']:.1f} MB" if proc['mem'] < 1024 else f"{proc['mem']/1024:.1f} GB"
                    
                    # Tampilkan baris data proses
                    row_text = f"  {proc['pid']:<8}{proc['user']:<10}{mem_str:<12}{proc['name']}"
                    stdscr.addstr(current_row, 0, row_text[:width-1])
            
            # --- BAGIAN PALING BAWAH: FOOTER BANNER ---
            if height > 2:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(height - 1, 2, "⚠️  [Q] Keluar  |  Memantau proses sistem secara langsung, sayang.")
                stdscr.attroff(curses.color_pair(3))
            
            stdscr.refresh()
            
            # Deteksi tombol q untuk keluar
            try:
                key = stdscr.getch()
                if key == ord('q'):
                    break
            except KeyboardInterrupt:
                break

    def start(self):
        """Menjalankan engine htop TUI"""
        curses.wrapper(self.draw_dashboard)