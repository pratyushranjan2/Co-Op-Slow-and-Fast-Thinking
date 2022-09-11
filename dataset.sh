for run in {1..3000}
do
  python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=3 -a evalFn=better -q
done
SRC_DIR="/home/sarthak/AI/pacman/multi_agent_pacman/data.csv"
DST_DIR="/home/sarthak/AI/pacman/neural_network/pacman_nn"
FILEN="data.csv"
cp "$SRC_DIR" "$DST_DIR"

cd $DST_DIR
python train_pacman_nn.py