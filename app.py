import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

cepspesquisados = []
dadospesquisados = []


@app.route("/converter", methods=['POST'])
def converter():
    variaveis = request.get_json(force=True)

    unidade_origem = variaveis.get("UnidadeOrigem")
    unidade_destino = variaveis.get("UnidadeDestino")
    valor = float(variaveis.get("valor"))

    if unidade_origem == "C":
        if unidade_destino == "F":
            return retornajson(9 / 5 * valor + 32)
        elif unidade_destino == "K":
            return retornajson(valor + 273.15)
        else:
            return "Formato não suportado!"
    elif unidade_origem == "F":
        if unidade_destino == "C":
            return retornajson((valor - 32) * 5 / 9)
        elif unidade_destino == "K":
            return retornajson((valor - 32) * 5 / 9 + 273.15)
        else:
            return "Formato não suportado!"
    elif unidade_origem == "K":
        if unidade_destino == "F":
            return retornajson((valor - 273.15) * 9 / 5 + 32)
        elif unidade_destino == "C":
            return retornajson(valor - 273.15)
        else:
            return "Formato não suportado!"
    else:
        return "Formato não suportado!"


def retornajson(valor):
    return jsonify({"ValorConvertido": "%.2f" % valor})


@app.route("/consulta/cep/<int:cep>", methods=['GET'])
def cep(cep):
    if cepspesquisados.__contains__(cep):
        return dadospesquisados.__getitem__(cepspesquisados.index(cep))
    else:
        viacep = 'https://viacep.com.br/ws/%s/json/' % cep
        resposta = requests.get(viacep).json()

        dados = {'rua': resposta.get("logradouro"),
                 'cidade': resposta.get("localidade"),
                 'estado': resposta.get("uf")}

        cepspesquisados.insert(len(cepspesquisados) + 1, cep)
        dadospesquisados.insert(len(dadospesquisados) + 1, jsonify(dados))
        return dados


if __name__ == "__main__":
    app.run()
