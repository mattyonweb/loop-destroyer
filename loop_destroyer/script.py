import subprocess
import os, sys
import shutil

def sox(fname_input, fname_output, effects="", quiet=False):
    incipit = "sox " + ("-q " if quiet else "") + f"{fname_input} {fname_output}" 
    if effects:
        return incipit + f" {effects}"
    return incipit

def harm_gen(i, fst_harm=1/100, snd_harm=3/500, thr_harm=-1/175):
    s = "ladspa harmonic_gen_1220 1 "
    s += f"{i * fst_harm:.3f} {i * snd_harm:.3f} {i * thr_harm:.3f} norm -1 reverb 35 50 20"
    return s

def gen_fname(basepath, i, ext):
    return os.path.join(basepath, f"{i:05}" + "." + ext)

# =========================================================== #
import argparse

parser = argparse.ArgumentParser(description='loop destroyer.')
parser.add_argument('input_dir',
                    help="dir containing initial .wav samples")
parser.add_argument("-o", '--output_dir',
                    help="dir for output files")
parser.add_argument("--output_fname",
                    help="name of the disintegrated .mp3", action="store", default="disintegrated.mp3")
parser.add_argument('--reverse',
                    help="from distortion to pureness", action="store_true", default=False)
parser.add_argument('--spectrogram',
                    help="create spectrogram video", action="store_true", default=False)
parser.add_argument("-q", '--quiet',
                    help="quiet output", action="store_true", default=False)
args = parser.parse_args()

CURRENT_DIR = args.input_dir
TEMP_DIR    = os.path.join(CURRENT_DIR, ".out")
FINAL_DIR   = "./finale" if args.output_dir is None else args.output_dir
REVERSE     = args.reverse
SPECTROGRAM = shutil.which("ffmpeg") and args.spectrogram
QUIET       = args.quiet

OUT_MP3_FNAME = os.path.join(FINAL_DIR, args.output_fname)
SPECTROGRAM_FNAME = os.path.join(FINAL_DIR, "spectrogram.mp4")


# =========================================================== #
# Preparing

# Create TEMP_DIR and FINAL_DIR
try: os.mkdir(TEMP_DIR)
except FileExistsError: pass
    
try: os.mkdir(FINAL_DIR)
except FileExistsError:
    if os.path.isfile(OUT_MP3_FNAME): os.remove(OUT_MP3_FNAME)
    if os.path.isfile(SPECTROGRAM_FNAME): os.remove(SPECTROGRAM_FNAME)
        
        
# Check if ffmpeg and sox exists
if not shutil.which("sox"):
    print("sox command not found! You need sox to destroy your samples!", file=sys.stderr)
    print("You can download it from: http://sox.sourceforge.net/", file=sys.stderr)
    sys.exit(1)
if args.spectrogram and not shutil.which("ffmpeg"):
    print("[WARNING] ffmpeg is not installed. This is not necessary, but to obtain "\
          "a nice spectrogram of the file, ffmpeg must be installed.", file=sys.stderr)
          

# =========================================================== #

# I samples che andremo a trattare sono tutti gli .wav in CURRENT_DIR
input_files = [f for f in os.listdir(CURRENT_DIR) if f.endswith(".wav")]


# Degrada ogni sample. In pratica crei un certo numero di
# samples, progressivamente sempre più degradati, a partire
# dal sample iniziale; quindi, concatenali.
for input_file in input_files:
    # Copiamo il sample originale in TEMP_DIR
    shutil.copy(os.path.join(CURRENT_DIR, input_file),
                gen_fname(TEMP_DIR, 0, "wav"))
    
    # Applica al file della precedente iterazione (i-1) l'effetto
    # e crea il nuovo file (indice: i)
    for i in range(1, 20):
        effect = harm_gen(i, 1/400, 1/480, -1/430)
        cmd    = sox(gen_fname(TEMP_DIR, i-1, "wav"),
                     gen_fname(TEMP_DIR, i, "wav"),
                     effects=effect,
                     quiet=QUIET)

        # Esegui il comando per la generazione del nuovo audio
        p = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, check=True)

        
    # Concatena tutti i file progressivamente degradati in un
    # unico file, salvalo in FINAL_DIR
    if REVERSE:
        cmd = sox(" ".join([gen_fname(TEMP_DIR, i, "wav") for i in range(19, 0, -1)]),
                  os.path.join(FINAL_DIR, input_file),
                  effects="", quiet=QUIET)

    else:
        cmd = sox(os.path.join(TEMP_DIR, "*.wav"),
                  os.path.join(FINAL_DIR, input_file),
                  effects="", quiet=QUIET)


    print(cmd)
    subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, check=True)

    # Rimuovi i singoli samples degradati, non servono più
    os.system("rm -f " + os.path.join(TEMP_DIR, "*.wav"))

    
# =========================================================== #

# Crea un unico file .mp3 con le tracce degradate sovrapposte
# TODO: sox quiet
merge_cmd = "sox -m".split(" ")
for fname in os.listdir(FINAL_DIR):
    merge_cmd.append(f"'|sox {os.path.join(FINAL_DIR, fname)} -p'")
merge_cmd.append(OUT_MP3_FNAME)

print(merge_cmd)
os.system(" ".join(merge_cmd))


# =========================================================== #
# Crea spettrogramma

if SPECTROGRAM:
    cmd = f"ffmpeg -hide_banner -loglevel warning -i {OUT_MP3_FNAME} "\
           "-filter_complex showspectrum=mode=separate:color=intensity:slide=1:"\
           "scale=cbrt:size=1050x500:fps=1 -y -acodec copy " +\
           SPECTROGRAM_FNAME
    
    subprocess.run(cmd.split(" "), check=True)
