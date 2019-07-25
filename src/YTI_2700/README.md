# README.md - loqoman 2019/07/25

Writing a file is psudocode to help understand the extact sequence of messages
Message sequencing is more important than figuring out serial/tcp implementation,
and the best way to be productivee is to have both on hand, and implement the proper one.

## YTI Message Sequence  

### --- Debugging --- 

    make HANDSKAE
    SET [RESULT REPORTING MODE] <TR0>
    DISABLE PRINTER <TP0>

    # Reporting system information

    REPORT MODEL NUMBER <V0>
    REPORT SOFTWARE VERSION <V1>
    REPORT SOFTWARE REVISION <V2>
    REPORT SYSTEM TIME <RM>

    # Reporting current status

    REPORT MACHINE STATUS <RY>
    

### --- Communication proof of concept ---

Obj: Prove communication can be estabished with the YTI 2700 SELECT

Settings:

    Baud: 9600
    Data Length: 7
    Parity Bit: Even (See: https://en.wikipedia.org/wiki/Parity_bit)
    Stop Bit: 1 (Currently seems irrelevent. See: https://electronics.stackexchange.com/questions/335695/why-the-start-bit-and-the-stop-bits-are-necessary)
    Handshake: None (From RTS/CTS)
    Configuration: Non-Multidrop

Commands:

    Nb on handshakes:
        The RTS/CTS handshake seems to be a matter of driving physical wires
        HIGH/LOW, and seems unnessissary for a proof-of-concept.
        Based on preliminary research, it seems like XON/OFF seems to make the most sense, but
        it is a possibility hardware flow control is automaticlly implemented, and behaves
        functionally similar to having 'None' Handshake.

    

