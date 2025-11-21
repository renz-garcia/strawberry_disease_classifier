IDX_TO_LABEL = {
    0: "Anthracnose",
    1: "Healthy",
}

def get_label(index):
    return IDX_TO_LABEL.get(index, "Unknown")