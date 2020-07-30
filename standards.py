# B (Pli Minimal)
# Bmax (Pli Minimal)
# H (hors-tout) pour pliage inverse


thickness_mapping = {
    # 16G
    '0.060"': "16G",
    '16G (0.062")': "16G",
    '16G (0.0598")': "16G",
    '16G (0.0595")': "16G",
    # 14G
    '0.075"': "14G",
    '14G (0.0747")': "14G",
    '14G (0.0751")': "14G",
    # 11G
    '0.120"': "11G",
    '11G (0.125")': "11G",
    '11G (0.120")': "11G",
    '11G (0.1196")': "11G",
    # "3/16"
    '0.187"': "3/16",
    # "1/4"
    '0.250"': "1/4",
    # "3/8"
    '0.375"': "3/8",
    '3/8"': "3/8",
    # "1/2"
    '0.500"': "1/2",
    '1/2"': "1/2",
}

PLIAGE = {
    "16G": {
        "B": 0.472,
        "Bmax": {"STEEL PLATE": 2.723, "SS.PLATE": 2.754},
        "H": {"STEEL PLATE": 0.790, "SS.PLATE": 0.821, "AL.PLATE": 0.758},
        "A": 90,
    },
    "14G": {
        "B": 0.472,
        "Bmax": {"STEEL PLATE": 2.754, "SS.PLATE": 2.785},
        "H": {"STEEL PLATE": 0.848, "SS.PLATE": 0.848, "AL.PLATE": None},
        "A": 90,
    },
    "11G": {
        "B": 0.709,
        "Bmax": {"STEEL PLATE": 2.802, "SS.PLATE": 2.833},
        "H": {"STEEL PLATE": 1.038, "SS.PLATE": 1.100, "AL.PLATE": 0.975},
        "A": 90,
    },
    "3/16": {
        "B": 1.181,
        "Bmax": {"STEEL PLATE": 2.897, "SS.PLATE": 2.928},
        "H": {"STEEL PLATE": 1.636, "SS.PLATE": 1.730, "AL.PLATE": 1.573},
        "A": 93,
    },
    "1/4": {
        "B": 1.476,
        "Bmax": {"STEEL PLATE": 2.969, "SS.PLATE": 3.000},
        "H": {"STEEL PLATE": 1.997, "SS.PLATE": 2.122, "AL.PLATE": 1.935},
        "A": 96,
    },
    "3/8": {
        "B": 2.362,
        "Bmax": {"STEEL PLATE": 3.144, "SS.PLATE": 3.237},
        "H": {"STEEL PLATE": 3.129, "SS.PLATE": 3.316, "AL.PLATE": 3.316},
        "A": 96,
    },
    "1/2": {
        "B": 2.952,
        "Bmax": {"STEEL PLATE": 3.311, "SS.PLATE": 3.342},
        "H": {"STEEL PLATE": 3.838, "SS.PLATE": 4.057, "AL.PLATE": 3.869},
        "A": 103,
    },
}
