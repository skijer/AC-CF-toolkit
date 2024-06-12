# Villagers Data Extractor - Animal Crossing

This data extractor is designed to extract information from binary files containing villager data in the game Animal Crossing. The extractor processes these binary files and produces an Excel file with the villager information in a readable and organized format.

## Requirements

- Python 3.x
- Python Libraries: `openpyxl`

You can install the necessary libraries by running:


## How to Use

1. Clone or download this repository to your local machine.

2. Make sure you have Python 3.x installed on your system.

3. Install the necessary dependencies using the command `pip install -r requirements.txt`.

4. Place the binary file containing the villager data in the same folder as the `npc-pack extractor.py` script. Make sure the file has the extension `.bin`.

5. Open a terminal in the location where the files are located:

- Replace `pack.bin` with your villager data ACCF binary file, can be found on a wii ISO Npc/Normal/Setup.

6. Once the process is complete, you will find a generated Excel file in the same location with the specified name.

## File Structure

- `npc-pack extractor.py`: The main script containing the logic to extract and process the villager data.
- `requirements.txt`: Text file listing the project's dependencies.
- `example-pack.bin`: A binary file containing the villager data (not provided with a real one for legal reasons, get your own one using WiiScrubber, WiiBaFu or Dolphin).
- `example-pack.xlsx`: Example output Excel file containing the villager information.

## Contributions

Contributions are welcome. If you wish to improve this data extractor, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
