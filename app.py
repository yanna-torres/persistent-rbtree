import sys
from tree.persistent import PersistentRedBlackTree


def decode_input(input_filename, output_filename, tree):
    output_lines = []

    with open(input_filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            if not parts:
                continue
            command = parts[0]
            if command == "INC" and len(parts) == 2:
                value = int(parts[1])
                tree.insert(value)
            elif command == "REM" and len(parts) == 2:
                value = int(parts[1])
                tree.delete(value)
            elif command == "SUC" and len(parts) == 3:
                value = int(parts[1])
                version = int(parts[2])
                succ = tree.successor(value, version)
                output_lines.append(f"SUC {value} {version}")
                output_lines.append(str(succ))
            elif command == "IMP" and len(parts) == 2:
                version = int(parts[1])
                result = tree.print_version(version)
                output_lines.append(f"IMP {version}")
                output_lines.append(" ".join(result))
            else:
                print(f"Invalid command: {line.strip()}")

    with open(output_filename, "w") as out_file:
        out_file.write("\n".join(output_lines))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <input_file.txt>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "output.txt"
    tree = PersistentRedBlackTree()
    decode_input(input_filename, output_filename, tree)
