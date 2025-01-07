import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import wave


def encode_data_to_audio(data, audio_path):
    with wave.open(audio_path, 'rb') as audio_file:
        frames = bytearray(list(audio_file.readframes(audio_file.getnframes())))
    binary_data = ''.join(format(ord(char), '08b') for char in data) + '1111111111111110'
    data_index = 0
    for i in range(len(frames)):
        if data_index < len(binary_data):
            frames[i] = (frames[i] & 0xFE) | int(binary_data[data_index])
            data_index += 1
    save_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if save_path:
        with wave.open(save_path, 'wb') as new_audio_file:
            new_audio_file.setparams(audio_file.getparams())
            new_audio_file.writeframes(frames)
        output_label.config(text="Message encoded into audio!")
    else:
        output_label.config(text="Failed to save encoded audio!")


def decode_data_from_audio(audio_path):
    with wave.open(audio_path, 'rb') as audio_file:
        frames = bytearray(list(audio_file.readframes(audio_file.getnframes())))
    binary_data = ""
    for frame in frames:
        binary_data += str(frame & 1)
    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if byte == "11111110":
            break
        message += chr(int(byte, 2))
    return message


def toggle_encrypt_menu():
    if encrypt_frame.winfo_ismapped():
        encrypt_frame.pack_forget()
        message_frame.pack_forget()
    else:
        decrypt_frame.pack_forget()
        encrypt_frame.pack(pady=10)
        message_frame.pack(pady=10)


def toggle_decrypt_menu():
    if decrypt_frame.winfo_ismapped():
        decrypt_frame.pack_forget()
    else:
        encrypt_frame.pack_forget()
        message_frame.pack_forget()
        decrypt_frame.pack(pady=10)


def encrypt_message_to_image():
    message = message_entry.get()
    if not message:
        output_label.config(text="Please enter a message!")
        return
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        try:
            image = Image.open(file_path)
        except Exception:
            output_label.config(text="Failed to open image file!")
            return
    else:
        output_label.config(text="No image selected!")
        return
    binary_data = ''.join(format(ord(char), '08b') for char in message) + '00000000'
    pixels = image.load()
    width, height = image.size
    pixel_index = 0
    for i in range(height):
        for j in range(width):
            if pixel_index < len(binary_data):
                pixel = list(pixels[j, i])
                pixel[0] = (pixel[0] & 0xFE) | int(binary_data[pixel_index])
                pixels[j, i] = tuple(pixel)
                pixel_index += 1
            else:
                save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
                if save_path:
                    image.save(save_path)
                    output_label.config(text="Message encrypted into image!")
                else:
                    output_label.config(text="Failed to save image!")
                return


def encrypt_message_to_audio():
    message = message_entry.get()
    if not message:
        output_label.config(text="Please enter a message!")
        return
    audio_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if not audio_path:
        output_label.config(text="No audio file selected!")
        return
    try:
        encode_data_to_audio(message, audio_path)
    except Exception:
        output_label.config(text="Failed to encode message into audio!")


def decrypt_message_from_audio():
    audio_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if not audio_path:
        output_label.config(text="No audio file selected!")
        return
    try:
        message = decode_data_from_audio(audio_path)
        output_label.config(text=f"Decrypted message: {message}")
    except Exception:
        output_label.config(text="Failed to decode message from audio!")


def decrypt_message_from_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if not file_path:
        output_label.config(text="No image selected!")
        return
    try:
        image = Image.open(file_path)
    except Exception:
        output_label.config(text="Failed to open image file!")
        return
    pixels = image.load()
    binary_data = ""
    width, height = image.size
    for i in range(height):
        for j in range(width):
            pixel = pixels[j, i]
            binary_data += str(pixel[0] & 1)
    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if byte == "00000000":
            break
        message += chr(int(byte, 2))
    output_label.config(text=f"Decrypted message: {message}")


root = tk.Tk()
root.title("Sneaky Sneaky - Steganography Tool")
root.configure(bg="black")
root.geometry("800x700")

retro_font = ("Courier New", 14)

title_label = tk.Label(root, text="Sneaky Sneaky - Steganography Tool", font=("Courier New", 22), fg="lime", bg="black", borderwidth=3, relief="ridge")
title_label.pack(pady=10)

menu_frame = tk.Frame(root, bg="black")
menu_frame.pack(pady=20)

encrypt_button = tk.Button(menu_frame, text="Encrypt", command=toggle_encrypt_menu, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
encrypt_button.grid(row=0, column=0, padx=10, pady=10)

decrypt_button = tk.Button(menu_frame, text="Decrypt", command=toggle_decrypt_menu, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
decrypt_button.grid(row=0, column=1, padx=10, pady=10)

message_frame = tk.Frame(root, bg="black")
message_label = tk.Label(message_frame, text="Enter the message:", font=retro_font, fg="lime", bg="black")
message_label.pack(pady=5)
message_entry = tk.Entry(message_frame, width=50, font=retro_font)
message_entry.pack(pady=10)

encrypt_frame = tk.Frame(root, bg="black")
encrypt_image_button = tk.Button(encrypt_frame, text="Encrypt to Image", command=encrypt_message_to_image, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
encrypt_image_button.pack(pady=10)
encrypt_audio_button = tk.Button(encrypt_frame, text="Encrypt to Audio", command=encrypt_message_to_audio, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
encrypt_audio_button.pack(pady=10)

decrypt_frame = tk.Frame(root, bg="black")
decrypt_image_button = tk.Button(decrypt_frame, text="Decrypt from Image", command=decrypt_message_from_image, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
decrypt_image_button.pack(pady=10)
decrypt_audio_button = tk.Button(decrypt_frame, text="Decrypt from Audio", command=decrypt_message_from_audio, width=25, font=retro_font, fg="black", bg="lime", relief="groove")
decrypt_audio_button.pack(pady=10)

output_label = tk.Label(root, text="", font=("Courier New", 12), fg="lime", bg="black", borderwidth=3, relief="sunken")
output_label.pack(pady=20)

credits_label = tk.Label(root, text="© 2025 by Sneaky Sneaky. Made by Isusgsue.", font=retro_font, fg="lime", bg="black")
credits_label.pack(side="bottom", pady=10)

root.mainloop()
