import os
import re
import json


class FileRenamer:
    """
    A class to clean and rename file names in a specified directory,
    while saving the original-to-new name mappings in a JSON file.
    If a file name contains the "｜" character, the part before it is used as the main name,
    and the part after it is considered the date, which is stored in the mapping.
    Additionally, Turkish characters can optionally be converted to their English equivalents.
    """

    def __init__(self, directory: str, mapping_filename: str = "rename_mapping.json", convert_turkish: bool = False):
        """
        Args:
            directory (str): The directory to process.
            mapping_filename (str): The JSON file name where mapping data will be saved.
            convert_turkish (bool): Whether to convert Turkish characters to English.
        """
        self.directory = directory
        self.mapping_filepath = os.path.join(directory, mapping_filename)
        # Mapping: {original_file_name: {"new_name": new_file_name, "date": date_info}}
        self.mapping = {}
        self.convert_turkish = convert_turkish

    def convert_turkish_chars(self, text: str) -> str:
        """
        Converts Turkish characters to their English counterparts.

        Args:
            text (str): The text to convert.

        Returns:
            str: The converted text.
        """
        turkish_mapping = str.maketrans({
            'ü': 'u',
            'Ü': 'U',
            'ö': 'o',
            'Ö': 'O',
            'ş': 's',
            'Ş': 'S',
            'ğ': 'g',
            'Ğ': 'G',
            'ç': 'c',
            'Ç': 'C',
            'ı': 'i',
            'İ': 'I'
        })
        return text.translate(turkish_mapping)

    def clean_file_name(self, file_name: str) -> (str, str):
        """
        Cleans the file name; if the "｜" character exists, the part before it is taken as the main name
        and the part after it is considered the date information.

        Args:
            file_name (str): The original file name.

        Returns:
            tuple: (new_file_name, date_info)
        """
        base_name, ext = os.path.splitext(file_name)
        if "｜" in base_name:
            main_part, date_part = base_name.split("｜", 1)
            date_part = date_part.strip()
        else:
            main_part = base_name
            date_part = ""

        # Remove unwanted characters; keep letters, digits, underscores, spaces, hyphens, and dots.
        cleaned_main = re.sub(r"[^\w\s\-\.]", "", main_part)
        # Replace multiple spaces with an underscore.
        cleaned_main = re.sub(r"\s+", "_", cleaned_main).strip("_")

        if self.convert_turkish:
            cleaned_main = self.convert_turkish_chars(cleaned_main)

        new_file_name = f"{cleaned_main}{ext}"
        return new_file_name, date_part

    def rename_files(self) -> None:
        """
        For each file in the directory, a cleaned name is generated,
        the file is renamed, and the old-to-new mapping is saved in the mapping file.
        """
        for file_name in os.listdir(self.directory):
            old_path = os.path.join(self.directory, file_name)
            if not os.path.isfile(old_path):
                continue

            new_file_name, date_info = self.clean_file_name(file_name)
            new_path = os.path.join(self.directory, new_file_name)

            if old_path != new_path:
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {file_name} -> {new_file_name}")
                    self.mapping[file_name] = {"new_name": new_file_name, "date": date_info}
                except Exception as e:
                    print(f"Error renaming {file_name} -> {new_file_name}: {e}")
            else:
                print(f"No changes for: {file_name}")

        self._save_mapping()

    def _save_mapping(self) -> None:
        """
        Saves the generated mapping data to the JSON file.
        """
        try:
            with open(self.mapping_filepath, "w", encoding="utf-8") as f:
                json.dump(self.mapping, f, indent=4, ensure_ascii=False)
            print(f"Mapping saved: {self.mapping_filepath}")
        except Exception as e:
            print(f"Failed to save mapping: {e}")


class FileNameReverter:
    """
    A class to revert renamed files back to their original names using a previously saved mapping file.
    """

    def __init__(self, directory: str, mapping_filename: str = "rename_mapping.json"):
        """
        Args:
            directory (str): The directory to process.
            mapping_filename (str): The JSON file name containing the mapping data.
        """
        self.directory = directory
        self.mapping_filepath = os.path.join(directory, mapping_filename)
        self.mapping = {}

    def load_mapping(self) -> bool:
        """
        Loads the mapping file.

        Returns:
            bool: True if the mapping file was loaded successfully, False otherwise.
        """
        if not os.path.exists(self.mapping_filepath):
            print(f"Mapping file not found: {self.mapping_filepath}")
            return False
        try:
            with open(self.mapping_filepath, "r", encoding="utf-8") as f:
                self.mapping = json.load(f)
            return True
        except Exception as e:
            print(f"Failed to load mapping file: {e}")
            return False

    def revert_files(self) -> None:
        """
        Reverts the renamed files back to their original names using the mapping file.
        """
        if not self.load_mapping():
            return

        for original_name, info in self.mapping.items():
            new_name = info["new_name"]
            new_path = os.path.join(self.directory, new_name)
            original_path = os.path.join(self.directory, original_name)
            if os.path.exists(new_path):
                try:
                    os.rename(new_path, original_path)
                    print(f"Reverted: {new_name} -> {original_name}")
                except Exception as e:
                    print(f"Error reverting {new_name} to {original_name}: {e}")
            else:
                print(f"Warning: {new_name} not found, cannot revert.")


def main():
    print("Select Operation:")
    print("1: Rename files")
    print("2: Revert file names")
    choice = input("Your choice (1 or 2): ").strip()

    folder_choice = input("Which folder do you want to process? (audio, video, both): ").strip().lower()

    if choice == "1":
        convert_choice = input("Do you want to convert Turkish characters to English? (yes/no): ").strip().lower()
        convert_turkish = convert_choice in ("yes", "y", "evet", "e")

        if folder_choice in ("audio", "both"):
            audio_directory = "audio"
            print("Renaming audio files...")
            audio_renamer = FileRenamer(audio_directory, mapping_filename="audio_rename_mapping.json",
                                        convert_turkish=convert_turkish)
            audio_renamer.rename_files()
        if folder_choice in ("video", "both"):
            video_directory = "video"
            print("Renaming video files...")
            video_renamer = FileRenamer(video_directory, mapping_filename="video_rename_mapping.json",
                                        convert_turkish=convert_turkish)
            video_renamer.rename_files()
    elif choice == "2":
        if folder_choice in ("audio", "both"):
            audio_directory = "audio"
            print("Reverting audio file names...")
            audio_reverter = FileNameReverter(audio_directory, mapping_filename="audio_rename_mapping.json")
            audio_reverter.revert_files()
        if folder_choice in ("video", "both"):
            video_directory = "video"
            print("Reverting video file names...")
            video_reverter = FileNameReverter(video_directory, mapping_filename="video_rename_mapping.json")
            video_reverter.revert_files()
    else:
        print("Invalid selection.")


if __name__ == "__main__":
    main()
