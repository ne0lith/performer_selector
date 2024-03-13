import os
import string
from pathlib import Path
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from typing import List, Dict, Union


class PerformerSelector:
    """
    A class for selecting performers from specified root directories.
    """

    PROMPT_STRING = "Performer: "

    def __init__(
        self, performers_root_directories: List[str], return_full_path: bool = True
    ):
        """
        Initialize the PerformerSelector instance.

        Args:
            performers_root_directories (List[str]): List of root directories where performers are located.
            return_full_path (bool, optional): Flag to determine whether to return full path or just performer name. Defaults to True.
        """
        self.performers_root_directories = performers_root_directories
        self.return_full_path = return_full_path
        self.allowed_characters = set(string.ascii_letters + string.digits + " .()_[]-")
        self.performer_length_limit = 100

    def _is_valid_performer_name(self, name: str) -> bool:
        """
        Check if the performer name is valid.

        Args:
            name (str): Performer name to validate.

        Returns:
            bool: True if the performer name is valid, False otherwise.
        """
        if not name:
            print("Error: Please enter a performer name.")
            return False

        if not all(char in self.allowed_characters for char in name):
            print("Error: Performer name contains invalid characters.")
            return False

        if len(name) > self.performer_length_limit:
            print("Error: Performer name is too long. Please enter a shorter name.")
            return False

        return True

    def _get_direct_subfolders(self, root_path: str) -> List[str]:
        """
        Get the direct subfolders of the root directory.

        Args:
            root_path (str): Root directory path.

        Returns:
            List[str]: List of direct subfolder names.
        """
        try:
            if not os.path.isdir(root_path):
                raise ValueError(
                    f"The provided path '{root_path}' is not a valid directory."
                )

            subfolders = [
                name
                for name in os.listdir(root_path)
                if os.path.isdir(os.path.join(root_path, name))
                and not self._is_junction(os.path.join(root_path, name))
            ]
            return subfolders
        except PermissionError:
            print(f"Permission error accessing '{root_path}'")
            return []
        except OSError as e:
            print(f"Error accessing '{root_path}': {e}")
            return []

    def _is_junction(self, path):
        """
        Determine if a path is a junction.

        Args:
            path: Path to check.

        Returns:
            bool: True if the path is a junction, False otherwise.
        """
        try:
            return bool(os.readlink(path))
        except OSError:
            return False

    def get_performer_paths(self) -> List[Path]:
        """
        Merge the performers into a single list along with their paths.

        Returns:
            List[Path]: List of Path objects representing performer directories.
        """
        performers_paths = []
        for root_dir in self.performers_root_directories:
            performers = self._get_direct_subfolders(root_dir)
            performers_paths.extend(
                [Path(root_dir, performer) for performer in performers]
            )
        return performers_paths

    def choose_performer(self, performers_paths: List[Path]) -> Union[Path, str]:
        """
        Handles user input and returns the selected performer.

        Args:
            performers_paths (List[Path]): List of Path objects representing performer directories.

        Returns:
            Union[Path, str]: Selected performer path or name.
        """
        performers_dict: Dict[str, str] = {
            performer.name: str(performer) for performer in performers_paths
        }

        while True:
            try:
                user_input = prompt(
                    self.PROMPT_STRING,
                    completer=FuzzyWordCompleter(performers_dict.keys()),
                    complete_while_typing=True,
                ).strip()

                if not self._is_valid_performer_name(user_input):
                    continue

                chosen_path = performers_dict.get(user_input)

                if chosen_path:
                    chosen_path_obj = Path(chosen_path)
                    if chosen_path_obj.exists() and chosen_path_obj.is_dir():
                        return (
                            chosen_path_obj
                            if self.return_full_path
                            else chosen_path_obj.name
                        )
                    else:
                        print("Error: The selected performer directory does not exist.")
                else:
                    print("Error: Invalid choice. Please choose a valid performer.")
            except KeyboardInterrupt:
                print("\nExiting...")
                exit(1)


def main():
    performers_root_directories = []
    performer_selector = PerformerSelector(
        performers_root_directories, return_full_path=True
    )
    performers_paths = performer_selector.get_performer_paths()
    chosen_path = performer_selector.choose_performer(performers_paths)
    print(chosen_path)


if __name__ == "__main__":
    main()
