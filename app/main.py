from generator.generator import Generator

if __name__ == "__main__":
    informations = "Développeur"
    generator = Generator(informations)
    print(generator.run())