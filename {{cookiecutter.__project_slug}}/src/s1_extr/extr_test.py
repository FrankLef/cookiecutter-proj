from src.s0_helpers.setup import tdict


def main(subprocess: str) -> int:
    specs = tdict.get_specs()
    print(specs.shape)
    return 0