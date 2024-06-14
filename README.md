# Villagers Data Extractor and Generator - Animal Crossing City Folk/Let's Go to the City

This data extractor is designed to extract and recompress information from binary files containing villager data in the game Animal Crossing. The extractor processes these binary files and produces an Excel file with a changed (extension to avoid mistakes) with the villager information in a readable and organized format.

## Requirements

- Python 3.x
- Python Libraries: `openpyxl`, `tqdm`, `pandas` 

You can install the necessary libraries by running:


## How to Use

1. Clone or download this repository to your local machine.

2. Make sure you have Python 3.x installed on your system.

3. Install the necessary dependencies using the command `pip install -r requirements.txt`.

4. Place the binary file containing the villager data in the same folder as the `npc-pack extractor.py` and `npc-pack generator.py` scripts. Make sure the file has the extension `.bin`.

5. Open a terminal in the location where the files are located:

- Add your `pack.bin` with your villager data ACCF binary file, can be found on a wii ISO Npc/Normal/Setup.

6. Once the process is complete, you will find a generated .acdat file in the same location with the specified name.

7. Open the .acdat with Microsoft Excel, or change the resulted file extension on both python scripts.

## File Structure

- `npc-pack extractor.py`: The main script containing the logic to extract and process the villager data.
- `npc-pack extractor.py`: The secondary script containing the logic to compress the Excel .acdat int a .bin again.
- `requirements.txt`: Text file listing the project's dependencies.
- `example-pack.bin`: A binary file containing the villager data (try to get your own one using WiiScrubber, WiiBaFu or Dolphin).
- `example-pack.acdat`: Example output Excel file containing the villager information.
- `src folder`: containing two files one to recreate the original header for the binaries, and an item list provide by Aurum (https://github.com/SunakazeKun)

## Contributions

Contributions are welcome. If you wish to improve this data extractor, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
