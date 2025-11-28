class Classifier:

    def classify(self, value, origin):
        if origin == "valid":
            return "valida"
        if origin == "invalid":
            return "invalida"
        if origin == "extreme":
            return "extrema"
        return "desconocido"
