class MeshOfInterest:
    vals = {
        "D023361": "Validation Studies",
        "D017418": "Meta Analysis",
        "D064888": "Observational Study",
        "D002363": "Case Report",
        "D017429": "Clinical Trial, Phase IV",
        "D000068397": "Clinical Study",
        "D016429": "Clinical Conference"
    }

    def __init__(self):
        pass

    def get_mesh_ids(self):
        return list(self.vals.keys())

    def get_strs(self):
        return list(self.vals.values())
