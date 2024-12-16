import socket
import sys
import signal
from prettytable import PrettyTable


# Colors
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def def_handler(sig, frame):
    print(f"{bcolors.FAIL}\n\n[!] Quitting...\n{bcolors.ENDC}")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


# List of names of UPM schools without common words
schools = [
    "Ingeniería Aeronáutica y del Espacio",
    "Politécnica de Enseñanza Superior",
    "Caminos, Canales y Puertos",
    "Sistemas Optoelectrónicos y Microtecnología",
    "Energía Solar",
    "Montes, Forestal y del Medio Natural",
    "Edificación",
    "Ciencias de la Actividad Física y del Deporte (INEF)",
    "Telecomunicación",
    "Navales",
    "Arquitectura",
    "Agronómica, Alimentaria y de Biosistemas",
    "Minas y Energía",
    "Ingeniería y Diseño Industrial",
    "Industriales",
    "Sistemas Informáticos",
    "Diseño de Moda de Madrid",
    "Topografía, Geodesia y Cartografía",
    "Biotecnología y Genómica de Plantas (CBGP)",
    "Microgravedad 'Ignacio Da Riva'",
    "Domótica Integral (CeDInt)",
    "Tecnología Biomédica (CTB)",
    "Ingenieros Informáticos",
]

if len(sys.argv) != 2:
    print(
        f"{bcolors.FAIL}[!] Use: python schools_disovery.py <subdomains_file.txt>{bcolors.ENDC}"
    )
    sys.exit(1)

file_subdomains = sys.argv[1]
try:
    with open(file_subdomains, "r") as f:
        subdomains = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"{bcolors.FAIL}[!] File {file_subdomains} not found{bcolors.ENDC}")
    sys.exit(1)

# Creating a table to show results
table = PrettyTable(["School", "Subdomain", "IP"])

# Comparing schools with subdomains
for subdomain in subdomains:
    try:
        ip_address = socket.gethostbyname(subdomain)
        for school in schools:
            if (
                school.lower()
                .replace("\u00e1", "a")
                .replace("\u00e9", "e")
                .replace("\u00ed", "i")
                .replace("\u00f3", "o")
                .replace("\u00fa", "u")
                in subdomain.lower()
            ):
                table.add_row([school, subdomain, ip_address])
                break
    except socket.gaierror:
        print(f"{bcolors.FAIL}[!] Error obtaining IP from {subdomain}{bcolors.ENDC}")

# Showing results
print(table)
