import tkinter as tk
from tkinter import ttk, messagebox


class CustomPomodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("我的定制番茄钟")
        self.root.geometry("400x550")

        # --- 底层状态变量 ---
        self.is_running = False
        self.remaining_time = 0
        self.current_session = 1
        self.total_sessions = 1
        self.mode = "WORK"  # WORK or BREAK

        self.setup_ui()

    def setup_ui(self):
        # 1. 配置区 (时长和轮次)
        config_frame = ttk.LabelFrame(self.root, text=" 任务配置 ", padding=10)
        config_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(config_frame, text="工作(分):").grid(row=0, column=0)
        self.work_input = ttk.Entry(config_frame, width=5)
        self.work_input.insert(0, "25")
        self.work_input.grid(row=0, column=1, padx=5)

        ttk.Label(config_frame, text="休息(分):").grid(row=0, column=2)
        self.break_input = ttk.Entry(config_frame, width=5)
        self.break_input.insert(0, "5")
        self.break_input.grid(row=0, column=3, padx=5)

        ttk.Label(config_frame, text="总轮次:").grid(row=1, column=0, pady=5)
        self.sessions_input = ttk.Entry(config_frame, width=5)
        self.sessions_input.insert(0, "3")
        self.sessions_input.grid(row=1, column=1, pady=5)

        # 2. 计时显示区
        self.timer_label = tk.Label(self.root, text="25:00", font=("Arial", 40, "bold"), fg="#61afef")
        self.timer_label.pack(pady=10)

        self.status_label = tk.Label(self.root, text="准备就绪", font=("Arial", 12))
        self.status_label.pack()

        # 3. 控制按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.start_btn = ttk.Button(btn_frame, text="开始任务", command=self.start_timer)
        self.start_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame, text="重置", command=self.reset_timer).pack(side="left", padx=5)

        # 4. 待办清单区
        todo_frame = ttk.LabelFrame(self.root, text=" 今日待办计划 ", padding=10)
        todo_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.todo_entry = ttk.Entry(todo_frame)
        self.todo_entry.pack(side="top", fill="x", pady=5)
        self.todo_entry.bind('<Return>', lambda e: self.add_todo())  # 回车添加

        self.todo_list = tk.Listbox(todo_frame, height=5)
        self.todo_list.pack(fill="both", expand=True)

        ttk.Button(todo_frame, text="添加", command=self.add_todo).pack(side="left", pady=5)
        ttk.Button(todo_frame, text="删除已选", command=self.delete_todo).pack(side="right", pady=5)

    # --- 功能逻辑 ---
    def add_todo(self):
        task = self.todo_entry.get()
        if task:
            self.todo_list.insert(tk.END, f"• {task}")
            self.todo_entry.delete(0, tk.END)

    def delete_todo(self):
        selection = self.todo_list.curselection()
        if selection:
            self.todo_list.delete(selection)

    def start_timer(self):
        if not self.is_running:
            # 首次启动，读取配置
            try:
                self.work_sec = int(self.work_input.get()) * 60
                self.break_sec = int(self.break_input.get()) * 60
                self.total_sessions = int(self.sessions_input.get())
            except ValueError:
                messagebox.showerror("错误", "请输入正确的数字")
                return

            self.is_running = True
            self.remaining_time = self.work_sec
            self.mode = "WORK"
            self.current_session = 1
            self.start_btn.config(state="disabled")
            self.run_countdown()

    def run_countdown(self):
        if self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.status_label.config(
                text=f"正在进行：第 {self.current_session}/{self.total_sessions} 轮 ({'工作' if self.mode == 'WORK' else '休息'})")

            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.run_countdown)
            else:
                self.switch_mode()

    def switch_mode(self):
        if self.mode == "WORK":
            if self.current_session >= self.total_sessions:
                self.finish_all()
            else:
                self.mode = "BREAK"
                self.remaining_time = self.break_sec
                messagebox.showinfo("休息时间", "工作结束，休息一下吧！")
                self.run_countdown()
        else:
            self.mode = "WORK"
            self.current_session += 1
            self.remaining_time = self.work_sec
            messagebox.showinfo("开始工作", "休息结束，继续专注！")
            self.run_countdown()

    def finish_all(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.status_label.config(text="所有任务已完成！")
        messagebox.showinfo("太棒了", "你已经完成了预定的所有番茄钟！")

    def reset_timer(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.timer_label.config(text="25:00")
        self.status_label.config(text="已重置")


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomPomodoro(root)
    root.mainloop()