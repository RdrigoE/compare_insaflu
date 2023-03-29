import csv
from pathlib import Path


def get_consensus_website(path: Path):
    with open(path.absolute(), "r", encoding="UTF-8") as handler:
        reader = list(map(lambda row: list(map(lambda item: item.replace('"',''), row[0].split("\t"))), list(csv.reader(handler))[8:]))
    sample_dict = {}
    for row in reader:
        sample_dict[row[0][5:]] = row[-8:]
    # for k,v in sample_dict.items():
    #     print(k,v)
    return sample_dict


def get_consensus_snakemake(path: Path):
    with open(path.absolute(), "r", encoding="UTF-8") as handler:
        reader = list(csv.reader(handler))[4:]
    sample_dict = {}
    for row in reader:
        sample_dict[row[0]] = row[-8:]
    # for k,v in sample_dict.items():
    #     print(k,v)
    return sample_dict


website = get_consensus_website(Path("./compare/coverage.tsv"))
snakemake = get_consensus_snakemake(Path("./snakemake/coverage.csv"))

for key in website:
    if website[key] == snakemake[key]:
        print(key, ":" ,website[key])
    # print(website[key])
    # print(snakemake[key])
    # break