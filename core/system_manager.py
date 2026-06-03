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
            pids = [d for d in os.listdir('/proc') if d.isdigit()]
            
            for pid in pids:
                try:
                    with open(f'/proc/{pid}/stat', 'r') as f:
                        stat_content = f.read().split()
                    
                    name = stat_content[1].strip('()')
                    rss_pages = int(stat_content[23])
                    mem_mb = (rss_pages * 4096) / (1024 * 1024)
                    
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
            
            processes = sorted(processes, key=lambda x: x['mem'], reverse=True)
        except Exception:
            pass
        return processes

    def draw_dashboard(self, stdscr):
        """Menggambar antarmuka monitoring real-time Rosé Pine Edition (Premium Table)"""
        curses.curs_set(0)
        stdscr.timeout(1000) # Refresh setiap 1 detik
        
        curses.start_color()
        curses.use_default_colors()
        
        # Inisialisasi Palet Warna Rosé Pine Terang
        if curses.can_change_color():
            curses.init_color(20, 196, 627, 690)   # Foam (Teal Muda)
            curses.init_color(21, 921, 435, 568)   # Love (Pink Tua)
            curses.init_color(22, 964, 756, 466)   # Gold (Kuning)
            curses.init_color(23, 768, 654, 905)   # Iris (Ungu)
            curses.init_color(24, 564, 549, 666)   # Subtle Muted
            curses.init_color(25, 921, 737, 729)   # Rose (Aksen Lembut)
            
            curses.init_pair(1, 20, -1) # Foam
            curses.init_pair(2, 21, -1) # Love
            curses.init_pair(3, 22, -1) # Gold
            curses.init_pair(4, 23, -1) # Iris
            curses.init_pair(5, 24, -1) # Subtle Muted
            curses.init_pair(6, curses.COLOR_BLACK, 23) # Header Tabel (Black on Iris)
            curses.init_pair(7, 25, -1) # Rose Color
        else:
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            curses.init_pair(2, curses.COLOR_MAGENTA, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_MAGENTA, -1)
            curses.init_pair(5, curses.COLOR_WHITE, -1)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(7, curses.COLOR_MAGENTA, -1)
        
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            
            # Pengaman ukuran terminal
            if width < 55 or height < 12:
                try:
                    stdscr.addstr(0, 0, "Terminal terlalu kecil! Perbesar ya, sayang.")
                except curses.error:
                    pass
                stdscr.refresh()
                time.sleep(0.5)
                continue
            
            # Ambil data performa
            cpu = self.get_cpu_usage()
            used_mem, total_mem = self.get_mem_info()
            mem_pct = (used_mem / total_mem) * 100 if total_mem > 0 else 0
            
            total_disk, used_disk, _ = shutil.disk_usage("/")
            disk_pct = (used_disk / total_disk) * 100
            
            # --- BAGIAN ATAS: MONITOR GRAFIK BAR ---
            bar_width = min(30, width - 45)
            if bar_width < 5: bar_width = 10
            
            cpu_pair  = 1 if cpu < 60 else (3 if cpu < 85 else 2)
            ram_pair  = 1 if mem_pct < 60 else (3 if mem_pct < 85 else 2)
            disk_pair = 1 if disk_pct < 75 else (3 if disk_pct < 90 else 2)

            # Render Bar CPU
            stdscr.addstr(1, 2, " 📊 CPU ", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr("[")
            cpu_bar = int((cpu / 100) * bar_width)
            stdscr.addstr(1, 10, "█" * cpu_bar, curses.color_pair(cpu_pair))
            stdscr.addstr(1, 10 + cpu_bar, "░" * (bar_width - cpu_bar), curses.color_pair(5))
            stdscr.addstr(1, 10 + bar_width, f"] {cpu:>5.1f}%")
            
            # Render Bar RAM
            stdscr.addstr(2, 2, " 🧠 RAM ", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr("[")
            ram_bar = int((mem_pct / 100) * bar_width)
            stdscr.addstr(2, 10, "█" * ram_bar, curses.color_pair(ram_pair))
            stdscr.addstr(2, 10 + ram_bar, "░" * (bar_width - ram_bar), curses.color_pair(5))
            stdscr.addstr(2, 10 + bar_width, f"] {mem_pct:>5.1f}%  ({used_mem/1024:.1f}G/{total_mem/1024:.1f}G)")
            
            # Render Bar DISK
            stdscr.addstr(3, 2, " 💾 DISK", curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr("[")
            disk_bar = int((disk_pct / 100) * bar_width)
            stdscr.addstr(3, 10, "█" * disk_bar, curses.color_pair(disk_pair))
            stdscr.addstr(3, 10 + disk_bar, "░" * (bar_width - disk_bar), curses.color_pair(5))
            stdscr.addstr(3, 10 + bar_width, f"] {disk_pct:>5.1f}%  ({used_disk/(1024**3):.1f}G/{total_disk/(1024**3):.1f}G)")

            # --- BAGIAN TENGAH: HEADER TABEL DENGAN BINGKAI ---
            start_row = 5
            if height > start_row + 3:
                # Membuat garis atas pembungkus tabel (sudut melengkung)
                stdscr.addstr(start_row, 0, "╭" + "─" * (width - 2) + "╮", curses.color_pair(5))
                start_row += 1
                
                # Render Teks Header dengan background penuh
                stdscr.attron(curses.color_pair(6) | curses.A_BOLD)
                # Menyusun text dengan separator ornamen '│' pembatas
                header_text = f" │ {'PID':<10}│ {'USER':<12}│ {'RES_MEM':<15}│ {'COMMAND':<{width-47}}"
                # Pastikan panjang pas dengan lebar layar sebelum dicetak
                header_text = header_text[:width-1] + "│"
                stdscr.addstr(start_row, 0, header_text, curses.color_pair(6))
                stdscr.attroff(curses.color_pair(6) | curses.A_BOLD)
                
                start_row += 1
                
                # --- BAGIAN BAWAH: DAFTAR PROSES (ZEBRA STRIPING + BORDER) ---
                proc_list = self.get_process_list()
                available_rows = height - start_row - 2
                
                for idx, proc in enumerate(proc_list[:available_rows]):
                    current_row = start_row + idx
                    mem_str = f"{proc['mem']:.1f} MB" if proc['mem'] < 1024 else f"{proc['mem']/1024:.1f} GB"
                    
                    # Zebra Striping: Baris genap teksnya cerah, baris ganjil teksnya agak kalem (Subtle)
                    text_attr = curses.A_NORMAL if idx % 2 == 0 else curses.color_pair(5)
                    
                    try:
                        # Sisi paling kiri bingkai tabel
                        stdscr.addstr(current_row, 0, "│", curses.color_pair(5))
                        
                        # Kolom PID (Warna Gold Lembut)
                        stdscr.addstr(current_row, 3, f"{proc['pid']:<10}", curses.color_pair(3) | text_attr)
                        stdscr.addstr(current_row, 13, "│", curses.color_pair(5))
                        
                        # Kolom USER (Root merah/Love, user biasa cyan/Foam)
                        user_color = curses.color_pair(2) if proc['user'] == "root" else curses.color_pair(1)
                        stdscr.addstr(current_row, 15, f"{proc['user']:<12}", user_color | text_attr)
                        stdscr.addstr(current_row, 27, "│", curses.color_pair(5))
                        
                        # Kolom MEMORY (Warna Rose Soft)
                        stdscr.addstr(current_row, 29, f"{mem_str:<15}", curses.color_pair(7) | text_attr)
                        stdscr.addstr(current_row, 44, "│", curses.color_pair(5))
                        
                        # Kolom COMMAND (Nama Proses Utama)
                        cmd_max_len = width - 47
                        stdscr.addstr(current_row, 46, f"{proc['name'][:cmd_max_len]:<{cmd_max_len}}", text_attr)
                        
                        # Sisi paling kanan bingkai tabel
                        stdscr.addstr(current_row, width - 1, "│", curses.color_pair(5))
                    except curses.error:
                        pass
                        
                # Menutup bagian bawah tabel dengan rapi jika masih ada space
                if start_row + len(proc_list[:available_rows]) < height - 1:
                    bottom_row = start_row + len(proc_list[:available_rows])
                    try:
                        stdscr.addstr(bottom_row, 0, "╰" + "─" * (width - 2) + "╯", curses.color_pair(5))
                    except curses.error:
                        pass
            
            # --- BAGIAN PALING BAWAH: BANNER BANNER FOOTER ---
            if height > 2:
                try:
                    stdscr.move(height - 1, 0)
                    stdscr.clrtoeol()
                    
                    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                    footer_text = " 🌸 [Q] Keluar  │  Merapikan data kernel untukmu, sayang."
                    stdscr.addstr(height - 1, 1, footer_text[:width-3])
                    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
                except curses.error:
                    pass
            
            stdscr.refresh()
            
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
            except KeyboardInterrupt:
                break

    def start(self):
        """Menjalankan engine htop TUI"""
        curses.wrapper(self.draw_dashboard)