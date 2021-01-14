import subprocess
import os
from shutil import copy

def sox(fname_input, fname_output):
    return f"sox {fname_input} {fname_output} "

def harm_gen(i, fst_harm=1/100, snd_harm=3/500, thr_harm=-1/175):
    s = "ladspa harmonic_gen_1220 1 "
    s += f"{i * fst_harm:.3f} {i * snd_harm:.3f} {i * thr_harm:.3f} norm -1 reverb 35 50 20"
    return s

def gen_fname(basepath, i, ext):
    return os.path.join(basepath, f"{i:05}" + "." + ext)

# =========================================================== #
import argparse

parser = argparse.ArgumentParser(description='Destroy and loop.')
parser.add_argument('input_dir', help="dir containing .wav files")
parser.add_argument('--output_dir', help="dir for output files")
parser.add_argument('--reverse', help="dir for output files", action="store_true", default=False)
args = parser.parse_args()

CURRENT_DIR = args.input_dir
TEMP_DIR    = os.path.join(CURRENT_DIR, ".out")
FINAL_DIR   = os.path.join(CURRENT_DIR, "finale") if args.output_dir is None else args.output_dir
REVERSE     = args.reverse

print(CURRENT_DIR)
# =========================================================== #

# Crea le cartelle temporanee e finali
try: os.mkdir(TEMP_DIR)
except FileExistsError: pass
try: os.mkdir(FINAL_DIR)
except FileExistsError: pass

# =========================================================== #

# I samples che andremo a trattare sono tutti gli .wav in CURRENT_DIR
input_files = [f for f in os.listdir(CURRENT_DIR) if f.endswith(".wav")]


# Degrada ogni sample. In pratica crei un certo numero di
# samples, progressivamente sempre più degradati, a partire
# dal sample iniziale; quindi, concatenali.
for input_file in input_files:
    # Copiamo il sample originale in TEMP_DIR
    copy(os.path.join(CURRENT_DIR, input_file),
         gen_fname(TEMP_DIR, 0, "wav"))

    # Applica al file della precedente iterazione (i-1) l'effetto
    # e crea il nuovo file (indice: i)
    for i in range(1, 20):
        effect = harm_gen(i, 1/400, 1/480, -1/430)
        base_cmd = sox(gen_fname(TEMP_DIR, i-1, "wav"),
                       gen_fname(TEMP_DIR, i, "wav"))

        cmd = base_cmd + effect
        print(cmd)

        # Esegui il comando per la generazione del nuovo audio
        p = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)

        
    # Concatena tutti i file progressivamente degradati in un
    # unico file, salvalo in FINAL_DIR
    if REVERSE:
        cmd = ("sox " + " ".join([gen_fname(TEMP_DIR, i, "wav") for i in range(19, 0, -1)]) +
               " " + os.path.join(FINAL_DIR, input_file))
    else:
        cmd = ("sox " + os.path.join(TEMP_DIR, "*.wav") + " " +
               os.path.join(FINAL_DIR, input_file))
        
    subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)

    # Rimuovi i singoli samples degradati, non servono più
    os.system("rm -f " + os.path.join(TEMP_DIR, "*.wav"))

    
# =========================================================== #

# Crea un unico file .mp3 con le tracce degradate sovrapposte
merge_cmd = "sox -m".split(" ")
for fname in os.listdir(FINAL_DIR):
    merge_cmd.append(f"'|sox {os.path.join(FINAL_DIR, fname)} -p'")
merge_cmd.append("out.mp3")

os.system(" ".join(merge_cmd))


# =========================================================== #
# Crea spettrogramma
cmd = f"ffmpeg -i out.mp3 -filter_complex showspectrum=mode=separate:color=intensity:slide=1:scale=cbrt:size=1050x500:fps=1 -y -acodec copy video.mp4"
subprocess.run(cmd.split(" "))
