from analyzer import features_v2
from writer import csv_writer


def main() -> None:
    analyze_results = features_v2.analyze()
    csv_writer.write(analyze_results)


if __name__ == "__main__":
    main()
