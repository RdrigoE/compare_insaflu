import csv
from typing_extensions import TypedDict
import sys


class SnakemakeEntry(TypedDict):
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    info: dict[str, str]
    ann: dict[str, str]
    names: list[str]
    values: list[str]


def remove_smallcase(string):
    word = ""
    for letter in string:
        if not letter.islower():
            word += letter
    return word


def smaller(string: str) -> str:
    return string[: 2] + remove_smallcase(string[2:])


def convert_list_to_dict(data: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    snp_annotation = ["Allele", "Annotation", "Annotation_Impact", "Gene_Name", "Gene_ID", "Feature_Type", "Feature_ID",
                      "Transcript_BioType", "Rank", "HGVS.c", "HGVS.p", "cDNA.pos/cDNA.length", "CDS_CDSLength", "AA.pos/AA.length", "Distance", "ERRORS/WARNINGS/INFO"]
    new_dict = {}

    ann_dict = {}
    for item in data:
        k, v = item.split("=")
        if k.upper() == "ANN":
            ann_dict = {}
            new_v = v.split("|")
            for idx, v in enumerate(new_v):
                ann_dict[snp_annotation[idx]] = v
        else:
            new_dict[k] = v
    return new_dict, ann_dict


def main():
    input = sys.argv[1]
    output = sys.argv[2]
    with open(input) as handler:
        lines = handler.readlines()
    vcf_data = []
    for line in lines[1:]:
        l = line.split()
        info, ann = convert_list_to_dict(l[7].split(";"))
        entry = SnakemakeEntry(
            chrom=l[0],
            pos=int(l[1]),
            ref=l[3],
            alt=l[4],
            qual=float(l[5]),
            info=info,
            ann=ann,
            names=l[8].split(":"),
            values=l[9].split(":")
        )

        get_freq = round(float(entry["info"]["AO"].replace(
            ",", "."))/float(entry["info"]["DP"].replace(",", ".")) * 100, 1)
        default = [entry["chrom"],
                   entry["pos"],
                   entry["info"]["TYPE"],
                   entry["ref"],
                   entry["alt"],
                   get_freq,
                   entry["info"]["DP"],
                   entry["alt"] + ":" + entry["info"]["AO"],
                   entry["ref"] + ":" + entry["info"]["RO"],
                   ]

        if entry.get("ann"):
            ann = entry["ann"]

            default.extend(["CDS",
                            "+",
                            ann["CDS_CDSLength"],
                            ann["AA.pos/AA.length"],
                            ann["Annotation"],
                            ann["HGVS.c"],
                            ann["HGVS.p"],
                            smaller(ann["HGVS.p"]),
                            ann["Gene_Name"],
                            ann["Gene_Name"],
                            ])
        vcf_data.append(default)
        with open(output, "w") as handler:
            writer = csv.writer(handler)
            writer.writerows(vcf_data)


port csv
from typing_extensions import TypedDict
import sys


class SnakemakeEntry(TypedDict):
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    info: dict[str, str]
    ann: dict[str, str]
    names: list[str]
    values: list[str]


def remove_smallcase(string):
    word = ""
    for letter in string:
        if not letter.islower():
            word += letter
    return word


def smaller(string: str) -> str:
    return string[: 2] + remove_smallcase(string[2:])


def convert_list_to_dict(data: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    snp_annotation = ["Allele", "Annotation", "Annotation_Impact", "Gene_Name", "Gene_ID", "Feature_Type", "Feature_ID",
                      "Transcript_BioType", "Rank", "HGVS.c", "HGVS.p", "cDNA.pos/cDNA.length", "CDS_CDSLength", "AA.pos/AA.length", "Distance", "ERRORS/WARNINGS/INFO"]
    new_dict = {}

    ann_dict = {}
    for item in data:
        k, v = item.split("=")
        if k.upper() == "ANN":
            ann_dict = {}
            new_v = v.split("|")
            for idx, v in enumerate(new_v):
                ann_dict[snp_annotation[idx]] = v
        else:
            new_dict[k] = v
    return new_dict, ann_dict


def main():
    input = sys.argv[1]
    output = sys.argv[2]
    with open(input) as handler:
        lines = handler.readlines()
    vcf_data = []
    for line in lines[1:]:
        l = line.split()
        info, ann = convert_list_to_dict(l[7].split(";"))
        entry = SnakemakeEntry(
            chrom=l[0],
            pos=int(l[1]),
            ref=l[3],
            alt=l[4],
            qual=float(l[5]),
            info=info,
            ann=ann,
            names=l[8].split(":"),
            values=l[9].split(":")
        )

        get_freq = round(float(entry["info"]["AO"].replace(
            ",", "."))/float(entry["info"]["DP"].replace(",", ".")) * 100, 1)
        default = [entry["chrom"],
                   entry["pos"],
                   entry["info"]["TYPE"],
                   entry["ref"],
                   entry["alt"],
                   get_freq,
                   entry["info"]["DP"],
                   entry["alt"] + ":" + entry["info"]["AO"],
                   entry["ref"] + ":" + entry["info"]["RO"],
                   ]

        if entry.get("ann"):
            ann = entry["ann"]

            default.extend(["CDS",
                            "+",
                            ann["CDS_CDSLength"],
                            ann["AA.pos/AA.length"],
                            ann["Annotation"],
                            ann["HGVS.c"],
                            ann["HGVS.p"],
                            smaller(ann["HGVS.p"]),
                            ann["Gene_Name"],
                            ann["Gene_Name"],
                            ])
        vcf_data.append(default)
        with open(output, "w") as handler:
            writer = csv.writer(handler)
            writer.writerows(vcf_data)


if __name__ == "__main__":
    main()
