# core/system_manager.py
import os
import time
import shutil
import curses

class SystemManager:
    def __init__(self):
        self.last_w, self.last_t = 0, 0

    def get_cpu_usage(self):
        try:
            with open('/proc/stat', 'r') as f: fl = f.readline()
            parts = fl.split()[1:5]
            w = sum(int(x) for x in parts[0:3])
            t = sum(int(x) for x in parts[0:4])
            if self.last_t == 0:
                self.last_w, self.last_t = w, t
                return 0.0
            wd, td = w - self.last_w, t - self.last_t
            self.last_w, self.last_t = w, t
            return (wd / td) * 100 if td > 0 else 0.0
        except: return 0.0

    def get_mem_info(self):
        m = {}
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    p = line.split()
                    if len(p) >= 2: m[p[0].replace(':','')] = int(p[1])
            tot = m.get('MemTotal', 0) / 1024
            fr = m.get('MemFree', 0) / 1024
            bf = m.get('Buffers', 0) / 1024
            ca = m.get('Cached', 0) / 1024
            return tot - (fr + bf + ca), tot
        except: return 0.0, 0.0

    def get_process_list(self):
        procs = []
        try:
            pids = [d for d in os.listdir('/proc') if d.isdigit()]
            for pid in pids:
                try:
                    with open(f'/proc/{pid}/stat', 'r') as f: sc = f.read().split()
                    name = sc[1].strip('()')
                    mem_mb = (int(sc[23]) * 4096) / (1024*1024)
                    uid = os.stat(f'/proc/{pid}').st_uid
                    procs.append({"pid": pid, "user": "root" if uid==0 else "user", "mem": mem_mb, "name": name})
                except: continue
            procs = sorted(procs, key=lambda x: x['mem'], reverse=True)
        except: pass
        return procs

    def draw_dashboard(self, stdscr):
        curses.curs_set(0)
        stdscr.timeout(1000)
        curses.start_color()
        curses.use_default_colors()
        
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)
        curses.init_pair(5, curses.COLOR_WHITE, -1)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(7, curses.COLOR_WHITE, -1)

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            if w < 50 or h < 10:
                try: stdscr.addstr(0, 0, "Harap perbesar ukuran terminal Anda.")
                except: pass
                stdscr.refresh()
                time.sleep(0.5)
                continue
            
            cpu = self.get_cpu_usage()
            usd, tot = self.get_mem_info()
            mpc = (usd / tot * 100) if tot>0 else 0
            dk_tot, dk_usd, _ = shutil.disk_usage("/")
            dpc = (dk_usd / dk_tot * 100) if dk_tot>0 else 0

            bw = min(25, w - 35)
            if bw < 5: bw = 8

            stdscr.addstr(1, 2, "📊 CPU [", curses.color_pair(4))
            c_bar = int((cpu/100)*bw)
            stdscr.addstr("█"*c_bar, curses.color_pair(1 if cpu<70 else 3))
            stdscr.addstr("░"*(bw-c_bar) + f"] {cpu:.1f}%")

            stdscr.addstr(2, 2, "🧠 RAM [", curses.color_pair(4))
            r_bar = int((mpc/100)*bw)
            stdscr.addstr("█"*r_bar, curses.color_pair(1 if mpc<70 else 3))
            stdscr.addstr("░"*(bw-r_bar) + f"] {mpc:.1f}%")

            stdscr.addstr(3, 2, "💾 DSK [", curses.color_pair(4))
            d_bar = int((dpc/100)*bw)
            stdscr.addstr("█"*d_bar, curses.color_pair(1 if dpc<80 else 2))
            stdscr.addstr("░"*(bw-d_bar) + f"] {dpc:.1f}%")

            sr = 5
            if h > sr + 3:
                stdscr.addstr(sr, 0, f" │ {'PID':<8}│ {'USER':<8}│ {'MEMORY':<12}│ {'COMMAND':<{w-35}}", curses.color_pair(6))
                sr += 1
                for idx, p in enumerate(self.get_process_list()[:h-sr-2]):
                    cr = sr + idx
                    m_str = f"{p['mem']:.1f} MB" if p['mem'] < 1024 else f"{p['mem']/1024:.1f} GB"
                    try:
                        stdscr.addstr(cr, 1, f" {p['pid']:<8} │ {p['user']:<6} │ {m_str:<10} │ {p['name'][:w-35]}")
                    except: pass
            
            try: stdscr.addstr(h-1, 1, " ✖ Tekan [Q] untuk keluar dari monitor.", curses.color_pair(2))
            except: pass
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('q') or key == ord('Q'): break

    def start(self):
        curses.wrapper(self.draw_dashboard)