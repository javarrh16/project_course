from Bio import pairwise2
from Bio.pairwise2 import format_alignment


alignments = pairwise2.align.localxx('VLSAADKTNVKAAWSKVGGHAGEYGAEALERMFLGFPTTKTYFPHFDLSHGSAQVKAHGKKVGDALTLAVGHLDDLPGALSDLSNLHAHKLRVDPVNFKLLSHCLLSTLAVHLPNDFTPAVHASLDKFLSSVSTVLTSKYR','NLKDKILGVAKELFIKNGYNATTTGEIVKLSESSKGNLYYHFKTKENLFLEILNIEESKWQEQWKKEQIKAKTNREKFYLYNELSLTTEYYYPLQNAIIEFYTEYYKTNSINEKMNKLENKYIDAYHVIFKEGNLNGEWSINDVNAVSKIAANAVNGIVTFTHEQNINERIKLMNKFSQIFLNGLS')
print(format_alignment(*alignments[0]))

