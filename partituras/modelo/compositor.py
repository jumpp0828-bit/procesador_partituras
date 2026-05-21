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

    def encontrar_caracteres_invalidos(self, partitura):
        return [
            (i, caracter)
            for i, caracter in enumerate(partitura)
            if ord(caracter) > 127
        ]

class ReglaTransposicion(ReglaTransformacion):

    NOTAS = ["do", "re", "mi", "fa", "sol", "la", "si"]

    def partitura_valida(self, partitura):

        errores = []

        numeros = self.encontrar_numeros_partitura(partitura)

        if numeros:
            mensaje = ", ".join(
                [f"{c} en posición {i}" for i, c in numeros]
            )
            errores.append(
                ContieneNumero(mensaje)
            )

        invalidos = self.encontrar_caracteres_invalidos(partitura)

        if invalidos:
            mensaje = ", ".join(
                [f"{c} en posición {i}" for i, c in invalidos]
            )

            errores.append(
                ContieneCaracterInvalido(mensaje)
            )

        partitura = partitura.lower()

        tokens = partitura.split()

        permitidos = self.NOTAS + ["|", "-"]

        tokens_invalidos = [
            t for t in tokens
            if t not in permitidos
        ]

        if tokens_invalidos:
            errores.append(
                ContieneCaracterInvalido(
                    f"Tokens inválidos: {tokens_invalidos}"
                )
            )

        notas = [
            t for t in tokens
            if t in self.NOTAS
        ]

        if not notas:
            errores.append(
                SinNotas("La partitura no contiene notas")
            )

        if errores:
            raise ExceptionGroup(
                "Errores de validación",
                errores
            )

        return True

    def transformar(self, partitura):

        self.partitura_valida(partitura)

        partitura = partitura.lower()

        tokens = partitura.split()

        resultado = [
            self._transponer(t)
            if t in self.NOTAS
            else t
            for t in tokens
        ]

        return " ".join(resultado)

    def revertir(self, partitura):

        self.partitura_valida(partitura)

        partitura = partitura.lower()

        tokens = partitura.split()

        resultado = [
            self._revertir_nota(t)
            if t in self.NOTAS
            else t
            for t in tokens
        ]

        return " ".join(resultado)

    def _transponer(self, nota):

        indice = self.NOTAS.index(nota)

        nuevo = (indice + self.token) % len(self.NOTAS)

        return self.NOTAS[nuevo]

    def _revertir_nota(self, nota):

        indice = self.NOTAS.index(nota)

        nuevo = (indice - self.token) % len(self.NOTAS)

        return self.NOTAS[nuevo]

class ReglaFrecuencia(ReglaTransformacion):

    FRECUENCIAS = {
        "do": 261,
        "re": 293,
        "mi": 329,
        "fa": 349,
        "sol": 392,
        "la": 440,
        "si": 493
    }

    def partitura_valida(self, partitura):

        errores = []

        numeros = self.encontrar_numeros_partitura(partitura)

        if numeros:
            mensaje = ", ".join(
                [f"{c} en posición {i}" for i, c in numeros]
            )

            errores.append(
                ContieneNumero(mensaje)
            )

        invalidos = self.encontrar_caracteres_invalidos(partitura)

        if invalidos:
            mensaje = ", ".join(
                [f"{c} en posición {i}" for i, c in invalidos]
            )

            errores.append(
                ContieneCaracterInvalido(mensaje)
            )

        if partitura != partitura.strip():
            errores.append(
                EspacioBordes(
                    "Hay espacios al inicio o final"
                )
            )

        if "  " in partitura:
            errores.append(
                EspacioMultiple(
                    "Hay múltiples espacios"
                )
            )

        partitura = partitura.lower()

        tokens = partitura.split()

        invalidos = [
            t for t in tokens
            if t not in self.FRECUENCIAS
        ]

        if invalidos:
            errores.append(
                ContieneCaracterInvalido(
                    f"Notas inválidas: {invalidos}"
                )
            )

        if errores:
            raise ExceptionGroup(
                "Errores de validación",
                errores
            )

        return True

    def transformar(self, partitura):

        self.partitura_valida(partitura)

        partitura = partitura.lower()

        resultado = [
            str(self.FRECUENCIAS[nota] * self.token)
            for nota in partitura.split()
        ]

        return " ".join(resultado)