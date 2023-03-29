from pathlib import Path
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO import SeqRecord


def get_consensus(path) -> dict[str, str]:
    record_dict = {}
    with open(path, "r", encoding="UTF-8") as handler:
        records = list(SimpleFastaParser(handler))
        for record in records:
            record_dict[record[0].split(" ")[0]] = record[1]
    return record_dict


if __name__ == "__main__":
    website = get_consensus("./compare/AllConsensus.fasta")
    print("website done")
    snakemake = get_consensus("./snakemake/AllConsensus.fasta")
    print("snakemake done")
    equals = {}
    for key in website:
        if website.get(key) == snakemake.get(key):
            if equals.get(key[:-3], False):
                equals[key[:-3]].append(key[-1:])
            else:
                equals[key[:-3]] = [key[-1:]]
    for k, v in equals.items():
        print(k, ":", v)
