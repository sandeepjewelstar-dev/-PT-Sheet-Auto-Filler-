"""
Main GUI Application - PT Sheet Auto-Filler
User-friendly interface to process CAD images and auto-fill Excel sheets
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
import logging
from datetime import datetime

from ocr_extractor import extract_from_image
from excel_writer import fill_pt_sheet, validate_filled_sheet
from validator import validate_data, generate_validation_report

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PTSheetAutoFillerApp:
    """Main GUI Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔮 PT Sheet Auto-Filler v1.0")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        
        # Set style
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.image_path = tk.StringVar()
        self.template_path = tk.StringVar()
        self.processing = False
        
        # Build UI
        self.build_ui()
        
        logger.info("✅ Application started successfully")
    
    def build_ui(self):
        """Build the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="💎 PT Sheet Auto-Filler",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Automatic CAD Image to Excel PT Sheet Conversion",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section 1: Image Selection
        self.build_section(
            main_frame,
            "Step 1: Select CAD Image",
            self.image_path,
            self.select_image,
            "*.jpg *.png *.pdf"
        )
        
        # Section 2: Template Selection
        self.build_section(
            main_frame,
            "Step 2: Select Excel Template",
            self.template_path,
            self.select_template,
            "*.xlsx"
        )
        
        # Section 3: Process Button
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=20)
        
        self.process_btn = tk.Button(
            button_frame,
            text="⚡ Process & Fill Excel",
            command=self.process_files,
            font=("Arial", 12, "bold"),
            bg='#27ae60',
            fg='white',
            height=2,
            cursor='hand2'
        )
        self.process_btn.pack(fill=tk.X)
        
        # Section 4: Progress and Status
        status_frame = tk.LabelFrame(
            main_frame,
            text="📊 Processing Status",
            bg='#f0f0f0',
            font=("Arial", 10, "bold")
        )
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X, padx=10, pady=10)
        
        # Status text
        self.status_text = tk.Text(
            status_frame,
            height=12,
            width=60,
            font=("Courier", 9),
            bg='white',
            fg='#2c3e50'
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(self.status_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.status_text.yview
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#ecf0f1')
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = tk.Label(
            footer_frame,
            text="💼 PT Sheet Auto-Filler © 2024 | Offline Software",
            font=("Arial", 8),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        footer_label.pack(pady=10)
    
    def build_section(self, parent, title, var, callback, file_types):
        """Build a file selection section"""
        
        section = tk.LabelFrame(
            parent,
            text=title,
            bg='#f0f0f0',
            font=("Arial", 10, "bold")
        )
        section.pack(fill=tk.X, pady=10)
        
        # Display selected file
        display_label = tk.Label(
            section,
            textvariable=var,
            bg='white',
            fg='#2c3e50',
            font=("Arial", 9),
            wraplength=400,
            justify=tk.LEFT,
            relief=tk.SUNKEN,
            padx=10,
            pady=10
        )
        display_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Browse button
        browse_btn = tk.Button(
            section,
            text="📁 Browse...",
            command=callback,
            bg='#3498db',
            fg='white',
            font=("Arial", 9),
            cursor='hand2'
        )
        browse_btn.pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def select_image(self):
        """Select CAD image file"""
        file_path = filedialog.askopenfilename(
            title="Select CAD Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png"),
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.image_path.set(file_path)
            self.log(f"✅ Selected image: {Path(file_path).name}")
    
    def select_template(self):
        """Select Excel template file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel Template",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.template_path.set(file_path)
            self.log(f"✅ Selected template: {Path(file_path).name}")
    
    def process_files(self):
        """Main processing function"""
        
        # Validate inputs
        if not self.image_path.get():
            messagebox.showerror("Error", "Please select a CAD image")
            return
        
        if not self.template_path.get():
            messagebox.showerror("Error", "Please select an Excel template")
            return
        
        # Disable button during processing
        self.process_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        # Run processing in separate thread
        thread = threading.Thread(target=self.process_thread)
        thread.daemon = True
        thread.start()
    
    def process_thread(self):
        """Processing thread"""
        
        try:
            self.log("\n" + "="*60)
            self.log("🚀 STARTING PT SHEET AUTO-FILL PROCESS")
            self.log("="*60)
            
            # Step 1: Extract from image
            self.log("\n📸 Step 1: Extracting data from CAD image...")
            self.log(f"   Image: {Path(self.image_path.get()).name}")
            
            extracted_data = extract_from_image(self.image_path.get())
            
            if not extracted_data:
                raise Exception("Failed to extract data from image")
            
            self.log("✅ Data extraction completed")
            
            # Step 2: Validate data
            self.log("\n🔍 Step 2: Validating extracted data...")
            is_valid, errors = validate_data(extracted_data)
            
            if not is_valid:
                self.log(f"⚠️  Validation warnings: {len(errors)} issues found")
                for error in errors[:5]:  # Show first 5 errors
                    self.log(f"   ⚠️  {error}")
            else:
                self.log("✅ All data validation checks passed")
            
            # Step 3: Fill Excel
            self.log("\n✍️  Step 3: Filling Excel PT sheet...")
            self.log(f"   Template: {Path(self.template_path.get()).name}")
            
            output_file = fill_pt_sheet(self.template_path.get(), extracted_data)
            
            if not output_file:
                raise Exception("Failed to fill Excel sheet")
            
            self.log(f"✅ Excel sheet filled successfully")
            self.log(f"   Output: {Path(output_file).name}")
            
            # Step 4: Validate filled sheet
            self.log("\n📋 Step 4: Validating filled Excel sheet...")
            is_sheet_valid = validate_filled_sheet(output_file)
            
            if is_sheet_valid:
                self.log("✅ Excel sheet validation passed")
            else:
                self.log("⚠️  Some fields may be empty")
            
            # Summary
            self.log("\n" + "="*60)
            self.log("✅ PROCESS COMPLETED SUCCESSFULLY!")
            self.log("="*60)
            self.log(f"\n📊 Extracted Data Summary:")
            self.log(f"   Product ID: {extracted_data.get('product_id', 'N/A')}")
            self.log(f"   CAD Person: {extracted_data.get('cad_person', 'N/A')}")
            self.log(f"   Materials: {len(extracted_data.get('materials', {}))}")
            self.log(f"   Stones: {len(extracted_data.get('stones', []))}")
            self.log(f"   Total QTY: {extracted_data.get('total_qty', 'N/A')}")
            self.log(f"\n💾 Output File: {output_file}")
            
            messagebox.showinfo(
                "Success! ✅",
                f"Excel PT sheet filled successfully!\n\n"
                f"Output file:\n{output_file}"
            )
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}")
            messagebox.showerror("Error", f"Processing failed:\n{str(e)}")
            logger.error(f"Processing error: {str(e)}", exc_info=True)
        
        finally:
            self.progress.stop()
            self.process_btn.config(state=tk.NORMAL)
            self.root.after(0, lambda: self.status_text.see(tk.END))
    
    def log(self, message):
        """Log message to status text area"""
        self.status_text.insert(tk.END, message + "\n")
        self.root.update()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PTSheetAutoFillerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
