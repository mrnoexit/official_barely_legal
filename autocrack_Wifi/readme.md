HS

This directory contains scripts for processing WPA handshake files.
Dependencies

This script requires the following dependencies:

    hcxpcapngtool: Used for converting pcap files to HC22000 format
    hashcat: Used for cracking the WPA handshakes

Usage

    Place this script in the same directory as your handshake files.
    Run the script: python3 process.py.

This script will automatically convert your handshake files to HC22000 format and attempt to crack them using hashcat.
Output

The script will generate the following output:

    HC22000 files: These files will be used for cracking with hashcat.
    Crack output files: These files will contain the cracked passwords for each handshake.

Supported Formats

This script supports the following file formats:

    .cap: WPA handshake files captured using Wireshark.
    .hccap: WPA handshake files converted to HC22000 format.
    .22000: HC22000 format files.

Disclaimer

This script is intended for educational purposes only. Use at your own risk.
