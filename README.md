# 📊 BPM-Video-Generator

## 🎯 Objectif

Transformer un fichier `.tcx` (Garmin) en :

- données BPM (JSON / CSV)
- une vidéo overlay avec cœur animé + BPM

---

## ⚙️ Installation

### 1. Installer Python

https://www.python.org/downloads/

### 2. Installer les dépendances

Dans un terminal :

pip install pillow imageio imageio-ffmpeg numpy

---

## ▶️ Utilisation

### 1. Se placer dans le dossier scripts

cd scripts

---

### 2. Extraire les données du fichier TCX

python extract_match_data.py

**Résultat :**

- `output/heart_rate_data.json`
- `output/heart_rate_data.csv`

---

### 3. Générer la vidéo

#### Version normale (fond noir)

python video_normal.py

**Résultat :**

- `output/overlay.mp4`

---

#### Version transparente (pour montage vidéo)

python video_transparent.py

**Résultat :**

- `output/overlay_transparent.mov`

---

## 🔁 Changer de fichier TCX

Dans `extract_match_data.py` :

TCX_FILE = "../data/Match.tcx"

Remplacer par :

TCX_FILE = "../data/MonMatch.tcx"

---

## 📄 Fichier TCX

Un fichier `.tcx` est un fichier XML Garmin contenant :

- le temps
- la fréquence cardiaque
- parfois le GPS

### Exemple


```xml
<Trackpoint>
  <Time>2026-03-20T20:39:19Z</Time>
  <HeartRateBpm>
    <Value>119</Value>
  </HeartRateBpm>
</Trackpoint>
```


## 🎬 Résultat

La vidéo affiche :

- ❤️ un cœur animé  
- 📊 le BPM en temps réel  
- 🎨 une couleur selon l’intensité  

### 🎨 Couleurs

- `< 120 BPM` → blanc  
- `120–139 BPM` → jaune  
- `140–159 BPM` → orange  
- `≥ 160 BPM` → rouge  

## ⚠️ Remarques
MP4 ne supporte pas la transparence
MOV supporte la transparence
alternative : fond vert pour montage

# 💬Auteur

SOUMET Quentin
Projet personnel pour analyse de match de ping-pong 🏓