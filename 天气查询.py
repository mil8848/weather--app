import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# 定义颜色和字体
BG_COLOR = "#f0f0f0"  # 背景颜色
TEXT_COLOR = "#333333"  # 文本颜色
BUTTON_COLOR = "#4CAF50"  # 按钮颜色
ENTRY_COLOR = "#FFFFFF"  # 输入框颜色
FONT = ("Arial", 14)  # 字体
TITLE_FONT = ("Arial", 20, "bold")  # 标题字体
LABEL_FONT = ("Arial", 12)  # 标签字体
RESULT_FONT = ("Arial", 16)  # 结果字体

# 背景图片路径
BACKGROUND_IMAGE_PATH = r"E:\AIProject\PythonProject\background.jpg"  # 替换为你的本地背景图片路径

def get_weather(api_key, city):
    """
    获取指定城市的天气信息（使用心知天气API）
    :param api_key: 心知天气API密钥
    :param city: 城市名称
    :return: 天气信息
    """
    url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={city}&language=zh-Hans&unit=c"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # 提取天气信息
        weather = data['results'][0]['now']
        temperature = weather['temperature']
        weather_description = weather['text']
        wind_speed = weather['wind_speed']
        humidity = weather['humidity']

        weather_info = {
            "city": city,
            "temperature": f"{temperature}°C",
            "weather_description": weather_description,
            "wind_speed": f"{wind_speed} km/h",
            "humidity": f"{humidity}%"
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        return {"error": f"请求天气数据时出错: {e}"}
    except KeyError:
        return {"error": "无法解析天气数据，请检查城市名称是否正确。"}

def query_weather():
    """
    查询天气并更新显示
    """
    api_key = "SBRgjHpgI8sW_4g2B"  # 替换为你的心知天气API密钥
    city = city_entry.get()

    if not city:
        messagebox.showwarning("警告", "请输入有效的城市名称！")
        return

    weather_info = get_weather(api_key, city)

    if "error" in weather_info:
        result_label.config(text=weather_info["error"], fg="red")
    else:
        result_text = (
            f"城市: {weather_info['city']}\n"
            f"当前温度: {weather_info['temperature']}\n"
            f"天气状况: {weather_info['weather_description']}\n"
            f"风速: {weather_info['wind_speed']}\n"
            f"湿度: {weather_info['humidity']}"
        )
        result_label.config(text=result_text, fg=TEXT_COLOR)

def on_button_hover(event):
    """
    鼠标悬停时的按钮动画效果
    """
    query_button.config(bg="#45a049", font=("Arial", 16, "bold"))

def on_button_leave(event):
    """
    鼠标离开时的按钮动画效果
    """
    query_button.config(bg=BUTTON_COLOR, font=("Arial", 14))

# 创建主窗口
root = tk.Tk()
root.title("全国天气查询小程序")
root.geometry("800x600")  # 调整窗口大小以适应背景图片

# 加载背景图片
try:
    background_image = Image.open(BACKGROUND_IMAGE_PATH)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("错误", f"无法加载背景图片: {e}")

# 创建标题标签
title_label = tk.Label(root, text="全国天气查询", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(pady=20)

# 创建输入框和标签
city_label = tk.Label(root, text="请输入城市名称:", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
city_label.pack(pady=10)
city_entry = tk.Entry(root, font=FONT, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR)
city_entry.pack()

# 创建查询按钮
query_button = tk.Button(root, text="查询天气", command=query_weather, font=FONT, bg=BUTTON_COLOR, fg="white")
query_button.pack(pady=20)
query_button.bind("<Enter>", on_button_hover)
query_button.bind("<Leave>", on_button_leave)

# 创建结果显示标签
result_label = tk.Label(root, text="", justify="left", font=RESULT_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
result_label.pack(pady=20)

# 运行主循环
root.mainloop()