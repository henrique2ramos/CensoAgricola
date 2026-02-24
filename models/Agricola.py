class Agricola():
    def __init__(self, cod_uf, cod_municipio, cod_distrito, cod_subdistrito, situacao, nom_tip_seglogr, nom_titulo_seglogr, nom_seglogr, num_endereco, dsc_modificador, nom_comp_elem1, val_comp_elem1, nom_comp_elem2, val_comp_elem2, nom_comp_elem3, val_comp_elem3, nom_comp_elem4, val_comp_elem4, nom_comp_elem5, val_comp_elem5, latitude, longitude, altitude, desc_localidade, cod_especie, cep):
        self.cod_uf = cod_uf
        self.cod_municipio = cod_municipio
        self.cod_distrito = cod_distrito
        self.cod_subdistrito = cod_subdistrito
        self.situacao = situacao
        self.nom_tip_seglogr = nom_tip_seglogr
        self.nom_titulo_seglogr = nom_titulo_seglogr
        self.nom_seglogr = nom_seglogr
        self.num_endereco = num_endereco
        self.dsc_modificador = dsc_modificador
        self.nom_comp_elem1 = nom_comp_elem1
        self.val_comp_elem1 = val_comp_elem1
        self.nom_comp_elem2 = nom_comp_elem2
        self.val_comp_elem2 = val_comp_elem2
        self.nom_comp_elem3 = nom_comp_elem3
        self.val_comp_elem3 = val_comp_elem3
        self.nom_comp_elem4 = nom_comp_elem4
        self.val_comp_elem4 = val_comp_elem4
        self.nom_comp_elem5 = nom_comp_elem5
        self.val_comp_elem5 = val_comp_elem5
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.desc_localidade = desc_localidade
        self.cod_especie = cod_especie
        self.cep = cep

    def __str__(self):
        return f'<Agricola {self.cod_uf} - {self.cod_municipio} - {self.cod_distrito} - {self.cod_subdistrito}>'

    def to_json(self):
        return {
            "cod_uf": self.cod_uf,
            "cod_municipio": self.cod_municipio,
            "cod_distrito": self.cod_distrito,
            "cod_subdistrito": self.cod_subdistrito,
            "situacao": self.situacao,
            "nom_tip_seglogr": self.nom_tip_seglogr,
            "nom_titulo_seglogr": self.nom_titulo_seglogr,
            "nom_seglogr": self.nom_seglogr,
            "num_endereco": self.num_endereco,
            "dsc_modificador": self.dsc_modificador,
            "nom_comp_elem1": self.nom_comp_elem1,
            "val_comp_elem1": self.val_comp_elem1,
            "nom_comp_elem2": self.nom_comp_elem2,
            "val_comp_elem2": self.val_comp_elem2,
            "nom_comp_elem3": self.nom_comp_elem3,
            "val_comp_elem3": self.val_comp_elem3,
            "nom_comp_elem4": self.nom_comp_elem4,
            "val_comp_elem4": self.val_comp_elem4,
            "nom_comp_elem5": self.nom_comp_elem5,
            "val_comp_elem5": self.val_comp_elem5,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "desc_localidade": self.desc_localidade,
            "cod_especie": self.cod_especie,
            "cep": self.cep
        }
