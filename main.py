import os
import platform
import datetime
import concurrent.futures
from PIL import Image
import pyheif
from tqdm import tqdm
import questionary
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for automatic reset after each print

def convert_heic_to_jpg(heic_file_path, output_directory):
    try:
        heif_file = pyheif.read(heic_file_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        output_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(heic_file_path))[0] + '.jpg')
        image.save(output_file_path, "JPEG")
        return True
    except Exception as e:
        print(Fore.RED + f"Error converting {heic_file_path}: {e}")
        return False

def navigate_folders(current_path='.'):
    print(Fore.CYAN + "\nNavigating directories...")
    while True:
        heic_count = len([file for file in os.listdir(current_path) if file.lower().endswith('.heic')])
        print(Fore.YELLOW + "\nCurrent directory: ", Fore.GREEN + f"{current_path} (HEIC files: {heic_count})\n")
        print(Fore.CYAN + "Navigate to the folder containing your HEIC files.")
        print("Select '✅  Use {folder_name}' to confirm the folder for conversion.")
        print("Select '..' to go up one level.\n")

        folder_name = os.path.basename(current_path) or 'this folder'
        items = ['..'] + [f"✅  Use {folder_name}"] + [f"📂 {item}" for item in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, item))]
        selected = questionary.select(
            "Choose a directory:",
            choices=items
        ).ask()

        if selected == '..':
            current_path = os.path.dirname(current_path) or '.'
        elif selected == f"✅  Use {folder_name}":
            return current_path
        else:
            new_path = os.path.join(current_path, selected[2:])  # Remove the '📂 ' prefix
            if os.path.isdir(new_path):
                current_path = new_path

def main():
    print("HEIC to JPEG Converter")
    input_folder = navigate_folders()
    if not input_folder:
        print("No folder selected, exiting.")
        return

    print(Fore.CYAN +f"\nSelected folder: {input_folder}\n")

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    output_folder = os.path.join(input_folder, f"converted_{current_time}")
    os.makedirs(output_folder, exist_ok=True)

    heic_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.lower().endswith('.heic')]
    if not heic_files:
        print("No HEIC files found in the selected directory.")
        return

    print(f"Converting {len(heic_files)} HEIC files...")

    successful_conversions = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(convert_heic_to_jpg, heic_file, output_folder): heic_file for heic_file in heic_files}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), unit="file", desc="Converting Files", ascii=True):
            if future.result():
                successful_conversions += 1

    print(Fore.GREEN +f"\nConversion complete. {successful_conversions} files converted successfully out of {len(heic_files)}. 🎉")

def clear_console():
    os_name = platform.system()
    if os_name == 'Windows':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux and macOS

if __name__ == "__main__":
    clear_console()
    main()
