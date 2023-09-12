import click
import re
MAXWORDS = 500 + (256*5)

def split_fibers(fibers, max_words=MAXWORDS):
    # Split each fiber into chunks of up to max_words words
    sfibers = []
    for fiber in fibers:
        words = fiber.split()
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i : i + max_words])
            sfibers.append(chunk)
    return sfibers

def refactor_into_fiber_bundles(lines, bundle_size=10):
    bundles = []
    temp = []
    for line in lines:
        # Split the line into fibers
        # fibers = line.split('.')
        fibers = re.split(r"[\.\n]", line)

        # Filter out empty lines or lines with only whitespace
        fibers = [fiber.strip() for fiber in fibers if re.search(r"\S", fiber)]

        # Add filtered fibers to the current bundle
        temp.extend(split_fibers(fibers))
    # now lete
    current_bundle = []
    # print(temp)
    for line in temp:
        current_bundle.append(line)

        # Check if the current bundle size exceeds the desired bundle size
        if len(current_bundle) >= bundle_size:
            # Add the current bundle to the list of bundles
            bundles.append(current_bundle)
            # Start a new bundle
            current_bundle = []

    # Add the last bundle if it's not empty
    if current_bundle:
        bundles.append(current_bundle)

    return bundles

def read_input_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        lines = refactor_into_fiber_bundles(lines)
        for l in lines:
            print("bundle")
            for l2 in l:
                print(l2)

@click.command()
@click.option('--input-file')
def main(input_file ):
    read_input_file(input_file)

if __name__ == '__main__':
    main()


