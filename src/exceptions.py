class ErreurBibliotheque(Exception):
    def __init__(self, message: str, code_erreur: int = 0):
        super().__init__(message)
        self.code_erreur = code_erreur

