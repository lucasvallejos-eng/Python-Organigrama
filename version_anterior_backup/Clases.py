class Nucleo:
    def __int__(self, Uno , Dos , Tres , Cuatro , Cinco ):
        self.Uno = Uno
        self.Dos = Dos
        self.Tres = Tres
        self.Cuatro = Cuatro
        self.Cinco = Cinco

class Personas:
    def __int__(self, COD , DOC , APE , NOM , TEL , DIR , DEP , SAL ):
        self.COD = COD
        self.DOC = DOC
        self.APE = APE
        self.NOM = NOM
        self.TEL = TEL
        self.DIR = DIR
        self.DEP = DEP
        self.SAL = SAL

class Organigrama(Nucleo):
    def __int__(self,Uno , Dos , Tres , Cuatro , Cinco , COD_ORG , ORG , FEC ):
        super().__init__( Uno , Dos , Tres , Cuatro , Cinco)
        self.COD_ORG = COD_ORG
        self.ORG = ORG
        self.FEC = FEC


class Dependencia(Nucleo,Personas):
    def __int__(self, Uno , Dos , Tres , Cuatro , Cinco , COD_DEP , NOM_DEP , CODRES , COD_PERS , COD , DOC , APE , NOM_PER , TEL , DIR , DEP , SAL ):
        super().__init__(Uno , Dos , Tres , Cuatro , Cinco)
        super().__init__( COD_PERS , COD ,DOC , APE , NOM_PER , TEL , DIR , DEP , SAL)
        self.COD_DEP = COD_DEP
        self.NOM = NOM_DEP
        self.CODRES = CODRES