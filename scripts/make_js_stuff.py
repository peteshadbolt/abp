from abp import clifford
import json

with open("../server/tables.js", "w") as f:
    f.write("var decompositions = ")
    f.write(json.dumps(clifford.decompositions))
    f.write(";\n")

    f.write("var conjugation_table = ")
    f.write(json.dumps(clifford.conjugation_table.tolist()))
    f.write(";\n")

    f.write("var times_table = ")
    f.write(json.dumps(clifford.times_table.tolist()))
    f.write(";\n")

    f.write("var cz_table = ")
    f.write(json.dumps(clifford.cz_table.tolist()))
    f.write(";\n")

    f.write("var clifford = ")
    f.write(json.dumps(clifford.by_name))
    f.write(";\n")


