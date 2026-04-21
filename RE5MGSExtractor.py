import sys
import os
import glob

#Resident Evil 5 .MGS text extractor by MJay - 2026. Made with ChatGPT help.

#Some info here:
#All data (and text) is a 4 byte, Little Endian Sequence (Example: 6C003D00 = a)
#0x40 = Header size
#0x08 = File size
#0x1C = Unknown header value (do not overwrite)

#Script procedure:

#Reads .msg files
#Starts reading text data after the 0x40-byte header
#Processes the file in 4-byte little-endian blocks
#Converts normal characters and special commands into readable text
#Exports as .txt, separating each text blocks with <END>

RE5HexToChar = {
    "00003D00" : "0",
    "02003D00" : "1",
    "04003D00" : "2",
    "06003D00" : "3",
    "08003D00" : "4",
    "0A003D00" : "5",
    "0C003D00" : "6",
    "0E003D00" : "7",
    "10003D00" : "8",
    "12003D00" : "9",
    "14002100" : "!",
    "16004400" : "?",
    "18002400" : "(",
    "1A002400" : ")",
    "1C001F00" : " ",
    "1E004F00" : "&",
    "20002300" : ":",
    "22002300" : ";",
    "24001F00" : ",",
    "26001F00" : ".",
    "28003500" : "\"",
    "2A001A00" : "'",
    "2C003B00" : "~",
    "2E002400" : "-",
    "30004000" : "+",
    "32001F00" : "/",
    "34003B00" : "@",
    "16015E00" : "%",
    "36003B00" : "$",
    "38004D00" : "A",
    "3A004F00" : "B",
    "3C004F00" : "C",
    "3E004F00" : "D",
    "40004900" : "E",
    "42004400" : "F",
    "44005600" : "G",
    "46004F00" : "H",
    "48001F00" : "I",
    "4A003D00" : "J",
    "4C004F00" : "K",
    "4E004400" : "L",
    "50005B00" : "M",
    "52004F00" : "N",
    "54005600" : "O",
    "56004900" : "P",
    "58005600" : "Q",
    "5A004F00" : "R",
    "5C004900" : "S",
    "5E004100" : "T",
    "60004F00" : "U",
    "62004900" : "V",
    "64006800" : "W",
    "66004900" : "X",
    "68004800" : "Y",
    "6A004400" : "Z",
    "6C003D00" : "a",
    "6E004400" : "b",
    "70003D00" : "c",
    "72004400" : "d",
    "74003D00" : "e",
    "76002400" : "f",
    "78004400" : "g",
    "7A004400" : "h",
    "7C001F00" : "i",
    "7E001D00" : "j",
    "80003D00" : "k",
    "82001F00" : "l",
    "84006200" : "m",
    "86004400" : "n",
    "88004400" : "o",
    "8A004400" : "p",
    "8C004400" : "q",
    "8E002A00" : "r",
    "90003D00" : "s",
    "92002400" : "t",
    "94004400" : "u",
    "96003B00" : "v",
    "98005700" : "w",
    "9A003D00" : "x",
    "9C003A00" : "y",
    "9E003700" : "z",
    "A0043F00" : "[",
    "A2043F00" : "]",
    "A4002300" : "¡",
    "A6004400" : "¿",
    "A8005100" : "®",
    "AA003B00" : "º",
    "AC004F00" : "À",
    "AE004F00" : "Á",
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
    "D0004F00" : "Ú",
    "D2004F00" : "Û",
    "D4004F00" : "Ü",
    "D6004400" : "ß",
    "D8003D00" : "à",
    "DA003D00" : "á",
    "DC003D00" : "â",
    "DE003D00" : "ä",
    "E0003D00" : "ç",
    "E2003D00" : "è",
    "E4003D00" : "é",
    "E6003D00" : "ê",
    "E8003D00" : "ë",
    "EA001F00" : "ì",
    "EC001F00" : "í",
    "EE001F00" : "î",
    "F0001F00" : "ï",
    "F2004400" : "ñ",
    "F4004400" : "ò",
    "F6004400" : "ó",
    "F8004400" : "ô",
    "FA004400" : "ö",
    "FC004400" : "ù",
    "FE004400" : "ú",
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
    "00001A04" : "[AttackKey]",
    "00002F04" : "[MoveFoward]",
    "01002F04" : "[MoveBackwards]",
    "02002F04" : "[TurnLeft]",
    "03002F04" : "[TurnRight]",
    "04002F04" : "[ReloadKey]",
    "0B002F04" : "[LocatePartnerKey]",
    "0C002F04" : "[AimKey]",
    "0D002F04" : "[ReadyKnifeKey]",
    "0E002F04" : "[AttackKey]",
    "10002F04" : "[CallPartner]",
    "13002F04" : "[MouseWheelUp]",
    "14002F04" : "[MouseWheelDown]",
    "16002F04" : "[InventoryKey]",
    "22002F04" : "[PartnerOffensive]",
    "23002F04" : "[PartnerDefensive]",
    "28002E04" : "[BackSpaceKey]",
    "32002E04" : "[BackKey]",
    "38002E04" : "[LeftArrowKey]",
    "3A002E04" : "[RightArrowKey]",
    "5D002E04" : "[ViewMapKey]",
    "61002E04" : "[InteractKey]",
    "71002E04" : "[F1Key]",
}

RE5SingleBlockCommands = {
    "00002404" : "[OnlinePartner]",
}


#RE5ItemCommand = { #??
#    "00002B04" : "[Item0]",
#    "00002D04" : "[Item1]"
#}

# Directory from CMD
FileDirectory = sys.argv[1]

# Get all .msg files
MGSFiles = glob.glob(os.path.join(FileDirectory, "*.msg"))

# Loop through each file
for FilePath in MGSFiles: #Search .msg files inside given folder
    FileName = os.path.basename(FilePath)
    print(f"\nExtracting: {FileName}")
    print("DONE!")
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

                elif HexValue == "00002404": #Value used for getting the online partner nickname
                    CurrentTextBuffer += "[OnlinePartner]"

                #elif HexValue == "00002B04": #Value used for getting the item
                    #CurrentTextBuffer += "[Item]"

                elif HexValue == "00000104": #Value used to mark the end of the text block
                    TextPath.write(CurrentTextBuffer + "<END>\n")
                    CurrentTextBuffer = ""

                elif HexValue in RE5TextAlignCommands:
                    CurrentTextBuffer += RE5TextAlignCommands[HexValue]

                elif HexValue in RE5HexToChar: #Convert extracted data with table
                    CurrentTextBuffer += RE5HexToChar[HexValue]

                elif HexValue == "00002F04": #Adds CommandID for fixed PC keys
                    NextBlock = DataFile[TextPosition + BlockSize:TextPosition + BlockSize*2]
                    CommandID = NextBlock.hex().upper()

                    if CommandID in RE5FixedPCKeys: #Checks if CommandID exists in RE5FixedPCKeys
                       CurrentTextBuffer += RE5FixedPCKeys[CommandID] #Adds mapped button value to the current text buffer. += = Append value to the current text buffer
                    else:
                        CurrentTextBuffer += f"[00002F04][{CommandID}]" #Adds CommandID value to text within brackets
                    TextPosition += BlockSize * 2 #Advances 2 blocks (8 bytes)
                    continue #Go back to while loop
                else:
                    CurrentTextBuffer += f"[{HexValue}]" #Unknown value, so it keeps hex value for debugging
                TextPosition += BlockSize #Advance loop through file
