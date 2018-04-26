#!/user/bin/env python3

def readPhenotypes(hpoObo):
    """
    Reads the phenotypes from an .obo file.
    :param hpoObo: the path to the .obo file
    :return: dict with phenotype names as keys and their id as value
    """

    # Strings to identify parts of file.
    termString = '[Term]'
    idString = 'id: '
    nameString = 'name: '
    synonymString = 'synonym: "'

    # Default values for processing.
    phenotypes = {}
    hpoId = None
    name = None

    # Goes through the .obo file.
    for line in open(hpoObo):
        # Resets id and name for new phenotype.
        if line.startswith(termString):
            hpoId = None
            name = None
        # Sets id/name when found.
        elif line.startswith(idString):
            hpoId = line.lstrip(idString).strip()
        elif line.startswith(nameString):
            name = line.lstrip(nameString).strip()
        # Sets a synonym as alternative for name when found on a line.
        elif line.startswith(synonymString):
            name = line.lstrip(synonymString).split('"', 1)[0].strip()

        # If a combination of an id and a name/synonym is stored, saves it to the dictionary.
        # Afterwards, resets name to None so that it won't be triggered by every line (unless a new synonym is found).
        if hpoId is not None and name is not None:
            phenotypes[name] = hpoId
            name = None

    return phenotypes

def retrieveLovdPhenotypes(benchmarkData):
    """
    Retrieves the LOVDs with the phenotypes belonging to each LOVD.
    :param benchmarkData: the file from which the retrieve the LOVDs and their phenotypes
    :return: dict with as keys the LOVDs and a list with phenotypes as value for each key
    """
    # Stores all LOVDs
    lovdPhenotypes = {}

    # Goes through the benchmarking file.
    for i, line in enumerate(open(benchmarkData)):
        # Skips first line (header).
        if i == 0:
            continue

        # Splits the values on their separator.
        line = line.rstrip().split('\t')

        # Checks whether this LOVD was already processed (skips if this is the case).
        if line[0] in lovdPhenotypes.keys():
            continue

        # Adds the phenotypes with their corresponding key.
        lovdPhenotypes[line[0]] = line[4].split(';')

    return lovdPhenotypes