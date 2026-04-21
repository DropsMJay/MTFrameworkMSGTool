import sys
import os
import glob

#Devil May Cry 4 .MGS text extractor by MJay - 2026. Made with ChatGPT help.
#(UNFINISHED!!!!)
#Some info here:
#All data (and text) is a 4 byte, Little Endian Sequence (Example: 6C003D00 = a)
#0x40 = Header size
#0x08 = File size
#0x1C = String number

DMC4HexToChar = {
    "00004D00" : "0",
    "02003D00" : "1",
    "04004400" : "2",
    "06003D00" : "3",
    "08003D00" : "4",
    "0A003D00" : "5",
    "0C003D00" : "6",
    "0E003D00" : "7",
    "10003D00" : "8",
    "12003D00" : "9",
    "14001700" : "!",
    "16003C00" : "?",
    "18002400" : "(",
    "1A002400" : ")",
    "1C002800" : " ",
    "1E004F00" : "&",
    "20001600" : ":",
    "22001600" : ";",
    "24001600" : ",",
    "26001700" : ".",
    "28002900" : "\"",
    "2A001700" : "'",
    "2C003B00" : "~",
    "2E002000" : "-",
    "30004000" : "+",
    "32001F00" : "/",
    "34003B00" : "@",
    "16015E00" : "%",
    "36003B00" : "$",
    "38006100" : "A",
    "3A005300" : "B",
    "3C005200" : "C",
    "3E005B00" : "D",
    "40005100" : "E",
    "42004D00" : "F",
    "44005B00" : "G",
    "46004F00" : "H",
    "48001E00" : "I",
    "4A004700" : "J",
    "4C005400" : "K",
    "4E004B00" : "L",
    "50006F00" : "M",
    "52005A00" : "N",
    "54006300" : "O",
    "56004800" : "P",
    "58006A00" : "Q",
    "5A005100" : "R",
    "5C004D00" : "S",
    "5E005100" : "T",
    "60005100" : "U",
    "62005400" : "V",
    "64007D00" : "W",
    "66004900" : "X",
    "68005000" : "Y",
    "6A004400" : "Z",
    "6C003D00" : "a",
    "6E004700" : "b",
    "70004000" : "c",
    "72004500" : "d",
    "74004100" : "e",
    "76002B00" : "f",
    "78004300" : "g",
    "7A004500" : "h",
    "7C001D00" : "i",
    "7E001800" : "j",
    "80004600" : "k",
    "82001C00" : "l",
    "84006D00" : "m",
    "86004400" : "n",
    "88004500" : "o",
    "8A004600" : "p",
    "8C004400" : "q",
    "8E002C00" : "r",
    "90003B00" : "s",
    "92002800" : "t",
    "94004600" : "u",
    "96004100" : "v",
    "98005F00" : "w",
    "9A004100" : "x",
    "9C004300" : "y",
    "9E003700" : "z",
    "A0043F00" : "[",
    "A2043F00" : "]",
    "A4001700" : "¡",
    "A6003C00" : "¿",
    "A8005100" : "®",
    "AA003B00" : "º",
    "AC004F00" : "À",
    "AE006000" : "Á",
    "B0004F00" : "Â",
    "B2004F00" : "Ä",
    "B4004F00" : "Ç",
    "B6004900" : "È",
    "B8004900" : "É",
    "BA004900" : "Ê",
    "BC004900" : "Ë",
    "BE001F00" : "Ì",
    "C0001F00" : "Í",
    "C2001F00" : "Î",
    "C4001F00" : "Ï",
    "C6004F00" : "Ñ",
    "C8005600" : "Ò",
    "CA005600" : "Ó",
    "CC005600" : "Ô",
    "CE005600" : "Ö",
    "D0005100" : "Ú",
    "D2004F00" : "Û",
    "D4004F00" : "Ü",
    "D6004400" : "ß",
    "D8003D00" : "à",
    "DA003D00" : "á",
    "DC003D00" : "â",
    "DE003D00" : "ä",
    "E0004000" : "ç",
    "E2003D00" : "è",
    "E4004100" : "é",
    "E6004100" : "ê",
    "E8003D00" : "ë",
    "EA001F00" : "ì",
    "EC002200" : "í",
    "EE001F00" : "î",
    "F0001F00" : "ï",
    "F2004500" : "ñ",
    "F4004400" : "ò",
    "F6004500" : "ó",
    "F8004500" : "ô",
    "FA004400" : "ö",
    "FC004400" : "ù",
    "FE004500" : "ú",
    "00014400" : "û",
    "02014400" : "ü",
    "04015B00" : "Œ",
    "06016800" : "œ",
    "1A013D00" : "_",
    "C2046200" : "∞",
    "C6042A00" : "*",
    "CA044400" : "β",
    "B0047E00" : "→",
    "AC047E00" : "↑",
    "D2047E00" : "…",
}

RE5ButtonCommands = {
    "00001904" : "[BTN A]",
    "01001904" : "[BTN B]",
    "02001904" : "[BTN X]",
    "03001904" : "[BTN Y]",
    "04001904" : "[BTN LS]",
    "26001904" : "[BTN LSu]",
    "27001904" : "[BTN LSd]",
    "05001904" : "[BTN RS]",
    "06001904" : "[BTN START]",
    "07001904" : "[BTN BACK]",
    "08001904" : "[BTN LT]",
    "09001904" : "[BTN RT]",
    "0A001904" : "[BTN LB]",
    "0B001904" : "[BTN RB]",
    "0C001904" : "[BTN DPAD]",
}

RE5SpecialCommands = {
    "03001F04" : "[GreenText]",
    "02001F04" : "[RedText]",
    "06001F04" : "[TextColorReset]",
}

RE5TextAlignCommands = {
    "00001004" : "[CenteredTextIn]",
    "00001104" : "[CenteredTextOut]",
    "08013F00" : "[TabSpacing]",
}

RE5SpeakerCommands = {
    "00002804" : "[Chris]",
    "01002804" : "[Sheva]",
    "07002804" : "[Wesker]",
    "04002804" : "[RadioChatter]",
    "02002804" : "[Josh]",
}

RE5FixedPCKeys = {
    "32002E04" : "[BackKey]",
    "61002E04" : "[InteractKey]",
    "00001A04" : "[ConfirmKey]",
    "16002F04" : "[InventoryKey]",
    "0D002F04" : "[ReadyKnifeKey]",
    "5D002E04" : "[ViewMapKey]",
    "71002E04" : "[F1Key]",
    "0C002F04" : "[AimKey]",
    "04002F04" : "[ReloadKey]",
    "38002E04" : "[LeftArrowKey]",
    "0E002F04" : "[AttackKey]",
    "3A002E04" : "[RightArrowKey]",
    "00002F04" : "[MoveFoward]",
    "01002F04" : "[MoveBackwards]",
    "02002F04" : "[TurnLeft]",
    "03002F04" : "[TurnRight]",
    "28002E04" : "[BackSpaceKey]",
    "00001A04" : "[AttackKey]",
    "22002F04" : "[PartnerOffensive]",
    "23002F04" : "[PartnerDefensive]",
    "10002F04" : "[CallPartner]",
    "13002F04" : "[MouseWheelUp]",
    "14002F04" : "[MouseWheelDown]",
    "0B002F04" : "[LocatePartnerKey]",
}

# Directory from CMD
FileDirectory = sys.argv[1]

# Get all .msg files
MGSFiles = glob.glob(os.path.join(FileDirectory, "*.msg"))

# Loop through each file
for FilePath in MGSFiles: #Search .msg files inside given folder
    with open(FilePath, "rb") as file:
        DataFile = file.read() #Read entire file into memory (bytes)
        TextPosition = 0x40 #Start of text section (0x40). Acts as a cursor while reading the file
        CurrentTextBuffer = "" #Creates and stores readed chars
        BlockSize = 4
        TextPath = FilePath.replace(".msg", ".txt")

        with open(TextPath, "w", encoding="utf-8") as TextPath: #Create text file (decoded strings)

            while TextPosition < len(DataFile): #Search for texts until the end of the file. DataFile = Total file size
                DataBlock = DataFile[TextPosition:TextPosition+BlockSize] #Read 4 bytes from current position (each char = 4 bytes)
                HexValue = DataBlock.hex().upper() #Convert values into text (.hex converts everything into hexacimal text - .upper makes everything upper case)

                if HexValue == "00001904": #Detects the initializer for special commands (Buttons, Text alignment?)
                    NextBlock = DataFile[TextPosition + BlockSize:TextPosition + BlockSize*2] #Reads next data block
                    CommandID = NextBlock.hex().upper() #CommandID = Value that defines a special command
                    if CommandID in RE5ButtonCommands: #Checks if CommandID exists in RE5ButtonCommands
                        CurrentTextBuffer += RE5ButtonCommands[CommandID] #Adds mapped button value to the current text buffer. += = Append value to the current text buffer
                    else:
                        CurrentTextBuffer += f"[00001904][{CommandID}]" #Adds CommandID value to text within brackets
                    TextPosition += BlockSize * 2 #Advances 2 blocks (8 bytes)
                    continue #Go back to while loop

                elif HexValue == "00001F04": #Special commands for color/Tab identation
                    NextBlock = DataFile[TextPosition + BlockSize:TextPosition + BlockSize*2]
                    CommandID = NextBlock.hex().upper()
                    if CommandID in RE5SpecialCommands:
                        CurrentTextBuffer += RE5SpecialCommands[CommandID]
                    else:
                        CurrentTextBuffer += f"[00001F04][{CommandID}]"
                    TextPosition += BlockSize * 2
                    continue

                elif HexValue == "00002804": #Special commands for subtitles/characters
                    NextBlock = DataFile[TextPosition + BlockSize:TextPosition + BlockSize*2]
                    CommandID = NextBlock.hex().upper()
                    if CommandID in RE5SpeakerCommands:
                        CurrentTextBuffer += RE5SpeakerCommands[CommandID]
                    else:
                        CurrentTextBuffer += f"[00002804][{CommandID}]"
                    TextPosition += BlockSize * 2
                    continue

                elif HexValue == "00000304": #Value used for line break
                    CurrentTextBuffer += "|"

                elif HexValue == "00000604": #Value used for getting the online partner nickname
                    CurrentTextBuffer += "¤"

                elif HexValue == "00000104": #Value used to mark the end of the text block
                    TextPath.write(CurrentTextBuffer + "<END>\n")
                    CurrentTextBuffer = ""

                elif HexValue in RE5TextAlignCommands:
                    CurrentTextBuffer += RE5TextAlignCommands[HexValue]

                elif HexValue in DMC4HexToChar: #Convert extracted data with table
                    CurrentTextBuffer += DMC4HexToChar[HexValue]

                elif HexValue == "00002F04": #Adds CommandID for fixed PC keys
                    NextBlock = DataFile[TextPosition + BlockSize:TextPosition + BlockSize*2]
                    CommandID = NextBlock.hex().upper()
                    if CommandID in RE5FixedPCKeys: #Checks if CommandID exists in RE5FixedPCKeys
                       CurrentTextBuffer += RE5FixedPCKeys[CommandID] #Adds mapped button value to the current text buffer. += = Append value to the current text buffer
                    else:
                        CurrentTextBuffer += f"[00002E04][{CommandID}]" #Adds CommandID value to text within brackets
                    TextPosition += BlockSize * 2 #Advances 2 blocks (8 bytes)
                    continue #Go back to while loop
                else:
                    CurrentTextBuffer += f"[{HexValue}]" #Unknown value, so it keeps hex value for debugging
                TextPosition += BlockSize #Advance loop through file