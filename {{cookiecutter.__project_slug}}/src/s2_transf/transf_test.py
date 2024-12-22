from src.s0_helpers import tdict


def main(subprocess: str) -> int:
    df = tdict.main()
    print(df.shape)
    return 0