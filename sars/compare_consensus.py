from pathlib import Path
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO import SeqRecord
import sys


def get_consensus(path) -> dict[str, str]:
    record_dict = {}
    with open(path, "r", encoding="UTF-8") as handler:
        records = list(SimpleFastaParser(handler))
        for record in records:
            record_dict[record[0].split(" ")[0]] = record[1]
    return record_dict


if __name__ == "__main__":
    try:
        debug = sys.argv[1]
    except:
        debug = False
    website = get_consensus("./website/AllConsensus.fasta")
    snakemake = get_consensus("./snakemake/AllConsensus.fasta")
    total_website = len(website.keys())
    total_snakemake = len(snakemake.keys())
    print(f"website: {total_website} | snakemake: {total_snakemake}")
    total = len(website.keys())
    count = 0
    for key in website:
        if website.get(key) == snakemake.get(key):
            count += 1
        else:
            if debug:
                print(key)
    print(f"There is {count} samples that are exactly equal out of {total}")
