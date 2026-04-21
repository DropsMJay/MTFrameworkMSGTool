import sys
import os
import glob
import struct

#Resident Evil 5 .MGS text inseter by MJay - 2026. Made with ChatGPT help.

#Script procedure:

#Reads .txt files
#Splits the content using <END>
#Converts characters and tags back into 4-byte game data
#Rebuilds the text section
#Reuses the original header
#Updates the file size at 0x08
#Saves the rebuilt file as a new .msg

RE5InvertedAlphabet = { #Convert all chars back to their HEX values
    "0" : "00003D00",
    "1" : "02003D00",
    "2" : "04003D00",
    "3" : "06003D00",
    "4" : "08003D00",
    "5" : "0A003D00",
    "6" : "0C003D00",
    "7" : "0E003D00",
    "8" : "10003D00",
    "9" : "12003D00",
    "!" : "14002100",
    "?" : "16004400",
    "(" : "18002400",
    ")" : "1A002400",
    " " : "1C001F00",
    "&" : "1E004F00",
    ":" : "20002300",
    ";" : "22002300",
    "," : "24001F00",
    "." : "26001F00",
    "\"" : "28003500",
    "'" : "2A001A00",
    "~" : "2C003B00",
    "-" : "2E002400",
    "+" : "30004000",
    "/" : "32001F00",
    "@" : "34003B00",
    "%" : "16015E00",
    "$" : "36003B00",
    "A" : "38004D00",
    "B" : "3A004F00",
    "C" : "3C004F00",
    "D" : "3E004F00",
    "E" : "40004900",
    "F" : "42004400",
    "G" : "44005600",
    "H" : "46004F00",
    "I" : "48001F00",
    "J" : "4A003D00",
    "K" : "4C004F00",
    "L" : "4E004400",
    "M" : "50005B00",
    "N" : "52004F00",
    "O" : "54005600",
    "P" : "56004900",
    "Q" : "58005600",
    "R" : "5A004F00",
    "S" : "5C004900",
    "T" : "5E004100",
    "U" : "60004F00",
    "V" : "62004900",
    "W" : "64006800",
    "X" : "66004900",
    "Y" : "68004800",
    "Z" : "6A004400",
    "a" : "6C003D00",
    "b" : "6E004400",
    "c" : "70003D00",
    "d" : "72004400",
    "e" : "74003D00",
    "f" : "76002400",
    "g" : "78004400",
    "h" : "7A004400",
    "i" : "7C001F00",
    "j" : "7E001D00",
    "k" : "80003D00",
    "l" : "82001F00",
    "m" : "84006200",
    "n" : "86004400",
    "o" : "88004400",
    "p" : "8A004400",
    "q" : "8C004400",
    "r" : "8E002A00",
    "s" : "90003D00",
    "t" : "92002400",
    "u" : "94004400",
    "v" : "96003B00",
    "w" : "98005700",
    "x" : "9A003D00",
    "y" : "9C003A00",
    "z" : "9E003700",
    "[" : "A0043F00",
    "]" : "A2043F00",
    "¡" : "A4002300",
    "¿" : "A6004400",
    "®" : "A8005100",
    "º" : "AA003B00",
    "À" : "AC004F00",
    "Á" : "AE004F00",
    "Â" : "B0004F00",
    "Ä" : "B2004F00",
    "Ç" : "B4004F00",
    "È" : "B6004900",
    "É" : "B8004900",
    "Ê" : "BA004900",
    "Ë" : "BC004900",
    "Ì" : "BE001F00",
    "Í" : "C0001F00",
    "Î" : "C2001F00",
    "Ï" : "C4001F00",
    "Ñ" : "C6004F00",
    "Ò" : "C8005600",
    "Ó" : "CA005600",
    "Ô" : "CC005600",
    "Ö" : "CE005600",
    "Ú" : "D0004F00",
    "Û" : "D2004F00",
    "Ü" : "D4004F00",
    "ß" : "D6004400",
    "à" : "D8003D00",
    "á" : "DA003D00",
    "â" : "DC003D00",
    "ä" : "DE003D00",
    "ç" : "E0003D00",
    "è" : "E2003D00",
    "é" : "E4003D00",
    "ê" : "E6003D00",
    "ë" : "E8003D00",
    "ì" : "EA001F00",
    "í" : "EC001F00",
    "î" : "EE001F00",
    "ï" : "F0001F00",
    "ñ" : "F2004400",
    "ò" : "F4004400",
    "ó" : "F6004400",
    "ô" : "F8004400",
    "ö" : "FA004400",
    "ù" : "FC004400",
    "ú" : "FE004400",
    "û" : "00014400",
    "ü" : "02014400",
    "Œ" : "04015B00",
    "œ" : "06016800",
    "_" : "1A013D00",
    "∞" : "C2046200",
    "*" : "C6042A00",
    "β" : "CA044400",
    "→" : "B0047E00",
    "↑" : "AC047E00",
    "…" : "D2047E00",
}

RE5ButtonCommands = {
    "[BTN A]" : "00001904",
    "[BTN B]" : "01001904",
    "[BTN X]" : "02001904",
    "[BTN Y]" : "03001904",
    "[BTN LS]" : "04001904",
    "[BTN LSu]" : "26001904",
    "[BTN LSd]" : "27001904",
    "[BTN RS]" : "05001904",
    "[BTN START]" : "06001904",
    "[BTN BACK]" : "07001904",
    "[BTN LT]" : "08001904",
    "[BTN RT]" : "09001904",
    "[BTN LB]" : "0A001904",
    "[BTN RB]" : "0B001904",
    "[BTN DPAD]" : "0C001904",
}

RE5SpecialCommands = {
    "[GreenText]" : "03001F04",
    "[RedText]" : "02001F04",
    "[TextColorReset]" : "06001F04",
}

RE5TextAlignCommands = {
    "[CenteredTextIn]" : "00001004",
    "[CenteredTextOut]" : "00001104",
    "[TabSpacing]" : "08013F00",
}

RE5SpeakerCommands = {
    "[Chris]" : "00002804",
    "[Sheva]" : "01002804",
    "[Wesker]" : "07002804",
    "[RadioChatter]" : "04002804",
    "[Josh]" : "02002804",
}

RE5FixedPCKeys = {
    "[BackKey]" : "32002E04",
    "[InteractKey]" : "61002E04",
    "[InventoryKey]" : "16002F04",
    "[ReadyKnifeKey]" : "0D002F04",
    "[ViewMapKey]" : "5D002E04",
    "[F1Key]" : "71002E04",
    "[AimKey]" : "0C002F04",
    "[ReloadKey]" : "04002F04",
    "[LeftArrowKey]" : "38002E04",
    "[AttackKey]" : "0E002F04",
    "[RightArrowKey]" : "3A002E04",
    "[MoveFoward]" : "00002F04",
    "[MoveBackwards]" : "01002F04",
    "[TurnLeft]" : "02002F04",
    "[TurnRight]" : "03002F04",
    "[BackSpaceKey]" : "28002E04",
    "[AttackKey]" : "00001A04",
    "[PartnerOffensive]" : "22002F04",
    "[PartnerDefensive]" : "23002F04",
    "[CallPartner]" : "10002F04",
    "[MouseWheelUp]" : "13002F04",
    "[MouseWheelDown]" : "14002F04",
    "[LocatePartnerKey]" : "0B002F04",
}

RE5SingleBlockCommands = {
    "[OnlinePartner]": "00002404",
}

# Directory from CMD
FileDirectory = sys.argv[1]

TXTFileList = glob.glob(os.path.join(FileDirectory, "*.txt")) #Find all .txt files in the folder
for FilePath in TXTFileList:
    if "_new" in FilePath:
        continue

for FilePath in TXTFileList: #Creates a list with all .txt files inside folder
    FileName = os.path.basename(FilePath)
    print(f"\nProcessing: {FileName}")
    print("DONE!")
    with open(FilePath, "r", encoding="utf-8") as file: #Open and read .txt files with UTF-8 encoding
        FullText = file.read()

    Messages = FullText.split("<END>") #Split the entire file into blocks using <END> delimiter. Messages = List of text blocks
    FileBytes = b"" #b"" = Byte buffer to build the new .msg file

    for TextBlock in Messages[:-1]: #Loop ignore empty blocks. TextBlock = One complete string
        TextBlock = TextBlock.lstrip("\n") #If this text block is empty, skip it
        #TextBlock = TextBlock[1:]
        #continue #Go to the next block

        BlockBytes = b"" #Buffer that accumulates encoded bytes for the current block
        CursorPosition = 0 # Cursor between each value

        while CursorPosition < len(TextBlock): #Goes around the entire string, looking for chars and Tags
            if TextBlock[CursorPosition] == "[": #Search for the beggining of IDs
                IDEnd = TextBlock.find("]", CursorPosition) #Search for the end of IDs

                if IDEnd != -1:
                    FullTag = TextBlock[CursorPosition:IDEnd + 1] #Gets the full text between [ and ]

                    if FullTag in RE5ButtonCommands:
                        BlockBytes += bytes.fromhex("00001904") #Commands related for controls
                        BlockBytes += bytes.fromhex(RE5ButtonCommands[FullTag]) #bytes.fromhex = Convert "readable" bytes to real bytes
                        CursorPosition = IDEnd + 1
                        continue

                    elif FullTag in RE5FixedPCKeys:
                        BlockBytes += bytes.fromhex("00002F04") #Commands related for controls
                        BlockBytes += bytes.fromhex(RE5FixedPCKeys[FullTag]) #bytes.fromhex = Convert "readable" bytes to real bytes
                        CursorPosition = IDEnd + 1
                        continue

                    elif FullTag in RE5SpecialCommands:
                        BlockBytes += bytes.fromhex("00001F04") #Commands related for text color
                        BlockBytes += bytes.fromhex(RE5SpecialCommands[FullTag])
                        CursorPosition = IDEnd + 1
                        continue

                    elif FullTag in RE5SpeakerCommands:
                        BlockBytes += bytes.fromhex("00002804") #Commands related for subtitle speaker
                        BlockBytes += bytes.fromhex(RE5SpeakerCommands[FullTag])
                        CursorPosition = IDEnd + 1
                        continue

                    elif FullTag in RE5TextAlignCommands: #Commands related for text formating
                        BlockBytes += bytes.fromhex(RE5TextAlignCommands[FullTag])
                        CursorPosition = IDEnd + 1
                        continue

                    elif FullTag in RE5SingleBlockCommands:
                        BlockBytes += bytes.fromhex(RE5SingleBlockCommands[FullTag])
                        CursorPosition = IDEnd + 1
                        continue

                    elif ( #Safe RAW bytes
                        len(FullTag) == 10 and
                        all(c in "0123456789ABCDEFabcdef" for c in FullTag[1:-1])
                    ):
                        BlockBytes += bytes.fromhex(FullTag[1:-1])
                        CursorPosition = IDEnd + 1
                        continue

            if TextBlock[CursorPosition] == "|": #Char used to breakline in game
                BlockBytes += bytes.fromhex("00000304")
                CursorPosition += 1
                continue

            char = TextBlock[CursorPosition]
            if char in RE5InvertedAlphabet:
                BlockBytes += bytes.fromhex(RE5InvertedAlphabet[char])
                CursorPosition += 1
            else:
                print(f"Warning. Unknown char: {char}")
                CursorPosition += 1
                continue

        BlockBytes += bytes.fromhex("00000104")
        FileBytes += BlockBytes

    MsgPath = FilePath.replace(".txt", ".msg")
    with open(MsgPath, "rb") as msg_file:
        original_data = msg_file.read()

    Header = bytearray(original_data[:0x40])
    string_count = len([b for b in Messages if b.strip() != ""])

    new_data = Header + FileBytes
    file_size = len(new_data)

    Header[0x08:0x0C] = struct.pack("<I", file_size)
    #Header[0x1C:0x20] = struct.pack("<I", string_count) #I was wrong...

    new_data = Header + FileBytes

    new_msg_path = FilePath.replace(".txt", ".msgNEW")
    with open(new_msg_path, "wb") as out_file:
        out_file.write(new_data)
    
    #DEBUG: See original and new text section area.
    #print(f"{FileName} → New: {len(FileBytes)} | Original: {len(original_data) - 0x40}")
