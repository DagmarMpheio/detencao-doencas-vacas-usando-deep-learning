from simple_image_download import simple_image_download as simp

response = simp.simple_image_download

keywords = ['febre aftosa','febre aftosa em bovinos','Infectious Bovine Keratoconjunctivitis','ceratoconjuntivite infecciosa bovina','Pleuropneumonia Contagiosa Bovina','Doenças de casco Bovina']

for kw in keywords:
    response().download(kw, 100)