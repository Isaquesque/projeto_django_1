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
    _time_units=[
        "minutos",
        "horas"
    ]
    @classmethod
    def generate(cls):
        title = fake.text(max_nb_chars=50,ext_word_list=cls._title_words,)
        name = fake.name()
        date = fake.date(pattern="%d/%m/%Y")
        time = fake.time(pattern="%I:%M")
        category = fake.word(ext_word_list=cls._category_choices)
        text = fake.text(max_nb_chars=300)
        preparation_time = fake.random_int(min=1,max=300)
        preparation_time_unit = fake.text(max_nb_chars=7,ext_word_list=cls._time_units)
        portions = fake.random_int(min=1,max=50)
        preparation_steps = fake.text(max_nb_chars=5000)

        data = {
            "title": title,
            "slug":"-".join(title.split(" ")),
            "name": name,
            "date": date,
            "time": time,
            "category": category,
            "text": text,
            "preparation_time": preparation_time,
            "preparation_time_unit":preparation_time_unit,
            "portions": portions,
            "preparation_steps": preparation_steps
        }

        return data
if __name__ == "__main__":
    data = DataGenerator.generate()
    print(data["preparation_steps"])
        