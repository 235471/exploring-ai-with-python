lista_de_nomes = ["Maria Silva", "João Santos", "Ana Oliveira", "Pedro Costa", "Juliana Pereira"]
lista_de_medias = [8.9, 7.5, 4.2, 1.4, 9.5]
i = 0

for media in lista_de_medias:
    media = media + 1
    if media > 10:
        media = 10
    print(media)

while i < len(lista_de_medias):
    lista_de_medias[i] = lista_de_medias[i] + 1
    if lista_de_medias[i] > 10:
        lista_de_medias[i] = 10
    i = i + 1

print(lista_de_medias)

for i in range(len(lista_de_medias)):
    lista_de_medias[i] = lista_de_medias[i] + 1
    if lista_de_medias[i] > 10:
        lista_de_medias[i] = 10

print(lista_de_medias)

for i, media in enumerate(lista_de_medias):
    lista_de_medias[i] = min(media + 1, 10)

print(lista_de_medias)

dicionario_alunos_media = dict(zip(lista_de_nomes, lista_de_medias))

for element in dicionario_alunos_media.items():
    print(element)

for nome, media in dicionario_alunos_media.items():
    print(f"{nome}: {media}")

# adicionar novo item ao dicionario
dicionario_alunos_media["Carlos Souza"] = 6.5

# remover item do dicionario
dicionario_alunos_media.pop("Carlos Souza")

# transformar dicionario em lista de dicionarios
new_dicionario_alunos_media = [{"Nome": nome, "Media": media} for nome, media in dicionario_alunos_media.items()]

print(new_dicionario_alunos_media)