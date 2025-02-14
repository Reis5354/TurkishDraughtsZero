from utils import *
import logging

log = logging.getLogger(__name__)

def main():
    log.info('Loading DamaGame...')
    from dama.DamaGame import DamaGame  # Othello yerine Dama'yı import et
    game = DamaGame()

    log.info('Loading NNetWrapper...')
    from dama.DamaNNet import NNetWrapper as nn  # Dama için Neural Network
    nnet = nn(game)

    if args.load_model:
        log.info('Loading checkpoint "%s"...', args.load_model)
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    from Coach import Coach
    c = Coach(game, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()

if __name__ == "__main__":
    main()