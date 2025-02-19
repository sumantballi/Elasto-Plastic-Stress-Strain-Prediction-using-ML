import os 
from tqdm import tqdm
from functools import reduce

# This function has been used to to preprocess the data from the fea_database folder.
# The resulting data is written to the preprocessed folder.
def main():
    for r, d, f in os.walk("fea_database"):
        if r.endswith("/data"):
            with tqdm(f) as pbar: 
                pbar.set_description_str(f"Processing {r}")
                for file_name in pbar: 
                    file = os.path.join(r, file_name)
                    with open(file) as c: 
                        lines = c.readlines()
                    input_segment = []
                    output_segment = []
                    is_input = True
                    for idx, line in enumerate(lines):
                        if idx < 1:
                            continue
                        if "OUTPUT" in line:
                            is_input = False
                            continue
                        line = line.split()
                        if len(line) == 0:
                            continue
                        line = reduce(lambda l1, l2: l1 + "," + l2, line) + "\n"
                        if is_input:
                            input_segment.append(line)
                        if not is_input:
                            output_segment.append(line)
            
                    directory = r.split("/")[1]
                    store_path = os.path.join("preprocessed", "input", directory)
                    if not os.path.exists(store_path):
                        os.mkdir(store_path)
                    store_path = os.path.join(store_path, file_name.replace(".txt", ".csv"))
                    with open(store_path, "w") as store_file: 
                        store_file.writelines(input_segment)

                    store_path = os.path.join("preprocessed", "output", directory)
                    if not os.path.exists(store_path):
                        os.mkdir(store_path)
                    store_path = os.path.join(store_path, file_name.replace(".txt", ".csv"))
                    with open(store_path, "w") as store_file: 
                        store_file.writelines(output_segment)


if __name__ == "__main__":
    main()
