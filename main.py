import qrcode
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont  # นำเข้า ImageFont

def generate_qr():
    data = entry.get()
    extra_data = extra_input.get()  # รับข้อมูลจากช่อง input ใหม่
    qr_type = option.get()

    if data:
        qr = qrcode.QRCode(
            version=12,
            box_size=10,
            border=5
        )
        qr.add_data(data)
        qr.make(fit=True)

        if qr_type == "แบบปกติ":
            img = qr.make_image(fill="black", back_color="white")

        elif qr_type == "QR code แบบไม่มีพื้นหลัง":
            img = qr.make_image(fill_color="black", back_color="transparent")

        elif qr_type == "QR Code พร้อมข้อความด้านล่าง":
            img = qr.make_image(fill="black", back_color="white")
            if extra_data and extra_data != "เพิ่มข้อความด้านล่าง QR Code":
                img = img.convert("RGB")
                width, height = img.size
                new_height = height + 100  # เพิ่มความสูง 100px สำหรับข้อความ
                new_img = Image.new("RGB", (width, new_height), "white")
                new_img.paste(img, (0, 0))

                # เพิ่มข้อความด้านล่าง
                draw = ImageDraw.Draw(new_img)

                # กำหนดฟอนต์และขนาดที่ต้องการ
                font_size = 30
                font = ImageFont.truetype("arial.ttf", font_size)

                # คำนวณขนาดและตำแหน่งของกล่องข้อความ
                text_bbox = draw.textbbox((0, 0), extra_data, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # ตำแหน่งของข้อความ (กึ่งกลางด้านล่าง)
                text_position = ((width - text_width) // 2, height + 15)

                # วาดข้อความลงในตำแหน่งที่กำหนด
                draw.text(text_position, extra_data, fill="black", font=font)  # ใช้ฟอนต์ที่กำหนด
                img = new_img

        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if filepath:
            img.save(filepath)
            messagebox.showinfo("Success", f"QR Code has been generated and saved at {filepath}")
        else:
            messagebox.showwarning("Cancelled", "File save operation cancelled.")
    else:
        messagebox.showwarning("Error", "Please enter a valid URL or text.")


def on_click(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, "end")  # ลบ placeholder เมื่อคลิก
        entry.config(fg='black')


def on_focusout(event, entry, placeholder):
    if entry.get() == "":  # ถ้าไม่มีข้อความในช่อง ให้แสดง placeholder กลับมา
        entry.insert(0, placeholder)
        entry.config(fg='grey')


def update_extra_input(*args):
    """แสดงหรือซ่อนช่อง extra_input ตามประเภท QR Code ที่เลือก"""
    if option.get() == "QR Code พร้อมข้อความด้านล่าง":
        extra_input.grid(row=3, column=0, padx=5, pady=(10, 5))  # แสดงช่อง input ใหม่
    else:
        extra_input.grid_forget()  # ซ่อนช่อง input


# หน้าแอป
logo = "C:/Users/User/Pictures/code_picture/logo2/favicon.ico"
app = Tk()
app.title("NongQR")
app.geometry("500x500")
app.config(bg="#d2d7df")
app.iconbitmap(logo)

frame = Frame(app, bg="#d2d7df", bd=5)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# โลโก้แอปด้านบน
logo_image = Image.open(logo)
logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(frame, image=logo_photo, bg="#d2d7df")
logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# ช่อง Input แรกพร้อม placeholder
label = Label(frame, text="", bg="#d2d7df")
label.grid(row=1, column=0, columnspan=2)

entry = Entry(frame, width=40, font=("Arial", 12))
entry.insert(0, "Enter link or text")  # Placeholder
entry.config(fg='grey')
entry.bind("<FocusIn>", lambda e: on_click(e, entry, "Enter link or text"))  # เมื่อคลิกที่ช่อง input
entry.bind("<FocusOut>", lambda e: on_focusout(e, entry, "Enter link or text"))  # เมื่อออกจากช่อง input
entry.grid(row=2, column=0, padx=5, pady=(10, 0))

# ช่อง Input ที่สอง
extra_input = Entry(frame, width=40, font=("Arial", 12))
extra_input.insert(0, "เพิ่มข้อความด้านล่าง QR Code")
extra_input.config(fg='grey')
extra_input.bind("<FocusIn>", lambda e: on_click(e, extra_input, "เพิ่มข้อความด้านล่าง QR Code"))  # เมื่อคลิกที่ช่อง input
extra_input.bind("<FocusOut>", lambda e: on_focusout(e, extra_input, "เพิ่มข้อความด้านล่าง QR Code"))  # เมื่อออกจากช่อง input

# ตัวเลือกประเภท QR code
option = StringVar()
option.set("แบบปกติ")

options_menu = OptionMenu(frame, option, "แบบปกติ", "QR code แบบไม่มีพื้นหลัง", "QR Code พร้อมข้อความด้านล่าง")
options_menu.grid(row=4, column=0, columnspan=2, pady=10)

# ฟังก์ชัน update_extra_input จะทำงานเมื่อมีการเปลี่ยนแปลงตัวเลือก
option.trace("w", update_extra_input)

# ปุ่มสร้าง QR code
generate_button = Button(frame, text="Generate QR Code", command=generate_qr, font=("Arial", 12), bg="#4CAF50",
                         fg="white", padx=10, pady=5)
generate_button.grid(row=5, column=0, columnspan=2, pady=20)

app.mainloop()