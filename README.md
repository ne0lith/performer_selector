# Performer Selector

Performers Selector is a Python module designed to facilitate the selection of performers from specified root directories. This can be useful in scenarios where you have a collection of performers stored in different directories and you need to select one of them.

## Features

- Select performers from specified root directories.
- Allows customization of whether to return full path or just performer name.
- Handles user input with fuzzy autocomplete features.
- Validates performer names and directory paths.

## Installation

Performers Selector can be installed using pip:

```bash
pip install -e git+https://github.com/ne0lith/performer_selector.git#egg=performer_selector
```

## Usage

```python
from performers_selector import PerformerSelector

# Define root directories containing performer directories
performers_root_directories = ["/path/to/root/directory1", "/path/to/root/directory2"]

# Initialize PerformerSelector instance
performer_selector = PerformerSelector(
    performers_root_directories, return_full_path=True
)

# Get performer paths
performers_paths = performer_selector.get_performer_paths()

# Choose a performer
chosen_path = performer_selector.choose_performer(performers_paths)

print(chosen_path)
```

## Example

```python
performers_root_directories = ["/home/user/artists", "/home/user/bands"]
performer_selector = PerformerSelector(performers_root_directories)
performers_paths = performer_selector.get_performer_paths()
chosen_path = performer_selector.choose_performer(performers_paths)
print(chosen_path)
```
