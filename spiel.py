import random
from typing import List, Set, Dict, Tuple, Optional

class Spiel:
    def __init__(self):
        self.figuren: dict[int, int] = dict()
        self.aktiver_spieler: int = random.randint(0,3)
        self.augenzahl: int = 0

        # alle figuren werden auf -100 gesetzt, d.h. home
        for i in range(4):
            for k in range(4):
                self.figuren[i*10+k] = -100

    def rel_pos(self, figur: int) -> int:
        if self.figuren[figur] == -100:
            return -100
        elif self.figuren[figur] > figur//10*10+40:
            return self.figuren[figur]
        else:
            pos = self.figuren[figur] - figur//10*10
            if pos < 0 and pos > -100:
                pos += 40
            return pos
    
    def rausschmeissen(self, angreifer: int) -> bool:
            try:
                self.figuren[angreifer] += self.augenzahl
                self.figuren[angreifer + self.augenzahl] = -100
                return True
            except:
                return False
    
    def zieleinlauf(self, figur: int) -> bool:
        # wenn die figur schon im ziel ist
        if self.figuren[figur] > figur//10*10+40:
            # steht zwischen dem ersten feld des ziels und dem gewürfelten feld schon eine figur
            if any(i in self.figuren.values() for i in range(self.figuren[figur],self.figuren[figur]+self.augenzahl)):
                return False
            else:
                # wenn nicht figur dorthin ziehen
                if self.figuren[figur] + self.augenzahl <= figur//10*10+43:
                    self.figuren[figur] += self.augenzahl
                    return True
                else:
                    return False
        # wenn die figur noch nicht im ziel ist    
        # steht zwischen dem ersten feld des ziels und dem gewürfelten feld schon eine figur
        elif any(i in self.figuren.values() for i in range(figur//10*10+40, self.rel_pos(figur) + self.augenzahl + figur//10*10+1)):
            return False
        else:
            # wenn nicht figur dorthin ziehen
            if self.rel_pos(figur) + self.augenzahl + figur//10*10 <= figur//10*10+43:
                self.figuren[figur] = self.rel_pos(figur) + self.augenzahl + figur//10*10
                return True
            else:
                return False

    def ziehen(self, figur: int) -> bool:
        # ist das zielfeld noch im spielbereich?
        try:
            if self.rel_pos(figur) + self.augenzahl < 40:
                self.figuren[figur] += self.augenzahl
            else:
                self.zieleinlauf(figur)
            return True
        except:
            return False
    
    def figur_im_feld(self) -> bool:
        # hat der aktive spieler eine figur auf dem feld? True wenn Figur auf Feld
        # eine liste aller values der figuren des aktuellen spielers wird mit den möglichen feldern 0-39 verglichen, wenn ein feld in der liste ist, dann ist eine figur auf dem spielfeld
        return any(i in {k: v for k, v in self.figuren.items() if k//10 == self.aktiver_spieler}.values() for i in range(40))

    def setzen_ziel_moeglich(self) -> bool:
        # gibt es im ziel noch zugmöglichkeiten, True wenn noch Zugmöglichkeiten
        # es wird verglichen, wieviele freie felder es zwischen dem ersten besetzten feld des zielbereichs und dem letzten gibt und wieviele davon besetzt sind, wenn die beiden werte übereinstimmen, kann nicht mehr gesetzt werden
        zielfelder = dict()
        zielfelder = {k: v for k, v in self.figuren.items() if k//10 == self.aktiver_spieler and v >= self.aktiver_spieler*10+40}.values()
        
        return len(range(min(zielfelder), self.aktiver_spieler*10+44)) != len(zielfelder) if len(zielfelder) > 0 else False
            
    def rausschmeissen_moeglich(self) -> Optional[int]:
        if self.figur_im_feld():
            for figur_k, figur_v in {k: v for k, v in self.figuren.items() if k//10 == self.aktiver_spieler}.items():
                
                if figur_v == -100:
                    continue
                
                elif figur_v > figur_k//10*10+40:
                    continue
                
                elif figur_v + self.augenzahl in self.figuren.values() and figur_k != list(self.figuren.keys())[list(self.figuren.values()).index(self.figuren[figur_k] + self.augenzahl)]:
                    return figur_v
            return None

        else:
            return None
    
    def freimachen_moeglich(self) -> Optional[int]:
        try:
            return list({k: v for k, v in self.figuren.items() if k//10 == self.aktiver_spieler and self.rel_pos(k) == 0}.keys())[0]
        except:
            return None
    
    def einsetzen(self) -> bool:
        try:
            # erste figur des spielers, die noch draußen ist, wird genommen
            figur = list({k: v for k, v in self.figuren.items() if k//10 == self.aktiver_spieler and v == -100}.keys())[0]
            # und auf das erste feld gesetzt
            self.figuren[figur] = self.aktiver_spieler*10
            return True
        except:
            return False
    
    def test_integritaet(self) -> bool:
        assert max(self.figuren.values()) <= 73
        assert len(self.figuren) == 16
        return True
        

def main():
    spiel = Spiel()
    zielfiguren: dict[int, int] = {0:0, 1:0, 2:0, 3:0}
    
    # spielen bis jemand vier figuren im ziel hat
    while 4 not in zielfiguren.values():
        spiel.augenzahl = 6
        wuerfe = 1 if spiel.figur_im_feld() and spiel.setzen_ziel_moeglich() else 3
        print(spiel.figuren)
        while wuerfe > 0:
            
            # spieler ist an der reihe solang eine 6 gewürfelt wurde und er noch würfe hat
            spiel.augenzahl = random.randint(1,6)
            print(f"{spiel.aktiver_spieler} würfelt {spiel.augenzahl}")
            
            # muss er rausschmeissen?
            if (angreifer := spiel.rausschmeissen_moeglich()) is not None:
                spiel.rausschmeissen(angreifer)
            
            # muss er freimachen?
            elif (aktive_figur := spiel.freimachen_moeglich()) is not None:
                spiel.ziehen(aktive_figur)
            
            # muss er einsetzen
            elif spiel.augenzahl == 6 and len({k: v for k, v in spiel.figuren.items() if k//10 == spiel.aktiver_spieler and v == -100}) > 0:
                spiel.einsetzen()
            
            # kann er im ziel ziehen?
            elif spiel.setzen_ziel_moeglich():
                # beginnend mit der am weitesten vorn stehenden figur wird versucht, diese im zielbereich zu setzen. sobald eine figur gezogen wurde, geht es weiter.
                for figur in sorted({k: v for k, v in spiel.figuren.items() if v >= spiel.aktiver_spieler*10+40}.keys(), reverse=True):
                    if spiel.zieleinlauf(figur):
                        break
            
            elif spiel.figur_im_feld():
                try:
                    figur = sorted(list({k: v for k, v in spiel.figuren.items() if k//10 == spiel.aktiver_spieler and spiel.figur_im_feld()}.keys()), reverse=True)[0]
                    spiel.ziehen(figur)
                except:
                    None

            wuerfe = 1 if spiel.augenzahl == 6 else wuerfe - 1
            spiel.test_integritaet()
                        
        # setzen möglich (1x oder 3x würfeln)? OK
        # würfeln OK
        # aktive figur und aktion wählen
            # muss er rausschmeißen?
            # muss er freimachen?
            # hat er eine sechs und kann einsetzen?
            # kann er im ziel ziehen?
            # erste figur wählen
        # würfe anpassen OK
        # nach schleife
        # nächsten spieler bestimmen
        # zielfiguren aktualisieren

        spiel.aktiver_spieler = spiel.aktiver_spieler + 1 if spiel.aktiver_spieler < 3 else 0
        # zielfiguren = {0:0, 1:0, 2:0, 3:0}
        
        zielfiguren = {spieler: len({k: v for k, v in spiel.figuren.items() if k//10 == spieler and v >= spieler*10+40}) for spieler in range(4)}
    
    print(f"Sieger: {zielfiguren}")


if __name__ == '__main__':
    main()