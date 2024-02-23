import axios from "axios";
import {runInAction, observable, action} from 'mobx';

import {API_HOST_URL} from './constants'
import Crossword, {Clue, Position} from "./model";

export default class CrosswordStore {
    @observable accessor isLoaded = false;
    @observable accessor crossword = null;

    constructor(crosswordId ) {
        this.crosswordId = crosswordId;
    }

    @action
    async loadCrossword() {
        const data = await axios.get(
            `${API_HOST_URL}/crosswords/?crossword_id=${this.crosswordId}`,
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        // need to fetch unique clues
        const uniqueClues = {}
        let allClues = []
        data.data.clues.forEach((clue) => {
            if (uniqueClues[clue.clue] === undefined) {
                uniqueClues[clue.clue] = clue.clue
                allClues = allClues.concat([new Clue({
                    clue: clue.clue,
                    position: new Position({
                        row: data.data.board.words_position[clue.word][0][0],
                        column: data.data.board.words_position[clue.word][0][1],
                        direction: data.data.board.words_position[clue.word][1],
                    }),
                    length: clue.word.length,
                    // TODO: remove later
                    content: clue.word
                })])
            }
        });

        runInAction(() => {
            this.isLoaded = true;
            this.crossword = new Crossword(data.data.board.matrix, allClues);
        });
    }
}