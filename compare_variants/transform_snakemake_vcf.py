import csv
from typing_extensions import TypedDict
from typing import Union


class ANN_entry(TypedDict):
    "Allele"
    "Annotation"
    "Annotation_Impact"
    "Gene_Name"
    "Gene_ID"
    "Feature_Type"
    "Feature_ID"
    "Transcript_BioType"
    "Rank"
    "HGVS.c"
    "HGVS.p"
    "cDNA.pos/cDNA.length"
    "CDS_CDSLength"
    "AA.pos/AA.length"
    "Distance"
    "ERRORS/WARNINGS/INFO"


class SnakemakeEntry(TypedDict):
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    info: dict[str, Union[str, ANN_entry]]
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


def convert_list_to_dict(data: list[str]) -> dict[str, Union[str, ANN_entry]]:
    snp_annotation = ["Allele", "Annotation", "Annotation_Impact", "Gene_Name", "Gene_ID", "Feature_Type", "Feature_ID",
                      "Transcript_BioType", "Rank", "HGVS.c", "HGVS.p", "cDNA.pos/cDNA.length", "CDS_CDSLength", "AA.pos/AA.length", "Distance", "ERRORS/WARNINGS/INFO"]
    new_dict = {}
    for item in data:
        k, v = item.split("=")
        if k == "ANN":
            ann_dict: ANN_entry = {}
            new_v = v.split("|")
            for idx, v in enumerate(new_v):
                ann_dict[snp_annotation[idx]] = v
            new_dict[k] = ann_dict
        else:
            new_dict[k] = v
    return new_dict


with open("./snakemake_87.vcf") as handler:
    lines = handler.readlines()
vcf_data = []
for line in lines[1:]:
    l = line.split()
    entry = SnakemakeEntry(
        chrom=l[0],
        pos=int(l[1]),
        ref=l[3],
        alt=l[4],
        qual=float(l[5]),
        info=convert_list_to_dict(l[7].split(";")),
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

    if entry["info"].get("ANN"):
        ann = entry["info"]["ANN"]
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
    with open("snakemake_tsv.csv", "w") as handler:
        writer = csv.writer(handler)
        writer.writerows(vcf_data)
