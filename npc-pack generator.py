import pandas as pd
from tqdm import tqdm
'''Code made to recompile the data from the xlsx, eventhought the file extension is changed you can open it with Excel
   I did the code and optimized with chatgpt, so keep on mind that this may be broke in order to make it faster
   you can add new items to the item list just complete the data as in aurums' item list
   you can also add new model masters and brres, those files are on npc/normal folders'''
def encode_utf16_be_fixed_length(text, length):
    """Encodes the string to UTF-16BE and pads or truncates it to the specified byte length."""
    encoded = text.encode('utf-16-be')
    if len(encoded) > length:
        encoded = encoded[:length]
    elif len(encoded) < length:
        encoded += b'\x00' * (length - len(encoded))
    return encoded

def get_byte_from_nibbles(high_nibble, low_nibble):
    """Combine high and low nibbles into a single byte."""
    return (high_nibble << 4) | low_nibble

def reverse_personality(value):
    """Convert personality string back to the byte representation."""
    stat_characteristics = ["Lazy", "Jock", "Cranky", "Normal", "Peppy", "Snooty"]
    if value in stat_characteristics:
        return stat_characteristics.index(value)
    else:
        raise ValueError(f"Invalid personality: {value}")

def reverse_favorite_furniture_styles(value):
    """Convert favorite furniture styles string back to the byte representation."""
    stat_characteristics = ["", "", "", "", "", "Playful and Retro", "Dignified and Retro", "", "", "Playful and Trendy", "Dignified and Trendy"]
    if value in stat_characteristics:
        return stat_characteristics.index(value)
    else:
        raise ValueError(f"Invalid furniture style: {value}")

def combine_personality_and_styles(personality, style):
    """Combine personality and favorite furniture styles into a single byte."""
    high_nibble = reverse_personality(personality)
    low_nibble = reverse_favorite_furniture_styles(style)
    return get_byte_from_nibbles(high_nibble, low_nibble)

def read_excel_data(input_path):
    """Read the Excel file and load the sheet named 'Villager Data'."""
    return pd.read_excel(input_path, sheet_name='Villager Data')

def load_item_data(item_path):
    """Read the item data from the Excel file and convert to dictionary for fast lookup."""
    df_items = pd.read_excel(item_path, engine='openpyxl')
    item_dict = {}
    for _, row in df_items.iterrows():
        try:
            hex_id = int(str(row['HEX ID']), 16)
            item_dict[row['English']] = hex(hex_id * 4 + 0x9000)[2:]
        except ValueError:
            item_dict[row['English']] = "FFF1"  # Or handle appropriately if 'HEX ID' cannot be converted

    return item_dict


def feature_hex_transform(data, item_dict):
    """Transform hex feature from data based on item dictionary."""
    return item_dict.get(data, "FFF1")

def write_bin_file(output_path, df, item_dict):
    with open(output_path, 'wb') as bin_file:
        # Read header.bin and write its contents to the output binary file
        with open('src/header.bin', 'rb') as header_file:
            header_data = header_file.read()
            bin_file.write(header_data)

        for index, row in tqdm(df.iterrows(), total=len(df), desc="Writing binary file"):
            # Write House information
            bin_file.write(bytes.fromhex("00"))  # Column: 'space' (Hexadecimal)
            bin_file.write(int(row['Master model number']).to_bytes(1, byteorder='big'))  # Column: 'Master model number' (Integer)

            # Write Default shirt to Item 11 (columns 3 to 17)
            for item in ['Default shirt', 'Default Floor', 'Default Wall', 'Default Parasol', 'Item 01', 'Item 02', 'Item 03', 'Item 04', 'Item 05', 'Item 06', 'Item 07', 'Item 09', 'Item 10', 'Item 11', 'K.K. Song']:
                value = row[item]
                if isinstance(value, str):
                    transformed_value = feature_hex_transform(value, item_dict)
                    bin_file.write(bytes.fromhex(transformed_value))
                else:
                    bin_file.write(bytes.fromhex("FFF1"))

            # Write K.K. Song and Unknown (columns 18 and 19)
            bin_file.write(bytes.fromhex(row['Unknown']))  # Column: 'Unknown' (Hexadecimal)

            # Write Japanese to Korean (columns 20 to 27) with exact 9 characters (18 bytes)
            for lang in ['Japanese', 'English', 'Spanish America', 'Spanish', 'French', 'Italian', 'German', 'Korean']:
                encoded = encode_utf16_be_fixed_length(row[lang], 18)  # 9 characters * 2 bytes/char = 18 bytes
                bin_file.write(encoded)

            # Write Catch-Phrases (columns 28 to 37) with exact 11 characters (22 bytes)
            for lang in ["Catch-Japanese", "Catch-English US", "Catch-Spanish America", "Catch-French Canada", "Catch-English", "Catch-Spanish", "Catch-French", "Catch-Italian", "Catch-German", "Catch-Korean"]:
                encoded = encode_utf16_be_fixed_length(row[lang], 22)  # 11 characters * 2 bytes/char = 22 bytes
                bin_file.write(encoded)

            # Write Japanese to Korean (columns 28 to 36)
            for stat in ['Specie', 'Month of birth', 'Day of birth', 'Unknown-Stat', 'Favorite clothing', 'Less favorite clothing', 'Favorite furniture color', 'Favorite furniture series', 'Personality', 'Starting villager']:
                value = row[stat]
                if stat == 'Specie':
                    # Write as index of characteristic lists
                    stat_characteristics = ["cat", "elephant", "sheep", "bear", "dog", "squirrel", "rabbit", "duck", "hip", "wolf", "mouse", "pig", "chicken", "bull", "cow", "bird", "frog", "alligator", "goat", "tiger", "anteater", "koala", "horse", "octopus", "lion", "bear cub", "rhinoceros", "gorilla", "ostrich", "kangaroo", "eagle", "penguin", "monkey"]
                    bin_file.write(stat_characteristics.index(value).to_bytes(1, byteorder='big'))
                elif stat in ['Month of birth', 'Day of birth']:
                    bin_file.write(int(value).to_bytes(1, byteorder='big'))
                elif stat == 'Unknown-Stat':
                    bin_file.write(bytes.fromhex(row['Unknown-Stat']))
                elif stat in ['Favorite clothing', 'Less favorite clothing']:
                    # Write as index of characteristic lists
                    stat_characteristics = ["cute", "cool", "subtle", "gaudy", "strange", "funky", "refined", "fresh", "stylish", "striking"]
                    bin_file.write(stat_characteristics.index(value).to_bytes(1, byteorder='big'))
                elif stat == 'Favorite furniture color':
                    # Write as index of characteristic lists
                    stat_characteristics = ["", "yellow", "red", "orange", "green", "blue", "white", "black", "purple", "brown", "pink", "gray", "colorful", "aqua", "beige"]
                    bin_file.write(stat_characteristics.index(value).to_bytes(1, byteorder='big'))
                elif stat == 'Favorite furniture series':
                    # Write as index of characteristic lists
                    stat_characteristics = ["Exotic series", "Lovely series", "Classic series", "Ranch series", "Cabana series", "Blue series", "Modern series", "Regal series", "Green series", "Cabin series", "Kiddies series", "Robo series"]
                    bin_file.write(stat_characteristics.index(value).to_bytes(1, byteorder='big'))
                elif stat == 'Personality':
                    # Write the byte of the combination of both
                    personality_byte = combine_personality_and_styles(row['Personality'], row['Favorite furniture styles'])
                    bin_file.write(personality_byte.to_bytes(1, byteorder='big'))
                elif stat == 'Starting villager':
                    # Write as hexadecimal '80' (Yes) or '00' (No)
                    bin_file.write(bytes.fromhex('80') if value == 'Yes' else bytes.fromhex('00'))
        # Write 16 bytes of empty data
        bin_file.write(b'\x00' * 16)

def excel_to_bin(input_path, output_path, item_path):
    # Read data from Excel file
    df = read_excel_data(input_path)
    # Load item data
    item_dict = load_item_data(item_path)
    # Write data to binary file
    write_bin_file(output_path, df, item_dict)

# Execute the conversion
if __name__ == "__main__":
    excel_to_bin('pack.acdat', 'new-pack.bin', "src/aurum's-item-list.xlsx")
