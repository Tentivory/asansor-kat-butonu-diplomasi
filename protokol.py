#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör kat butonu diplomasi protokolü.

Gercekten calisir. Asansor gerektirmez.
Gizli denetim kodu ic-tutanakta durur; burada yokmus gibi davranilir.
"""

from __future__ import annotations

import argparse
import random
import textwrap


YASAK_CUMLELER = [
    "ben basayim mi",
    "kacinci kat",
    "hava nasil",
    "cok bekletti",
    "parti",
]


def utanç_puani(kat: int, yolcu: int, goz_temasi: bool, cumle: str) -> int:
    puan = 12
    puan += min(kat, 40)  # yuksek kat, uzun sessizlik
    puan += yolcu * 9
    if goz_temasi:
        puan += 37
    if kat == 1:
        puan += 15  # zaten inecektin, neden basildi
    norm = cumle.strip().lower()
    if any(y in norm for y in YASAK_CUMLELER):
        puan += 22
    if "basili" in norm or "yaniyor" in norm:
        puan -= 8  # medeni tespit
    return max(0, puan)


def karar(puan: int) -> str:
    if puan < 30:
        return "MEDENI SESSİZLİK. Kat butonuna bakılmaz, tavana da bakılmaz, ayakkabıya bakılır."
    if puan < 60:
        return "NOTA. Bir taraf hafifçe öksürecek, diğeri duymamış gibi yapacak."
    if puan < 90:
        return "KRİZ. Kapı açılınca herkes farklı yöne dağılacak. Özür yok."
    return "ULUSLARARASI OLAY. Asansör nötr bölge ilan edilir, konuşma ateşkesi yürürlüğe girer."


def rapor(kat: int, yolcu: int, goz_temasi: bool, cumle: str) -> str:
    puan = utanç_puani(kat, yolcu, goz_temasi, cumle)
    buton = "YANIYOR" if random.random() > 0.15 else "KARANLIK, basılabilir"
    govde = textwrap.dedent(
        f"""
        -------------------------------------------------
        TUTANAK NO: AB-{kat:02d}-{yolcu:02d}-{puan:03d}
        KONU: Kat butonu teması ve bakış ihlali
        -------------------------------------------------
        Talep edilen kat     : {kat}
        Kabin nüfusu         : {yolcu}
        Göz teması           : {"tespit edildi" if goz_temasi else "reddedildi"}
        Buton ışığı          : {buton}
        Sarf edilen cümle   : {cumle.strip() or "(sessizlik, kabul)"}
        Utanç puanı         : {puan}/120
        Karar                : {karar(puan)}
        Ek not               : İkinci basış protokol dışıdır.
        -------------------------------------------------
        """
    ).strip()
    return govde


def main() -> None:
    p = argparse.ArgumentParser(description="Asansör kat butonu diplomasi protokolü")
    p.add_argument("--kat", type=int, default=4)
    p.add_argument("--yolcu", type=int, default=2)
    p.add_argument("--goz-temasi", choices=["evet", "hayir"], default="hayir")
    p.add_argument("--cumle", default="")
    a = p.parse_args()
    if a.kat < 0 or a.yolcu < 1:
        raise SystemExit("Kat eksi, yolcu sifir olamaz. Protokol bunu da utanç sayar.")
    print(rapor(a.kat, a.yolcu, a.goz_temasi == "evet", a.cumle))
    print()
    print("DAMGA: ASANSÖR KAT BUTONU DİPLOMASİ DAİRESİ")
    print("İMZA: Kayyum Grok")
    print("TARİH: 4 Ekim 2026")
    print("KAŞE: Buton zaten yanıyordu.")


if __name__ == "__main__":
    main()
