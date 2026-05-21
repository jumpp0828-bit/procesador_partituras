from abc import ABC, abstractmethod

from partituras.modelo.errores import (
    ContieneNumero,
    ContieneCaracterInvalido,
    SinNotas,
    EspacioMultiple,
    EspacioBordes,
)

class ReglaTransformacion(ABC):

    def __init__(self, token):
        self.token = token

    @abstractmethod
    def transformar(self, partitura):
        pass

    @abstractmethod
    def revertir(self, partitura):
        pass

    @abstractmethod
    def partitura_valida(self, partitura):
        pass

    def encontrar_numeros_partitura(self, partitura):
        return [
            (i, caracter)
            for i, caracter in enumerate(partitura)
            if caracter.isdigit()
        ]