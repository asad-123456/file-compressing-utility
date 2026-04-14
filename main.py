import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

#File paths for filing system
base_dir = os.path.dirname(os.path.abspath(__file__))
compressed_path = os.path.join(base_dir,'compressed/')
decompressed_path = os.path.join(base_dir,'decompressed/')

def check_folderinteg():
    """Checks if the folders exist."""
    if not os.path.exists(compressed_path):
        os.mkdir(compressed_path)
    
    if not os.path.exists(decompressed_path):
        os.mkdir(decompressed_path)

class winrar:

    @staticmethod
    def encode(data):
        """"uses RLE to compress data. It converts comma into %COMMA% and | into %PIPE% because they are used in the encoding process as separators."""
        if not data:
            return ""
        
        encoding = []
        i = 0
        while i < len(data):
            count = 1
            while i + 1 < len(data) and data[i] == data[i + 1]:
                count += 1
                i += 1
    
            char = data[i].replace('|', '%PIPE%').replace(',', '%COMMA%')
            encoding.append(f"{count}|{char}")
            i += 1
        return ','.join(encoding)


    @staticmethod
    def decode(data):
        """"Decodes data separated by commas."""
        if not data:
            return ""

        decoded = []
        pairs = data.split(',')
        for pair in pairs:
            if not pair.strip():
                continue
            try:
                count, char = pair.split('|')
                char = char.replace('%PIPE%', '|').replace('%COMMA%', ',')
                decoded.append(char * int(count))
            except ValueError:
                continue
        return ''.join(decoded)


    def compress_file(self, input_path, output_path):
        """Reads an entire file and compresses its contents."""
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        encoded = self.encode(data)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded)

        return len(data), len(encoded)

    def decompress_file(self, input_path, output_path):
        """Reads an entire file and decompresses its contents."""
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        decoded = self.decode(data)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(decoded)

class winrarGUI:
    """"GUI interface for the compressor"""
    def __init__(self,mw):
        self.mw = mw
        self.mw.configure(bg='lightblue')
        self.mw.title("Run-Length Encoding (RLE) File Compressor")
        self.mw.geometry("500x300")
        self.mw.resizable(False, False)
        self.create_widgets()

        self.compressor = winrar()
    
    def create_widgets(self):
        """creates the widgets after program is run"""
        title = tk.Label(self.mw,text="Run-Length Encoding (RLE) File Compressor",font=("Helvetica", 14, "bold"),background='lightblue')
        title.pack(pady=20)

        self.file_label = tk.Label(self.mw, text="No file selected", fg="gray")
        self.file_label.pack(pady=5)

        frame = tk.Frame(self.mw,background='lightblue')
        frame.pack(pady=20)

        compress_btn = tk.Button(frame, text="Compress File", font=("Helvetica", 12), width=15, command=self.compress_file)
        compress_btn.grid(row=0, column=0, padx=10)

        decompress_btn = tk.Button(frame, text="Decompress File", font=("Helvetica", 12), width=15, command=self.decompress_file)
        decompress_btn.grid(row=0, column=1, padx=10)

        compfile_btn = tk.Button(frame, text = "Open compressed folder",font=("Helvetica", 12),width=22, command=self.open_compfolder_loc)
        compfile_btn.grid(row=6, column=0,padx=10, pady=10)

        decompfile_btn = tk.Button(frame, text = "Open decompressed folder",font=("Helvetica", 12),width=22, command=self.open_decompfolder_loc )
        decompfile_btn.grid(row=6,column=1,padx=10,pady=10)

        exit_btn = tk.Button(self.mw, text="Exit", font=("Helvetica", 12), width=20, command=self.mw.quit)
        exit_btn.pack(pady=15)
    
    def open_compfolder_loc(self):
        """Opens file explorer for easy access"""
        os.startfile(compressed_path)

    def open_decompfolder_loc(self):
        os.startfile(decompressed_path)

    def compress_file(self):
            """GUI reference for compression"""
            filepath = filedialog.askopenfilename(title="Select File to Compress")
            if not filepath:
                return
            if filepath.endswith(".rle"):
                messagebox.showerror("Invalid file", "You selected an RLE file. Use Decompress instead.")
                return


            self.file_label.config(text=f"Compressing: {os.path.basename(filepath)}", fg="black")

            output_path = os.path.join(compressed_path, os.path.basename(filepath) + ".rle")
            original_size, compressed_size = self.compressor.compress_file(filepath, output_path)

            ratio = (compressed_size / original_size)*100 if original_size > 0 else 0

            if compressed_size > original_size:
                result = messagebox.askyesno(title='Warning!',message="The compressed file will be larger than original. Do you want to continue?")
                if result == False:
                    messagebox.showinfo("Compression canceled","Compression canceled")
                    os.remove(output_path)
                    return

            messagebox.showinfo("Compression Complete",
                                f"File saved as:\n{output_path}\n\n"
                                f"Original size: {original_size} bytes\n"
                                f"Compressed size: {compressed_size} bytes\n"
                                f"Compression ratio: {ratio:.2f}%")
            
            self.file_label.config(text=f"Compression completed successfully!", fg="black")

    def decompress_file(self):
        """GUI reference for decompression"""
        filepath = filedialog.askopenfilename(title="Select .rle File to Decompress",initialdir=compressed_path,filetypes=[("RLE Files", "*.rle"), ("All Files", "*.*")])
        if not filepath:
            return

        self.file_label.config(text=f"Decompressing: {os.path.basename(filepath)}", fg="black")

        output_path = os.path.join(decompressed_path,os.path.basename(filepath).replace(".rle", "_decoded.txt"))
        self.compressor.decompress_file(filepath, output_path)

        messagebox.showinfo("Decompression Complete",
                            f"File saved as:\n{output_path}")
        
        self.file_label.config(text=f"Decompression completed successfully!", fg="black")

    

if __name__ =='__main__':
    check_folderinteg()
    root = tk.Tk()
    app = winrarGUI(root)
    root.mainloop()
    