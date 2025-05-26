from faker import Faker

fake = Faker("pt-BR")


class DataGenerator():
    _title_words = [
        "Receita",
        "Delícia", 
        "Saborosa", 
        "Crocante", 
        "Cremosa", 
        "Especial", 
        "Caseira", 
        "Tradicional", 
        "Saudável", 
        "Refrescante", 
        "Doce", 
        "Salgada", 
        "Apimentada", 
        "Exótica", 
        "Leve", 
        "Rápida", 
        "Simples", 
        "Prática", 
        "Elegante", 
        "Aromática", 
        "Irresistível"
    ]

    _category_choices = [
        "café da manhã",
        "almoço",
        "jantar",
        "lanche",
        "sobremesa"
    ]

    def generate():
        title = fake.text(max_nb_chars=50,ext_word_list=DataGenerator._title_words)
        name = fake.name()
        date = fake.date(pattern="%d/%m/%Y")
        time = fake.time(pattern="%I:%M")
        category = fake.word(ext_word_list=DataGenerator._category_choices)
        text = fake.text(max_nb_chars=300)
        preparation_time = fake.random_int(min=1,max=300)
        portions = fake.random_int(min=1,max=50)
        preparation_steps = fake.text(max_nb_chars=5000)

        data = {
            "title": title,
            "name": name,
            "date": date,
            "time": time,
            "category": category,
            "text": text,
            "preparation_time": preparation_time,
            "portions": portions,
            "preparation_steps": preparation_steps
        }

        return data
if __name__ == "__main__":
    data = DataGenerator.generate()
    print(data["preparation_steps"])
        