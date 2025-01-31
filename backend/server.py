import subprocess

ascii_art = """
      ____          _    _ _               _            ____                              _
     | ___ \\       | |  | | |             | |          /  __ \\                           | |
     | |_/ /___ ___| |  | | |__   ___  ___| |___ ______| /  \\/ ___  _ __  _ __   ___  ___| |_
     |    // _ \\_  / |/\\| | '_ \\ / _ \\/ _ \\ / __|______| |    / _ \\| '_ \\| '_ \\ / _ \\/ __| __|
     | |\\ \\  __// /\\  /\\  / | | |  __/  __/ \\__ \\      | \\__/\\ (_) | | | | | | |  __/ (__| |_
     \\_| \\_\\___/___|\\/  \\/|_| |_|\\___|\\___|_|___/       \\____/\\___/|_| |_|_| |_|\\___|\\___|\\__|

↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑         ↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑      ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑     ↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑                                    ↑↑↑↑↑↑        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑↑   ↑↑↑↑↑↑↑  ↑↑↑↑↑     ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑      ↑↑↑↑↑↑↑     ↑       ↑  ↑ ↑↑↑↑↑↑↑ ↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑  ↑↑ ↑  ↑↑↑↑↑↑   ↑           ↑↑ ↑↑↑↑↑↑↑↑ ↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑    ↑ ↑    ↑↑↑↑↑↑↑           ↑ ↑↑↑ ↑↑↑↑↑↑↑↑ ↑↑ ↑↑↑↑       ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑ ↑ ↑↑↑↑ ↑↑↑↑↑ ↑ ↑↑↑↑↑↑↑↑↑ ↑ ↑↑↑ ↑↑    ↑↑ ↑↑ ↑   ↑↑ ↑ ↑    ↑↑↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑                ↑↑              ↑↑↑ ↑     ↑↑ ↑↑  ↑↑↑ ↑ ↑ ↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑                             ↑↑↑↑           ↑ ↑↑↑↑    ↑↑↑↑↑↑ ↑↑↑ ↑ ↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑                          ↑ ↑↑↑↑ ↑↑↑↑↑↑            ↑ ↑   ↑       ↑                     ↑↑↑↑↑↑
↑↑↑↑↑↑                             ↑↑↑↑↑ ↑                ↑↑ ↑  ↑       ↑                      ↑↑↑↑↑
↑↑↑↑↑                                    ↑↑                 ↑  ↑↑        ↑                      ↑↑↑↑
↑↑↑↑↑ ↑↑  ↑↑ ↑ ↑↑ ↑↑↑↑↑ ↑↑↑↑↑ ↑ ↑↑ ↑↑  ↑ ↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑ ↑ ↑     ↑ ↑↑↑↑ ↑ ↑↑↑  ↑↑↑↑↑↑ ↑↑↑↑ ↑ ↑↑↑↑↑↑
↑↑↑↑↑ ↑    ↑ ↑            ↑↑↑ ↑ ↑↑ ↑     ↑↑             ↑   ↑            ↑    ↑↑              ↑ ↑↑↑↑
↑↑↑↑↑ ↑↑  ↑↑ ↑                   ↑ ↑↑  ↑ ↑↑     ↑↑↑↑↑↑↑     ↑    ↑       ↑       ↑↑↑↑↑↑↑      ↑ ↑↑↑↑
↑↑↑↑↑↑      ↑              ↑ ↑           ↑↑   ↑↑↑↑↑↑↑↑↑↑↑   ↑   ↑       ↑↑     ↑↑↑↑↑↑↑↑↑↑↑      ↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑   ↑            ↑  ↑    ↑ ↑↑ ↑   ↑ ↑↑↑      ↑↑       ↑↑ ↑    ↑↑    ↑↑↑       ↑↑  ↑  ↑↑↑↑↑
↑↑↑↑        ↑ ↑            ↑  ↑               ↑    ↑↑    ↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑  ↑ ↑↑↑  ↑ ↑     ↑   ↑ ↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑   ↑ ↑↑     ↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑   ↑↑↑   ↑ ↑↑ ↑  ↑  ↑↑ ↑↑↑↑
↑↑↑↑        ↑ ↑↑           ↑  ↑  ↑         ↑↑   ↑ ↑ ↑↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑ ↑  ↑↑↑↑ ↑  ↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑ ↑↑↑↑↑↑↑↑↑↑↑ ↑  ↑↑ ↑↑↑↑ ↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑    ↑ ↑↑↑↑↑↑↑  ↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑  ↑↑  ↑↑↑ ↑  ↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑ ↑↑↑  ↑↑↑↑↑ ↑  ↑↑↑↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑ ↑  ↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑ ↑↑↑↑↑↑ ↑  ↑ ↑  ↑ ↑ ↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑   ↑↑ ↑↑   ↑ ↑↑  ↑↑↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑ ↑↑ ↑  ↑    ↑ ↑ ↑↑↑↑↑↑  ↑↑↑↑↑↑↑ ↑ ↑     ↑↑  ↑↑↑↑     ↑↑↑↑↑
↑↑↑↑↑↑↑  ↑↑  ↑ ↑↑ ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ ↑ ↑↑↑↑      ↑↑↑↑↑↑  ↑      ↑↑↑↑↑↑↑↑↑↑   ↑↑          ↑↑↑↑
↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
"""

version = "0.7.4"
contributors = ["Issac Kee", "Colton Lee", "Ethan Lowrey", "Kenzie Mccabe", "Peyton Dineyazhe"]
contributors_str = ""
for contributor in contributors:
    contributors_str += f"{contributor}, "
contributors_str += " "
contributors_str, _ = contributors_str.split(",  ", 1)
contributors_str += "."
org = "AISES"

print(ascii_art)
print("\n\nWelcome to the RezWheels server!") # Add some whitespace for clarity.
print(f"[Version]: {version}")
print(f"[Contributors]: {contributors_str}")
print(f"[Organization]: {org}")

# import node_endpoint
import flask_endpoint

input()
